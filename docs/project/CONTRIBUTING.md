# Contributing to StartHub

Thank you for your interest in contributing to StartHub! This guide will help you get started with development.

---

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)
- [Project Structure](#project-structure)

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have:

- **Java 21+** - [Download](https://www.oracle.com/java/technologies/downloads/)
- **Python 3.12+** - [Download](https://www.python.org/downloads/)
- **MySQL 8.0+** - [Download](https://dev.mysql.com/downloads/)
- **Git** - [Download](https://git-scm.com/downloads)
- **Git Bash** (Windows) or compatible shell

### Verify Installation

```bash
java -version      # Should show Java 21 or higher
python --version   # Should show Python 3.12 or higher
mysql --version    # Should show MySQL 8.0 or higher
git --version      # Any recent version
```

---

## 💻 Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/StartHub.git
cd StartHub

# Add upstream remote
git remote add upstream https://github.com/sreita/StartHub.git
```

### 2. Create Python Virtual Environment

```bash
python -m venv .venv

# Activate (Windows Git Bash)
source .venv/Scripts/activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r services/fastapi/requirements.txt
```

### 3. Configure Environment Variables

**FastAPI** (`services/fastapi/.env`):
```bash
cd services/fastapi
cp .env.example .env
```

Edit `.env`:
```bash
DATABASE_URL=mysql+mysqlconnector://root:YOUR_PASSWORD@localhost:3306/starthub
APP_DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Spring Boot** (`services/spring-auth/.env`):
```bash
cd services/spring-auth
cp .env.example .env
```

Edit `.env`:
```bash
DB_PASSWORD=YOUR_PASSWORD
DB_USERNAME=root
DB_URL=jdbc:mysql://localhost:3306/starthub
SERVER_PORT=8081
```

### 4. Setup Database

```bash
cd Database/utilities
bash reload_all.sh
```

This creates:
- Database `starthub`
- All tables and relationships
- Sample data (users, startups, comments, votes)

### 5. Setup MailHog (Optional)

```bash
bash scripts/setup_mailhog.sh
```

MailHog provides email testing without sending real emails.

### 6. Start Development Environment

```bash
bash scripts/start_all.sh
```

Verify services are running:
- Frontend: http://localhost:3000
- FastAPI: http://127.0.0.1:8000/docs
- Spring Boot: http://localhost:8081/api/v1
- MailHog: http://localhost:8025

---

## 🔄 Development Workflow

### Creating a Feature

1. **Sync with upstream**:
   ```bash
   git fetch upstream
   git checkout integration/all-features
   git merge upstream/integration/all-features
   ```

2. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make changes**: Edit code, add features, fix bugs

4. **Test locally**:
   ```bash
   # Run Python test suites (comprehensive)
   source .venv/Scripts/activate
   python scripts/test/test_crud_complete.py
   python scripts/test/test_search.py
   
   # Run integration tests (shell scripts)
   bash scripts/test/test_backend.sh
   bash scripts/test/test_frontend.sh
   bash scripts/test/test_all_features.sh
   
   # Run unit tests
   cd services/fastapi && pytest tests/ -v
   cd services/spring-auth && ./mvnw.cmd test
   ```

5. **Commit changes**:
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request** on GitHub

### Commit Message Format

Follow conventional commits:

```
<type>: <description>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```bash
git commit -m "feat: add startup search by category"
git commit -m "fix: resolve CORS error on login endpoint"
git commit -m "docs: update API documentation"
git commit -m "test: add unit tests for vote service"
```

---

## 📏 Code Standards

### Python (FastAPI)

**Style**: Follow PEP 8

```python
# Use type hints
def get_startup(startup_id: int) -> Startup:
    return db.query(Startup).filter(Startup.id == startup_id).first()

# Docstrings for functions
def create_comment(content: str, startup_id: int, user_id: int) -> Comment:
    """
    Create a new comment on a startup.
    
    Args:
        content: Comment text
        startup_id: ID of the startup
        user_id: ID of the user creating comment
        
    Returns:
        Created comment object
    """
    pass

# Use meaningful variable names
startup_count = db.query(Startup).count()  # ✅ Good
sc = db.query(Startup).count()             # ❌ Bad
```

**Linting**:
```bash
# Install linting tools
pip install black flake8 mypy

# Format code
black services/fastapi/app/

# Check style
flake8 services/fastapi/app/

# Type checking
mypy services/fastapi/app/
```

### Java (Spring Boot)

**Style**: Follow Google Java Style Guide

```java
// Use meaningful names
public class StartupService {  // ✅ Good
public class SS {              // ❌ Bad

// Constants in UPPER_CASE
private static final int MAX_RETRIES = 3;

// CamelCase for methods
public UserDto getUserProfile(Long userId) { }

// Javadoc for public methods
/**
 * Authenticates a user and returns JWT token.
 *
 * @param email User's email address
 * @param password User's password
 * @return JWT token string
 * @throws AuthenticationException if credentials are invalid
 */
public String authenticate(String email, String password) { }
```

### JavaScript (Frontend)

**Style**: Use modern ES6+ syntax

```javascript
// Use const/let, not var
const API_URL = 'http://127.0.0.1:8000';  // ✅ Good
var API_URL = 'http://127.0.0.1:8000';    // ❌ Bad

// Arrow functions
const fetchStartups = async () => {
    const response = await fetch(`${API_URL}/startups`);
    return response.json();
};

// Destructuring
const { name, description, category_id } = startupData;

// Template literals
const message = `Welcome, ${user.firstName}!`;
```

### SQL

```sql
-- Use uppercase for keywords
SELECT * FROM Startup WHERE category_id = 1;

-- Indent for readability
SELECT 
    s.startup_id,
    s.name,
    COUNT(c.comment_id) AS comment_count
FROM Startup s
LEFT JOIN Comment c ON s.startup_id = c.startup_id
GROUP BY s.startup_id;

-- Comment complex queries
-- Get top 10 startups by upvote count
SELECT s.*, COUNT(v.vote_id) AS upvotes
FROM Startup s
LEFT JOIN Vote v ON s.startup_id = v.startup_id AND v.vote_type = 'upvote'
GROUP BY s.startup_id
ORDER BY upvotes DESC
LIMIT 10;
```

---

## 🧪 Testing Guidelines

### Before Committing

Run all tests:
```bash
# Stop services
bash scripts/stop_all.sh

# Clean state
cd Database/utilities && bash truncate_all.sh

# Reload data
bash reload_all.sh

# Start services
cd ../..
bash scripts/start_all.sh

# Wait for services to start
sleep 10

# Run shell script tests
bash scripts/test/test_backend.sh
bash scripts/test/test_frontend.sh
bash scripts/test/test_all_features.sh

# Run Python test suites
source .venv/Scripts/activate
python scripts/test/test_crud_complete.py
python scripts/test/test_search.py
```

### Writing Tests

**FastAPI Tests** (`services/fastapi/tests/`):

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_startup():
    """Test startup creation endpoint."""
    response = client.post(
        "/startups/?user_id=1",
        json={
            "name": "Test Startup",
            "description": "Test description",
            "category_id": 1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Startup"

def test_get_nonexistent_startup():
    """Test getting startup that doesn't exist."""
    response = client.get("/startups/99999")
    assert response.status_code == 404
```

**Spring Boot Tests** (`services/spring-auth/src/test/java/`):

```java
@SpringBootTest
@AutoConfigureMockMvc
class AuthControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    void testUserRegistration() throws Exception {
        mockMvc.perform(post("/api/v1/registration")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"firstName\":\"John\",\"lastName\":\"Doe\",\"email\":\"john@test.com\",\"password\":\"Test123!\"}"))
            .andExpect(status().isOk());
    }
    
    @Test
    void testLoginWithInvalidCredentials() throws Exception {
        mockMvc.perform(post("/api/v1/auth/login")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"email\":\"invalid@test.com\",\"password\":\"wrong\"}"))
            .andExpect(status().isUnauthorized());
    }
}
```

### Test Coverage Goals

- **FastAPI**: Aim for 80%+ coverage
  ```bash
  pytest tests/ --cov=app --cov-report=html
  # View coverage report at htmlcov/index.html
  ```

- **Spring Boot**: Aim for 70%+ coverage
  ```bash
  ./mvnw.cmd test jacoco:report
  # View report at target/site/jacoco/index.html
  ```

---

## 📤 Submitting Changes

### Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages follow convention
- [ ] No merge conflicts with main branch
- [ ] `.env` files are not committed
- [ ] No passwords or secrets in code

### Pull Request Template

```markdown
## Description
Brief description of what this PR does

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Related Issues
Fixes #123

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

### Code Review Process

1. **Submit PR**: Create pull request on GitHub
2. **Automated Checks**: GitHub Actions runs tests
3. **Code Review**: Team member reviews code
4. **Address Feedback**: Make requested changes
5. **Approval**: PR approved by reviewer
6. **Merge**: PR merged to main branch

---

## 📁 Project Structure

### Backend (FastAPI)

```
services/fastapi/
├── app/
│   ├── main.py              # Entry point
│   ├── api/                 # API routes
│   │   └── routes/          # Endpoint implementations
│   ├── core/                # Configuration
│   ├── db/                  # Database setup
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── repositories/        # Data access layer
│   └── services/            # Business logic
└── tests/                   # Unit tests
```

**Add a new endpoint**:
1. Create route in `api/routes/`
2. Add schema in `schemas/`
3. Add service logic in `services/`
4. Register route in `api/router.py`
5. Write tests in `tests/`

### Backend (Spring Boot)

```
services/spring-auth/
└── src/
    ├── main/
    │   ├── java/com/example/demo/
    │   │   ├── appuser/         # User management
    │   │   ├── controller/      # REST controllers
    │   │   ├── email/           # Email service
    │   │   ├── registration/    # Registration logic
    │   │   └── security/        # Security config
    │   └── resources/
    │       ├── application.yml  # Configuration
    │       └── certs/           # JWT keys
    └── test/                    # Unit tests
```

**Add a new endpoint**:
1. Create method in appropriate controller
2. Add service logic if needed
3. Update security config if endpoint needs protection
4. Write tests in `src/test/`

### Frontend

```
frontend/
├── *.html               # Pages
├── components/          # Reusable HTML components
├── css/
│   ├── base/            # Reset styles
│   ├── components/      # Component styles
│   ├── layout/          # Layout utilities
│   ├── modes/           # Themes (night mode)
│   └── pages/           # Page-specific styles
└── js/
    ├── auth.js          # Authentication logic
    ├── home.js          # Home page
    ├── navbar.js        # Navigation
    ├── startup_form.js  # Startup creation
    ├── startup_info.js  # Startup details
    └── utils.js         # Utilities
```

**Add a new page**:
1. Create HTML file in `frontend/`
2. Add styles in `css/pages/` if needed
3. Create JS file in `js/` for functionality
4. Update navbar links if needed
5. Test with `bash scripts/test_frontend.sh`

---

## 🐛 Debugging Tips

### Backend Debugging

**FastAPI**:
```python
# Add breakpoint
import pdb; pdb.set_trace()

# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Print SQL queries
# In .env: APP_DEBUG=true
```

**Spring Boot**:
```java
// Add logging
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

private static final Logger logger = LoggerFactory.getLogger(MyClass.class);
logger.info("Debug message: {}", variable);

// Enable debug in application.yml
logging:
  level:
    com.example.demo: DEBUG
```

### Frontend Debugging

```javascript
// Console logging
console.log('Debug:', variable);
console.error('Error:', error);
console.table(arrayData);

// Network inspection
// Open DevTools (F12) -> Network tab

// Breakpoint
debugger;  // Pauses execution
```

---

## 📚 Additional Resources

- [Main README](../README.md)
- [Testing Guide](TESTING_GUIDE.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Project Status](PROJECT_STATUS.md)
- [MailHog Guide](MAILHOG.md)

### External Documentation

- [FastAPI](https://fastapi.tiangolo.com/)
- [Spring Boot](https://spring.io/projects/spring-boot)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [MySQL](https://dev.mysql.com/doc/)

---

## 🙋 Questions?

If you have questions or need help:

1. Check existing documentation
2. Search existing GitHub issues
3. Ask in team chat
4. Create a new issue with `question` label

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

**Thank you for contributing to StartHub!** 🚀

_Last Updated: November 28, 2025_
