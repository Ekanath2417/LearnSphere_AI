# LearnSphere AI

LearnSphere AI is a private study operating system built during the **MINDFORGEAI AIML Internship** at **CHATAKE INNOWORKS PVT. LTD.** It gives students one calm workspace for subjects, study plans, files, notes, voice-recording uploads, practice checks, diary reflections, and learning signals.

> Current state: a runnable, full-stack local MVP with a persistent SQLite store and a premium responsive interface. The AI assistant is intentionally a safe local fallback until an approved server-side provider is configured.

## Run locally

```powershell
cd 06_code
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python backend\app.py
```

Open [http://localhost:5000](http://localhost:5000). Create a new account; it receives sample subjects, tasks, and a note so the workspace is immediately explorable. In this workspace, port 5000 was already occupied, so the verified running instance is available at [http://localhost:5050](http://localhost:5050).

## What is included

- Persistent sign-up/sign-in, subjects, tasks, notes, diary, focus sessions, quiz results, and resource metadata.
- Private file upload library for PDFs, documents, images, and audio/voice notes (25 MB limit).
- Study dashboard, planner, knowledge base, practice lab, learning insights, and diary.
- Predictive-learning UI labelled as **indicative**, never as a formal academic result.
- Provider-neutral AI connection design; it never collects a student’s ChatGPT, Google, Gemini, or NotebookLM password.
- Deployment assets, tests, repository policy, product blueprint, team plan, and academic/industry reports.

## Repository map

| Folder | Purpose |
| --- | --- |
| `01_project_definition` | Vision, blueprint, prompt, and scope |
| `05_design` | Canonical reusable design, technology and implementation system |
| `02_research_and_sources` | Research log and source notes |
| `04_active_workspace` | Team working agreements |
| `06_code` | Flask application, SPA, database, and runtime config |
| `08_testing` | API smoke test and test notes |
| `10_management` | Three-person work plan and delivery controls |
| `11_deployment` | Docker, Render, and local deployment guides |
| `12_presentation_and_demo` | Academic and industry reports |

## Production hand-off

The MVP uses SQLite and local storage to make demonstrations simple. Before public deployment, move to PostgreSQL/object storage, put the app behind HTTPS, set a strong `JWT_SECRET_KEY`, define explicit CORS origins, add rate limiting and virus scanning, and complete a data/privacy review. See [deployment guide](11_deployment/DEPLOYMENT.md) and [product blueprint](01_project_definition/PRODUCT_BLUEPRINT.md).

The complete reusable design and implementation specification is [LearnSphere Design, Technology and Implementation System](05_design/LEARNSPHERE_DESIGN_AND_IMPLEMENTATION_SYSTEM.md).

For a fresh engineering session or cloud hand-off, start with the [continuity handoff](10_management/CONTINUITY_HANDOFF.md) and [AWS release runbook](11_deployment/AWS_RELEASE_RUNBOOK.md).

## Branding

LearnSphere AI is an internship project under CHATAKE INNOWORKS PVT. LTD. / MINDFORGEAI Division. The visual system is inspired by the organisation’s engineering-led, research-oriented public identity, while LearnSphere remains a distinct student product. © 2026 CHATAKE INNOWORKS PVT. LTD. All project rights reserved.
