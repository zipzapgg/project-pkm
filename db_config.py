import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """
    Membuat koneksi ke database MySQL menggunakan environment variables.
    Auto-reconnect dan timeout aman untuk deployment di PythonAnywhere.
    """
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT', 3307),
            connection_timeout=10,
            autocommit=True
        )
        if conn.is_connected():
            return conn
    except mysql.connector.Error as e:
        print(f"⚠️ Database connection error: {e}")
        return None
