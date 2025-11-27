from flask import Flask, render_template, request, redirect, url_for, flash
from fuzzy_logic.profile_matching import hitung_rekomendasi
from forms import TesMinatForm
import mysql.connector
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kuncirahasia123'

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sistem_pakar"
    )

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
        flash("Mohon lengkapi data dengan nilai angka (0-100) yang valid!", "danger")
        return redirect(url_for('tes'))

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

    rekomendasi, skor, confidence, details = hitung_rekomendasi(
        data['mtk'], data['bindo'], data['bing'], 
        data['sains'], data['sosial'], 
        data['log'], data['sos'], data['kre'], data['bah']
    )

    minat_chart = {
        'logika': data['log'], 
        'sosial': data['sos'], 
        'kreatif': data['kre'], 
        'bahasa': data['bah']
    }

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS siswa_new (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nisn VARCHAR(20),
            nama VARCHAR(100),
            mtk FLOAT, bindo FLOAT, bing FLOAT, 
            sains FLOAT, sosial FLOAT,
            log INT, sos INT, kre INT, bah INT,
            hasil TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
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

    return render_template('hasil.html', 
                            nama=data['nama'],
                            hasil=rekomendasi,
                            skor=skor,
                            confidence=confidence,
                            details=details,
                            minat=minat_chart)

@app.route('/admin')
def admin():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM siswa_new ORDER BY id DESC")
        data_siswa = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin.html', data=data_siswa)
    except Exception as e:
        return f"Gagal koneksi database: {e}"

@app.route('/hapus_siswa/<nisn>', methods=['POST'])
def hapus_siswa(nisn):
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