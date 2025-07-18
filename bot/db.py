import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_PARAMS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}


def log_button_event(user_id, button_type):
    query = "INSERT INTO button_events (user_id, action_type) VALUES (%s, %s)"

    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (user_id, button_type))
            conn.commit()


def get_today_stats(user_id: int) -> str:
    query = """
    SELECT action_type, COUNT(*) AS count
    FROM button_events
    WHERE user_id = %s AND pressed_at::date = CURRENT_DATE
    GROUP BY action_type
    ORDER BY count DESC;
    """

    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (user_id,))
            rows = cur.fetchall()

    if not rows:
        return "You haven't done anything today!"

    lines = ["📊 Your activity today:"]
    for action_type, count in rows:
        lines.append(f"• {action_type}: {count} times")

    return "\n".join(lines)


def apply_migrations():
    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            with open("migrations/001_init.sql", "r") as f:
                cur.execute(f.read())
            conn.commit()
