SELECT COUNT(*) FROM `User`;
SELECT COUNT(*) FROM Startup;
SELECT COUNT(*) FROM Comment;
SELECT COUNT(*) FROM Vote;
SELECT COUNT(*) FROM UserStartupPartnership;

SELECT * FROM StartupVoteStats ORDER BY total_votes DESC LIMIT 10;
SELECT * FROM StartupDetails ORDER BY created_date DESC LIMIT 10;