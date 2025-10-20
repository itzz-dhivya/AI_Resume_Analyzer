-- ===================================================
-- DATABASE SETUP
-- ===================================================
CREATE DATABASE IF NOT EXISTS resume_analyzer;
USE resume_analyzer;
ALTER TABLE users MODIFY email VARCHAR(255) NULL;

-- 1️⃣ Users Table
CREATE TABLE IF NOT EXISTS a_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('user','admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2️⃣ Feedback Table
CREATE TABLE IF NOT EXISTS b_feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3️⃣ Analysis Results Table
CREATE TABLE IF NOT EXISTS c_analysis_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    role_name VARCHAR(100) NOT NULL,
    matched_skills TEXT,
    missing_skills TEXT,
    score DECIMAL(5,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES a_users(id) ON DELETE CASCADE
);
