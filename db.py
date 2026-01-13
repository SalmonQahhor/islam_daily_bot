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

def setup_database():
    """Eski jadvalni o'chirib, yangi to'g'ri jadval yaratish"""
    conn = get_connection()
    cur = conn.cursor()
    # Diqqat: Bu qator eski ma'lumotlarni o'chirib tashlaydi (tozalash uchun)
    cur.execute("DROP TABLE IF EXISTS users") 
    cur.execute("""
        CREATE TABLE users (
            telegram_id BIGINT PRIMARY KEY,
            region VARCHAR(100)
        )
    """)
    print("✅ Yangi 'users' jadvali muvaffaqiyatli yaratildi (BIGINT bilan).")
    cur.close()
    conn.close()

# Bot birinchi marta ishlaganda jadvalni to'g'rilab olishi uchun:
# Uni faqat bir marta yurgizib, keyin o'chirib qo'ysangiz ham bo'ladi.
# Hozircha qoldiring:
try:
    #setup_database()
except Exception as e:
    print(f"Jadval yaratishda xato (balki allaqachon bordir): {e}")

def get_user(telegram_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM users WHERE telegram_id=%s", (int(telegram_id),))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()

def save_user(telegram_id, region=None):
    conn = get_connection()
    cur = conn.cursor()
    try:
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
        cur.execute(
            "UPDATE users SET region=%s WHERE telegram_id=%s",
            (region, int(telegram_id)),
        )
    finally:
        cur.close()
        conn.close()

def get_all_users():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT telegram_id FROM users")
        rows = cur.fetchall()
        return [row[0] for row in rows]
    finally:
        cur.close()
        conn.close()

def count_user():
    return len(get_all_users())
