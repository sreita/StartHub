-- ============================================================================
-- FILE: truncate_all.sql
-- PURPOSE: Clean all StarHub tables while keeping schema intact.
-- AUTHOR: yoshikagua
-- DATE: 2025-11-13
-- ============================================================================

USE starthub;

-- Step 1. Disable foreign key checks temporarily
SET FOREIGN_KEY_CHECKS = 0;

-- Step 2. Truncate all data tables
TRUNCATE TABLE Vote;
TRUNCATE TABLE Comment;
TRUNCATE TABLE UserStartupPartnership;
TRUNCATE TABLE Startup;
TRUNCATE TABLE `User`;
TRUNCATE TABLE Category;

-- Step 3. Reset auto-increment counters (optional)
ALTER TABLE Vote AUTO_INCREMENT = 1;
ALTER TABLE Comment AUTO_INCREMENT = 1;
ALTER TABLE Startup AUTO_INCREMENT = 1;
ALTER TABLE `User` AUTO_INCREMENT = 1;
ALTER TABLE Category AUTO_INCREMENT = 1;

-- Step 4. Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- Step 5. Verify cleanup
SHOW TABLES;
SELECT 'Tables truncated successfully!' AS status;

-- ============================================================================
-- END OF FILE
-- ============================================================================
