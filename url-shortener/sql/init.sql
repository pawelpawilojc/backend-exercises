CREATE DATABASE IF NOT EXISTS url_shortener_db;

USE url_shortener_db;

CREATE TABLE IF NOT EXISTS urls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    original_url TEXT NOT NULL,
    short_code VARCHAR(10) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    access_count INT DEFAULT 0
);
