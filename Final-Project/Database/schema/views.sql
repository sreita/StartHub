-- views.sql
DROP VIEW IF EXISTS StartupVoteStats;
DROP VIEW IF EXISTS StartupDetails;

CREATE VIEW StartupVoteStats AS
SELECT 
    s.startup_id,
    s.name AS startup_name,
    COUNT(CASE WHEN v.vote_type = 'upvote' THEN 1 END) AS upvotes,
    COUNT(CASE WHEN v.vote_type = 'downvote' THEN 1 END) AS downvotes,
    COUNT(v.vote_id) AS total_votes,
    (COUNT(CASE WHEN v.vote_type = 'upvote' THEN 1 END) - 
     COUNT(CASE WHEN v.vote_type = 'downvote' THEN 1 END)) AS net_votes
FROM Startup s
LEFT JOIN Vote v ON s.startup_id = v.startup_id
GROUP BY s.startup_id, s.name;

CREATE VIEW StartupDetails AS
SELECT 
    s.startup_id,
    s.name AS startup_name,
    s.description,
    s.email,
    s.website,
    s.social_media,
    s.created_date,
    u.user_id AS owner_id,
    CONCAT(u.first_name, ' ', u.last_name) AS owner_name,
    u.email AS owner_email,
    c.category_id,
    c.name AS category_name
FROM Startup s
INNER JOIN `User` u ON s.owner_user_id = u.user_id
INNER JOIN Category c ON s.category_id = c.category_id;
