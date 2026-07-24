-- Seeding Sample Data for Personal Health & Wellness System

-- 1. Insert Sample Users
-- Passwords are hashed values of 'password123' compatible with werkzeug.security
INSERT INTO users (name, email, phone, age, gender, height, weight, bmi, skin_type, city, password_hash)
VALUES (
    'Alice Smith', 
    'alice@example.com', 
    '+1 (555) 123-4567', 
    29, 
    'Female', 
    168.0, 
    62.0, 
    21.97, 
    'Type II (Fair)', 
    'Mumbai', 
    'pbkdf2:sha256:260000$WvQJvC3b$05b4fb9a5c889f0413ea01831be276f7c68832a81878d6b801a6136d8be69be5'
);

INSERT INTO users (name, email, phone, age, gender, height, weight, bmi, skin_type, city, password_hash)
VALUES (
    'Bob Johnson', 
    'bob@example.com', 
    '+1 (555) 987-6543', 
    35, 
    'Male', 
    182.0, 
    85.0, 
    25.66, 
    'Type IV (Olive)', 
    'Delhi', 
    'pbkdf2:sha256:260000$WvQJvC3b$05b4fb9a5c889f0413ea01831be276f7c68832a81878d6b801a6136d8be69be5'
);

-- 2. Insert User Settings
INSERT INTO user_settings (user_id, email_notifications, sms_notifications, dark_mode, weather_refresh_interval)
VALUES (1, 1, 0, 1, 60);

INSERT INTO user_settings (user_id, email_notifications, sms_notifications, dark_mode, weather_refresh_interval)
VALUES (2, 1, 1, 0, 30);

-- 3. Insert Static Recommendation Reference Categories
INSERT INTO recommendations (category, title, recommendation_text, priority)
VALUES (
    'hydration', 
    'Routine Hydration Guide', 
    'Keep your body fluids balanced. Drink water regularly, aiming for 8 glasses a day minimum.', 
    'info'
);

INSERT INTO recommendations (category, title, recommendation_text, priority)
VALUES (
    'uv', 
    'Moderate Solar Protection', 
    'UV index is moderate. Apply SPF 15+ sunscreen and wear sunglasses for extended outdoor durations.', 
    'warning'
);

-- 4. Insert Recommendation History logs
INSERT INTO recommendation_history (user_id, city, temperature, uv_index, category, title, recommendation_text)
VALUES (
    1, 
    'Mumbai', 
    30.5, 
    5.2, 
    'hydration', 
    'High Heat Hydration', 
    'The weather is hot. Increase your fluid intake to at least 2.8L today.'
);

INSERT INTO recommendation_history (user_id, city, temperature, uv_index, category, title, recommendation_text)
VALUES (
    1, 
    'Mumbai', 
    30.5, 
    5.2, 
    'uv', 
    'Moderate Solar Protection', 
    'UV levels are moderate. Apply sunscreen before going out.'
);

-- 5. Seeding Weather History logs
INSERT INTO weather (user_id, city, temperature, humidity, uv_index, condition, wind_speed, pressure, visibility)
VALUES (1, 'Mumbai', 30.5, 80, 5.2, 'Rain', 14.5, 1008, 8.0);

INSERT INTO weather (user_id, city, temperature, humidity, uv_index, condition, wind_speed, pressure, visibility)
VALUES (2, 'Delhi', 39.2, 30, 8.5, 'Clear', 12.0, 1005, 10.0);

-- 6. Seeding Audit Logs
INSERT INTO audit_logs (user_id, action, ip_address)
VALUES (1, 'User Sign Up', '192.168.1.10');

INSERT INTO audit_logs (user_id, action, ip_address)
VALUES (1, 'Preferences Updated', '192.168.1.10');
