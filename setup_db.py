import mysql.connector

def create_table():
    try:
        # 1. Koneksi ke Database 'sistem_pakar'
        print("🔌 Menghubungkan ke Database sistem_pakar...")
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sistem_pakar"  # <--- Sesuai nama DB kamu
        )
        cursor = conn.cursor()

        # 2. Hapus tabel lama jika ada (biar bersih)
        print("🗑️  Membersihkan tabel lama...")
        cursor.execute("DROP TABLE IF EXISTS siswa")
        cursor.execute("DROP TABLE IF EXISTS siswa_new")

        # 3. Buat Tabel Baru (Struktur Kurikulum Merdeka)
        print("🔨 Membuat tabel baru (siswa_new)...")
        query = """
        CREATE TABLE siswa_new (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nisn VARCHAR(20),
            nama VARCHAR(100),
            mtk FLOAT,
            bindo FLOAT,
            bing FLOAT,
            sains FLOAT,
            sosial FLOAT,
            log INT,
            sos INT,
            kre INT,
            bah INT,
            hasil TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(query)

        conn.commit()
        print("✅ SUKSES! Tabel 'siswa_new' berhasil dibuat.")
        print("   Sekarang aplikasi siap dijalankan.")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"❌ ERROR: {err}")
        print("   Pastikan XAMPP sudah nyala dan nama database 'sistem_pakar' sudah dibuat di phpMyAdmin.")

if __name__ == "__main__":
    create_table()