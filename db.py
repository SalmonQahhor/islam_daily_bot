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
