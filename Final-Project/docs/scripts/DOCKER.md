# 🐳 Docker Scripts - StartHub

This directory contains scripts to manage the StartHub project with Docker.

## 📋 Available Scripts

### 1. `start.sh` - Main Docker Manager
**General-purpose tool to start, stop, and manage containers.**

**Commands:**
```bash
# Start everything (from repo root)
bash scripts/docker/start.sh start

# Stop everything
bash scripts/docker/start.sh stop

# Restart everything
bash scripts/docker/start.sh restart

# Check status
bash scripts/docker/start.sh status

# View logs (all or specific service)
bash scripts/docker/start.sh logs
bash scripts/docker/start.sh logs spring    # Spring Boot service logs

# Build images without cache
bash scripts/docker/start.sh build

# Full rebuild
bash scripts/docker/start.sh rebuild

# Clean volumes
bash scripts/docker/start.sh clean

# Run tests
bash scripts/docker/start.sh test

# Open shell in container
bash scripts/docker/start.sh shell spring
bash scripts/docker/start.sh shell fastapi
bash scripts/docker/start.sh shell db

# View help menu
bash scripts/docker/start.sh help
```

### 2. `dev.sh` - Development Mode
**Starts Docker with real-time logs. Perfect for development.**

```bash
bash dev.sh
```

**Features:**
- ✅ Starts all containers
- ✅ Shows live logs
- ✅ Immediate access to all services
- ✅ Press Ctrl+C to stop

### 3. `helpers.sh` - Helper Functions
**Library of reusable functions for Docker scripts.**

Provides reusable functions:
- `check_docker()` - Verify Docker availability
- `get_compose_file()` - Get compose file path
- `wait_for_service()` - Wait for service readiness
- `docker_exec()` - Execute command in container
- `docker_logs()` - View logs
- `docker_status()` - View status
- `docker_cleanup()` - Clean up system

---

## 🚀 Quick Usage

### Development (with logs)
```bash
bash dev.sh
```

### Development (without logs)
```bash
bash scripts/docker/start.sh start
bash scripts/docker/start.sh status
```

### View live logs
```bash
bash scripts/docker/start.sh logs          # All services
bash scripts/docker/start.sh logs spring   # Spring Boot only
bash scripts/docker/start.sh logs fastapi  # FastAPI only
bash scripts/docker/start.sh logs db       # MySQL only
```

### Run tests
```bash
bash scripts/docker/start.sh test
```

### Make changes and rebuild
```bash
# After Java/Python changes
bash scripts/docker/start.sh rebuild

# Or without cache
bash scripts/docker/start.sh build
bash scripts/docker/start.sh restart
```

---

## 🌐 Available Services

Once started, access:

| Service | URL | Port |
|---------|-----|------|
| **Frontend** | http://localhost:3000 | 3000 |
| **Spring Boot API** | http://localhost:8081 | 8081 |
| **FastAPI** | http://localhost:8000 | 8000 |
| **MailHog** | http://localhost:8025 | 8025 |
| **MySQL** | localhost | 3307 |

---

## 🐚 Shell in Containers

Access a shell inside a container:

```bash
# Spring Boot
bash start.sh shell spring
# Now you're in /app inside the container

# FastAPI
bash start.sh shell fastapi

# MySQL
bash start.sh shell db
mysql -u root -proot starthub_db
```

---

## 🧹 Maintenance

### Clean entire system
```bash
bash start.sh clean
```

### Rebuild after Dockerfile changes
```bash
bash start.sh rebuild
```

### View detailed status
```bash
bash start.sh status
```

---

## 📍 Important Locations

- **Docker Compose:** `../../docker/compose.yaml`
- **Frontend:** `../../frontend/`
- **Spring Boot:** `../../services/spring-auth/`
- **FastAPI:** `../../services/fastapi/`
- **Database:** `../../Database/`

---

## 🔧 Customization

To change ports or environment variables, edit `docker/compose.yaml` in the project root.

---

**Last Updated:** December 8, 2025
