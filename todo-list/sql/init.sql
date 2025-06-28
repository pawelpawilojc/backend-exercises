CREATE DATABASE IF NOT EXISTS todo_db;

USE todo_db;

CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status ENUM('to_do', 'in_progress', 'done') NOT NULL,
    priority INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
