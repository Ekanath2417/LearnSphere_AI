# Change Map

| What you want to change | Primary file | Also check | Verification |
| --- | --- | --- | --- |
| Home / landing copy | `06_code/frontend/index.html` | `assets/app.css` | Refresh `localhost:5051` |
| Sign-in and registration UI | `06_code/frontend/index.html` | `assets/app.js`, `backend/app.py` | Register and sign in locally |
| API host used on GitHub Pages | `06_code/frontend/assets/runtime-config.js` | Render service, `CORS_ORIGINS` | Browser network request to `/api/health` |
| Dashboard / planner interaction | `06_code/frontend/assets/app.js` | `backend/app.py`, database schema | Run local app and tests |
| Visual styling | `06_code/frontend/assets/app.css` | Mobile browser width | Refresh and inspect mobile layout |
| Website information pages | `06_code/frontend/pages/*.html` | `pages/pages.css` | Open each page URL locally |
| Authentication rules | `06_code/backend/app.py` | `.env.example`, tests | `08_testing` suite |
| Notes / syllabus / PYQs / timetable API | `06_code/backend/routes/` | `services/`, `models/` | API tests and UI flow |
| Database schema | `06_code/database/schema.sql` | `app.py` migrations | Fresh database test |
| Render deployment | `render.yaml` | `11_deployment/DEPLOYMENT.md` | Render logs and `/api/health` |
| GitHub Pages deployment | `.github/workflows/pages.yml` | `GITHUB_PAGES.md` | GitHub Actions workflow |
| Reports / presentation | `12_presentation_and_demo/` | evidence and screenshots | Check links and update date |

## Page File Guide

- `index.html`: full application shell, landing page, sign-in dialog, workspace shell.
- `pages/overview.html`: standalone explanation of the dashboard.
- `pages/planner.html`: standalone explanation of study planning.
- `pages/library.html`: standalone explanation of notes, syllabus, timetable, and PYQs.
- `pages/practice.html`: standalone explanation of practice and insights.
- `pages/team.html`: project, organisation, guide, and team credit page.
- `pages/pages.css`: shared page-level style rules.

