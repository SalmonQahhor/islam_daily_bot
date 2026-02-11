import mysql.connector
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()

def get_connection():
    
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT", 3306)),
        autocommit=True,
        connection_timeout=20, # Ulanish kutish vaqti (soniya)
        get_warnings=True
    )

def get_user(telegram_id):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE telegram_id=%s", (int(telegram_id),))
        return cur.fetchone()
    except Exception as e:
        print(f"Error getting user: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            cur.close()
            conn.close()

def save_user(telegram_id, region=None):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT IGNORE INTO users (telegram_id, region) VALUES (%s, %s)",
            (int(telegram_id), region),
        )
    except Exception as e:
        print(f"Error saving user: {e}")
    finally:
        if conn and conn.is_connected():
            cur.close()
            conn.close()

def update_region(telegram_id, region):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET region=%s WHERE telegram_id=%s", (region, int(telegram_id)))
    except Exception as e:
        print(f"Error updating region: {e}")
    finally:
        if conn and conn.is_connected():
            cur.close()
            conn.close()

def get_all_users():
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT telegram_id FROM users")
        rows = cur.fetchall()
        return [row[0] for row in rows]
    except Exception as e:
        print(f"Error fetching all users: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cur.close()
            conn.close()

def count_user():
    # Har safar get_all_users() orqali barcha IDlarni yuklab olish RAMni to'ldiradi.
    # Bu funksiyani SQL'ning o'zida sanaydigan qildim.
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users")
        result = cur.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print(f"Error counting users: {e}")
        return 0
    finally:
        if conn and conn.is_connected():
            cur.close()
            conn.close()

def check_task_limit(telegram_id):
    conn = None
    today = date.today()
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT click_count, last_click_date FROM users WHERE telegram_id=%s", (int(telegram_id),))
        user = cur.fetchone()
        
        if not user or user.get('last_click_date') != today:
            cur.execute(
                "UPDATE users SET click_count=1, last_click_date=%s WHERE telegram_id=%s", 
                (today, int(telegram_id))
            )
            return 1
        
        current_count = user.get('click_count', 0)
        if current_count < 2:
            new_count = current_count + 1
            cur.execute(
                "UPDATE users SET click_count=%s WHERE telegram_id=%s", 
                (new_count, int(telegram_id))
            )
            return new_count
        
        return 3
    except Exception as e:
        print(f"Error in check_task_limit: {e}")
        return 3
    finally:
        if conn and conn.is_connected():
            cur.close()
            conn.close()
