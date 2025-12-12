# StartHub

**Startup Management and Exploration Platform** — Microservices architecture with Spring Boot authentication and FastAPI data API.

---

## 📋 Project Description

**StartHub** is a social network for entrepreneurs and innovators that enables creating, sharing, and connecting through startup projects. Users can register, showcase their startups, interact through comments and votes, and explore projects organized by thematic categories.

The goal is to foster collaboration, visibility, and knowledge exchange within the startup ecosystem.

---

## 👥 Team

- **David Santiago Velasquez Gomez**
- **Stiven Aguirre Granada**
- **Juan Felipe Hernandez Ochoa**
- **Sergio Alejandro Reita Serrano**
- **David Andres Camelo Suarez**

_Project developed for **Software Engineering II** — Universidad Nacional de Colombia, 2025._

---

## 🏗️ Architecture

```
Final-Project/
├── services/
│   ├── fastapi/                        # Data backend (comments, votes, startups)
│   │   ├── app/                        # Source code (api/, models/, services/, etc.)
│   │   ├── alembic/                    # Database migrations
│   │   ├── requirements.txt
│   │   └── .env                        # Local configuration (not tracked)
│   └── spring-auth/                    # JWT authentication service
│       ├── src/
│       ├── pom.xml
│       └── .env                        # Local configuration (not tracked)
├── frontend/                           # Web interface (HTML/JS/CSS)
│   ├── js/                             # auth.js, home.js, startup_info.js, navbar.js
│   ├── css/                            # Styles (base/, components/, layout/, modes/, pages/)
│   ├── components/                     # Reusable HTML components (navbar)
│   └── *.html                          # Pages (login, signup, home, profile, etc.)
├── scripts/                            # Development and testing tools
│   ├── dev-server.py                   # HTTP server for frontend
│   ├── start_all.sh                    # Start all services (FastAPI, Spring, Frontend, MailHog)
│   ├── stop_all.sh                     # Stop all services
│   ├── *_mailhog.sh                    # MailHog management scripts
│   └── test/                           # Test suites
│       ├── test_crud_complete.py       # Complete CRUD test suite
│       ├── test_users_startups.py      # User & Startup tests
│       ├── test_votes_comments.py      # Vote & Comment tests
│       ├── test_search.py              # Search & Filter tests
│       ├── test_manual.py              # Quick smoke test
│       ├── test_backend.sh             # Backend validation (legacy)
│       ├── test_frontend.sh            # Frontend validation (legacy)
│       └── test_all_features.sh        # Integration tests (legacy)
├── docs/                               # Technical documentation
│   ├── MAILHOG.md                      # Email testing setup guide
│   ├── TESTING_GUIDE.md                # Quick testing reference
│   ├── INTEGRATION_TESTING.md          # Complete integration test documentation
│   ├── COMPLETE_MANUAL_TESTING.md      # Detailed testing scenarios
│   └── TROUBLESHOOTING.md              # Common issues and solutions
├── Database/                           # MySQL schema and seed scripts
│   ├── schema/                         # DDL and views
│   ├── seeds/                          # Sample data
│   ├── utilities/                      # Maintenance scripts (reload_all.sh, truncate_all.sh)
│   └── verifiers/                      # Data validation queries
├── tools/                              # External tools (MailHog - not tracked)
├── logs/                               # Service logs and PID files (not tracked)
└──.github/                            # GitHub Actions workflows
    └── workflows/                      # CI/CD pipelines (ci.yml, java-ci.yml, integration-test.yml)
```

---

## 🚀 Quick Start

### ⭐ Option 1: Docker (Recommended - Easiest)

**Prerequisites:**
- **Docker Desktop** (includes Docker Compose) — [Download](https://www.docker.com/products/docker-desktop)

**Installation:**

```bash
git clone https://github.com/sreita/StartHub.git
cd StartHub/Final-Project

# Start all services (builds images and containers on first run)
docker compose -f docker/compose.yaml up -d --build

# Or use the helper script (Windows: run-docker.bat, Unix: ./run-docker.sh)
./docker/run-docker.sh up -d --build
```

**Access the Application** (wait ~30-40 seconds for initialization):
- **Frontend**: http://localhost:3000
- **FastAPI Docs**: http://localhost:8000/docs
- **Spring Boot API**: http://localhost:8081/api/v1
- **MailHog Email UI**: http://localhost:8025
- **MySQL**: `localhost:3307` (user: `startHub`, password: `startHub123`)

**Useful Docker Commands:**
```bash
# View service status
./docker/run-docker.sh ps

# View logs
./docker/run-docker.sh logs -f

# Stop services
./docker/run-docker.sh down

# Full documentation
cat docker/README.md
```

For detailed Docker setup, see **[docs/setup/DOCKER_SETUP.md](docs/setup/DOCKER_SETUP.md)**.

---

### 🛠️ Option 2: Local Installation (Advanced)

**Prerequisites:**
- **Java 21+** (for Spring Boot)
- **Python 3.12+** with virtualenv
- **MySQL 8.0+** (local or remote)
- **Git Bash** (Windows) or compatible shell
- **MailHog** (optional, for email testing)

**1. Clone and Setup Environment:**

```bash
git clone https://github.com/sreita/StartHub.git
cd StartHub/Final-Project

# Create and activate Python virtual environment
python -m venv .venv
source .venv/Scripts/activate  # Windows Git Bash
# or: source .venv/bin/activate  # Linux/Mac

# Install Python dependencies
pip install -r services/fastapi/requirements.txt
```


### 2. Configure Environment Variables

Create `.env` files from the provided examples:

**FastAPI** (`services/fastapi/.env`):
```bash
cd services/fastapi
cp .env.example .env
# Edit .env with your MySQL credentials:
# DATABASE_URL=mysql+mysqlconnector://root:YOUR_PASSWORD@localhost:3306/starthub
# APP_DEBUG=true
# CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Spring Boot** (`services/spring-auth/.env`):
```bash
cd services/spring-auth
cp .env.example .env
# Edit .env with your credentials:
# DB_PASSWORD=YOUR_PASSWORD
# DB_USERNAME=root
# DB_URL=jdbc:mysql://localhost:3306/starthub
# SERVER_PORT=8081
```

⚠️ **Important**: Never commit `.env` files. They contain sensitive credentials and are ignored by `.gitignore`.

### 3. Setup MySQL Database

Ensure MySQL is running, then execute:

```bash
cd Database/utilities
bash reload_all.sh
```

This script will:
- Create the `starthub` database
- Load the schema (tables, relationships)
- Load views
- Populate sample data (users, startups, comments, votes)

### 4. Setup MailHog (Optional - for Email Testing)

```bash
bash scripts/setup_mailhog.sh
```

MailHog provides a fake SMTP server for testing email functionality without sending real emails.

### 5. Start All Services

```bash
bash scripts/start_all.sh
```

This starts:
- **MailHog** (SMTP: 1025, Web UI: 8025)
- **FastAPI** backend (port 8000)
- **Spring Boot** authentication (port 8081)
- **Frontend** server (port 3000)

**Access the Application**:
- **Frontend**: http://localhost:3000
- **FastAPI Docs** (Swagger): http://127.0.0.1:8000/docs
- **Spring Boot API**: http://localhost:8081/api/v1
- **MailHog UI**: http://localhost:8025

**Stop All Services**:
```bash
bash scripts/stop_all.sh
```

---

## 🔌 Ports and Services

|   Service    | Port |              Description               |
|--------------|------|----------------------------------------|
|  Frontend    | 3000 |          Static web interface          |
|    FastAPI   | 8000 |  Data API (startups, comments, votes)  |
| Spring Boot  | 8081 | JWT authentication and user management |
| MailHog SMTP | 1025 |       Email capture for testing        |
|  MailHog UI  | 8025 | Web interface to view captured emails  |

---

## 🔐 Authentication API (Spring Boot - Port 8081)

Base URL: `http://localhost:8081/api/v1`

### Endpoints

- `POST /registration` - Register new user
  ```bash
  curl -X POST http://localhost:8081/api/v1/registration \
    -H "Content-Type: application/json" \
    -d '{
      "firstName": "John",
      "lastName": "Doe",
      "email": "john.doe@example.com",
      "password": "SecurePass123!"
    }'
  ```

- `GET /registration/confirm?token=...` - Confirm email address
- `POST /auth/login` - Login (returns JWT token)
  ```bash
  curl -X POST http://localhost:8081/api/v1/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email": "john.doe@example.com", "password": "SecurePass123!"}'
  ```

- `POST /auth/logout` - Logout
- `POST /auth/recover-password` - Request password reset
- `POST /auth/reset-password` - Reset password with token

---

## 📊 Data API (FastAPI - Port 8000)

Base URL: `http://127.0.0.1:8000`

Interactive documentation: http://127.0.0.1:8000/docs

### Startup Endpoints

- `GET /startups` - List all startups
- `GET /startups/{id}` - Get startup details
- `POST /startups?user_id={id}` - Create new startup
- `PUT /startups/{id}?user_id={id}` - Update startup
- `DELETE /startups/{id}?user_id={id}` - Delete startup
- `GET /startups/my-startups?user_id={id}` - Get user's startups
- `GET /startups/search?q=...&categorias=...&sort_by=...` - Search and filter startups

### Comment Endpoints

- `GET /comments?startup_id={id}` - List comments for a startup
- `POST /comments?user_id={id}` - Create comment
- `PUT /comments/{id}?user_id={id}` - Update comment
- `DELETE /comments/{id}?user_id={id}` - Delete comment

### Vote Endpoints

- `GET /votes/count/{startup_id}` - Get vote counts (upvotes/downvotes)
- `POST /votes?user_id={id}` - Vote on startup (upvote/downvote)
- `DELETE /votes?user_id={id}&startup_id={id}` - Remove vote

### Health Check

- `GET /health` - API health status
- `GET /health/db` - Database connectivity check

---

## 🧪 Testing

### Comprehensive Python Test Suites

StartHub includes complete test coverage in `scripts/test/`:

```bash
# Complete CRUD test suite (recommended)
python scripts/test/test_crud_complete.py

# Specific feature tests
python scripts/test/test_users_startups.py    # User & Startup operations
python scripts/test/test_votes_comments.py    # Votes & Comments
python scripts/test/test_search.py            # Search & Filters

# Quick smoke test
python scripts/test/test_manual.py
```

**Test Coverage**:
- ✅ User registration, confirmation, login, profile management
- ✅ Startup CRUD (Create, Read, List, Update, Delete, Statistics)
- ✅ Vote operations (Upvote, Downvote, Count, Delete)
- ✅ Comment operations (Create, Read, Update, Delete)
- ✅ Search (Keyword, Categories, Filters, Sorting, Pagination, Autocomplete)
- ✅ User deletion and post-deletion verification

### Legacy Shell Script Tests

```bash
# Backend service validation
bash scripts/test/test_backend.sh

# Frontend resources validation
bash scripts/test/test_frontend.sh

# Integration test suite
bash scripts/test/test_all_features.sh
```

### Manual Testing

See comprehensive guides in `docs/`:
- [Testing Guide](docs/testing/TESTING_GUIDE.md) - Quick reference with all test commands
- [Integration Testing](docs/testing/INTEGRATION_TESTING.md) - Complete integration test documentation
- [Complete Manual Testing](docs/testing/COMPLETE_MANUAL_TESTING.md) - Detailed scenarios
- [Troubleshooting](docs/project/TROUBLESHOOTING.md) - Common issues

---

## 📧 Email Testing with MailHog

StartHub uses MailHog for email testing in development:

1. **Start MailHog**: `bash scripts/start_mailhog.sh`
2. **Open Web UI**: http://localhost:8025
3. **Register a user** on the application
4. **Check MailHog** to see the confirmation email
5. **Click the confirmation link** to activate the account

See [MailHog Documentation](docs/services/MAILHOG.md) for detailed instructions.

---

## 🗄️ Database Management

### Rebuild Database

Recreate the database from scratch with fresh sample data:

```bash
cd Database/utilities
bash reload_all.sh
```

### Clean Data (Keep Schema)

Remove all data but keep the table structure:

```bash
cd Database/utilities
bash truncate_all.sh
```

### Verify Database

```bash
cd Database/verifiers
mysql -u root -p starthub < verify_data.sql
mysql -u root -p starthub < verify_views.sql
```

---

## 📚 Documentation Hub

All documentation is centralized in the [`docs/`](docs/) directory, organized by topic. See **[docs/INDEX.md](docs/INDEX.md)** for a complete overview.

### Key Guides

|                               Guide                               |                 Purpose                |
|-------------------------------------------------------------------|----------------------------------------|
|             **[DOCKER_SETUP.md](docs/setup/DOCKER_SETUP.md)**             | Docker installation and environment setup |
|   **[DOCKER_ORCHESTRATION.md](docs/setup/DOCKER_ORCHESTRATION.md)**       | Compose services, networking, volumes, workflows |
|              **[TESTING_GUIDE.md](docs/testing/TESTING_GUIDE.md)**        | Running unit and integration tests |
|        **[INTEGRATION_TESTING.md](docs/testing/INTEGRATION_TESTING.md)**  | End-to-end testing procedures |
|  **[COMPLETE_MANUAL_TESTING.md](docs/testing/COMPLETE_MANUAL_TESTING.md)** | Step-by-step manual test cases |
|             **[MAILHOG.md](docs/services/MAILHOG.md)**                    | Email testing with MailHog |
|        **[TROUBLESHOOTING.md](docs/project/TROUBLESHOOTING.md)**          | Common issues and solutions |
|         **[PROJECT_STATUS.md](docs/project/PROJECT_STATUS.md)**           | Current project status and roadmap |
|           **[CONTRIBUTING.md](docs/project/CONTRIBUTING.md)**             | Contribution guidelines |

### Docker Documentation

The `docker/` directory contains the Compose file and helper scripts; detailed documentation lives in [`docs/setup`](docs/setup):

- **[docs/setup/DOCKER_ORCHESTRATION.md](docs/setup/DOCKER_ORCHESTRATION.md)** — Docker architecture, commands, networking, volumes
- **[docker/compose.yaml](docker/compose.yaml)**                        — Service orchestration configuration
- **docker/run-docker.sh** (Unix) / **docker/run-docker.bat** (Windows) — Helper scripts

---

## 🛠️ Development Commands

### Database Migrations (Alembic)

```bash
cd services/fastapi

# Create new migration
python -m alembic -c alembic.ini revision --autogenerate -m "description"

# Apply migrations
python -m alembic -c alembic.ini upgrade head

# Revert last migration
python -m alembic -c alembic.ini downgrade -1
```

### Spring Boot

```bash
cd services/spring-auth

# Build project
./mvnw.cmd clean package

# Run tests
./mvnw.cmd test

# Run with specific profile
./mvnw.cmd spring-boot:run -Dspring-boot.run.profiles=test
```

### Clean Build Artifacts

```bash
# Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name ".pytest_cache" -exec rm -rf {} +

# Java build files
cd services/spring-auth
./mvnw.cmd clean
```

---

## 🔄 CI/CD

GitHub Actions workflows are configured in `.github/workflows/`:

- **ci.yml** - FastAPI tests (Python 3.12, SQLite for tests)
- **java-ci.yml** - Spring Boot tests (JDK 21, H2 in-memory database)
- **integration-test.yml** - Full stack integration tests with MySQL

---

## 📝 Project Structure Details

### Frontend Structure

```
frontend/
├── *.html                      # Main pages
├── components/                 # Reusable components
│   └── navbar.html
├── css/
│   ├── base/                   # Reset styles
│   ├── components/             # Component-specific styles
│   ├── layout/                 # Layout utilities
│   ├── modes/                  # Theme variations (night mode)
│   ├── pages/                  # Page-specific styles
│   └── styles.css              # Main stylesheet
└── js/
    ├── auth.js                 # Authentication logic
    ├── home.js                 # Home page functionality
    ├── navbar.js               # Navigation bar component
    ├── startup_form.js         # Startup creation/editing
    ├── startup_info.js         # Startup details page
    └── utils.js                # Utility functions
```

### Backend Structure (FastAPI)

```
services/fastapi/
├── app/
│   ├── main.py                 # Application entry point
│   ├── api/                    # API routes
│   ├── core/                   # Configuration
│   ├── db/                     # Database connection
│   ├── models/                 # SQLAlchemy models
│   ├── repositories/           # Data access layer
│   ├── schemas/                # Pydantic schemas
│   └── services/               # Business logic
├── alembic/                    # Database migrations
├── requirements.txt
└── .env.example                # Environment template
```

### Backend Structure (Spring Boot)

```
services/spring-auth/
└── src/
    ├── main/
    │   ├── java/com/example/demo/
    │   │   ├── appuser/        # User entity and services
    │   │   ├── controller/     # REST controllers
    │   │   ├── email/          # Email service
    │   │   ├── registration/   # Registration logic
    │   │   └── security/       # JWT and security config
    │   └── resources/
    │       ├── application.yml # Main configuration
    │       ├── application-test.yml  # Test configuration
    │       └── certs/          # JWT keys
    └── test/                   # Unit tests
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Workflow

1. Make sure all services are stopped: `bash scripts/stop_all.sh`
2. Create your `.env` files from `.env.example` templates
3. Setup the database: `bash Database/utilities/reload_all.sh`
4. Start all services: `bash scripts/start_all.sh`
5. Run tests before committing:
   ```bash
   bash scripts/test_backend.sh
   bash scripts/test_frontend.sh
   ```

---

## 📄 License

This project is educational software developed for Software Engineering II course at Universidad del Norte.

---

## 🆘 Support

If you encounter issues:

1. Check [Troubleshooting Guide](docs/project/TROUBLESHOOTING.md)
2. Run diagnostic scripts: `bash scripts/test_backend.sh`
3. Check service logs in `logs/` directory
4. Verify all prerequisites are installed

For MailHog issues, see [MailHog Documentation](docs/services/MAILHOG.md).

---

**Last Updated**: November 28, 2025  
**Version**: 2.0  
**Status**: ✅ All services operational
