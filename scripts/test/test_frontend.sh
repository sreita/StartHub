#!/bin/bash

# ============================================================================
# FILE: test_frontend.sh
# PURPOSE: Test all frontend endpoints and resources
# AUTHOR: Copilot
# DATE: 2025-11-28
# ============================================================================

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

FRONTEND_URL="http://localhost:3000"
PASS_COUNT=0
FAIL_COUNT=0

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  StartHub Frontend Test Suite${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Check if frontend is running
if ! curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL/login.html" | grep -q "200"; then
    echo -e "${RED}Error: Frontend server not running on port 3000${NC}"
    echo -e "${YELLOW}Please start it with: bash scripts/start_all.sh${NC}"
    exit 1
fi

# Function to test endpoint
test_endpoint() {
    local name=$1
    local url=$2
    local expected_code=${3:-200}
    
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
    
    if [ "$HTTP_CODE" = "$expected_code" ]; then
        echo -e "${GREEN}✓${NC} $name (HTTP $HTTP_CODE)"
        ((PASS_COUNT++))
        return 0
    else
        echo -e "${RED}✗${NC} $name (Expected $expected_code, got $HTTP_CODE)"
        ((FAIL_COUNT++))
        return 1
    fi
}

# Function to check content
test_content() {
    local name=$1
    local url=$2
    local search_term=$3
    
    CONTENT=$(curl -s "$url" 2>/dev/null)
    
    if echo "$CONTENT" | grep -q "$search_term"; then
        echo -e "${GREEN}✓${NC} $name contains '$search_term'"
        ((PASS_COUNT++))
        return 0
    else
        echo -e "${RED}✗${NC} $name missing '$search_term'"
        ((FAIL_COUNT++))
        return 1
    fi
}

# Test HTML Pages
echo -e "${YELLOW}Testing HTML Pages...${NC}"
test_endpoint "Login Page" "$FRONTEND_URL/login.html"
test_endpoint "Signup Page" "$FRONTEND_URL/signup.html"
test_endpoint "Home Page" "$FRONTEND_URL/home.html"
test_endpoint "Startup Form" "$FRONTEND_URL/startup_form.html"
test_endpoint "Startup Info" "$FRONTEND_URL/startup_info.html"
test_endpoint "Profile Page" "$FRONTEND_URL/profile.html"
test_endpoint "Forgot Password" "$FRONTEND_URL/forgot_password.html"
test_endpoint "Reset Password" "$FRONTEND_URL/reset_password.html"
echo ""

# Test Components
echo -e "${YELLOW}Testing Components...${NC}"
test_endpoint "Navbar Component" "$FRONTEND_URL/components/navbar.html"
echo ""

# Test CSS Files
echo -e "${YELLOW}Testing CSS Files...${NC}"
test_endpoint "Main Styles" "$FRONTEND_URL/css/styles.css"
test_endpoint "Reset CSS" "$FRONTEND_URL/css/base/reset.css"
test_endpoint "Buttons CSS" "$FRONTEND_URL/css/components/buttons.css"
test_endpoint "Cards CSS" "$FRONTEND_URL/css/components/cards.css"
test_endpoint "Forms CSS" "$FRONTEND_URL/css/components/forms.css"
test_endpoint "Navigation CSS" "$FRONTEND_URL/css/components/navigation.css"
test_endpoint "Auth CSS" "$FRONTEND_URL/css/pages/auth.css"
test_endpoint "Night Mode CSS" "$FRONTEND_URL/css/modes/night-mode.css"
echo ""

# Test JavaScript Files
echo -e "${YELLOW}Testing JavaScript Files...${NC}"
test_endpoint "Auth JS" "$FRONTEND_URL/js/auth.js"
test_endpoint "Home JS" "$FRONTEND_URL/js/home.js"
test_endpoint "Utils JS" "$FRONTEND_URL/js/utils.js"
test_endpoint "Navbar JS" "$FRONTEND_URL/js/navbar.js"
test_endpoint "Startup Form JS" "$FRONTEND_URL/js/startup_form.js"
test_endpoint "Startup Info JS" "$FRONTEND_URL/js/startup_info.js"
echo ""

# Test Content
echo -e "${YELLOW}Testing Page Content...${NC}"
test_content "Login Page Title" "$FRONTEND_URL/login.html" "<title>Login - StartHub</title>"
test_content "Home Page Title" "$FRONTEND_URL/home.html" "<title>StartHub - Inicio</title>"
test_content "Auth API Configuration" "$FRONTEND_URL/js/auth.js" "http://localhost:8081/api/v1"
test_content "Data API Configuration" "$FRONTEND_URL/js/home.js" "http://localhost:8000"
echo ""

# Test API Endpoints Referenced in Frontend
echo -e "${YELLOW}Testing Backend API Connectivity...${NC}"
AUTH_API="http://localhost:8081"
DATA_API="http://localhost:8000"

# Test Spring Boot
AUTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$AUTH_API/api/v1/auth/login" 2>/dev/null)
if [ "$AUTH_STATUS" = "405" ] || [ "$AUTH_STATUS" = "401" ] || [ "$AUTH_STATUS" = "403" ]; then
    echo -e "${GREEN}✓${NC} Spring Boot API accessible at $AUTH_API (HTTP $AUTH_STATUS)"
    ((PASS_COUNT++))
else
    echo -e "${YELLOW}⚠${NC} Spring Boot API may not be running at $AUTH_API (HTTP $AUTH_STATUS)"
fi

# Test FastAPI
DATA_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$DATA_API/startups/" 2>/dev/null)
if [ "$DATA_STATUS" = "200" ]; then
    echo -e "${GREEN}✓${NC} FastAPI accessible at $DATA_API (HTTP $DATA_STATUS)"
    ((PASS_COUNT++))
else
    echo -e "${YELLOW}⚠${NC} FastAPI may not be running at $DATA_API (HTTP $DATA_STATUS)"
fi

echo ""
echo -e "${BLUE}============================================${NC}"
echo -e "${GREEN}Tests Passed: $PASS_COUNT${NC}"
if [ $FAIL_COUNT -gt 0 ]; then
    echo -e "${RED}Tests Failed: $FAIL_COUNT${NC}"
else
    echo -e "${GREEN}Tests Failed: 0${NC}"
fi
echo -e "${BLUE}============================================${NC}"
echo ""

if [ $FAIL_COUNT -gt 0 ]; then
    exit 1
fi

exit 0

# ============================================================================
# END OF FILE
# ============================================================================
