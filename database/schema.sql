-- Complete ShaktiDB Database Schema
-- Compatible with PostgreSQL & SQLite3

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- SQLite fallback compatibility
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    age INT,
    gender VARCHAR(20),
    height DECIMAL(5,2), -- in cm
    weight DECIMAL(5,2), -- in kg
    bmi DECIMAL(4,2),
    skin_type VARCHAR(50),
    city VARCHAR(100),
    password_hash VARCHAR(256) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Weather Logs Table
CREATE TABLE IF NOT EXISTS weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT,
    city VARCHAR(100) NOT NULL,
    temperature DECIMAL(4,1),
    humidity INT,
    uv_index DECIMAL(3,1),
    condition VARCHAR(50),
    wind_speed DECIMAL(4,1),
    pressure INT,
    visibility DECIMAL(4,1),
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 3. Static/Reference Recommendations Table
CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category VARCHAR(50) NOT NULL,
    title VARCHAR(150) NOT NULL,
    recommendation_text TEXT NOT NULL,
    priority VARCHAR(20) DEFAULT 'info'
);

-- 4. Recommendation History Logs
CREATE TABLE IF NOT EXISTS recommendation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT NOT NULL,
    city VARCHAR(100),
    temperature DECIMAL(4,1),
    uv_index DECIMAL(3,1),
    category VARCHAR(50),
    title VARCHAR(150),
    recommendation_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 5. User Settings Configuration Table
CREATE TABLE IF NOT EXISTS user_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT UNIQUE NOT NULL,
    email_notifications INT DEFAULT 1, -- 0=disabled, 1=enabled
    sms_notifications INT DEFAULT 0,
    dark_mode INT DEFAULT 0,
    weather_refresh_interval INT DEFAULT 60, -- minutes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 6. Security/Audit Logs Table
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT,
    action VARCHAR(150) NOT NULL,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Indices for performance optimizations
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_rec_history_user ON recommendation_history(user_id);
CREATE INDEX IF NOT EXISTS idx_weather_city ON weather(city);
CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_logs(user_id);
