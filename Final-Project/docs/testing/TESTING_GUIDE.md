# 🧪 Testing Guide - StartHub

Complete testing guide with automated test suites and manual testing procedures.

## Quick Start Commands

- Start all services: `bash scripts/docker/start.sh start`
- Stop all services: `bash scripts/docker/start.sh stop`
- Smoke test (health checks): `python scripts/test/test_manual.py`

---

## 📁 Test Structure

```
scripts/test/
├── integration/          # Integration tests between services
│   ├── test_complete_system.sh      # Complete system test
│   ├── test_authentication.sh       # Authentication tests
│   ├── test_startups.sh            # Startup management tests
│   └── test_interactions.sh        # Votes and comments tests
│
├── e2e/                 # End-to-end tests
│   └── test_docker_integration.sh  # Tests in Docker
│
├── unit/                # Unit tests
│   ├── test_crud_complete.py
│   ├── test_users_startups.py
│   ├── test_votes_comments.py
│   ├── test_search.py
│   └── test_manual.py
│
├── run_all_tests.sh     # Master script that runs all tests
└── reorganize_tests.sh  # Organizes tests into folders
```

---

## 🚀 Running Tests

### Prerequisites
1. Docker must be running
2. All containers must be active:
```bash
bash scripts/docker/start.sh start
sleep 10  # Wait for services to initialize
```

### Run All Tests (Recommended)
```bash
bash scripts/test/run_all_tests.sh
```

### Run Specific Test Suites

#### Integration Tests (Shell)
```bash
bash scripts/test/integration/test_complete_system.sh
bash scripts/test/integration/test_authentication.sh
bash scripts/test/integration/test_startups.sh
bash scripts/test/integration/test_interactions.sh
```

#### End-to-End Tests (Shell)
```bash
bash scripts/test/e2e/test_docker_integration.sh
```

#### Unit Tests (Python)
```bash
# Full CRUD test suite (recommended)
python scripts/test/unit/test_crud_complete.py

# Specific feature tests
python scripts/test/unit/test_users_startups.py
python scripts/test/unit/test_votes_comments.py
python scripts/test/unit/test_search.py

# Quick smoke test
python scripts/test/unit/test_manual.py
```

---

## 📋 Integration Test Suites

### 1. `test_complete_system.sh` - Complete System Test
**Full suite testing all system functionalities in an integrated flow**

**Tests Included**:
- ✅ User registration
- ✅ Email confirmation
- ✅ Login with JWT
- ✅ Get profile
- ✅ Update profile
- ✅ Password recovery
- ✅ Password reset
- ✅ Startup management
- ✅ Votes
- ✅ Comments

```bash
bash scripts/test/integration/test_complete_system.sh
```

### 2. `test_authentication.sh` - Authentication Tests
**Tests all authentication endpoints and user management**

**Endpoints Tested**:
- `POST /api/v1/registration` - Register user
- `GET /api/v1/registration/confirm?token=...` - Confirm email
- `POST /api/v1/auth/login` - Login and get JWT
- `GET /api/v1/users/me` - Get authenticated profile
- `PUT /api/v1/users/me` - Update profile
- `POST /api/v1/auth/recover-password` - Request recovery
- `POST /api/v1/auth/reset-password` - Reset password

```bash
bash scripts/test/integration/test_authentication.sh
```

### 3. `test_startups.sh` - Startup Management Tests
**Tests all startup-related endpoints**

**Endpoints Tested**:
- `GET /api/v1/categories/` - Get categories
- `POST /api/v1/startups/` - Create startup
- `GET /api/v1/startups/{id}` - Get startup by ID
- `GET /api/v1/startups/?skip=0&limit=50` - List with pagination
- `GET /api/v1/startups/?search=...` - Search startups

```bash
bash scripts/test/integration/test_startups.sh
```

### 4. `test_interactions.sh` - Votes and Comments Tests
**Tests interactions with startups**

**Endpoints Tested**:
- `POST /api/v1/votes/?user_id=...` - Create vote (upvote/downvote)
- `GET /api/v1/votes/count/{startup_id}` - Get vote count
- `GET /api/v1/votes/user/{user_id}` - Get user votes
- `POST /api/v1/comments/?user_id=...` - Create comment
- `GET /api/v1/comments/?startup_id=...` - Get comments
- `PUT /api/v1/comments/{id}` - Update comment
- `DELETE /api/v1/comments/{id}` - Delete comment

```bash
bash scripts/test/integration/test_interactions.sh
```

---

## 🧪 Unit Test Suites (Python)

### 1. `test_crud_complete.py` - Complete CRUD Operations

**User Operations**:
1. Registration with unique email
2. Email confirmation via token
3. Login and JWT retrieval
4. Profile retrieval
5. Profile update
6. Re-login after update
7. User deletion
8. Post-deletion verification (profile inaccessible, login fails)

**Startup Operations**:
1. Create startup
2. Read startup details
3. Update startup (name, description, category)
4. List all startups
5. List user's startups
6. Get startup with statistics (votes, comments)
7. Delete startup
8. Verify deletion

**Vote Operations**:
1. Create upvote
2. Read vote counts
3. Change vote to downvote
4. Delete vote
5. Verify vote removal

**Comment Operations**:
1. Create comment
2. List comments for startup
3. Update comment content
4. Delete comment
5. Verify comment removal

```bash
python scripts/test/unit/test_crud_complete.py
```

### 2. `test_users_startups.py` - Users and Startups Focus

- User registration and confirmation
- Login and re-login
- Profile operations
- Startup CRUD operations
- Startup listing and statistics

```bash
python scripts/test/unit/test_users_startups.py
```

### 3. `test_votes_comments.py` - Votes and Comments Focus

- Complete vote operations
- Vote count verification
- Comment CRUD operations
- Content validation

```bash
python scripts/test/unit/test_votes_comments.py
```

### 4. `test_search.py` - Search Functionality

**Search Features**:
- Search by keyword
- Filter by single category
- Filter by multiple categories
- Filter by minimum votes
- Filter by minimum comments
- Sort by relevance, votes, comments, or recency
- Pagination (page and limit parameters)
- Autocomplete suggestions
- Detailed startup view

```bash
python scripts/test/unit/test_search.py
```

### 5. `test_manual.py` - Quick Smoke Test

- FastAPI health check
- Rapid service validation

```bash
python scripts/test/unit/test_manual.py
```

---

## 📊 Test Results Summary

**Date**: December 8, 2025

### Tests Executed

1. **test_docker_e2e.sh** - ✅ 22/22 PASSED
   - Strict validations of correct behavior
   - Verifies response content, not just HTTP codes
   
2. **test_crud_complete.py** - ✅ ALL PASSED
   - Complete user, startup, vote, and comment CRUD
   - Database data validation
   
3. **test_all_features.sh** - ⚠️ FAILS due to Spring Boot bug

### ⚠️ BUG DETECTED: Spring Boot Authentication

**Problem**: Spring Boot returns **HTTP 500** (Internal Server Error) when it should return **401** (Unauthorized) or **403** (Forbidden) for incorrect credentials.

**Evidence**:
```bash
# Login with wrong password
curl -X POST http://localhost:8081/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"valid@email.com","password":"WrongPassword"}'

# Current response: HTTP 500 ❌
# Expected response: HTTP 401 ✅
```

**Affected Cases**:
- Login with wrong password → 500 (should be 401)
- Login with non-existent user → 500 (should be 401/404)

**Impact**:
- Strict tests fail (expected test behavior)
- API doesn't follow HTTP standards
- Frontend clients show generic error messages

**Recommendation**: Fix exception handler in Spring Boot to:
1. Catch `BadCredentialsException` → return 401
2. Catch `UsernameNotFoundException` → return 401
3. Don't expose stack traces in error responses

### ✅ Successful Validations

**FastAPI** (Port 8000):
- ✅ Complete startup CRUD
- ✅ Complete vote CRUD
- ✅ Complete comment CRUD
- ✅ Health checks and database connection
- ✅ Correct data validation in responses

**Database** (MySQL):
- ✅ Schema correctly loaded
- ✅ Seeds inserted
- ✅ Relations working (FK, cascades)
- ✅ Vote count accuracy

**Frontend** (Port 3000):
- ✅ Pages accessible (home, login)
- ✅ Files served correctly

**MailHog** (Port 8025):
- ✅ Email capture from confirmations
- ✅ Tokens generated correctly

---

## 📈 Test Summary Table

| Component    | Status | Notes                                      |
|--------------|--------|---------------------------------------------|
| FastAPI      | ✅ OK  | All validations passed                     |
| Spring Boot  | ⚠️ BUG | Returns 500 on failed auth (fix needed)    |
| MySQL        | ✅ OK  | Correct data, relations working            |
| Frontend     | ✅ OK  | Served correctly                           |
| MailHog      | ✅ OK  | Emails captured                            |
| Docker Stack | ✅ OK  | All services running                       |

**Total**: 22/22 behavior validations passed in test_docker_e2e.sh

**Required Action**: Fix authentication exception handling in Spring Boot.

---

## 🐛 Troubleshooting Tests

### Test fails due to connectivity
```bash
# Verify that containers are running
docker compose -f docker/compose.yaml ps

# Restart services
docker compose -f docker/compose.yaml down
docker compose -f docker/compose.yaml up -d
```

### Test fails on authentication
- Verify database is accessible
- Verify Spring Boot is running on port 8081
- Check Spring Boot logs: `docker compose logs spring-auth`

### Test fails on FastAPI
- Verify FastAPI is running on port 8000
- Check FastAPI logs: `docker compose logs fastapi`

---

## 📝 Adding New Tests

To add a new test:

1. Create file `test_module_name.sh` in appropriate directory
2. Include documentation header
3. Use `test_result()` functions to report results
4. Return appropriate exit code (0 = success, 1 = failure)
5. Add line to `run_all_tests.sh` to execute it

**Example**:
```bash
#!/bin/bash
# Test for Module X

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

TESTS_PASSED=0
TESTS_FAILED=0

test_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗${NC} $2"
        ((TESTS_FAILED++))
    fi
}

# Your tests here...

exit [ $TESTS_FAILED -eq 0 ] ? 0 : 1
```

---

## ℹ️ Test Information

- **Database**: MySQL on port 3307 (internal: 3306)
- **Spring Boot**: Port 8081
- **FastAPI**: Port 8000
- **Frontend**: Port 3000 (Nginx)
- **MailHog**: Port 8025 (SMTP), 1025 (Email testing)

---

**Last Updated**: December 8, 2025

**System Status**: ⚠️ 95% Operational (Spring Boot auth fix needed)