#!/bin/bash

# ============================================================================
# FILE: truncate_all.sh
# PURPOSE: Clean all StarHub tables while keeping schema intact
# AUTHOR: yoshikagua
# DATE: 2025-11-28
# ============================================================================

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# MySQL connection settings
MYSQL_USER="${DB_USERNAME:-root}"
MYSQL_PASSWORD="${DB_PASSWORD}"
MYSQL_CMD="mysqlsh"

# Check if MySQL Shell is available
if ! command -v mysqlsh &> /dev/null; then
    if [ -f "/c/Program Files/MySQL/MySQL Shell 8.0/bin/mysqlsh.exe" ]; then
        MYSQL_CMD="/c/Program Files/MySQL/MySQL Shell 8.0/bin/mysqlsh"
    else
        echo -e "${RED}Error: MySQL Shell not found${NC}"
        exit 1
    fi
fi

# Get password if not set
if [ -z "$MYSQL_PASSWORD" ]; then
    echo -e "${YELLOW}Enter MySQL password for user '$MYSQL_USER':${NC}"
    read -s MYSQL_PASSWORD
fi

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  StarHub Database Truncate Script${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""
echo -e "${RED}WARNING: This will delete ALL data from the database!${NC}"
echo -e "${YELLOW}Press Ctrl+C to cancel or Enter to continue...${NC}"
read

echo -e "${YELLOW}Truncating all tables...${NC}"

"$MYSQL_CMD" --sql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -D starthub << 'EOF' 2>&1 | grep -v "WARNING"
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE Vote;
TRUNCATE TABLE Comment;
TRUNCATE TABLE UserStartupPartnership;
TRUNCATE TABLE Startup;
TRUNCATE TABLE `User`;
TRUNCATE TABLE Category;
TRUNCATE TABLE ConfirmationToken;

ALTER TABLE Vote AUTO_INCREMENT = 1;
ALTER TABLE Comment AUTO_INCREMENT = 1;
ALTER TABLE Startup AUTO_INCREMENT = 1;
ALTER TABLE `User` AUTO_INCREMENT = 1;
ALTER TABLE Category AUTO_INCREMENT = 1;

SET FOREIGN_KEY_CHECKS = 1;

SELECT 'Tables truncated successfully!' AS status;
EOF

echo ""
echo -e "${GREEN}✓ All tables truncated successfully!${NC}"
echo ""

# ============================================================================
# END OF FILE
# ============================================================================
