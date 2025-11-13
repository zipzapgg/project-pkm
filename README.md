# 🎓 Sistem Pakar Rekomendasi Jurusan Kuliah

Sistem rekomendasi jurusan kuliah berbasis **Fuzzy Logic** untuk membantu siswa SMA menentukan pilihan jurusan yang sesuai dengan kemampuan akademik dan minat pribadi.

## ✨ Fitur Utama

- 🧠 **Fuzzy Logic Engine** - Analisis cerdas menggunakan scikit-fuzzy
- 🎯 **10 Jurusan** - Rekomendasi dari berbagai bidang (IT, Bisnis, Bahasa, Seni, dll)
- 📊 **Visualisasi Data** - Chart radar untuk profil minat siswa
- 💾 **Database MySQL** - Penyimpanan hasil tes siswa
- 🔐 **Admin Panel** - Dashboard admin dengan Basic Authentication
- 📱 **Responsive Design** - Tampilan modern dan mobile-friendly

## 🚀 Teknologi yang Digunakan

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Fuzzy Logic**: scikit-fuzzy, numpy
- **Frontend**: Bootstrap 5, Chart.js
- **Styling**: Custom CSS dengan Glassmorphism
- **Deployment**: PythonAnywhere

## 📋 Prasyarat

- Python 3.8+
- MySQL Server
- pip (Python package manager)

## 🛠️ Instalasi

### 1. Clone Repository

```bash
git clone <repository-url>
cd sistem-pakar-jurusan
```

### 2. Buat Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Database

Buat database MySQL:

```sql
CREATE DATABASE sistem_pakar_jurusan;

USE sistem_pakar_jurusan;

CREATE TABLE siswa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nisn VARCHAR(10) UNIQUE NOT NULL,
    nama VARCHAR(100) NOT NULL,
    nilai_mtk FLOAT NOT NULL,
    nilai_bhs FLOAT NOT NULL,
    nilai_bing FLOAT NOT NULL,
    nilai_ipa FLOAT NOT NULL,
    minat_logika INT NOT NULL,
    minat_sosial INT NOT NULL,
    minat_kreatif INT NOT NULL,
    minat_bahasa INT NOT NULL,
    hasil_jurusan TEXT NOT NULL,
    waktu_tes TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Konfigurasi Environment Variables

Buat file `.env` di root project:

```env
FLASK_SECRET_KEY=your_secret_key_here
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=sistem_pakar_jurusan
DB_PORT=3306
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_admin_password
```

### 6. Jalankan Aplikasi

```bash
python app.py
```

Buka browser dan akses: `http://127.0.0.1:5000`

## 📁 Struktur Project

```
sistem-pakar-jurusan/
├── app.py                  # Main application file
├── db_config.py           # Database configuration
├── forms.py               # WTForms validation
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (gitignored)
├── .gitignore            # Git ignore rules
│
├── fuzzy_logic/
│   └── fuzzy_model.py    # Fuzzy logic implementation
│
├── static/
│   ├── css/
│   │   └── style.css     # Custom styling
│   └── img/
│       └── fuzzy_icon.png
│
└── templates/
    ├── base.html          # Base template
    ├── index.html         # Homepage
    ├── tes.html           # Test form
    ├── hasil.html         # Result page
    ├── admin.html         # Admin dashboard
    └── tentang.html       # About page
```

## 🎯 Cara Menggunakan

### Untuk Siswa:

1. **Akses Halaman Tes** - Klik "Mulai Tes Sekarang"
2. **Isi Data Diri** - Nama dan NISN (10 digit)
3. **Input Nilai Akademik** - Masukkan nilai 4 mata pelajaran (0-100)
4. **Tentukan Minat** - Geser slider minat di 4 kategori (1-5)
5. **Lihat Hasil** - Sistem akan menampilkan top 3 jurusan rekomendasi

### Untuk Admin:

1. Akses `/admin` di browser
2. Login menggunakan kredensial admin dari `.env`
3. Lihat data siswa yang telah mengikuti tes
4. (Opsional) Export data ke CSV

## 🔧 Konfigurasi Fuzzy Logic

Sistem menggunakan 3 membership function:
- **Rendah**: Nilai/minat rendah
- **Sedang**: Nilai/minat menengah
- **Tinggi**: Nilai/minat tinggi

Perhitungan skor akhir:
```
Skor Final = (40% × Fuzzy Score) + (30% × Academic Score) + (30% × Interest Score)
```

## 🎓 Jurusan yang Tersedia

1. 💻 Teknik Informatika
2. 📊 Sistem Informasi
3. 📢 Ilmu Komunikasi
4. 🧠 Psikologi
5. 🎨 Desain Komunikasi Visual
6. 📚 Sastra Inggris
7. 📖 Sastra Indonesia
8. 💼 Manajemen
9. 🏗️ Arsitektur
10. 👨‍🏫 Pendidikan Guru (PGSD)

## 🚢 Deployment ke PythonAnywhere

1. Upload semua file kecuali `venv/` dan `.env`
2. Buat file `.env` baru di PythonAnywhere dengan kredensial production
3. Install dependencies: `pip install -r requirements.txt`
4. Setup database MySQL di PythonAnywhere
5. Konfigurasi WSGI file sesuai dokumentasi PythonAnywhere
6. Reload web app

## 🔒 Keamanan

- ✅ CSRF Protection dengan Flask-WTF
- ✅ Basic Authentication untuk admin panel
- ✅ Environment variables untuk kredensial sensitif
- ✅ Input validation (server-side & client-side)
- ✅ SQL Injection prevention dengan parameterized queries

## 📝 License

© 2025 Kelompok PKM 05TPLP032 — Universitas Pamulang

## 👥 Tim Pengembang

Program Kreativitas Mahasiswa (PKM) - Pengabdian kepada Masyarakat
Universitas Pamulang

---

**Catatan**: Sistem ini dikembangkan untuk keperluan akademik dan pengabdian kepada masyarakat di SMAN 6 Kabupaten Tangerang.
