# Integration Test Suite - test_all_features.sh

Comprehensive integration testing script for the StartHub platform. This script validates the complete authentication flow and verifies all critical services are operational.

---

## 📋 Overview

**Script**: `scripts/test/test_all_features.sh`  
**Purpose**: End-to-end integration testing  
**Dependencies**: All services must be running (Spring Boot, FastAPI optional, Frontend optional)

---

## 🎯 What It Tests

### Core Tests (Always Run)

#### 1. **Server Availability**
- ✅ Spring Boot Authentication API (Port 8081)
- ⚠️ FastAPI Data API (Port 8000) - Optional
- ⚠️ Frontend (Port 3000) - Optional

#### 2. **User Registration**
- Creates unique test user with timestamp-based email
- Validates registration response
- Extracts confirmation token

#### 3. **Email Confirmation**
- Uses confirmation token from registration
- Validates account activation
- Confirms user is enabled in database

#### 4. **Successful Login**
- Authenticates with registered credentials
- Extracts JWT token from response
- Validates token format

#### 5. **Failed Login - Wrong Password**
- Attempts login with incorrect password
- Expects HTTP 401/403 response
- Validates error handling

#### 6. **Failed Login - Non-existent User**
- Attempts login with fake email
- Expects HTTP 401/403/404 response
- Validates user validation logic

#### 7. **Protected Endpoint Access - With Token**
- Accesses protected endpoint with valid JWT
- Expects HTTP 200 or 404 (endpoint-dependent)
- Validates JWT authentication

#### 8. **Protected Endpoint Access - Without Token**
- Accesses protected endpoint without authentication
- Expects HTTP 401/403 response
- Validates authorization enforcement

### Optional Tests (If Services Running)

#### 9. **FastAPI Health Check** (if port 8000 active)
- Validates FastAPI service health
- Checks `/health` endpoint

#### 10. **Database Connectivity** (if FastAPI running)
- Tests database connection
- Checks `/health/db` endpoint

#### 11. **List Startups** (if FastAPI running)
- Validates data API functionality
- Tests `/startups` endpoint

#### 12. **Frontend Home Page** (if port 3000 active)
- Validates frontend is serving pages
- Tests `home.html` accessibility

#### 13. **Frontend Login Page** (if port 3000 active)
- Validates login page loads
- Tests `login.html` accessibility

---

## 🚀 Usage

### Prerequisites

Start all required services:

```bash
bash scripts/start_all.sh
```

Wait for services to initialize (recommended 10 seconds):

```bash
sleep 10
```

### Run Tests

```bash
bash scripts/test/test_all_features.sh
```

### Expected Output

```
╔══════════════════════════════════════════════════════════╗
║      StartHub - Integration Test Suite                  ║
╚══════════════════════════════════════════════════════════╝

═══ Server Availability Check ═══

Checking Spring Boot (Port 8081)...
✓ Spring Boot (Port 8081) is running
Checking FastAPI (Port 8000)...
✓ FastAPI (Port 8000) is running
Checking Frontend (Port 3000)...
✓ Frontend (Port 3000) is running

═══ Authentication Flow Tests ═══

Test User:
  Email: integration_test_1732779600@starthub.test
  Password: SecurePass123!

Testing user registration...

[Test 1] User Registration
✓ PASSED

Testing email confirmation...

[Test 2] Email Confirmation
✓ PASSED

Testing successful login...

[Test 3] Successful Login
✓ PASSED

Testing failed login with wrong password...

[Test 4] Failed Login (Wrong Password)
✓ PASSED

Testing failed login with non-existent user...

[Test 5] Failed Login (Non-existent User)
✓ PASSED

Testing access to protected endpoint with valid token...

[Test 6] Protected Endpoint Access (Valid Token)
✓ PASSED

Testing access to protected endpoint without token...

[Test 7] Protected Endpoint Access (No Token)
✓ PASSED

═══ Data API Tests ═══

Testing FastAPI health check...

[Test 8] FastAPI Health Check
✓ PASSED

Testing database connectivity...

[Test 9] Database Connection
✓ PASSED

Testing list startups endpoint...

[Test 10] List Startups
✓ PASSED

═══ Frontend Tests ═══

Testing home page...

[Test 11] Frontend Home Page
✓ PASSED

Testing login page...

[Test 12] Frontend Login Page
✓ PASSED

═══════════════════════════════════════════════════
                   TEST SUMMARY
═══════════════════════════════════════════════════

Total Tests:    12
Passed Tests:   12
Failed Tests:   0

✓ All tests passed!
```

---

## 🔍 Test Details

### Test User Generation

Each test run creates a unique user:
- **Email Format**: `integration_test_<timestamp>@starthub.test`
- **Password**: `SecurePass123!` (meets security requirements)
- **Name**: Integration Test

This prevents conflicts from previous test runs.

### Token Extraction

The script extracts tokens using multiple strategies:

1. **Confirmation Token**: From registration response (JSON or URL parameter)
2. **JWT Token**: From login response (JSON `"token"` field)

### Error Handling

- Tests continue even if optional services are unavailable
- Failed tests are counted but don't stop execution
- Final exit code indicates overall success/failure

---

## 📊 Exit Codes

- **0**: All tests passed
- **1**: One or more tests failed or required service unavailable

---

## 🐛 Troubleshooting

### Test Fails: "Spring Boot is not running"

**Cause**: Authentication service not available on port 8081.

**Solution**:
```bash
bash scripts/start_all.sh
sleep 10
bash scripts/test_all_features.sh
```

### Test Fails: "User Registration"

**Possible Causes**:
1. MailHog not running (email can't be sent)
2. Database connection issue
3. Validation error in request

**Solutions**:
```bash
# Start MailHog
bash scripts/start_mailhog.sh

# Check database
mysql -u root -p starthub -e "SELECT COUNT(*) FROM User;"

# Check Spring Boot logs
tail -f logs/spring.log
```

### Test Fails: "Email Confirmation"

**Cause**: Confirmation token not found in response.

**Solution**: Check MailHog UI for confirmation email:
```bash
# Open browser to
http://localhost:8025
```

### Test Fails: "Successful Login"

**Possible Causes**:
1. User not confirmed yet
2. Database connection issue
3. Incorrect credentials

**Solutions**:
```bash
# Check if user is enabled
mysql -u root -p starthub -e "SELECT email, enabled FROM User WHERE email LIKE 'integration_test%' ORDER BY created_at DESC LIMIT 1;"

# Manually enable user
mysql -u root -p starthub -e "UPDATE User SET enabled = 1 WHERE email = 'integration_test_xxx@starthub.test';"
```

### Test Fails: "Protected Endpoint Access"

**Cause**: JWT token invalid or endpoint doesn't exist.

**Solution**: Verify token and endpoint:
```bash
# Test manually with token
TOKEN="your_jwt_token_here"
curl -H "Authorization: Bearer $TOKEN" http://localhost:8081/api/v1/users/me
```

### Optional Tests Skipped

**Symptom**: FastAPI or Frontend tests show "Warning" and are skipped.

**Explanation**: These tests only run if the respective services are running. This is normal if you're only testing authentication.

**To include them**: Start all services:
```bash
bash scripts/start_all.sh
```

---

## 🔧 Customization

### Test Different Endpoints

Edit the script to test custom endpoints:

```bash
# Add after line with protected endpoint tests
echo -e "\n${YELLOW}Testing custom endpoint...${NC}"
run_test "Custom Endpoint" \
    "curl -s -H 'Authorization: Bearer $JWT_TOKEN' '$AUTH_API/custom/endpoint' \
        -o /dev/null -w '%{http_code}' 2>/dev/null | grep -q '200'"
```

### Change Test User Credentials

Modify these variables in the script:

```bash
TEST_PASSWORD="YourCustomPassword123!"
```

### Disable Specific Tests

Comment out unwanted tests:

```bash
# run_test "Optional Test" \
#     "some command"
```

---

## 📈 CI/CD Integration

This script is suitable for CI/CD pipelines:

### GitHub Actions Example

```yaml
- name: Run Integration Tests
  run: |
    bash scripts/start_all.sh
    sleep 15
    bash scripts/test_all_features.sh
```

### Exit Code Handling

```bash
# Run tests and capture exit code
bash scripts/test_all_features.sh
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✓ Integration tests passed"
else
    echo "✗ Integration tests failed"
    exit 1
fi
```

---

## 📝 Related Documentation

- [Testing Guide](TESTING_GUIDE.md) - Quick testing reference and Python test suites
- [Complete Manual Testing](COMPLETE_MANUAL_TESTING.md) - Detailed manual scenarios
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues
- [Backend Test Script](../scripts/test/test_backend.sh) - Backend-specific tests
- [Frontend Test Script](../scripts/test/test_frontend.sh) - Frontend-specific tests
- [Python Test Suites](../scripts/test/) - Comprehensive CRUD test automation

---

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2025-11-28 | Complete rewrite with English translations, enhanced error handling, optional service tests |
| 1.0 | 2025-11-01 | Initial version (Spanish) |

---

**Last Updated**: November 28, 2025  
**Maintainer**: StartHub Team  
**Script Location**: `scripts/test/test_all_features.sh`
