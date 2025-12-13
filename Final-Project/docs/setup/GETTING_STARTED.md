# 🚀 Quick Start Guide - StartHub

## ⚡ 30 Seconds to Run Everything

```bash
# 1. Navigate to project folder
cd c:/Users/yoshikagua/Desktop/U/Semestre\ 8/Ingenieria\ de\ Software\ II/Proyecto/StartHub

# 2. Start Docker
bash scripts/docker/start.sh start

# 3. Wait ~30 seconds for everything to initialize

# 4. Run tests
bash scripts/test/run_all_tests.sh
```

---

## 🌐 Service Access

Once started, access:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Web application |
| **Spring Boot** | http://localhost:8081/api/v1 | Authentication API |
| **FastAPI** | http://localhost:8000/api/v1 | Data API |
| **MailHog** | http://localhost:8025 | Email testing |

---

## 📁 Main Folder Structure

```
Final-Project/
├── docker/              # Docker Compose files
├── scripts/
│   ├── docker/          # Scripts to run with Docker
│   │   ├── start.sh     # Main orchestrator
│   │   ├── dev.sh       # Development mode (with logs)
│   │   └── README.md    # Documentation
│   └── test/            # Organized tests
│       ├── integration/ # Service tests
│       ├── e2e/         # End-to-end tests
│       ├── unit/        # Unit tests
│       └── run_all_tests.sh # Run all
├── services/
│   ├── spring-auth/     # Java backend
│   └── fastapi/         # Python backend
└── frontend/            # Frontend HTML/CSS/JS
```

---

## 🎮 Main Commands

### Docker - Basic Management

```bash
# Start all services
bash scripts/docker/start.sh start

# Check status
bash scripts/docker/start.sh status

# Stop all services
bash scripts/docker/start.sh stop

# Restart all services
bash scripts/docker/start.sh restart

# View all logs
bash scripts/docker/start.sh logs

# View logs for a specific service
bash scripts/docker/start.sh logs spring
bash scripts/docker/start.sh logs fastapi
bash scripts/docker/start.sh logs db
```

### Development Mode (With Live Logs)

```bash
bash scripts/docker/dev.sh
```

Starts Docker and displays logs in real-time. Press Ctrl+C to stop.

### Tests - Execution

```bash
# Run all tests
bash scripts/test/run_all_tests.sh

# Run integration tests
bash scripts/test/integration/test_complete_system.sh

# Run specific tests
bash scripts/test/integration/test_authentication.sh
bash scripts/test/integration/test_startups.sh
bash scripts/test/integration/test_interactions.sh
```

---

## 🐚 Container Shell Access

Access a shell inside containers:

```bash
# Spring Boot
bash scripts/docker/start.sh shell spring

# FastAPI
bash scripts/docker/start.sh shell fastapi

# MySQL
bash scripts/docker/start.sh shell db
```

---

## 🔄 Typical Development Workflow

### 1. Start everything
```bash
bash scripts/docker/start.sh start
```

### 2. Make code changes
Edit files in `services/spring-auth/` or `services/fastapi/`

### 3. Rebuild if major changes
```bash
bash scripts/docker/start.sh rebuild
```

### 4. View logs for debugging
```bash
bash scripts/docker/start.sh logs spring
```

### 5. Run tests
```bash
bash scripts/test/run_all_tests.sh
```

### 6. Stop when done
```bash
bash scripts/docker/start.sh stop
```

---

## 🧹 Maintenance

### Clean system (removes data)
```bash
bash scripts/docker/start.sh clean
```

### Rebuild everything from scratch
```bash
bash scripts/docker/start.sh rebuild
```

### View detailed status
```bash
bash scripts/docker/start.sh status
```

---

## 🆘 Quick Troubleshooting

### Docker not responding
```bash
# Restart Docker Desktop (Windows/Mac) or daemon (Linux)
# Then:
bash scripts/docker/start.sh start
```

### Tests can't connect to services
```bash
# Verify they're running
bash scripts/docker/start.sh status

# Restart
bash scripts/docker/start.sh restart
```

### View error logs
```bash
# Spring Boot
bash scripts/docker/start.sh logs spring

# FastAPI  
bash scripts/docker/start.sh logs fastapi

# MySQL
bash scripts/docker/start.sh logs db
```

---

## 📊 Available Tests

### Integration (40+ tests)
- Authentication
- Startup management
- Votes and comments
- Complete system

### E2E
- Docker tests
- Container verification

### Unit
- Python tests
- Bash tests

---

## 💡 Helpful Tips

### View all available commands
```bash
bash scripts/docker/start.sh help
```

### Quick development with live logs
```bash
bash scripts/docker/dev.sh
```

### Run a specific test without running all
```bash
bash scripts/test/integration/test_authentication.sh
```

### Access MySQL directly
```bash
bash scripts/docker/start.sh shell db
mysql -u root -proot starthub_db
```

---

## 📚 Complete Documentation

- [Docker Scripts](../scripts/DOCKER.md) - Docker orchestration guide
- [Testing Guide](../testing/TESTING_GUIDE.md) - How to run tests
- [Docker Setup](./DOCKER_SETUP.md) - Detailed Docker configuration
- [Project Status](../project/PROJECT_STATUS.md) - Service status and progress

---

## 🎯 Common Next Steps

**I want to...** | **Command**
---|---
Start the system | `bash scripts/docker/start.sh start`
Check if everything works | `bash scripts/test/run_all_tests.sh`
Develop (with logs) | `bash scripts/docker/dev.sh`
Review logs | `bash scripts/docker/start.sh logs`
Access a service | `bash scripts/docker/start.sh shell <service>`
Stop everything | `bash scripts/docker/start.sh stop`
Clean everything | `bash scripts/docker/start.sh clean`

---

**Last Updated**: December 8, 2025

**Version**: 1.0 - Fully Operational ✅
