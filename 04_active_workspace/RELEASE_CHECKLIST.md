# Release Checklist

## Before Pushing

- [ ] Read `CHANGE_MAP.md` and limited edits to the intended feature.
- [ ] Tested the change at `http://localhost:5051`.
- [ ] Ran `python -m unittest discover -s 08_testing`.
- [ ] Confirmed `.env`, databases, uploads, and credentials are not staged.
- [ ] Checked `git diff --check` for whitespace problems.
- [ ] Used a meaningful commit message.

## Before Hosted Release

- [ ] GitHub Actions checks pass.
- [ ] GitHub Pages workflow passes.
- [ ] Render health endpoint responds: `/api/health`.
- [ ] Render `CORS_ORIGINS` includes `https://ekanath2417.github.io`.
- [ ] `runtime-config.js` points at the live Render API URL.
- [ ] Sign-up and sign-in use a new non-personal test account.

## After Release

- [ ] Open the public website in a private browser window.
- [ ] Test one public page and one authenticated workflow.
- [ ] Record the deployment date and known limitations in the relevant report.

