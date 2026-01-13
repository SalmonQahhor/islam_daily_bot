import mysql.connector
from config import DB_CONFIG


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def get_user(telegram_id):
    conn = get_connection()
    cur = conn.cursor(dictionary = True)
    cur.execute("SELECT * FROM users WHERE telegram_id=%s", (telegram_id,))
    user = cur.fetchone()
    conn.close()
    return user

def save_user(telegram_id, region=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT IGNORE INTO users (telegram_id, region) VALUES (%s, %s)",
        (telegram_id, region),
    )
    conn.commit()
    conn.close()

def update_region(telegram_id, region):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET region=%s WHERE telegram_id=%s",
        (region, telegram_id),
    )
    conn.commit()
    conn.close()
