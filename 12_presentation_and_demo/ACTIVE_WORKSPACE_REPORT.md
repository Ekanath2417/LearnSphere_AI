# Active Workspace and Deployment Report

## Abstract

LearnSphere AI is a student-centred study operating system created as part of the MindForgeAI Internship at Chatake Innoworks Pvt. Ltd. The active-workspace enhancement establishes a separate development clone, clear page-level frontend files, reproducible local execution, Git collaboration guidance, integration documentation, and a controlled deployment workflow. The goal is to help the student team make changes confidently without modifying the baseline project directly.

## Project Context

The application combines a Flask backend, SQLite MVP datastore, HTML/CSS/JavaScript interface, GitHub repository, GitHub Pages presentation site, and Render-hosted API. Its core learning workflow is capture, plan, focus, practice, and reflect. The design avoids unsupported academic claims: learning signals are indicative support and never official or diagnostic judgments.

## Active Workspace Design

The active workspace is located at `D:\LearnSphere_AI_ActiveWorkspace`. It is a Git clone of the published repository and runs independently on port 5051. The arrangement protects the original workspace as a reference copy while giving the team a practical location for feature branches, experiments, documentation updates, and verified releases.

## Maintainability Improvements

The frontend has a dedicated `pages` directory containing separate overview, planner, library, practice, and team page files. A shared `pages.css` keeps their presentation consistent. The running application shell remains in `index.html`, with dynamic workspace behavior in `assets/app.js`. `CHANGE_MAP.md` identifies the responsible file for common changes, reducing accidental cross-layer edits.

## Integration Architecture

The browser calls Flask API routes through `/api` locally. On GitHub Pages, `runtime-config.js` supplies the Render API base URL. Flask-CORS validates the Pages origin, Flask-JWT-Extended secures student-specific routes, and SQLite stores local MVP data. GitHub Actions verifies the code and publishes static frontend assets.

## Operating Procedure

The team starts the active workspace using `RUN_LOCALHOST.ps1`, opens `http://localhost:5051`, completes a focused change, runs the unit tests, reviews the Git diff, commits on a feature branch, and pushes for review. The booklet contains command explanations, release checks, troubleshooting, and security rules.

## Conclusion

The active workspace turns LearnSphere AI into a more maintainable internship deliverable. It provides clear ownership of pages and integrations, a separate local development server, and a documented route from local edits to GitHub and hosted deployment.

