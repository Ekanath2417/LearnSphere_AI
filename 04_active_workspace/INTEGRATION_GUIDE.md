# Integration Guide

## How the Pieces Connect

```text
Browser page -> frontend assets -> /api request -> Flask route -> SQLite database
GitHub Pages -> runtime-config.js -> Render Flask API -> CORS validation
Git push -> GitHub Actions -> GitHub Pages deployment
```

## Technology and Purpose

| Tool | Purpose | Where it is configured |
| --- | --- | --- |
| Python + Flask | Server, routes, frontend delivery | `06_code/backend/app.py` |
| SQLite | Local MVP data storage | `06_code/database/` |
| Flask-JWT-Extended | Sign-in tokens | `backend/app.py` |
| Flask-CORS | Allows Pages frontend to call API | `CORS_ORIGINS` |
| HTML/CSS/JavaScript | Student-facing interface | `06_code/frontend/` |
| Git + GitHub | Version history and collaboration | `.git`, GitHub repository |
| GitHub Actions + Pages | Website deployment | `.github/workflows/pages.yml` |
| Render + Gunicorn | Public Python API hosting | `render.yaml` |

## Local Environment Variables

Copy the example only for local work:

```powershell
Copy-Item 06_code\backend\.env.example 06_code\backend\.env
```

Set a local-only JWT secret. Never push `.env`.

```text
JWT_SECRET_KEY=long-local-development-secret
PORT=5051
FLASK_DEBUG=0
CORS_ORIGINS=http://localhost:5051,http://127.0.0.1:5051
```

## Production Connection Checklist

1. Render service status is `Live`.
2. `https://learnsphere-ai-c01p.onrender.com/api/health` responds.
3. Render variable `CORS_ORIGINS` is `https://ekanath2417.github.io`.
4. `runtime-config.js` contains the same Render service URL followed by `/api`.
5. GitHub Pages deployment succeeds.
6. Create a fresh test account on the hosted site; do not reuse personal passwords.

