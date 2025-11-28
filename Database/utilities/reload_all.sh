#!/bin/bash

# ============================================================================
# FILE: reload_all.sh
# PURPOSE: Rebuilds the entire StarHub database from scratch using MySQL Shell
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
    # Try with full path (Windows)
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
echo -e "${BLUE}  StarHub Database Reload Script${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Step 1: Drop and recreate database
echo -e "${YELLOW}[1/7] Dropping and recreating database...${NC}"
"$MYSQL_CMD" --sql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "DROP DATABASE IF EXISTS starthub; CREATE DATABASE starthub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>&1 | grep -v "WARNING"
echo -e "${GREEN}✓ Database recreated${NC}"

# Step 2: Load schema
echo -e "${YELLOW}[2/7] Loading schema...${NC}"
"$MYSQL_CMD" --sql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -D starthub < ../schema/schema.sql 2>&1 | grep -v "WARNING" | tail -5
echo -e "${GREEN}✓ Schema loaded${NC}"

# Step 3: Load views
echo -e "${YELLOW}[3/7] Loading views...${NC}"
"$MYSQL_CMD" --sql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -D starthub < ../schema/views.sql 2>&1 | grep -v "WARNING"
echo -e "${GREEN}✓ Views loaded${NC}"

# Step 4: Load seed data
echo -e "${YELLOW}[4/7] Loading seed data...${NC}"

echo "  - Categories..."
"$MYSQL_CMD" --sql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -D starthub < ../seeds/seed_categories.sql 2>&1 | grep -v "WARNING" | grep "Records:"

echo "  - Users..."
"$MYSQL_CMD" --sql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -D starthub < ../seeds/seed_users.sql 2>&1 | grep -v "WARNING" | grep "Records:"

echo "  - Startups..."
"$MYSQL_CMD" --sql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -D starthub < ../seeds/seed_startups.sql 2>&1 | grep -v "WARNING" | grep "Records:"

echo "  - Partnerships..."
"$MYSQL_CMD" --sql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -D starthub < ../seeds/seed_partnerships.sql 2>&1 | grep -v "WARNING" | grep "Records:"

echo "  - Comments..."
"$MYSQL_CMD" --sql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -D starthub < ../seeds/seed_comments.sql 2>&1 | grep -v "WARNING" | grep "Records:"

echo "  - Votes..."
"$MYSQL_CMD" --sql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -D starthub < ../seeds/seed_votes.sql 2>&1 | grep -v "WARNING" | grep "Records:"

echo -e "${GREEN}✓ Seed data loaded${NC}"

# Step 5: Verify tables
echo -e "${YELLOW}[5/7] Verifying tables...${NC}"
"$MYSQL_CMD" --sql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -D starthub -e "SHOW TABLES;" 2>&1 | grep -v "WARNING"
echo -e "${GREEN}✓ Tables verified${NC}"

# Step 6: Verify data counts
echo -e "${YELLOW}[6/7] Verifying data counts...${NC}"
"$MYSQL_CMD" --sql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -D starthub -e "
SELECT COUNT(*) AS total_categories FROM Category;
SELECT COUNT(*) AS total_users FROM \`User\`;
SELECT COUNT(*) AS total_startups FROM Startup;
SELECT COUNT(*) AS total_comments FROM Comment;
SELECT COUNT(*) AS total_votes FROM Vote;
SELECT COUNT(*) AS total_partnerships FROM UserStartupPartnership;
" 2>&1 | grep -v "WARNING"

echo -e "${GREEN}✓ Data counts verified${NC}"

# Step 7: Summary
echo ""
echo -e "${BLUE}============================================${NC}"
echo -e "${GREEN}✓ Database reload completed successfully!${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""
echo "Database: starthub"
echo "Character Set: utf8mb4"
echo "Collation: utf8mb4_unicode_ci"
echo ""

# ============================================================================
# END OF FILE
# ============================================================================
