import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT", 3306)),
        autocommit=True
    )

def get_user(telegram_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM users WHERE telegram_id=%s", (int(telegram_id),))
        return cur.fetchone()
    except Exception as e:
        print(f"Error getting user: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def save_user(telegram_id, region=None):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT IGNORE INTO users (telegram_id, region, lang) VALUES (%s, %s, %s)",
            (int(telegram_id), region, 'latin'),
        )
    except Exception as e:
        # Agar lang ustuni yo'qligi uchun xato bersa, faqat telegram_id va regionni yozadi
        cur.execute(
            "INSERT IGNORE INTO users (telegram_id, region) VALUES (%s, %s)",
            (int(telegram_id), region),
        )
    finally:
        cur.close()
        conn.close()

def update_region(telegram_id, region):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE users SET region=%s WHERE telegram_id=%s", (region, int(telegram_id)))
    finally:
        cur.close()
        conn.close()

def update_lang(telegram_id, lang):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE users SET lang=%s WHERE telegram_id=%s", (lang, int(telegram_id)))
    finally:
        cur.close()
        conn.close()

def get_all_users():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT telegram_id FROM users")
        return [row[0] for row in cur.fetchall()]
    finally:
        cur.close()
        conn.close()
