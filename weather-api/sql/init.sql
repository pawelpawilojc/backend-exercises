CREATE DATABASE IF NOT EXISTS weather_db;

USE weather_db;

CREATE TABLE IF NOT EXISTS searches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(255) NOT NULL,
    country VARCHAR(255),
    temperature FLOAT,
    description TEXT,
    humidity INT,
    wind_speed FLOAT,
    searched_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
