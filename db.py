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
        autocommit=True # Har bir amalni darhol saqlash uchun
    )

def get_user(telegram_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM users WHERE telegram_id=%s", (telegram_id,))
        user = cur.fetchone()
        return user
    finally:
        cur.close()
        conn.close()

def save_user(telegram_id, region=None):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Avval tekshiramiz, bazada bormi?
        cur.execute("SELECT telegram_id FROM users WHERE telegram_id=%s", (telegram_id,))
        if cur.fetchone() is None:
            cur.execute(
                "INSERT INTO users (telegram_id, region) VALUES (%s, %s)",
                (telegram_id, region),
            )
            print(f"✅ BAZA: Yangi foydalanuvchi saqlandi: {telegram_id}")
        else:
            print(f"ℹ️ BAZA: Foydalanuvchi allaqachon mavjud: {telegram_id}")
    except Exception as e:
        print(f"❌ BAZA SAQLASHDA XATO: {e}")
    finally:
        cur.close()
        conn.close()

def update_region(telegram_id, region):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE users SET region=%s WHERE telegram_id=%s",
            (region, telegram_id),
        )
        print(f"✅ BAZA: Region yangilandi: {telegram_id} -> {region}")
    finally:
        cur.close()
        conn.close()

def count_user():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM users")
        result = cur.fetchone()
        return result[0] if result else 0
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
