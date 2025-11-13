-- ============================================================================
-- FILE: reload_all.sql
-- PURPOSE: Rebuilds the entire StarHub database from scratch.
-- AUTHOR: yoshikagua
-- DATE: 2025-11-13
-- ============================================================================

-- Step 1. Drop and recreate the database
DROP DATABASE IF EXISTS starthub;
CREATE DATABASE starthub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE starthub;

-- Step 2. Import schema (tables, constraints, indexes)
SOURCE ../schema/schema.sql;

-- Step 3. Import views
SOURCE ../schema/views.sql;

-- Step 4. Insert seed data in correct dependency order
SOURCE ../seeds/seed_categories.sql;
SOURCE ../seeds/seed_users.sql;
SOURCE ../seeds/seed_startups.sql;
SOURCE ../seeds/seed_partnerships.sql;
SOURCE ../seeds/seed_comments.sql;
SOURCE ../seeds/seed_votes.sql;

-- Step 5. Confirm structure and data
SHOW TABLES;
SELECT COUNT(*) AS total_categories FROM Category;
SELECT COUNT(*) AS total_users FROM `User`;
SELECT COUNT(*) AS total_startups FROM Startup;
SELECT COUNT(*) AS total_comments FROM Comment;
SELECT COUNT(*) AS total_votes FROM Vote;
SELECT COUNT(*) AS total_partnerships FROM UserStartupPartnership;

-- ============================================================================
-- END OF FILE
-- ============================================================================
