from flask import Flask, render_template, request, redirect, url_for, flash, session
from fuzzy_logic.profile_matching import hitung_rekomendasi
from forms import TesMinatForm
import mysql.connector
import os
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

app = Flask(__name__)

# 2. Ambil Secret Key dari .env
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'kunci_default_jika_env_gagal')

# --- FUNGSI KONEKSI DATABASE ---
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=3306 # Default port MySQL
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error Database: {err}")
        return None

# --- PUBLIC ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tentang')
def tentang():
    return render_template('tentang.html')

@app.route('/tes')
def tes():
    form = TesMinatForm()
    return render_template('tes.html', form=form)

@app.route('/hasil', methods=['POST'])
def hasil():
    form = TesMinatForm(request.form)
    
    if not form.validate():
        flash("Mohon lengkapi data dengan nilai yang valid!", "danger")
        return redirect(url_for('tes'))

    # Ambil data dari form
    data = {
        'nama': form.nama.data,
        'nisn': form.nisn.data,
        'mtk': float(form.mtk.data),
        'bindo': float(form.bindo.data),
        'bing': float(form.bing.data),
        'sains': float(form.nilai_sains.data),
        'sosial': float(form.nilai_sosial.data),
        'log': int(form.minat_logika.data),
        'sos': int(form.minat_sosial.data),
        'kre': int(form.minat_kreatif.data),
        'bah': int(form.minat_bahasa.data)
    }

    # Hitung Profile Matching
    rekomendasi, skor, confidence, details = hitung_rekomendasi(
        data['mtk'], data['bindo'], data['bing'], 
        data['sains'], data['sosial'], 
        data['log'], data['sos'], data['kre'], data['bah']
    )

    # Siapkan data untuk Chart
    minat_chart = {'logika': data['log'], 'sosial': data['sos'], 'kreatif': data['kre'], 'bahasa': data['bah']}

    # Simpan ke Database (Hanya create table jika belum ada, tidak tiap request)
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        # Format string hasil rekomendasi
        hasil_str = ", ".join([f"{jur} ({skor}%)" for jur, skor in rekomendasi])
        
        query = """
            INSERT INTO siswa_new 
            (nisn, nama, mtk, bindo, bing, sains, sosial, log, sos, kre, bah, hasil) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        val = (data['nisn'], data['nama'], data['mtk'], data['bindo'], data['bing'], 
               data['sains'], data['sosial'], data['log'], data['sos'], data['kre'], data['bah'], hasil_str)
        
        cursor.execute(query, val)
        conn.commit()
        cursor.close()
        conn.close()

    return render_template('hasil.html', nama=data['nama'], hasil=rekomendasi, skor=skor, 
                           confidence=confidence, details=details, minat=minat_chart)

# --- ADMIN ROUTES (DENGAN PROTEKSI) ---

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    # Jika sudah login, lempar langsung ke dashboard
    if session.get('admin_logged_in'):
        return redirect(url_for('admin'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Cek kredensial dari .env
        env_user = os.getenv('ADMIN_USERNAME')
        env_pass = os.getenv('ADMIN_PASSWORD')

        if username == env_user and password == env_pass:
            session['admin_logged_in'] = True
            flash('Berhasil login sebagai Admin!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Username atau Password salah!', 'danger')
            
    return render_template('login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Anda telah logout.', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    # Proteksi: Cek session
    if not session.get('admin_logged_in'):
        flash('Silakan login terlebih dahulu.', 'warning')
        return redirect(url_for('admin_login'))

    try:
        conn = get_db_connection()
        if not conn:
            return "Gagal koneksi database. Cek .env anda."
            
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM siswa_new ORDER BY id DESC")
        data_siswa = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin.html', data=data_siswa)
    except Exception as e:
        return f"Terjadi kesalahan: {e}"

@app.route('/hapus_siswa/<nisn>', methods=['POST'])
def hapus_siswa(nisn):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM siswa_new WHERE nisn = %s", (nisn,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Data siswa berhasil dihapus!', 'success')
    except Exception as e:
        flash(f'Gagal menghapus: {e}', 'danger')
    
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)