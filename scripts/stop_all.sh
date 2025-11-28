#!/bin/bash

# StartHub - Stop All Services Script
# Gracefully stops all running services

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "=================================================="
echo "  StartHub - Stopping All Services"
echo "=================================================="
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to stop a service by PID file
stop_service() {
    local SERVICE_NAME=$1
    local PID_FILE=$2
    
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo -e "${YELLOW}Stopping $SERVICE_NAME (PID: $PID)...${NC}"
            kill $PID 2>/dev/null || kill -9 $PID 2>/dev/null
            echo -e "${GREEN}✓ $SERVICE_NAME stopped${NC}"
        else
            echo -e "${YELLOW}$SERVICE_NAME not running (stale PID file)${NC}"
        fi
        rm -f "$PID_FILE"
    else
        echo -e "${YELLOW}No PID file found for $SERVICE_NAME${NC}"
    fi
}

# Stop services
stop_service "FastAPI" "logs/fastapi.pid"
stop_service "Spring Boot" "logs/spring.pid"
stop_service "Frontend" "logs/frontend.pid"
stop_service "MailHog" "logs/mailhog.pid"

# Additional cleanup: kill any processes on our ports
echo ""
echo -e "${YELLOW}Checking for remaining processes on ports 1025, 3000, 8000, 8025, 8081...${NC}"

# Kill processes on specific ports (Windows-compatible)
for PORT in 1025 3000 8000 8025 8081; do
    if command -v netstat &> /dev/null; then
        PID=$(netstat -ano | grep ":$PORT " | grep LISTENING | awk '{print $5}' | head -1)
        if [ ! -z "$PID" ]; then
            echo -e "${YELLOW}Killing process on port $PORT (PID: $PID)${NC}"
            taskkill //PID $PID //F 2>/dev/null || kill -9 $PID 2>/dev/null
        fi
    fi
done

echo ""
echo "=================================================="
echo -e "${GREEN}✓ All services stopped${NC}"
echo "=================================================="
