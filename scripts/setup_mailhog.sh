#!/bin/bash

# ============================================================================
# FILE: setup_mailhog.sh
# PURPOSE: Download and setup MailHog for email testing
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

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  MailHog Setup for StartHub${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Create tools directory
mkdir -p "$MAILHOG_DIR"

# Detect OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    MAILHOG_URL="https://github.com/mailhog/MailHog/releases/download/v1.0.1/MailHog_windows_amd64.exe"
    MAILHOG_FILE="MailHog.exe"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    MAILHOG_URL="https://github.com/mailhog/MailHog/releases/download/v1.0.1/MailHog_darwin_amd64"
    MAILHOG_FILE="MailHog"
else
    MAILHOG_URL="https://github.com/mailhog/MailHog/releases/download/v1.0.1/MailHog_linux_amd64"
    MAILHOG_FILE="MailHog"
fi

# Check if already downloaded
if [ -f "$MAILHOG_DIR/$MAILHOG_FILE" ]; then
    echo -e "${GREEN}✓ MailHog already downloaded${NC}"
else
    echo -e "${YELLOW}Downloading MailHog...${NC}"
    curl -L "$MAILHOG_URL" -o "$MAILHOG_DIR/$MAILHOG_FILE"
    chmod +x "$MAILHOG_DIR/$MAILHOG_FILE"
    echo -e "${GREEN}✓ MailHog downloaded${NC}"
fi

echo ""
echo -e "${BLUE}============================================${NC}"
echo -e "${GREEN}✓ MailHog setup complete!${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""
echo "Installation directory: $MAILHOG_DIR"
echo ""
echo "To start MailHog:"
echo -e "  ${YELLOW}bash scripts/start_mailhog.sh${NC}"
echo ""
echo "Or manually:"
echo -e "  ${YELLOW}$MAILHOG_DIR/$MAILHOG_FILE${NC}"
echo ""
echo "MailHog will run on:"
echo "  - SMTP Server: localhost:1025"
echo "  - Web UI: http://localhost:8025"
echo ""

# ============================================================================
# END OF FILE
# ============================================================================
