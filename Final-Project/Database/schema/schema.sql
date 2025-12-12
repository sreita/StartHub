-- schema.sql
-- DDL: tablas e índices (sin datos de ejemplo ni vistas)
DROP TABLE IF EXISTS ConfirmationToken;
DROP TABLE IF EXISTS Vote;
DROP TABLE IF EXISTS Comment;
DROP TABLE IF EXISTS UserStartupPartnership;
DROP TABLE IF EXISTS Startup;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS `User`;

CREATE TABLE `User` (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_admin BOOLEAN DEFAULT FALSE,
    profile_info TEXT,
    is_enabled BOOLEAN NOT NULL DEFAULT FALSE, 
    is_locked BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT chk_email CHECK (email LIKE '%@%')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_user_email ON `User`(email);

CREATE TABLE Category (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_category_name ON Category(name);

CREATE TABLE Startup (
    startup_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    email VARCHAR(255),
    website VARCHAR(255),
    social_media VARCHAR(255),
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner_user_id INT NOT NULL,
    category_id INT NOT NULL,
    CONSTRAINT fk_startup_owner 
        FOREIGN KEY (owner_user_id) 
        REFERENCES `User`(user_id) 
        ON DELETE CASCADE,
    CONSTRAINT fk_startup_category 
        FOREIGN KEY (category_id) 
        REFERENCES Category(category_id) 
        ON DELETE RESTRICT,
    CONSTRAINT chk_startup_email CHECK (email LIKE '%@%' OR email IS NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_startup_name ON Startup(name);
CREATE INDEX idx_startup_owner ON Startup(owner_user_id);
CREATE INDEX idx_startup_category ON Startup(category_id);
CREATE INDEX idx_startup_created ON Startup(created_date);



CREATE TABLE ConfirmationToken (
    token_id INT PRIMARY KEY AUTO_INCREMENT,
    token VARCHAR(255) NOT NULL UNIQUE,
    created_at DATETIME NOT NULL,
    expires_at DATETIME NOT NULL,
    confirmed_at DATETIME,
    app_user_id INT NOT NULL,
    
    CONSTRAINT fk_token_user 
        FOREIGN KEY (app_user_id) 
        REFERENCES `User`(user_id)
        ON DELETE CASCADE 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_token_user ON ConfirmationToken(app_user_id);

CREATE TABLE PasswordResetToken (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    token VARCHAR(255) NOT NULL UNIQUE,
    user_id INT NOT NULL,
    expires_at DATETIME NOT NULL,
    confirmed_at DATETIME,
    
    CONSTRAINT fk_password_reset_user 
        FOREIGN KEY (user_id) 
        REFERENCES `User`(user_id) 
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_password_reset_token ON PasswordResetToken(token);
CREATE INDEX idx_password_reset_user ON PasswordResetToken(user_id);
CREATE INDEX idx_password_reset_expires ON PasswordResetToken(expires_at);


CREATE TABLE Comment (
    comment_id INT PRIMARY KEY AUTO_INCREMENT,
    content TEXT NOT NULL,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    modified_date DATETIME,
    user_id INT NOT NULL,
    startup_id INT NOT NULL,
    CONSTRAINT fk_comment_user 
        FOREIGN KEY (user_id) 
        REFERENCES `User`(user_id) 
        ON DELETE CASCADE,
    CONSTRAINT fk_comment_startup 
        FOREIGN KEY (startup_id) 
        REFERENCES Startup(startup_id) 
        ON DELETE CASCADE,
    CONSTRAINT chk_content_length CHECK (LENGTH(content) > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_comment_user ON Comment(user_id);
CREATE INDEX idx_comment_startup ON Comment(startup_id);
CREATE INDEX idx_comment_date ON Comment(created_date);

CREATE TABLE Vote (
    vote_id INT PRIMARY KEY AUTO_INCREMENT,
    vote_type ENUM('upvote', 'downvote') NOT NULL,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    startup_id INT NOT NULL,
    CONSTRAINT fk_vote_user 
        FOREIGN KEY (user_id) 
        REFERENCES `User`(user_id) 
        ON DELETE CASCADE,
    CONSTRAINT fk_vote_startup 
        FOREIGN KEY (startup_id) 
        REFERENCES Startup(startup_id) 
        ON DELETE CASCADE,
    CONSTRAINT unique_vote_per_user_startup 
        UNIQUE (user_id, startup_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_vote_user ON Vote(user_id);
CREATE INDEX idx_vote_startup ON Vote(startup_id);
CREATE INDEX idx_vote_type ON Vote(vote_type);

CREATE TABLE UserStartupPartnership (
    user_id INT NOT NULL,
    startup_id INT NOT NULL,
    partnership_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(100),
    PRIMARY KEY (user_id, startup_id),
    CONSTRAINT fk_partnership_user 
        FOREIGN KEY (user_id) 
        REFERENCES `User`(user_id) 
        ON DELETE CASCADE,
    CONSTRAINT fk_partnership_startup 
        FOREIGN KEY (startup_id) 
        REFERENCES Startup(startup_id) 
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_partnership_startup ON UserStartupPartnership(startup_id);
