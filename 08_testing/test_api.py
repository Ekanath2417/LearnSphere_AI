import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

CODE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "06_code"))
sys.path.insert(0, os.path.join(CODE, "backend"))
import app as application


class LearnSphereAPITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        application.DATABASE = Path(cls.temp_dir) / "test.db"
        application.UPLOADS = Path(cls.temp_dir) / "uploads"
        application.app.config["TESTING"] = True
        application.app.config["JWT_SECRET_KEY"] = "test-secret"
        application.init_db()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dir)

    def setUp(self):
        self.client = application.app.test_client()
        suffix = os.urandom(4).hex()
        result = self.client.post("/api/auth/register", json={"name": "Test Student", "email": f"student-{suffix}@learnsphere.test", "password": "Password123!"})
        self.assertEqual(result.status_code, 201)
        self.headers = {"Authorization": "Bearer " + result.get_json()["token"]}

    def test_student_can_plan_and_record_learning(self):
        dashboard = self.client.get("/api/dashboard", headers=self.headers)
        self.assertEqual(dashboard.status_code, 200)
        self.assertGreaterEqual(dashboard.get_json()["metrics"]["subjects"], 3)
        task = self.client.post("/api/tasks", headers=self.headers, json={"title": "Test revision", "planned_minutes": 30})
        self.assertEqual(task.status_code, 201)
        note = self.client.post("/api/notes", headers=self.headers, json={"title": "Test note", "body": "Recall beats rereading."})
        self.assertEqual(note.status_code, 201)
        insight = self.client.get("/api/insights", headers=self.headers)
        self.assertEqual(insight.status_code, 200)
        self.assertIn("predicted_mark", insight.get_json())

    def test_rejects_unauthorized_request(self):
        self.assertEqual(self.client.get("/api/dashboard").status_code, 401)


if __name__ == "__main__":
    unittest.main()
