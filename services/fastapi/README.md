# StartHub FastAPI Backend

Python (FastAPI) backend service implementing data management for startups, comments, votes, and search functionality.

---

## 📋 Overview

This service provides a RESTful API for all data operations in StartHub. It connects to a MySQL database and exposes endpoints for:

- **Startups**: CRUD operations, search, and filtering
- **Comments**: Create, read, update, delete comments on startups
- **Votes**: Upvote/downvote startups
- **Categories**: List available categories
- **Search**: Advanced search with filters and sorting

---

## 🏗️ Project Structure

```
services/fastapi/
├── app/
│   ├── main.py                  # Application entry point
│   ├── core/
│   │   └── config.py            # Environment configuration
│   ├── db/
│   │   ├── base.py              # SQLAlchemy base
│   │   └── session.py           # Database session management
│   ├── models/                  # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── comment.py
│   │   ├── vote.py
│   │   ├── startup.py
│   │   ├── user.py
│   │   └── search.py
│   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── comment.py
│   │   ├── vote.py
│   │   └── startup.py
│   ├── repositories/            # Data access layer
│   │   ├── comment_repository.py
│   │   ├── vote_repository.py
│   │   └── startup_repository.py
│   ├── services/                # Business logic
│   │   ├── comment_service.py
│   │   ├── vote_service.py
│   │   └── search_service.py
│   └── api/                     # API routes
│       ├── router.py
│       └── routes/
│           ├── comments.py
│           ├── votes.py
│           ├── startups.py
│           ├── search.py
│           └── dev.py
├── alembic/                     # Database migrations
│   ├── env.py
│   └── versions/
│       └── 20251118_000001_init_comments_votes.py
├── tests/                       # Unit tests
│   ├── conftest.py
│   ├── test_comments_votes.py
│   └── test_errors_comments_votes.py
├── alembic.ini                  # Alembic configuration
├── requirements.txt             # Python dependencies
├── .env                         # Local configuration (not tracked)
└── .env.example                 # Environment template
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```bash
# Database connection (MySQL)
DATABASE_URL=mysql+mysqlconnector://root:YOUR_PASSWORD@localhost:3306/starthub

# Application settings
APP_DEBUG=true

# CORS settings
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,*
```

**Important**:
- Use `mysql+mysqlconnector://` for MySQL
- For testing, you can use SQLite: `sqlite+pysqlite:///./starthub.db`
- Never commit `.env` to the repository

---

## 🚀 Installation and Setup

### Prerequisites

- **Python 3.12+**
- **MySQL 8.0+** (or use SQLite for testing)
- **Virtual environment** (recommended)

### 1. Create Virtual Environment

```bash
# From project root
python -m venv .venv

# Activate (Windows Git Bash)
source .venv/Scripts/activate

# Activate (Linux/Mac)
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
cd services/fastapi
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 4. Setup Database

**Option A - Use existing database**:

If you've already run `Database/utilities/reload_all.sh`, just align Alembic:

```bash
python -m alembic -c alembic.ini stamp head
```

**Option B - Let Alembic create tables**:

```bash
python -m alembic -c alembic.ini upgrade head
```

---

## ▶️ Running the Application

### Start Server

```bash
cd services/fastapi
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Options:
- `--reload`: Auto-reload on code changes (development only)
- `--host 127.0.0.1`: Listen address
- `--port 8000`: Port number

### Access API Documentation

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **OpenAPI JSON**: http://127.0.0.1:8000/openapi.json

### Health Check

```bash
curl http://127.0.0.1:8000/health
# {"status": "ok"}

curl http://127.0.0.1:8000/health/db
# {"ok": true, "result": 1}
```

---

## 📡 API Endpoints

### Startup Endpoints

```bash
# List all startups
GET /startups

# Get startup by ID
GET /startups/{startup_id}

# Get user's startups
GET /startups/my-startups?user_id={user_id}

# Create startup
POST /startups?user_id={user_id}
Content-Type: application/json
{
  "name": "My Startup",
  "description": "Description here",
  "category_id": 1,
  "funding_goal": 50000.0,
  "website": "https://example.com",
  "email": "contact@example.com"
}

# Update startup
PUT /startups/{startup_id}?user_id={user_id}
Content-Type: application/json
{
  "name": "Updated Name",
  "description": "Updated description"
}

# Delete startup
DELETE /startups/{startup_id}?user_id={user_id}
```

### Comment Endpoints

```bash
# List comments for a startup
GET /comments?startup_id={startup_id}&skip=0&limit=50

# Create comment
POST /comments?user_id={user_id}
Content-Type: application/json
{
  "startup_id": 1,
  "content": "Great idea!"
}

# Update comment
PUT /comments/{comment_id}?user_id={user_id}
Content-Type: application/json
{
  "content": "Updated comment text"
}

# Delete comment
DELETE /comments/{comment_id}?user_id={user_id}
```

### Vote Endpoints

```bash
# Get vote counts for a startup
GET /votes/count/{startup_id}
# Returns: {"upvotes": 5, "downvotes": 2}

# Vote on startup (upsert - creates or updates)
POST /votes?user_id={user_id}
Content-Type: application/json
{
  "startup_id": 1,
  "vote_type": "upvote"  # or "downvote"
}

# Delete vote
DELETE /votes?user_id={user_id}&startup_id={startup_id}
```

### Search Endpoints

```bash
# Search with query
GET /startups/search?q=tech

# Filter by categories
GET /startups/search?categorias=1,2

# Filter by minimum votes/comments
GET /startups/search?min_votos=5&min_comentarios=2

# Sort results
GET /startups/search?sort_by=votos_desc
# Options: votos_asc, votos_desc, comentarios_asc, comentarios_desc

# Autocomplete suggestions
GET /startups/autocomplete?q=fin
# Returns: ["Finance Startup", "Fintech App"]

# Combined search
GET /startups/search?q=tech&categorias=1&min_votos=2&sort_by=votos_desc
```

---

## 🧪 Testing

### Run All Tests

```bash
cd services/fastapi
pytest tests/ -v
```

### Run Specific Test File

```bash
pytest tests/test_comments_votes.py -v
```

### Run with Coverage

```bash
pytest tests/ --cov=app --cov-report=html
```

### Test Scenarios

The test suite covers:
- ✅ CRUD operations for startups
- ✅ Comment creation, update, deletion
- ✅ Vote upsert (create/update) logic
- ✅ Search and filtering
- ✅ Error handling (404, 403, validation errors)
- ✅ Foreign key constraints

---

## 🔄 Database Migrations (Alembic)

### Create New Migration

```bash
cd services/fastapi

# Auto-generate migration from model changes
python -m alembic -c alembic.ini revision --autogenerate -m "add new field"
```

### Apply Migrations

```bash
# Upgrade to latest
python -m alembic -c alembic.ini upgrade head

# Upgrade to specific version
python -m alembic -c alembic.ini upgrade <revision_id>
```

### Revert Migrations

```bash
# Downgrade one version
python -m alembic -c alembic.ini downgrade -1

# Downgrade to specific version
python -m alembic -c alembic.ini downgrade <revision_id>
```

### View Migration History

```bash
python -m alembic -c alembic.ini history
python -m alembic -c alembic.ini current
```

### Troubleshooting Migrations

If Alembic tries to create tables that already exist:

```bash
# Mark current database state as latest migration
python -m alembic -c alembic.ini stamp head
```

---

## 🔍 Example Requests

### Create Startup Example

```bash
curl -X POST "http://127.0.0.1:8000/startups/?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "EcoTech Solutions",
    "description": "Sustainable technology for a better future",
    "category_id": 5,
    "funding_goal": 100000.0,
    "website": "https://ecotech.example.com",
    "email": "info@ecotech.example.com"
  }'
```

### Update Startup Example

```bash
curl -X PUT "http://127.0.0.1:8000/startups/1?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "EcoTech Solutions - Updated",
    "description": "Updated description with more details"
  }'
```

### Add Comment Example

```bash
curl -X POST "http://127.0.0.1:8000/comments/?user_id=3" \
  -H "Content-Type: application/json" \
  -d '{
    "startup_id": 1,
    "content": "This is an amazing startup! I love the sustainable approach."
  }'
```

### Vote Example

```bash
curl -X POST "http://127.0.0.1:8000/votes/?user_id=2" \
  -H "Content-Type: application/json" \
  -d '{
    "startup_id": 1,
    "vote_type": "upvote"
  }'
```

### Search Example

```bash
# Search for technology startups with good engagement
curl "http://127.0.0.1:8000/startups/search?categorias=1&min_votos=2&sort_by=votos_desc"
```

---

## 🛠️ Development

### Enable Debug Mode

In `.env`:
```bash
APP_DEBUG=true
```

This enables:
- SQL query logging
- Detailed error messages
- Auto-reload on code changes

### Bootstrap Sample Data (Debug Only)

When `APP_DEBUG=true`, you can create minimal sample data:

```bash
curl -X POST http://127.0.0.1:8000/dev/bootstrap
```

This creates:
- 3 test users
- 2 test startups
- Sample comments and votes

⚠️ **This endpoint is disabled in production** (`APP_DEBUG=false`)

---

## 📝 Data Models

### Startup Model

```python
class Startup:
    startup_id: int
    name: str
    description: str
    category_id: int
    owner_id: int  # Foreign key to User
    funding_goal: float (optional)
    current_funding: float
    website: str (optional)
    email: str (optional)
    logo_url: str (optional)
    created_at: datetime
```

### Comment Model

```python
class Comment:
    comment_id: int
    startup_id: int  # Foreign key to Startup
    user_id: int     # Foreign key to User
    content: str
    created_at: datetime
```

### Vote Model

```python
class Vote:
    vote_id: int
    startup_id: int     # Foreign key to Startup
    user_id: int        # Foreign key to User
    vote_type: str      # "upvote" or "downvote"
    created_at: datetime
```

---

## 🔐 Security Notes

- **CORS**: Configured for `localhost:3000` by default
- **Input Validation**: Pydantic schemas validate all requests
- **SQL Injection**: SQLAlchemy ORM prevents SQL injection
- **Authentication**: This service doesn't handle authentication (delegated to Spring Boot)
- **Authorization**: Basic user_id checks, improve for production

---

## 🐛 Troubleshooting

### Database Connection Errors

**Error**: `Can't connect to MySQL server`

**Solutions**:
1. Check MySQL is running: `mysql -u root -p`
2. Verify credentials in `.env`
3. Check firewall allows port 3306
4. Try using `127.0.0.1` instead of `localhost`

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'app'`

**Solution**: Run from the correct directory:
```bash
cd services/fastapi
python -m uvicorn app.main:app --reload
```

### Alembic Errors

**Error**: `Table 'user' already exists`

**Solution**: Stamp current state:
```bash
python -m alembic -c alembic.ini stamp head
```

### CORS Errors

**Error**: Frontend can't access API

**Solution**: Add frontend URL to `.env`:
```bash
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 📋 Dependencies

Main packages (from `requirements.txt`):

- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **sqlalchemy** - ORM
- **mysql-connector-python** - MySQL driver
- **pydantic** - Data validation
- **alembic** - Database migrations
- **pytest** - Testing framework

---

## 🔄 CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`) runs:
- Linting checks
- Unit tests with SQLite
- Coverage reports

Tests run on every push to `main` and on pull requests.

---

**Last Updated**: November 28, 2025  
**API Version**: 1.0  
**Python Version**: 3.12+
