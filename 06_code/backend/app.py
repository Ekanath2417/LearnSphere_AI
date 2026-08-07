"""LearnSphere AI application server.

The API is deliberately provider-agnostic. AI requests use a transparent local
study-coach fallback until an administrator configures a server-side provider.
"""
from __future__ import annotations

import os
import re
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from functools import wraps
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"
DATABASE = ROOT / "database" / "learnsphere.db"
SCHEMA = ROOT / "database" / "schema.sql"
UPLOADS = ROOT / "storage" / "uploads"
ALLOWED_EXTENSIONS = {"pdf", "txt", "md", "docx", "png", "jpg", "jpeg", "webm", "m4a", "mp3", "wav"}

app = Flask(__name__, static_folder=str(FRONTEND), static_url_path="")
app.config.update(
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "replace-this-dev-secret-before-production"),
    MAX_CONTENT_LENGTH=25 * 1024 * 1024,
)
CORS(app, resources={r"/api/*": {"origins": os.getenv("CORS_ORIGINS", "*").split(",")}})
jwt = JWTManager(app)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def db() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


@contextmanager
def database_context():
    connection = db()
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def rows(cursor: sqlite3.Cursor) -> list[dict]:
    return [dict(row) for row in cursor.fetchall()]


def init_db() -> None:
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    UPLOADS.mkdir(parents=True, exist_ok=True)
    with database_context() as connection:
        connection.executescript(SCHEMA.read_text(encoding="utf-8"))
        columns = {row["name"] for row in connection.execute("PRAGMA table_info(users)")}
        if "name" not in columns:
            connection.execute("ALTER TABLE users ADD COLUMN name TEXT NOT NULL DEFAULT 'Student'")


def api_error(message: str, code: int = 400):
    return jsonify({"error": message}), code


def payload() -> dict:
    return request.get_json(silent=True) or {}


def user_id() -> int:
    return int(get_jwt_identity())


def required(*fields):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            body = payload()
            missing = [field for field in fields if not str(body.get(field, "")).strip()]
            if missing:
                return api_error(f"Required: {', '.join(missing)}")
            return view(*args, **kwargs)
        return wrapped
    return decorator


def create_student_seed(connection: sqlite3.Connection, student_id: int) -> None:
    subjects = [("Mathematics", "Build confidence through deliberate problem practice.", "#8B5CF6"),
                ("Data Structures", "Master concepts, patterns, and implementation.", "#22C55E"),
                ("Machine Learning", "Connect theory, experiments, and revision.", "#F59E0B")]
    for name, description, color in subjects:
        connection.execute("INSERT INTO subjects (user_id, name, description, color, created_at) VALUES (?, ?, ?, ?, ?)",
                           (student_id, name, description, color, now()))
    subject_id = connection.execute("SELECT id FROM subjects WHERE user_id = ? ORDER BY id LIMIT 1", (student_id,)).fetchone()[0]
    tasks = [("Review limits and continuity", "2026-08-08", 45, "today"),
             ("Complete problem set 04", "2026-08-09", 60, "upcoming"),
             ("Weekly reflection", "2026-08-10", 20, "upcoming")]
    for title, due, minutes, status in tasks:
        connection.execute("INSERT INTO tasks (user_id, subject_id, title, due_date, planned_minutes, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (student_id, subject_id, title, due, minutes, status, now()))
    connection.execute("INSERT INTO notes (user_id, subject_id, title, body, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                       (student_id, subject_id, "Limits — quick revision", "Key ideas, formulae, and questions to revisit before the next study block.", now(), now()))


@app.post("/api/auth/register")
@required("name", "email", "password")
def register():
    body = payload()
    email = body["email"].strip().lower()
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return api_error("Enter a valid email address")
    if len(body["password"]) < 8:
        return api_error("Password must contain at least 8 characters")
    try:
        with database_context() as connection:
            cursor = connection.execute("INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                                        (body["name"].strip(), email, generate_password_hash(body["password"]), now()))
            create_student_seed(connection, cursor.lastrowid)
            return jsonify({"token": create_access_token(identity=str(cursor.lastrowid)), "user": {"id": cursor.lastrowid, "name": body["name"].strip(), "email": email}}), 201
    except sqlite3.IntegrityError:
        return api_error("An account already exists for this email", 409)


@app.post("/api/auth/login")
@required("email", "password")
def login():
    body = payload()
    with database_context() as connection:
        account = connection.execute("SELECT * FROM users WHERE email = ?", (body["email"].strip().lower(),)).fetchone()
    if not account or not check_password_hash(account["password_hash"], body["password"]):
        return api_error("Incorrect email or password", 401)
    return jsonify({"token": create_access_token(identity=str(account["id"])), "user": {"id": account["id"], "name": account["name"], "email": account["email"]}})


@app.get("/api/me")
@jwt_required()
def me():
    with database_context() as connection:
        account = connection.execute("SELECT id, name, email, created_at FROM users WHERE id = ?", (user_id(),)).fetchone()
    return jsonify(dict(account))


@app.get("/api/dashboard")
@jwt_required()
def dashboard():
    uid = user_id()
    week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat(timespec="seconds")
    with database_context() as connection:
        subject_count = connection.execute("SELECT COUNT(*) FROM subjects WHERE user_id = ?", (uid,)).fetchone()[0]
        complete = connection.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND status = 'done'", (uid,)).fetchone()[0]
        planned = connection.execute("SELECT COALESCE(SUM(planned_minutes), 0) FROM tasks WHERE user_id = ?", (uid,)).fetchone()[0]
        activity = connection.execute("SELECT COALESCE(SUM(minutes), 0) FROM study_sessions WHERE user_id = ? AND started_at >= ?", (uid, week_ago)).fetchone()[0]
        task_rows = rows(connection.execute("SELECT tasks.*, subjects.name AS subject_name, subjects.color FROM tasks LEFT JOIN subjects ON subjects.id = tasks.subject_id WHERE tasks.user_id = ? AND tasks.status != 'done' ORDER BY due_date ASC LIMIT 6", (uid,)))
        subjects = rows(connection.execute("SELECT subjects.*, COUNT(tasks.id) AS task_count FROM subjects LEFT JOIN tasks ON tasks.subject_id = subjects.id AND tasks.status != 'done' WHERE subjects.user_id = ? GROUP BY subjects.id ORDER BY subjects.created_at DESC", (uid,)))
        quiz = connection.execute("SELECT score, total, topic FROM quizzes WHERE user_id = ? ORDER BY created_at DESC LIMIT 1", (uid,)).fetchone()
    consistency = min(100, round((activity / max(planned, 60)) * 100))
    return jsonify({"metrics": {"subjects": subject_count, "tasks_completed": complete, "focus_minutes": activity, "consistency": consistency}, "tasks": task_rows, "subjects": subjects, "latest_quiz": dict(quiz) if quiz else None})


@app.route("/api/subjects", methods=["GET", "POST"])
@jwt_required()
def subjects():
    uid = user_id()
    if request.method == "GET":
        with database_context() as connection:
            return jsonify(rows(connection.execute("SELECT * FROM subjects WHERE user_id = ? ORDER BY created_at DESC", (uid,))))
    body = payload()
    if not body.get("name", "").strip(): return api_error("Subject name is required")
    with database_context() as connection:
        cursor = connection.execute("INSERT INTO subjects (user_id, name, description, color, created_at) VALUES (?, ?, ?, ?, ?)", (uid, body["name"].strip(), body.get("description", "").strip(), body.get("color", "#8B5CF6"), now()))
    return jsonify({"id": cursor.lastrowid, "message": "Subject added"}), 201


@app.route("/api/tasks", methods=["GET", "POST", "PATCH"])
@jwt_required()
def tasks():
    uid = user_id()
    if request.method == "GET":
        with database_context() as connection:
            return jsonify(rows(connection.execute("SELECT tasks.*, subjects.name AS subject_name, subjects.color FROM tasks LEFT JOIN subjects ON subjects.id = tasks.subject_id WHERE tasks.user_id = ? ORDER BY due_date ASC", (uid,))))
    body = payload()
    if request.method == "PATCH":
        if not body.get("id"): return api_error("Task id is required")
        with database_context() as connection:
            connection.execute("UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?", (body.get("status", "done"), body["id"], uid))
        return jsonify({"message": "Task updated"})
    if not body.get("title", "").strip(): return api_error("Task title is required")
    with database_context() as connection:
        cursor = connection.execute("INSERT INTO tasks (user_id, subject_id, title, due_date, planned_minutes, status, created_at) VALUES (?, ?, ?, ?, ?, 'upcoming', ?)", (uid, body.get("subject_id"), body["title"].strip(), body.get("due_date"), int(body.get("planned_minutes", 30)), now()))
    return jsonify({"id": cursor.lastrowid, "message": "Task planned"}), 201


@app.route("/api/notes", methods=["GET", "POST"])
@jwt_required()
def notes():
    uid = user_id()
    if request.method == "GET":
        with database_context() as connection:
            return jsonify(rows(connection.execute("SELECT notes.*, subjects.name AS subject_name FROM notes LEFT JOIN subjects ON subjects.id = notes.subject_id WHERE notes.user_id = ? ORDER BY notes.updated_at DESC", (uid,))))
    body = payload()
    if not body.get("title", "").strip(): return api_error("Note title is required")
    with database_context() as connection:
        cursor = connection.execute("INSERT INTO notes (user_id, subject_id, title, body, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)", (uid, body.get("subject_id"), body["title"].strip(), body.get("body", ""), now(), now()))
    return jsonify({"id": cursor.lastrowid, "message": "Note saved"}), 201


@app.route("/api/diary", methods=["GET", "POST"])
@jwt_required()
def diary():
    uid = user_id()
    if request.method == "GET":
        with database_context() as connection:
            return jsonify(rows(connection.execute("SELECT * FROM diary_entries WHERE user_id = ? ORDER BY entry_date DESC", (uid,))))
    body = payload()
    if not body.get("body", "").strip(): return api_error("Diary entry cannot be empty")
    with database_context() as connection:
        connection.execute("INSERT INTO diary_entries (user_id, entry_date, mood, body, created_at) VALUES (?, ?, ?, ?, ?) ON CONFLICT(user_id, entry_date) DO UPDATE SET mood=excluded.mood, body=excluded.body", (uid, body.get("entry_date", now()[:10]), body.get("mood", "Focused"), body["body"].strip(), now()))
    return jsonify({"message": "Reflection saved"}), 201


@app.post("/api/resources/upload")
@jwt_required()
def upload_resource():
    file = request.files.get("file")
    if not file or not file.filename: return api_error("Choose a file to upload")
    extension = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if extension not in ALLOWED_EXTENSIONS: return api_error("Unsupported file type")
    filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    file.save(UPLOADS / filename)
    with database_context() as connection:
        cursor = connection.execute("INSERT INTO resources (user_id, subject_id, title, filename, mime_type, created_at) VALUES (?, ?, ?, ?, ?, ?)", (user_id(), request.form.get("subject_id") or None, request.form.get("title") or file.filename, filename, file.mimetype, now()))
    return jsonify({"id": cursor.lastrowid, "message": "Resource securely added to your library"}), 201


@app.get("/api/resources")
@jwt_required()
def resources():
    with database_context() as connection: return jsonify(rows(connection.execute("SELECT resources.*, subjects.name AS subject_name FROM resources LEFT JOIN subjects ON subjects.id = resources.subject_id WHERE resources.user_id = ? ORDER BY resources.created_at DESC", (user_id(),))))


@app.post("/api/study-sessions")
@jwt_required()
def study_session():
    body = payload()
    minutes = max(1, min(int(body.get("minutes", 25)), 600))
    with database_context() as connection: connection.execute("INSERT INTO study_sessions (user_id, subject_id, minutes, started_at, created_at) VALUES (?, ?, ?, ?, ?)", (user_id(), body.get("subject_id"), minutes, now(), now()))
    return jsonify({"message": f"{minutes} focused minutes recorded"}), 201


@app.post("/api/quizzes/generate")
@jwt_required()
def generate_quiz():
    body = payload(); topic = body.get("topic", "your current topic").strip()
    questions = [
        {"question": f"Which study action best checks understanding of {topic}?", "options": ["Active recall", "Rereading only", "Skipping practice", "Avoiding feedback"], "answer": 0},
        {"question": f"When should you review a difficult {topic} concept?", "options": ["Only before exams", "After spaced intervals", "Never", "After forgetting everything"], "answer": 1},
        {"question": f"What makes a strong answer in {topic}?", "options": ["Clear reasoning and examples", "More pages", "Copied text", "No structure"], "answer": 0},
    ]
    return jsonify({"topic": topic, "questions": questions, "source": "LearnSphere practice engine"})


@app.post("/api/quizzes/submit")
@jwt_required()
def submit_quiz():
    body = payload(); total = int(body.get("total", 3)); score = max(0, min(int(body.get("score", 0)), total))
    with database_context() as connection: connection.execute("INSERT INTO quizzes (user_id, topic, score, total, created_at) VALUES (?, ?, ?, ?, ?)", (user_id(), body.get("topic", "Practice"), score, total, now()))
    return jsonify({"message": "Result saved", "score": score, "total": total, "feedback": "Good work. Review missed concepts, then retest with a fresh set."})


@app.get("/api/insights")
@jwt_required()
def insights():
    uid = user_id()
    with database_context() as connection:
        planned = connection.execute("SELECT COALESCE(SUM(planned_minutes), 0) FROM tasks WHERE user_id = ?", (uid,)).fetchone()[0]
        logged = connection.execute("SELECT COALESCE(SUM(minutes), 0) FROM study_sessions WHERE user_id = ?", (uid,)).fetchone()[0]
        result = connection.execute("SELECT AVG(CAST(score AS FLOAT) / total) FROM quizzes WHERE user_id = ? AND total > 0", (uid,)).fetchone()[0]
    pace = round(logged / max(planned, 1) * 100)
    predicted = min(95, max(45, round(52 + (pace * .22) + ((result or .6) * 28))))
    return jsonify({"consistency": min(100, pace), "predicted_mark": predicted, "confidence": "Indicative", "recommendations": ["Schedule one 45-minute deep-work block on your weakest subject.", "Use active recall before opening reference material.", "Take a short quiz after each completed revision cycle."], "disclaimer": "This is a learning signal, not a formal academic prediction."})


@app.post("/api/chat")
@jwt_required()
def chat():
    message = payload().get("message", "").strip()
    if not message: return api_error("Write a question for your study coach")
    answer = f"Here is a study-first way to approach this: break ‘{message[:90]}’ into the definition, one worked example, and three recall questions. Tell me your subject or attach a resource so I can make that plan specific."
    return jsonify({"answer": answer, "mode": "local study-coach fallback", "notice": "Connect an approved server-side AI provider for generated, document-grounded responses. Never enter a personal ChatGPT password into LearnSphere."})


@app.get("/api/integrations")
@jwt_required()
def integrations():
    return jsonify({"providers": [{"name": "OpenAI", "status": "Administrator configuration required", "purpose": "Document-grounded study coaching"}, {"name": "Google Gemini", "status": "Administrator configuration required", "purpose": "Optional provider route"}, {"name": "NotebookLM", "status": "External workspace link", "purpose": "Open uploaded sources in a separate trusted service"}]})


@app.get("/")
@app.get("/<path:path>")
def frontend(path="index.html"):
    target = FRONTEND / path
    if path and target.is_file(): return send_from_directory(FRONTEND, path)
    return send_from_directory(FRONTEND, "index.html")


@app.errorhandler(413)
def too_large(_): return api_error("File exceeds the 25 MB upload limit", 413)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=os.getenv("FLASK_DEBUG") == "1")
