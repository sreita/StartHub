# StartHub Documentation Index

Master index for all StartHub project documentation. **Start here** to find guides for any task.

---

## ��� Core Guides

### Getting Started & Setup

- **[GETTING_STARTED.md](./setup/GETTING_STARTED.md)** ⭐ **START HERE** - 5-minute quick start with Docker
  - Prerequisites and installation
  - Running your first command
  - Accessing services
  - Creating test accounts

- **[DOCKER_SETUP.md](./setup/DOCKER_SETUP.md)** - Complete Docker installation and configuration
  - Docker Desktop installation by OS (Windows, Mac, Linux)
  - Project configuration
  - Service startup and shutdown commands
  - Service access URLs and credentials
  - Networking and service communication
  - Troubleshooting Docker issues

### Development & Testing

- **[TESTING_GUIDE.md](./testing/TESTING_GUIDE.md)** - How to run tests locally and results
  - Unit test execution
  - Integration test procedures
  - E2E test coverage
  - Test structure and organization
  - Known issues and bugs
  - Troubleshooting tests

### Documentation References

- **[STRUCTURE.md](./STRUCTURE.md)** - Complete project structure
  - Folder organization
  - File hierarchy
  - Module descriptions
  - Technology stack

- **[CHANGELOG.md](./CHANGELOG.md)** - All GitHub differences
  - What changed from original
  - New features added
  - Modifications made
  - Updates and improvements

### Scripts & Utilities

- **[Scripts Documentation](./scripts/)** - Script guides and usage
  - **[DOCKER.md](./scripts/DOCKER.md)** - Docker script reference (start.sh, dev.sh, helpers.sh)

### Services & Tools

- **[MAILHOG.md](./services/MAILHOG.md)** - Email testing with MailHog
  - Configuration
  - Email capture
  - Development testing

### Project Information

- **[CONTRIBUTING.md](./project/CONTRIBUTING.md)** - How to contribute to StartHub
  - Development setup
  - Code standards
  - Pull request process

- **[PROJECT_STATUS.md](./project/PROJECT_STATUS.md)** - Current project status and progress
  - Service status
  - Feature completion
  - Known issues

- **[TROUBLESHOOTING.md](./project/TROUBLESHOOTING.md)** - Common issues and solutions
  - Service issues
  - Database problems
  - Port conflicts
  - Connection issues

---

## ��� Quick Navigation

| I want to...                         | Go to...                                      |
|--------------------------------------|-----------------------------------------------|
| Get started in 5 minutes             | [GETTING_STARTED.md](./setup/GETTING_STARTED.md)     |
| Install and configure Docker        | [DOCKER_SETUP.md](./setup/DOCKER_SETUP.md)          |
| Run tests                            | [TESTING_GUIDE.md](./testing/TESTING_GUIDE.md)       |
| Understand the project structure    | [STRUCTURE.md](./STRUCTURE.md)                       |
| See what changed from GitHub        | [CHANGELOG.md](./CHANGELOG.md)                       |
| Use Docker scripts                  | [DOCKER.md](./scripts/DOCKER.md)                     |
| Set up email testing                | [MAILHOG.md](./services/MAILHOG.md)                 |
| Contribute to the project           | [CONTRIBUTING.md](./project/CONTRIBUTING.md)        |
| Fix common problems                 | [TROUBLESHOOTING.md](./project/TROUBLESHOOTING.md)   |

---

## ��� Directory Structure

```
docs/
├── INDEX.md                      ← You are here
├── CHANGELOG.md                  - GitHub differences (306 lines)
├── STRUCTURE.md                  - Project structure (271 lines)
│
├── setup/                        - Installation & configuration
│   ├── GETTING_STARTED.md       - Quick start guide (5 minutes)
│   ├── DOCKER_SETUP.md          - Complete Docker guide (145 lines)
│   └── SETUP_SUMMARY.md         - Configuration summary
│
├── scripts/                      - Script documentation
│   └── DOCKER.md                - Docker scripts reference (183 lines)
│
├── testing/                      - Testing documentation
│   └── TESTING_GUIDE.md         - Complete testing guide (408 lines)
│
├── project/                      - Project information
│   ├── CONTRIBUTING.md          - Contribution guidelines (666 lines)
│   ├── PROJECT_STATUS.md        - Current status (437 lines)
│   └── TROUBLESHOOTING.md       - Troubleshooting guide (668 lines)
│
└── services/                     - Service documentation
    └── MAILHOG.md               - Email testing service (161 lines)
```

---

## ��� By Role

### For Developers
1. [GETTING_STARTED.md](./setup/GETTING_STARTED.md) - Get the project running
2. [DOCKER.md](./scripts/DOCKER.md) - Manage Docker containers
3. [STRUCTURE.md](./STRUCTURE.md) - Understand the codebase
4. [CONTRIBUTING.md](./project/CONTRIBUTING.md) - Contribution guidelines

### For Testers
1. [GETTING_STARTED.md](./setup/GETTING_STARTED.md) - Set up environment
2. [TESTING_GUIDE.md](./testing/TESTING_GUIDE.md) - Run tests
3. [TROUBLESHOOTING.md](./project/TROUBLESHOOTING.md) - Fix issues

### For DevOps / Infrastructure
1. [DOCKER_SETUP.md](./setup/DOCKER_SETUP.md) - Docker configuration
2. [STRUCTURE.md](./STRUCTURE.md) - Architecture overview
3. [PROJECT_STATUS.md](./project/PROJECT_STATUS.md) - System status

---

## ��� Service Information

### Internal Service Addresses (within Docker)
- MySQL: `db:3306`
- FastAPI: `fastapi:8000`
- Spring Auth: `spring:8081`
- MailHog SMTP: `mailhog:1025`

### External Access (from host machine)
- Frontend: http://localhost:3000
- FastAPI API: http://localhost:8000
- FastAPI Docs: http://localhost:8000/docs
- Spring Auth: http://localhost:8081
- MailHog Web UI: http://localhost:8025

---

## ��� Technology Stack

| Service | Technology | Port | Purpose |
|---------|-----------|------|---------|
| Frontend | Nginx | 3000 | Web UI |
| Spring Boot | Java 21 | 8081 | Authentication API |
| FastAPI | Python 3.12 | 8000 | Data API |
| MySQL | MySQL 8.0 | 3307 | Database |
| MailHog | SMTP Testing | 8025 | Email Testing |

---

## ⚠️ Known Issues

- Spring Boot authentication returns HTTP 500 instead of 401/403 for invalid credentials
  - See [TESTING_GUIDE.md](./testing/TESTING_GUIDE.md) for details
  - Recommended fix: Improve exception handling in Spring Boot

---

## ✅ Setup Checklist

- [ ] Docker Desktop installed and running
- [ ] `.env` file created in project root
- [ ] `docker compose up -d --build` executed successfully
- [ ] All services in "Up" status (`docker compose ps`)
- [ ] Frontend accessible at http://localhost:3000
- [ ] FastAPI docs available at http://localhost:8000/docs
- [ ] Tests passing (`bash scripts/test/run_all_tests.sh`)

---

## ��� Quick Links

| Link | Purpose |
|------|---------|
| [GitHub Repository](https://github.com/sreita/StartHub) | Project source code |
| [Getting Started](./setup/GETTING_STARTED.md) | Start here |
| [Project Status](./project/PROJECT_STATUS.md) | Current state |
| [Troubleshooting](./project/TROUBLESHOOTING.md) | Fix problems |

---

## ��� Documentation Statistics

- **Total documentation files**: 12
- **Total lines of documentation**: 3,000+
- **Language**: 100% English
- **Last Updated**: December 8, 2025
- **Project Status**: ⚠️ 95% Operational (Spring Boot auth fix pending)

---

## ��� Next Steps

1. **New to the project?** Start with [GETTING_STARTED.md](./setup/GETTING_STARTED.md)
2. **Want to contribute?** Read [CONTRIBUTING.md](./project/CONTRIBUTING.md)
3. **Having issues?** Check [TROUBLESHOOTING.md](./project/TROUBLESHOOTING.md)
4. **Need details?** See [STRUCTURE.md](./STRUCTURE.md)

---

**Last Updated**: December 8, 2025  
**Maintained By**: Engineering Team  
**Questions?** Check [TROUBLESHOOTING.md](./project/TROUBLESHOOTING.md) or open a GitHub issue.
