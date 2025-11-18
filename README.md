# StartHub - Group Repository

## Project description

**StartHub** is a social networking platform designed for entrepreneurs and innovators to create, share, and connect through their startup projects. It allows users to register, showcase their startups, interact with others through comments and votes, and explore projects organized by thematic categories.  

The goal of **StartHub** is to foster collaboration, visibility, and knowledge exchange within the startup ecosystem.

---

## Group members

**David Santiago Velasquez Gomez**

**Stiven Aguirre Granada**

**Juan Felipe Hernandez Ochoa**

**Sergio Alejandro Reita Serrano**  

**David Andres Camelo Suarez**  

---

## Quick Start (Backend)

- Configure environment:
```bash
cp backend/.env.example backend/.env
# Edit DATABASE_URL (MySQL) and APP_DEBUG
```

- Install dependencies:
```bash
pip install -r backend/requirements.txt
```

- Migrations (if DB already exists and matches, use stamp):
```bash
alembic -c backend/alembic.ini upgrade head
# If it fails due to existing tables:
alembic -c backend/alembic.ini stamp head
```

- Run API:
```bash
python -m uvicorn backend.main:app --reload --port 8000
```

- Health & Docs:
```bash
curl -i http://127.0.0.1:8000/health
curl -i http://127.0.0.1:8000/health/db
# Swagger UI: http://127.0.0.1:8000/docs
```

## E2E (Comments & Votes)

```bash
# Minimal seed (APP_DEBUG=true)
curl -i -X POST http://127.0.0.1:8000/dev/bootstrap

# Create comment (user_id=1, startup_id=1)
curl -i -X POST "http://127.0.0.1:8000/comments/?user_id=1" \
	-H "Content-Type: application/json" \
	-d '{"content":"Hola mundo","startup_id":1}'

# List comments
curl -i "http://127.0.0.1:8000/comments/?startup_id=1"

# Upsert vote (upvote)
curl -i -X POST "http://127.0.0.1:8000/votes/?user_id=1" \
	-H "Content-Type: application/json" \
	-d '{"startup_id":1,"vote_type":"upvote"}'

# Count votes
curl -i "http://127.0.0.1:8000/votes/count/1"
```

See `backend/README.md` for deeper backend details and `Database/` for SQL schema and scripts.
