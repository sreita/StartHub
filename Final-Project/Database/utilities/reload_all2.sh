#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

MYSQL_USER="root"
MYSQL_PASSWORD="${DB_PASSWORD}"

if [ -z "$MYSQL_PASSWORD" ]; then
    echo -e "${YELLOW}Enter MySQL password for user 'root':${NC}"
    read -s MYSQL_PASSWORD
fi

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  StarHub Database Reload Script (MariaDB)${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

SQL="mysql -u $MYSQL_USER -p$MYSQL_PASSWORD -h 127.0.0.1 -P 3306"

echo -e "${YELLOW}[1/7] Dropping and recreating database...${NC}"
$SQL -e "DROP DATABASE IF EXISTS starthub; CREATE DATABASE starthub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
echo -e "${GREEN}✓ Database recreated${NC}"

echo -e "${YELLOW}[2/7] Loading schema...${NC}"
$SQL starthub < ../schema/schema.sql
echo -e "${GREEN}✓ Schema loaded${NC}"

echo -e "${YELLOW}[3/7] Loading views...${NC}"
$SQL starthub < ../schema/views.sql
echo -e "${GREEN}✓ Views loaded${NC}"

echo -e "${YELLOW}[4/7] Loading seed data...${NC}"

echo "  - Categories..."
$SQL starthub < ../seeds/seed_categories.sql

echo "  - Users..."
$SQL starthub < ../seeds/seed_users.sql

echo "  - Startups..."
$SQL starthub < ../seeds/seed_startups.sql

echo "  - Partnerships..."
$SQL starthub < ../seeds/seed_partnerships.sql

echo "  - Comments..."
$SQL starthub < ../seeds/seed_comments.sql

echo "  - Votes..."
$SQL starthub < ../seeds/seed_votes.sql

echo -e "${GREEN}✓ Seed data loaded${NC}"

echo -e "${YELLOW}[5/7] Verifying tables...${NC}"
$SQL starthub -e "SHOW TABLES;"
echo -e "${GREEN}✓ Tables verified${NC}"

echo -e "${YELLOW}[6/7] Verifying data counts...${NC}"
$SQL starthub -e "
SELECT COUNT(*) AS total_categories FROM Category;
SELECT COUNT(*) AS total_users FROM \`User\`;
SELECT COUNT(*) AS total_startups FROM Startup;
SELECT COUNT(*) AS total_comments FROM Comment;
SELECT COUNT(*) AS total_votes FROM Vote;
SELECT COUNT(*) AS total_partnerships FROM UserStartupPartnership;
"
echo -e "${GREEN}✓ Data counts verified${NC}"

echo ""
echo -e "${BLUE}============================================${NC}"
echo -e "${GREEN}✓ Database reload completed successfully!${NC}"
echo -e "${BLUE}============================================${NC}"
