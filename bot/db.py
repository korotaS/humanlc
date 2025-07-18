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
    conn = psycopg2.connect(**DB_PARAMS)
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO button_events (user_id, action_type) VALUES (%s, %s)",
            (user_id, button_type)
        )
        conn.commit()
    conn.close()


def apply_migrations():
    conn = psycopg2.connect(**DB_PARAMS)
    with conn.cursor() as cur:
        with open("migrations/001_init.sql", "r") as f:
            cur.execute(f.read())
        conn.commit()
    conn.close()
