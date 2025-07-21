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


def get_avg_day_stats(user_id: int) -> str:
    query = """
    WITH user_days AS (
      SELECT COUNT(DISTINCT pressed_at::date) AS total_days
      FROM button_events
      WHERE user_id = %s
    )
    SELECT
      b.action_type,
      ROUND(COUNT(*) * 1.0 / ud.total_days, 1) AS avg_per_day
    FROM button_events b, user_days ud
    WHERE b.user_id = %s
    GROUP BY b.action_type, ud.total_days
    ORDER BY avg_per_day DESC;
    """

    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (user_id, user_id))
            rows = cur.fetchall()

    if not rows:
        return "No data yet to calculate averages!"

    lines = ["📈 Daily averages:"]
    for action_type, avg in rows:
        lines.append(f"• {action_type}: {avg:.1f} per day")

    return "\n".join(lines)


def apply_migrations():
    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            with open("migrations/001_init.sql", "r") as f:
                cur.execute(f.read())
            conn.commit()
