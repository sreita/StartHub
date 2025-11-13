-- seed_startups.sql
INSERT INTO Startup (startup_id, name, description, email, website, social_media, created_date, owner_user_id, category_id) VALUES
(1, 'EcoGrow', 'Platform to optimize urban gardening and resource allocation.', 'contact@ecogrow.example', 'https://ecogrow.example', '@ecogrow', '2025-06-01 08:00:00', 2, 4),
(2, 'FitTrack', 'Wearable analysis and coaching for fitness improvement.', 'hello@fittrack.example', 'https://fittrack.example', '@fittrack', '2025-06-10 09:30:00', 3, 2),
(3, 'CodeConnect', 'A mentoring and collaboration network for developers.', 'team@codeconnect.example', 'https://codeconnect.example', '@codeconnect', '2025-07-05 12:00:00', 3, 1),
(4, 'Learnly', 'Microlearning platform for professional skills.', 'info@learnly.example', 'https://learnly.example', '@learnly', '2025-08-12 10:15:00', 4, 3),
(5, 'FinWise', 'Personal finance assistant using ML to optimize budgets.', 'support@finwise.example', 'https://finwise.example', '@finwise', '2025-09-01 11:45:00', 5, 5),

(6, 'SolarIQ', 'Analytics for rooftop solar performance and maintenance.', 'contact@solariq.example', 'https://solariq.example', '@solariq', '2025-09-10 09:00:00', 6, 4),
(7, 'HealthBridge', 'Platform to manage patient-doctor communication securely.', 'hello@healthbridge.example', 'https://healthbridge.example', '@healthbridge', '2025-09-15 10:20:00', 7, 2),
(8, 'TutorHub', 'Peer-to-peer tutoring marketplace for STEM subjects.', 'team@tutorhub.example', 'https://tutorhub.example', '@tutorhub', '2025-09-22 14:00:00', 8, 3),
(9, 'GreenLogix', 'Supply chain tracking for sustainable materials.', 'info@greenlogix.example', 'https://greenlogix.example', '@greenlogix', '2025-10-01 09:30:00', 9, 1),
(10, 'PocketBank', 'Mobile-first digital bank targeting freelancers.', 'support@pocketbank.example', 'https://pocketbank.example', '@pocketbank', '2025-10-10 11:00:00', 10, 5),

(11, 'DevStream', 'Live coding collaboration and streaming for teams.', 'contact@devstream.example', 'https://devstream.example', '@devstream', '2025-10-18 16:45:00', 12, 1),
(12, 'BioSense', 'Wearable biosensors for early health alerts.', 'hello@biosense.example', 'https://biosense.example', '@biosense', '2025-10-25 08:10:00', 11, 2);
