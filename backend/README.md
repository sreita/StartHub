StartHub Backend
================

This Python (FastAPI) backend implements Comments and Votes for Startups, aligned with the SQL schema in `Database/schema/schema.sql`.

Structure
```
backend/
  main.py
  core/
    config.py
  db/
    base.py
    session.py
  models/
    __init__.py
    comment.py
    vote.py
    startup.py
    user.py
  schemas/
    comment.py
    vote.py
  repositories/
    comment_repository.py
    vote_repository.py
  services/
    comment_service.py
    vote_service.py
  api/
    router.py
    routes/
      comments.py
      votes.py
      dev.py
  tests/
    conftest.py
    test_comments_votes.py
    test_errors_comments_votes.py
  requirements.txt
  .env.example
```

Configuration
- Create `backend/.env` from `.env.example` and adjust:
  - `DATABASE_URL`: e.g. `mysql+mysqlconnector://user:pass@localhost:3306/starthub_db`
  - `APP_DEBUG`: `true/false` to enable SQL logs
  - `CORS_ORIGINS`: `*` or comma-separated list (e.g. `http://localhost:5173,http://localhost:3000`)

Install
```bash
pip install -r backend/requirements.txt
```

Run
```bash
python -m uvicorn backend.main:app --reload
```

Health
- `GET /health` → {"status":"ok"}
- `GET /health/db` → database ping information

Quick E2E (cURL)
- Minimal seed (only with `APP_DEBUG=true`):
```bash
curl -i -X POST http://127.0.0.1:8000/dev/bootstrap
```
- Create comment (for `user_id=1` on `startup_id=1`):
```bash
curl -i -X POST "http://127.0.0.1:8000/comments/?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Hello world",
    "startup_id": 1
  }'
```
- List comments for startup 1:
```bash
curl -i "http://127.0.0.1:8000/comments/?startup_id=1"
```
- Upsert vote for `user_id=1`:
```bash
curl -i -X POST "http://127.0.0.1:8000/votes/?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "startup_id": 1,
    "vote_type": "upvote"
  }'
```
- Count votes for startup 1:
```bash
curl -i "http://127.0.0.1:8000/votes/count/1"
```

Endpoints
- `POST /comments` (create)
- `GET /comments?startup_id=1&skip=0&limit=50` (list with pagination)
- `PUT /comments/{comment_id}` (update own)
- `DELETE /comments/{comment_id}` (delete own)
- `POST /votes` (upsert vote; 201 if created, 200 if updated)
- `GET /votes/count/{startup_id}` (up/down counts)
- `DELETE /votes?user_id=&startup_id=` (delete vote)
- `POST /dev/bootstrap` (only when `APP_DEBUG=true`, seeds minimal data)

Tests
```bash
python -m pytest -q
```

Notes
- Models and services validate existence of `User` and `Startup` before operating.
- For production, create tables per `Database/schema/schema.sql` or manage migrations with Alembic.

Migrations (Alembic)
- Alembic is configured in `backend/alembic/` with `backend/alembic.ini`.
- Ensure `DATABASE_URL` in `backend/.env`.
- Basic commands:
```bash
# Create migration from current models
alembic -c backend/alembic.ini revision --autogenerate -m "init comments votes"

# Apply migrations
alembic -c backend/alembic.ini upgrade head

# Revert last change
alembic -c backend/alembic.ini downgrade -1
```

Troubleshooting (Alembic)
- If `upgrade` fails due to existing tables (e.g., `Table 'user' already exists`), align state with:
```bash
alembic -c backend/alembic.ini stamp head
```

CI
- Workflow in `.github/workflows/ci.yml` runs `pytest` on each push/PR to `main`.
