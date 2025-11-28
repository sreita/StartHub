#!/bin/bash

# ============================================================================
# FILE: stop_mailhog.sh
# PURPOSE: Stop MailHog email testing server
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

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="$PROJECT_ROOT/logs/mailhog.pid"

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  Stopping MailHog${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Check if PID file exists
if [ -f "$PID_FILE" ]; then
    MAILHOG_PID=$(cat "$PID_FILE")
    
    if ps -p $MAILHOG_PID > /dev/null 2>&1; then
        echo -e "${YELLOW}Stopping MailHog (PID: $MAILHOG_PID)...${NC}"
        kill $MAILHOG_PID 2>/dev/null || true
        sleep 1
        
        # Force kill if still running
        if ps -p $MAILHOG_PID > /dev/null 2>&1; then
            kill -9 $MAILHOG_PID 2>/dev/null || true
        fi
        
        echo -e "${GREEN}✓ MailHog stopped${NC}"
    else
        echo -e "${YELLOW}MailHog not running (stale PID file)${NC}"
    fi
    
    rm -f "$PID_FILE"
else
    echo -e "${YELLOW}No PID file found${NC}"
fi

# Check for processes on ports
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows - check ports 1025 and 8025
    for PORT in 1025 8025; do
        PID=$(netstat -ano | grep ":$PORT.*LISTENING" | awk '{print $5}' | head -1)
        if [ ! -z "$PID" ]; then
            echo -e "${YELLOW}Killing process on port $PORT (PID: $PID)...${NC}"
            taskkill //F //PID $PID 2>/dev/null || true
        fi
    done
else
    # Unix-like systems
    for PORT in 1025 8025; do
        PID=$(lsof -ti:$PORT 2>/dev/null || true)
        if [ ! -z "$PID" ]; then
            echo -e "${YELLOW}Killing process on port $PORT (PID: $PID)...${NC}"
            kill -9 $PID 2>/dev/null || true
        fi
    done
fi

echo ""
echo -e "${GREEN}✓ MailHog stopped${NC}"
echo ""

# ============================================================================
# END OF FILE
# ============================================================================
