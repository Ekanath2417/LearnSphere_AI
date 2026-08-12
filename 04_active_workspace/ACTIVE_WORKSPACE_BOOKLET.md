# LearnSphere AI Active Workspace Booklet

## Purpose

This is the safe day-to-day workspace for LearnSphere AI. Make future changes here, test them here, then send only reviewed changes to GitHub. The original project folder remains a reference copy.

## Workspace Location

`D:\LearnSphere_AI_ActiveWorkspace`

Open it in VS Code:

```powershell
code D:\LearnSphere_AI_ActiveWorkspace
```

## Start the Independent Local Website

The active workspace uses port `5051`, separate from the original project on port `5000`.

```powershell
cd D:\LearnSphere_AI_ActiveWorkspace
.\04_active_workspace\RUN_LOCALHOST.ps1
```

Open `http://localhost:5051`.

The first run creates `.venv` and installs `06_code/requirements.txt`. Keep the PowerShell window open while testing.

## Stop the Local Website

Press `Ctrl+C` in the PowerShell window that is running the server. If that window was closed, use:

```powershell
cd D:\LearnSphere_AI_ActiveWorkspace
.\04_active_workspace\STOP_LOCALHOST.ps1
```

## Everyday Change Cycle

1. Open the active workspace and pull the latest GitHub work.
2. Start `http://localhost:5051`.
3. Edit only the files named in `CHANGE_MAP.md` for the feature being changed.
4. Refresh the browser and test the affected flow.
5. Run the tests.
6. Review `git status` and `git diff`.
7. Commit and push the change.

## Essential Commands

```powershell
# Go to the active workspace
cd D:\LearnSphere_AI_ActiveWorkspace

# See changed files
git status

# Get latest approved work
git pull origin master

# Create a focused work branch
git switch -c feature/short-description

# Run automated tests
python -m unittest discover -s 08_testing

# Review exactly what will be committed
git diff

# Save a change locally
git add 06_code/frontend/index.html
git commit -m "Describe the change clearly"

# Send the branch to GitHub
git push -u origin feature/short-description

# After pull-request approval, return to master
git switch master
git pull origin master
```

## Git Safety Rules

- Never commit `.env`, databases, uploads, passwords, or tokens.
- Never run `git reset --hard` to remove work.
- Use `git status` before and after every change.
- One focused feature or fix per commit.
- Keep `master` deployable. Use feature branches for non-trivial changes.

## When a Change Does Not Appear

1. Confirm you started port `5051`, not the original port `5000`.
2. Hard-refresh the browser with `Ctrl+F5`.
3. Check the PowerShell server window for errors.
4. Confirm the saved file is inside `D:\LearnSphere_AI_ActiveWorkspace`.
5. Run the relevant tests and consult `CHANGE_MAP.md`.

## Hosted Application

- Website: `https://ekanath2417.github.io/LearnSphere_AI/`
- Repository: `https://github.com/Ekanath2417/LearnSphere_AI`
- API service: `https://learnsphere-ai-c01p.onrender.com`

GitHub Pages hosts the static frontend. Render hosts the Flask API. When changing authentication or data features, test locally first and then verify both the Pages runtime URL and Render CORS origin.

