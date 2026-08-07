# Deployment Guide

## Local demonstration

Use the commands in the root README. The app will be served at `http://localhost:5000`; no third-party AI key is needed for the demo fallback.

## Docker package

From the repository root:

```powershell
$env:JWT_SECRET_KEY = "generate-a-long-unique-secret"
docker compose -f 11_deployment/docker-compose.yml up --build
```

The compose package persists its SQLite database and uploads in Docker volumes. It is suitable for demonstrations, not a multi-instance public deployment.

## Managed hosting

`render.yaml` provisions a starter web service. Attach a managed PostgreSQL service and private object storage before public launch; SQLite and local files may be lost on ephemeral hosts. Set these secrets in the host dashboard:

- `JWT_SECRET_KEY`: a unique, high-entropy secret.
- `CORS_ORIGINS`: exact deployed frontend origin(s), never `*` in production.
- future provider keys: store only in secret management, never browser code or git.

## Production readiness gate

- [ ] PostgreSQL migrations and database backups
- [ ] private object storage with malware scanning and download authorization
- [ ] HTTPS, explicit CORS, secure cookie/token strategy, rate limits and CSRF review
- [ ] application monitoring, structured logs, and incident contact
- [ ] privacy policy, data deletion/export process and student consent text
- [ ] AI evaluation, prompt-injection tests, source citations and provider data-processing review
- [ ] accessibility and mobile acceptance testing

## Rollback

Deploy immutable tagged releases. If an issue is discovered, redeploy the previous passing image and preserve the database volume; do not overwrite student data during rollback.
