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
        port=int(os.getenv("MYSQLPORT", 3306))
    )

def get_user(telegram_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE telegram_id=%s", (telegram_id,))
    user = cur.fetchone()
    cur.close() 
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
    cur.close()
    conn.close()

def update_region(telegram_id, region):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET region=%s WHERE telegram_id=%s",
        (region, telegram_id),
    )
    conn.commit()
    cur.close()
    conn.close()

def count_user():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    result = cur.fetchone()
    cur.close() # <--- buni qo'shish kerak edi
    conn.close()
    return result[0] if result else 0

def get_all_users():
    conn = get_connection()
    cur = conn.cursor() # dictionary=True shart emas bu yerda
    try:
        cur.execute("SELECT telegram_id FROM users")
        rows = cur.fetchall()
        # Kelayotgan ma'lumotni terminalda tekshirish uchun:
        print(f"DEBUG: Bazadan olingan xom ma'lumot: {rows}")
        
        users = [row[0] for row in rows]
        print(f"DEBUG: Qayta ishlangan IDlar: {users}")
        
        return users
    except Exception as e:
        print(f"DATABASE ERROR: {e}")
        return []
    finally:
        cur.close()
        conn.close()
