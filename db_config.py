import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

# Konfigurasi Database & Pool
# Pool name dan size penting untuk manajemen koneksi
db_config = {
    "host": os.getenv('DB_HOST'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "database": os.getenv('DB_NAME'),
    "pool_name": "mypool",
    "pool_size": 10,          # Menyiapkan 10 koneksi standby
    "pool_reset_session": True
}

# Variabel global untuk menampung pool
cnx_pool = None

def init_pool():
    """Inisialisasi pool koneksi hanya sekali"""
    global cnx_pool
    try:
        cnx_pool = mysql.connector.pooling.MySQLConnectionPool(**db_config)
        print("✅ Database Connection Pool created successfully")
    except mysql.connector.Error as e:
        print(f"❌ Error creating connection pool: {e}")
        cnx_pool = None

# Panggil inisialisasi saat file di-load
if not cnx_pool:
    init_pool()

def get_connection():
    """
    Mengambil koneksi dari pool yang sudah tersedia.
    Tidak membuat koneksi baru (handshake) dari nol.
    """
    global cnx_pool
    try:
        if cnx_pool:
            # Ambil koneksi dari pool
            connection = cnx_pool.get_connection()
            return connection
        else:
            # Coba init ulang jika pool belum ada (fallback)
            init_pool()
            if cnx_pool:
                return cnx_pool.get_connection()
            return None
    except mysql.connector.Error as e:
        print(f"Error getting connection from pool: {e}")
        return None