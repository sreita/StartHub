#!/bin/bash

# ============================================================================
# FILE: start_mailhog.sh
# PURPOSE: Start MailHog email testing server
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
MAILHOG_DIR="$PROJECT_ROOT/tools/mailhog"

# Detect executable name
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    MAILHOG_FILE="MailHog.exe"
else
    MAILHOG_FILE="MailHog"
fi

MAILHOG_PATH="$MAILHOG_DIR/$MAILHOG_FILE"

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  Starting MailHog${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Check if MailHog is installed
if [ ! -f "$MAILHOG_PATH" ]; then
    echo -e "${RED}Error: MailHog not found${NC}"
    echo -e "${YELLOW}Please run: bash scripts/setup_mailhog.sh${NC}"
    exit 1
fi

# Check if already running
if lsof -Pi :1025 -sTCP:LISTEN -t >/dev/null 2>&1 || netstat -ano | grep ":1025.*LISTENING" >/dev/null 2>&1; then
    echo -e "${YELLOW}MailHog is already running on port 1025${NC}"
    echo -e "${GREEN}Web UI: http://localhost:8025${NC}"
    exit 0
fi

# Start MailHog in background
echo -e "${YELLOW}Starting MailHog...${NC}"
"$MAILHOG_PATH" > "$PROJECT_ROOT/logs/mailhog.log" 2>&1 &
MAILHOG_PID=$!

# Save PID
mkdir -p "$PROJECT_ROOT/logs"
echo "$MAILHOG_PID" > "$PROJECT_ROOT/logs/mailhog.pid"

# Wait a moment for startup
sleep 2

# Verify it started
if ps -p $MAILHOG_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓ MailHog started successfully (PID: $MAILHOG_PID)${NC}"
    echo ""
    echo -e "${BLUE}============================================${NC}"
    echo -e "${GREEN}  MailHog is now running!${NC}"
    echo -e "${BLUE}============================================${NC}"
    echo ""
    echo "Services:"
    echo "  - SMTP Server: localhost:1025"
    echo "  - Web UI: http://localhost:8025"
    echo ""
    echo "Logs: logs/mailhog.log"
    echo ""
    echo "To stop MailHog:"
    echo "  bash scripts/stop_mailhog.sh"
    echo ""
else
    echo -e "${RED}Failed to start MailHog${NC}"
    exit 1
fi

# ============================================================================
# END OF FILE
# ============================================================================
