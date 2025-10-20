-- ===================================================
-- DATABASE SETUP
-- ===================================================
CREATE DATABASE IF NOT EXISTS resume_analyzer;
USE resume_analyzer;
ALTER TABLE users MODIFY email VARCHAR(255) NULL;

-- ===================================================
-- 1️⃣ USERS TABLE
-- Login & registration info
-- ===================================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===================================================
-- 2️⃣ USER PROFILES TABLE
-- Stores extracted resume info per upload
-- ===================================================
CREATE TABLE IF NOT EXISTS user_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    full_name VARCHAR(255),
    phone VARCHAR(50),
    skills TEXT,
    experience TEXT,
    education TEXT,
    resume_text LONGTEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ===================================================
-- 3️⃣ ANALYSIS RESULTS TABLE
-- Stores AI analysis, job match %, suggested roles, etc.
-- ===================================================
CREATE TABLE IF NOT EXISTS analysis_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    resume_id INT,
    recommended_jobs TEXT,
    match_score DECIMAL(5,2),
    suggested_courses TEXT,
    strengths TEXT,
    weaknesses TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (resume_id) REFERENCES user_profiles(id) ON DELETE CASCADE
);

-- ===================================================
-- 4️⃣ FEEDBACK TABLE
-- Stores user feedback before thank-you page
-- ===================================================
CREATE TABLE IF NOT EXISTS feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comments TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ===================================================
-- 5️⃣ REPORTS TABLE (OPTIONAL)
-- Stores generated report details (PDF/chart summaries)
-- ===================================================
CREATE TABLE IF NOT EXISTS reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    resume_id INT,
    report_path VARCHAR(255),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (resume_id) REFERENCES user_profiles(id) ON DELETE CASCADE
);

-- ===================================================
-- 6️⃣ ADMIN TABLE (OPTIONAL)
-- For app administrators or moderators
-- ===================================================
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_name VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===================================================
-- ✅ SAMPLE DATA (Optional)
-- ===================================================
INSERT INTO users (username, email, password_hash)
VALUES ('testuser', 'test@example.com', 'abc123hash')
ON DUPLICATE KEY UPDATE username=username;

INSERT INTO admin_users (admin_name, email, password_hash)
VALUES ('Admin', 'admin@resumeai.com', 'adminhash')
ON DUPLICATE KEY UPDATE admin_name=admin_name;

-- ===================================================
-- 🧩 VERIFICATION COMMANDS
-- ===================================================
SHOW TABLES;

DESCRIBE users;
DESCRIBE user_profiles;
DESCRIBE analysis_results;
DESCRIBE feedback;
DESCRIBE reports;
DESCRIBE admin_users;

-- ===================================================
-- END OF SCRIPT
-- ===================================================
