CREATE TABLE IF NOT EXISTS button_events (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    action_type TEXT NOT NULL,
    pressed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);