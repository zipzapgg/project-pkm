import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_database_if_not_exists():
    try:
        print("🔌 Menghubungkan ke MySQL Server...")
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        cursor = conn.cursor()
        
        db_name = os.getenv('DB_NAME', 'sistem_pakar')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"✅ Database '{db_name}' siap!")
        
        cursor.close()
        conn.close()
        return True
    except Error as err:
        print(f"❌ ERROR saat membuat database: {err}")
        return False

def create_table():
    try:
        if not create_database_if_not_exists():
            return
        
        print(f"\n🔌 Menghubungkan ke Database {os.getenv('DB_NAME', 'sistem_pakar')}...")
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'sistem_pakar')
        )
        cursor = conn.cursor()

        print("🗑️  Membersihkan tabel lama...")
        cursor.execute("DROP TABLE IF EXISTS siswa")
        cursor.execute("DROP TABLE IF EXISTS siswa_new")

        print("🔨 Membuat tabel baru (siswa_new)...")
        query = """
        CREATE TABLE siswa_new (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nisn VARCHAR(20) NOT NULL,
            nama VARCHAR(100) NOT NULL,
            mtk FLOAT NOT NULL,
            bindo FLOAT NOT NULL,
            bing FLOAT NOT NULL,
            sains FLOAT DEFAULT 0,
            sosial FLOAT DEFAULT 0,
            log INT NOT NULL,
            sos INT NOT NULL,
            kre INT NOT NULL,
            bah INT NOT NULL,
            hasil TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_nisn (nisn),
            INDEX idx_timestamp (timestamp)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        cursor.execute(query)

        conn.commit()
        print("\n" + "="*60)
        print("✅ SUKSES! Tabel 'siswa_new' berhasil dibuat.")
        print("="*60)
        print("\n📋 Struktur tabel:")
        print("   - id (Primary Key)")
        print("   - nisn, nama")
        print("   - mtk, bindo, bing (Wajib)")
        print("   - sains, sosial (Pilihan)")
        print("   - log, sos, kre, bah (Minat)")
        print("   - hasil (Rekomendasi)")
        print("   - timestamp")
        print("\n🚀 Sekarang aplikasi siap dijalankan dengan: python app.py")

        cursor.close()
        conn.close()

    except Error as err:
        print(f"\n❌ ERROR: {err}")
        print("\n💡 Troubleshooting:")
        print("   1. Pastikan XAMPP/MySQL sudah running")
        print("   2. Cek file .env untuk konfigurasi database")
        print("   3. Pastikan user MySQL punya privilege CREATE TABLE")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("   SETUP DATABASE - SISTEM PAKAR REKOMENDASI JURUSAN")
    print("="*60 + "\n")
    create_table()