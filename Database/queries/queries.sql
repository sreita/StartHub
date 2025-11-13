-- queries.sql
-- 1. List views
SHOW FULL TABLES WHERE Table_type = 'VIEW';

-- 2. Show view definitions
SHOW CREATE VIEW StartupVoteStats;
SHOW CREATE VIEW StartupDetails;

-- 3. Check view contents
SELECT * FROM StartupVoteStats ORDER BY total_votes DESC LIMIT 20;
SELECT * FROM StartupDetails ORDER BY created_date DESC LIMIT 20;

-- 4. Cross-check votes totals
SELECT SUM(total_votes) AS total_votes_from_view, (SELECT COUNT(*) FROM Vote) AS total_votes_from_table
FROM StartupVoteStats;

SELECT v.startup_id,
       SUM(v.vote_type = 'upvote') AS upvotes_calc,
       SUM(v.vote_type = 'downvote') AS downvotes_calc,
       COUNT(*) AS total_votes_calc
FROM Vote v
GROUP BY v.startup_id
ORDER BY total_votes_calc DESC
LIMIT 20;

-- 5. Compare single startup (id = 1)
SELECT svs.*, vc.upvotes_calc, vc.downvotes_calc, vc.total_votes_calc
FROM StartupVoteStats svs
LEFT JOIN (
    SELECT v.startup_id,
           SUM(v.vote_type = 'upvote') AS upvotes_calc,
           SUM(v.vote_type = 'downvote') AS downvotes_calc,
           COUNT(*) AS total_votes_calc
    FROM Vote v
    GROUP BY v.startup_id
) vc ON svs.startup_id = vc.startup_id
WHERE svs.startup_id = 1;

-- 6. Integrity checks
SELECT user_id, startup_id, COUNT(*) cnt
FROM Vote
GROUP BY user_id, startup_id
HAVING cnt > 1;

SELECT s.startup_id, s.name, s.owner_user_id
FROM Startup s
LEFT JOIN `User` u ON s.owner_user_id = u.user_id
WHERE u.user_id IS NULL;

SELECT s.startup_id, s.name, s.category_id
FROM Startup s
LEFT JOIN Category c ON s.category_id = c.category_id
WHERE c.category_id IS NULL;

-- 7. Admin / reporting queries
SELECT s.startup_id, s.startup_name, s.net_votes
FROM StartupVoteStats s
ORDER BY s.net_votes DESC
LIMIT 10;

SELECT * FROM StartupDetails
ORDER BY created_date DESC
LIMIT 10;

SELECT c.comment_id, c.content, c.created_date,
       CONCAT(u.first_name, ' ', u.last_name) AS user_name,
       s.name AS startup_name
FROM Comment c
JOIN `User` u ON c.user_id = u.user_id
JOIN Startup s ON c.startup_id = s.startup_id
ORDER BY c.created_date DESC
LIMIT 20;

SELECT v.user_id, CONCAT(u.first_name,' ',u.last_name) AS user_name, COUNT(*) AS votes_count
FROM Vote v
JOIN `User` u ON v.user_id = u.user_id
GROUP BY v.user_id
ORDER BY votes_count DESC
LIMIT 20;

SELECT s.startup_id, s.name
FROM Startup s
LEFT JOIN Vote v ON s.startup_id = v.startup_id
WHERE v.vote_id IS NULL;
