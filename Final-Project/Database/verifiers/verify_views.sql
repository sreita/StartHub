-- ===========================
-- VERIFY VIEWS IN STARTHUB_DB
-- ===========================

USE starthub_db;

-- 1. Show all existing views
SHOW FULL TABLES IN starthub_db WHERE TABLE_TYPE LIKE 'VIEW';

-- 2. Show the definition of each view
SHOW CREATE VIEW StartupDetails;
SHOW CREATE VIEW StartupVoteStats;

-- 3. Test the data from the views
SELECT * FROM StartupDetails LIMIT 10;

SELECT * FROM StartupVoteStats LIMIT 10;

-- 4. Check joins and aggregated values manually (optional)
-- For example, view startup details with vote statistics
SELECT 
    sd.startup_name,
    sd.category,
    sv.total_upvotes,
    sv.total_downvotes
FROM StartupDetails sd
LEFT JOIN StartupVoteStats sv ON sd.startup_id = sv.startup_id
ORDER BY sv.total_upvotes DESC;
