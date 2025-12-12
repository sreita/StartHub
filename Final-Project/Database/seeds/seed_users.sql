-- seed_users.sql

INSERT INTO `User` (user_id, email, password_hash, first_name, last_name, registration_date, is_admin, profile_info, is_locked, is_enabled) VALUES
(1, 'admin@starthub.test', '$2b$12$examplehashadmin', 'Admin', 'One', '2025-01-10 10:00:00', TRUE, 'Platform administrator.', FALSE, TRUE), 
(2, 'ana@example.com', '$2b$12$examplehashana', 'Ana', 'Gomez', '2025-02-15 11:20:00', FALSE, 'Founder interested in green tech.', FALSE, FALSE),
(3, 'diego@example.com', '$2b$12$examplehashdiego', 'Diego', 'Mendez', '2025-03-01 09:30:00', FALSE, 'Full-stack developer.', FALSE, FALSE),
(4, 'sara@example.com', '$2b$12$examplehashsara', 'Sara', 'Lopez', '2025-04-22 14:45:00', FALSE, 'UX designer and startup mentor.', FALSE, TRUE),
(5, 'maria@example.com', '$2b$12$examplehashmaria', 'Maria', 'Perez', '2025-05-05 16:00:00', FALSE, 'Investor and advisor.', FALSE, FALSE),

(6, 'luis@example.com', '$2b$12$examplehashluis', 'Luis', 'Ramirez', '2025-05-20 09:10:00', FALSE, 'Hardware engineer.', FALSE, FALSE),
(7, 'julia@example.com', '$2b$12$examplehashjulia', 'Julia', 'Castro', '2025-06-02 12:30:00', FALSE, 'Data scientist.', FALSE, TRUE),
(8, 'miguel@example.com', '$2b$12$examplehashmiguel', 'Miguel', 'Ortiz', '2025-06-15 08:50:00', FALSE, 'Product manager.', FALSE, FALSE),
(9, 'laura@example.com', '$2b$12$examplehashlaura', 'Laura', 'Vargas', '2025-07-01 10:05:00', FALSE, 'Marketing specialist.', FALSE, TRUE),
(10, 'andres@example.com', '$2b$12$examplehashandres', 'Andres', 'Diaz', '2025-07-10 11:40:00', FALSE, 'DevOps engineer.', FALSE, FALSE),

(11, 'sofia@example.com', '$2b$12$examplehashsofia', 'Sofia', 'Ramos', '2025-07-20 09:00:00', FALSE, 'Content creator.', FALSE, FALSE),
(12, 'pablo@example.com', '$2b$12$examplehashpablo', 'Pablo', 'Martinez', '2025-08-03 13:15:00', FALSE, 'Mobile developer.', FALSE, FALSE),
(13, 'valeria@example.com', '$2b$12$examplehashvaleria', 'Valeria', 'Suarez', '2025-08-18 15:00:00', FALSE, 'Business analyst.', FALSE, FALSE),
(14, 'ricardo@example.com', '$2b$12$examplehashricardo', 'Ricardo', 'Lopez', '2025-09-01 08:20:00', FALSE, 'Hardware designer.', FALSE, FALSE),
(15, 'isabel@example.com', '$2b$12$examplehashisabel', 'Isabel', 'Gomez', '2025-09-10 17:30:00', FALSE, 'Startup community manager.', FALSE, TRUE);
