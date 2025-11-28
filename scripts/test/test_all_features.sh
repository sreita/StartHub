#!/bin/bash

# ============================================================================
# FILE: test_all_features.sh
# PURPOSE: Comprehensive integration tests for StartHub
# TESTS: Authentication flow, user registration, email confirmation, login
# AUTHOR: StartHub Team
# DATE: 2025-11-28
# ============================================================================

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# API endpoints
AUTH_API="http://localhost:8081/api/v1"
DATA_API="http://127.0.0.1:8000"
FRONTEND_URL="http://localhost:3000"

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

check_server() {
    local name=$1
    local url=$2
    echo -e "${YELLOW}Checking $name...${NC}"
    
    if curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null | grep -qE "200|405"; then
        echo -e "${GREEN}✓ $name is running${NC}"
        return 0
    else
        echo -e "${RED}✗ $name is NOT running${NC}"
        return 1
    fi
}

run_test() {
    local test_name=$1
    local command=$2
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    echo -e "\n${BLUE}[Test $TOTAL_TESTS] $test_name${NC}"
    
    if eval "$command" 2>/dev/null; then
        echo -e "${GREEN}✓ PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# ============================================================================
# HEADER
# ============================================================================

echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║      StartHub - Integration Test Suite                  ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# ============================================================================
# SERVER VERIFICATION
# ============================================================================

echo -e "${BLUE}═══ Server Availability Check ═══${NC}"
echo ""

SPRING_RUNNING=false
FASTAPI_RUNNING=false
FRONTEND_RUNNING=false

if check_server "Spring Boot (Port 8081)" "$AUTH_API/auth/login"; then
    SPRING_RUNNING=true
fi

if check_server "FastAPI (Port 8000)" "$DATA_API/health"; then
    FASTAPI_RUNNING=true
fi

if check_server "Frontend (Port 3000)" "$FRONTEND_URL/home.html"; then
    FRONTEND_RUNNING=true
fi

echo ""

# Check if required services are running
if [ "$SPRING_RUNNING" = false ]; then
    echo -e "${RED}Error: Spring Boot is not running${NC}"
    echo -e "${YELLOW}Start with: bash scripts/start_all.sh${NC}"
    exit 1
fi

if [ "$FASTAPI_RUNNING" = false ]; then
    echo -e "${YELLOW}Warning: FastAPI is not running (optional for auth tests)${NC}"
fi

if [ "$FRONTEND_RUNNING" = false ]; then
    echo -e "${YELLOW}Warning: Frontend is not running (optional for auth tests)${NC}"
fi

# ============================================================================
# AUTHENTICATION TESTS
# ============================================================================

echo -e "${BLUE}═══ Authentication Flow Tests ═══${NC}"

# Generate unique test user
TIMESTAMP=$(date +%s)
TEST_EMAIL="integration_test_${TIMESTAMP}@starthub.test"
TEST_PASSWORD="SecurePass123!"

echo -e "\n${YELLOW}Test User:${NC}"
echo -e "  Email: $TEST_EMAIL"
echo -e "  Password: $TEST_PASSWORD"

# Test 1: User Registration
echo -e "\n${YELLOW}Testing user registration...${NC}"
REG_RESPONSE=$(curl -s -X POST "$AUTH_API/registration" \
    -H "Content-Type: application/json" \
    -d '{
        "firstName": "Integration",
        "lastName": "Test",
        "email": "'$TEST_EMAIL'",
        "password": "'$TEST_PASSWORD'"
    }' 2>/dev/null)

run_test "User Registration" \
    "echo '$REG_RESPONSE' | grep -qE 'token|confirmation|success|email sent'"

# Extract confirmation token if available
CONFIRM_TOKEN=$(echo "$REG_RESPONSE" | grep -oP '(?<=token=)[^"&\s]+' | head -1)

if [ -z "$CONFIRM_TOKEN" ]; then
    # Try to extract from JSON response
    CONFIRM_TOKEN=$(echo "$REG_RESPONSE" | sed -n 's/.*"token"\s*:\s*"\([^"]*\)".*/\1/p')
fi

# Test 2: Email Confirmation
if [ -n "$CONFIRM_TOKEN" ]; then
    echo -e "\n${YELLOW}Testing email confirmation...${NC}"
    run_test "Email Confirmation" \
        "curl -s '$AUTH_API/registration/confirm?token=$CONFIRM_TOKEN' 2>/dev/null | grep -qiE 'confirmed|success|enabled'"
else
    echo -e "\n${YELLOW}Skipping email confirmation (no token received)${NC}"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# Wait a moment for database update
sleep 2

# Test 3: Successful Login
echo -e "\n${YELLOW}Testing successful login...${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "$AUTH_API/auth/login" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "'$TEST_EMAIL'",
        "password": "'$TEST_PASSWORD'"
    }' 2>/dev/null)

JWT_TOKEN=$(echo "$LOGIN_RESPONSE" | sed -n 's/.*"token"\s*:\s*"\([^"]*\)".*/\1/p')

run_test "Successful Login" \
    "test -n '$JWT_TOKEN'"

# Test 4: Failed Login (Wrong Password)
echo -e "\n${YELLOW}Testing failed login with wrong password...${NC}"
run_test "Failed Login (Wrong Password)" \
    "curl -s -o /dev/null -w '%{http_code}' -X POST '$AUTH_API/auth/login' \
        -H 'Content-Type: application/json' \
        -d '{\"email\":\"$TEST_EMAIL\",\"password\":\"WrongPassword!\"}' 2>/dev/null | \
        grep -qE '401|403'"

# Test 5: Failed Login (Non-existent User)
echo -e "\n${YELLOW}Testing failed login with non-existent user...${NC}"
run_test "Failed Login (Non-existent User)" \
    "curl -s -o /dev/null -w '%{http_code}' -X POST '$AUTH_API/auth/login' \
        -H 'Content-Type: application/json' \
        -d '{\"email\":\"nonexistent@test.com\",\"password\":\"Test123!\"}' 2>/dev/null | \
        grep -qE '401|403|404'"

# Test 6: Access Protected Endpoint with Valid Token
if [ -n "$JWT_TOKEN" ]; then
    echo -e "\n${YELLOW}Testing access to protected endpoint with valid token...${NC}"
    run_test "Protected Endpoint Access (Valid Token)" \
        "curl -s -H 'Authorization: Bearer $JWT_TOKEN' '$AUTH_API/users/me' \
            -o /dev/null -w '%{http_code}' 2>/dev/null | grep -qE '200|404'"
else
    echo -e "\n${YELLOW}Skipping protected endpoint test (no JWT token)${NC}"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# Test 7: Access Protected Endpoint without Token
echo -e "\n${YELLOW}Testing access to protected endpoint without token...${NC}"
run_test "Protected Endpoint Access (No Token)" \
    "curl -s -o /dev/null -w '%{http_code}' '$AUTH_API/users/me' 2>/dev/null | \
        grep -qE '401|403'"

# ============================================================================
# DATA API TESTS (if FastAPI is running)
# ============================================================================

if [ "$FASTAPI_RUNNING" = true ]; then
    echo -e "\n${BLUE}═══ Data API Tests ═══${NC}"
    
    # Test 8: Health Check
    echo -e "\n${YELLOW}Testing FastAPI health check...${NC}"
    run_test "FastAPI Health Check" \
        "curl -s '$DATA_API/health' 2>/dev/null | grep -q 'ok'"
    
    # Test 9: Database Connection
    echo -e "\n${YELLOW}Testing database connectivity...${NC}"
    run_test "Database Connection" \
        "curl -s '$DATA_API/health/db' 2>/dev/null | grep -q 'ok'"
    
    # Test 10: List Startups
    echo -e "\n${YELLOW}Testing list startups endpoint...${NC}"
    run_test "List Startups" \
        "curl -s -o /dev/null -w '%{http_code}' '$DATA_API/startups' 2>/dev/null | grep -q '200'"
fi

# ============================================================================
# FRONTEND TESTS (if frontend is running)
# ============================================================================

if [ "$FRONTEND_RUNNING" = true ]; then
    echo -e "\n${BLUE}═══ Frontend Tests ═══${NC}"
    
    # Test: Home Page
    echo -e "\n${YELLOW}Testing home page...${NC}"
    run_test "Frontend Home Page" \
        "curl -s -o /dev/null -w '%{http_code}' '$FRONTEND_URL/home.html' 2>/dev/null | grep -q '200'"
    
    # Test: Login Page
    echo -e "\n${YELLOW}Testing login page...${NC}"
    run_test "Frontend Login Page" \
        "curl -s -o /dev/null -w '%{http_code}' '$FRONTEND_URL/login.html' 2>/dev/null | grep -q '200'"
fi

# ============================================================================
# SUMMARY
# ============================================================================

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}                   TEST SUMMARY                     ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "Total Tests:    $TOTAL_TESTS"
echo -e "${GREEN}Passed Tests:   $PASSED_TESTS${NC}"
echo -e "${RED}Failed Tests:   $FAILED_TESTS${NC}"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    echo -e "${YELLOW}Check the output above for details${NC}"
    echo ""
    exit 1
fi

# ============================================================================
# END OF FILE
# ============================================================================