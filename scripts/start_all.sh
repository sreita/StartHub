#!/bin/bash

# StartHub - Full Stack Startup Script
# Starts all services: FastAPI backend, Spring Boot auth, and frontend server

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "=================================================="
echo "  StartHub - Starting All Services"
echo "=================================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Warning: Python virtual environment not found at .venv${NC}"
    echo -e "${YELLOW}Please create it with: python -m venv .venv${NC}"
    exit 1
fi

# Check if Java is installed
if ! command -v java &> /dev/null; then
    echo -e "${RED}Error: Java not found. Please install Java 18 or higher.${NC}"
    exit 1
fi

# Start MailHog if available
if [ -f "tools/mailhog/MailHog.exe" ] || [ -f "tools/mailhog/MailHog" ]; then
    if ! netstat -ano 2>/dev/null | grep ":1025.*LISTENING" >/dev/null 2>&1; then
        echo -e "${BLUE}[0/4] Starting MailHog (SMTP: 1025, Web: 8025)...${NC}"
        bash scripts/start_mailhog.sh 2>&1 | grep -E "started|running|Error" || true
        echo ""
    fi
else
    echo -e "${YELLOW}Note: MailHog not installed. Run 'bash scripts/setup_mailhog.sh' to enable email testing.${NC}"
    echo ""
fi

echo -e "${BLUE}[1/4] Starting FastAPI Backend (port 8000)...${NC}"
cd services/fastapi
source ../../.venv/Scripts/activate 2>/dev/null || source ../../.venv/bin/activate

# Check if requirements are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo -e "${YELLOW}Installing FastAPI dependencies...${NC}"
    pip install -r requirements.txt
fi

# Start FastAPI in background
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > ../../logs/fastapi.log 2>&1 &
FASTAPI_PID=$!
echo -e "${GREEN}✓ FastAPI started (PID: $FASTAPI_PID)${NC}"
echo "  Logs: logs/fastapi.log"
echo "  API Docs: http://localhost:8000/docs"
echo ""

cd "$PROJECT_ROOT"

echo -e "${BLUE}[2/4] Starting Spring Boot Authentication (port 8081)...${NC}"
cd services/spring-auth

# Ensure mvnw has execution permissions
if [ -f "mvnw" ]; then
    chmod +x mvnw
    echo -e "${GREEN}✓ Set execution permissions for mvnw${NC}"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file with default configuration...${NC}"
    cat > .env << EOF
DB_PASSWORD=
DB_USERNAME=root
DB_URL=jdbc:mysql://127.0.0.1:3306/starthub
SERVER_PORT=8081
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=hello
MAIL_PASSWORD=hello
EOF
    echo -e "${GREEN}✓ .env file created${NC}"
fi

# Load environment variables
set -a
source .env
set +a
echo -e "${GREEN}✓ Environment variables loaded from .env${NC}"

# Verify database connection
echo -e "${YELLOW}Testing database connection...${NC}"
if command -v mysql &> /dev/null; then
    if mysql -h 127.0.0.1 -u root -e "USE starthub;" 2>/dev/null; then
        echo -e "${GREEN}✓ Database connection successful${NC}"
    else
        echo -e "${RED}❌ Database connection failed${NC}"
        echo -e "${YELLOW}Attempting to create database...${NC}"
        mysql -h 127.0.0.1 -u root -e "CREATE DATABASE IF NOT EXISTS starthub;"
        if mysql -h 127.0.0.1 -u root -e "USE starthub;" 2>/dev/null; then
            echo -e "${GREEN}✓ Database created and connection successful${NC}"
        else
            echo -e "${RED}❌ Still cannot connect to database${NC}"
            exit 1
        fi
    fi
else
    echo -e "${YELLOW}⚠ mysql client not available, skipping database test${NC}"
fi

# Clean and compile
echo -e "${YELLOW}Compiling Spring Boot application...${NC}"
./mvnw clean compile -q
echo -e "${GREEN}✓ Compilation successful${NC}"

# Start Spring Boot
echo -e "${YELLOW}Starting Spring Boot server...${NC}"
./mvnw spring-boot:run >> ../../logs/spring-auth.log 2>&1 &
SPRING_PID=$!
echo $SPRING_PID > ../../logs/spring.pid
echo -e "${GREEN}✓ Spring Boot started (PID: $SPRING_PID)${NC}"
echo "  Logs: logs/spring-auth.log"
echo "  API: http://localhost:8081/api/v1"
echo "  Database: MySQL (starthub)"
echo ""

cd "$PROJECT_ROOT"

# Wait for Spring Boot with better feedback
echo -e "${YELLOW}Waiting for Spring Boot to initialize...${NC}"
SPRING_READY=false
for i in {1..60}; do
    if curl -s http://localhost:8081/api/v1/auth/login > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Spring Boot is ready! (after $i seconds)${NC}"
        SPRING_READY=true
        break
    fi

    # Show progress every 10 seconds
    if [ $((i % 10)) -eq 0 ]; then
        echo -e "${YELLOW}Still waiting... ($i/60 seconds)${NC}"
        # Show recent log entries if waiting too long
        if [ $i -gt 30 ]; then
            echo -e "${YELLOW}Recent log entries:${NC}"
            tail -3 logs/spring-auth.log | sed 's/^/  /'
        fi
    fi

    sleep 1
done

if [ "$SPRING_READY" = false ]; then
    echo -e "${RED}❌ Spring Boot failed to start within 60 seconds${NC}"
    echo -e "${YELLOW}Check logs/spring-auth.log for details:${NC}"
    tail -20 logs/spring-auth.log
    exit 1
fi

echo -e "${BLUE}[3/4] Starting Frontend Server (port 3000)...${NC}"
cd scripts
python dev-server.py > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
echo "  Logs: logs/frontend.log"
echo "  URL: http://localhost:3000"
echo ""

cd "$PROJECT_ROOT"

# Create logs directory if it doesn't exist
mkdir -p logs

# Save PIDs to file for cleanup
echo "$FASTAPI_PID" > logs/fastapi.pid
echo "$SPRING_PID" > logs/spring.pid
echo "$FRONTEND_PID" > logs/frontend.pid

echo "=================================================="
echo -e "${GREEN}✓ All services started successfully!${NC}"
echo "=================================================="
echo ""
echo "Services running:"
echo "  - MailHog SMTP: localhost:1025"
echo "  - MailHog UI:   http://localhost:8025"
echo "  - FastAPI:      http://localhost:8000/docs"
echo "  - Spring Auth:  http://localhost:8081/api/v1"
echo "  - Frontend:     http://localhost:3000"
echo ""
echo "To view logs:"
echo "  tail -f logs/fastapi.log"
echo "  tail -f logs/spring-auth.log"
echo "  tail -f logs/frontend.log"
echo ""
echo "To stop all services:"
echo "  bash scripts/stop_all.sh"
echo ""
echo -e "${GREEN}StartHub is ready! Open http://localhost:3000 in your browser.${NC}"
echo ""

# Monitor logs in real-time (optional)
# Uncomment the line below if you want to tail all logs together
# tail -f logs/fastapi.log logs/spring-auth.log logs/frontend.log