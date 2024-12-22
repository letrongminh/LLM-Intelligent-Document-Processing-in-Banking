CREATE DATABASE demo_bot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE demo_bot;
CREATE TABLE chat_conversations (
    id INT NOT NULL AUTO_INCREMENT,
    conversation_id VARCHAR(50) NOT NULL DEFAULT '',
    bot_id VARCHAR(100) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    message TEXT,
    is_request BOOLEAN DEFAULT TRUE,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);