-- seed_comments.sql
INSERT INTO Comment (comment_id, content, created_date, modified_date, user_id, startup_id) VALUES
(1, 'Amazing concept — I would love to try this in my neighborhood garden!', '2025-06-02 10:00:00', NULL, 3, 1),
(2, 'Do you have an API for data export?', '2025-06-11 13:20:00', NULL, 4, 2),
(3, 'This would help junior devs find mentors faster.', '2025-07-06 09:10:00', NULL, 2, 3),
(4, 'Consider adding adaptive learning paths for enterprise users.', '2025-08-13 15:30:00', NULL, 5, 4),
(5, 'Would invest if traction metrics improve.', '2025-09-02 16:00:00', NULL, 1, 5),

(6, 'Nice dashboard and analytics!', '2025-09-11 10:05:00', NULL, 6, 6),
(7, 'Security and privacy are essential for telemedicine.', '2025-09-16 12:45:00', NULL, 9, 7),
(8, 'Can tutors set their hourly rate on the platform?', '2025-09-23 14:30:00', NULL, 11, 8),
(9, 'Very interesting approach to traceability.', '2025-10-02 09:50:00', NULL, 4, 9),
(10, 'Mobile experience is smooth and intuitive.', '2025-10-11 11:20:00', NULL, 12, 10),

(11, 'Love the live collaboration features!', '2025-10-19 17:00:00', NULL, 13, 11),
(12, 'Have you validated sensors in real conditions?', '2025-10-26 09:30:00', NULL, 14, 12),
(13, 'What is your pricing model?', '2025-06-03 08:00:00', NULL, 2, 1),
(14, 'I can help with UX improvements.', '2025-06-12 09:00:00', NULL, 4, 2),
(15, 'Great mentor matching algorithm.', '2025-07-07 10:30:00', NULL, 7, 3),

(16, 'Would love an enterprise tier.', '2025-08-14 10:45:00', NULL, 5, 4),
(17, 'Is there a demo or sandbox?', '2025-09-04 12:00:00', NULL, 3, 5),
(18, 'How do you handle refunds?', '2025-09-12 15:00:00', NULL, 10, 10),
(19, 'Could integrate with CI/CD for deployments.', '2025-10-20 09:10:00', NULL, 12, 11),
(20, 'Interested in pilot for our factory.', '2025-10-03 14:40:00', NULL, 14, 9),

(21, 'Would like to try the hardware dev kit.', '2025-10-26 11:00:00', NULL, 6, 12),
(22, 'Amazing UX and onboarding flow.', '2025-09-24 17:00:00', NULL, 11, 8),
(23, 'Can we collaborate on marketing campaigns?', '2025-10-05 10:25:00', NULL, 9, 9),
(24, 'Where can I find the API docs?', '2025-06-15 13:35:00', NULL, 8, 1),
(25, 'The investor dashboard helped us decide.', '2025-09-02 18:00:00', NULL, 1, 5);
