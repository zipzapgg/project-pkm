from flask import Flask, render_template, request, redirect, url_for, flash
from db_config import get_connection
from fuzzy_logic.fuzzy_model import hitung_rekomendasi

app = Flask(__name__)
app.secret_key = 'rahasia123'

# ================= ROUTING UTAMA =================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tes')
def tes():
    return render_template('tes.html')

@app.route('/tentang')
def tentang():
    return render_template('tentang.html')

@app.route('/kontak')
def kontak():
    return render_template('kontak.html')

# ================= HASIL TES =================
@app.route('/hasil', methods=['GET', 'POST'])
def hasil():
    if request.method == 'GET':
        return redirect(url_for('tes'))

    try:
        nama = request.form.get('nama', '').strip()
        mtk = float(request.form.get('mtk', 0))
        bindo = float(request.form.get('bindo', 0))
        bing = float(request.form.get('bing', 0))
        ipa_ips = float(request.form.get('ipa_ips', 0))
        minat_logika = float(request.form.get('minat_logika', 0))
        minat_sosial = float(request.form.get('minat_sosial', 0))
        minat_kreatif = float(request.form.get('minat_kreatif', 0))
        minat_bahasa = float(request.form.get('minat_bahasa', 0))

        if not nama:
            flash("Nama tidak boleh kosong!", "error")
            return redirect(url_for('tes'))

        # Panggil fuzzy logic
        hasil_rekomendasi, skor = hitung_rekomendasi(
            mtk, bindo, bing, ipa_ips,
            minat_logika, minat_sosial, minat_kreatif, minat_bahasa
        )

        # Simpan ke database (jika server aktif)
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO siswa (nama, nilai_mtk, nilai_bhs, nilai_ipa, nilai_ips,
                                   minat_logika, minat_sosial, minat_kreatif, hasil_jurusan)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                nama, mtk, bindo, ipa_ips, 0,
                minat_logika, minat_sosial, minat_kreatif,
                hasil_rekomendasi[0][0]
            ))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print("⚠️ Database error (dilewati):", e)

        return render_template('hasil.html', nama=nama, hasil=hasil_rekomendasi, skor=skor)

    except Exception as e:
        print("Terjadi kesalahan:", e)
        flash("Pastikan semua kolom sudah diisi dengan benar!", "error")
        return redirect(url_for('tes'))

# ================= HALAMAN ADMIN =================
@app.route('/admin')
def admin():
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM siswa ORDER BY id DESC")
        data_siswa = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('admin.html', data=data_siswa)
    except Exception as e:
        print("⚠️ Database error:", e)
        flash("Gagal memuat data siswa!", "error")
        return redirect(url_for('index'))

# ================= MAIN =================
if __name__ == '__main__':
    app.run(debug=True)
