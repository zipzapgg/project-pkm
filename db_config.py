import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """
    Membuat koneksi langsung ke database.
    Lebih stabil untuk lingkungan serverless/free tier seperti PythonAnywhere.
    """
    try:
        # Ambil port dari .env, default ke 3306 jika tidak ada/salah
        port_env = os.getenv('DB_PORT')
        if not port_env:
            port_db = 3306
        else:
            port_db = int(port_env)

        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=port_db,
            autocommit=True  # Penting agar data langsung tersimpan
        )
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Error connecting to MySQL database: {e}")
        return None