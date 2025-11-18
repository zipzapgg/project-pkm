import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from flask_basicauth import BasicAuth
from db_config import get_connection
from fuzzy_logic.fuzzy_model import hitung_rekomendasi
from forms import TesForm
from mysql.connector import Error as MySQLError

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['BASIC_AUTH_USERNAME'] = os.getenv('ADMIN_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.getenv('ADMIN_PASSWORD')

auth = BasicAuth(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tes')
def tes():
    form = TesForm()
    return render_template('tes.html', form=form)

@app.route('/tentang')
def tentang():
    return render_template('tentang.html')

@app.route('/hasil', methods=['GET', 'POST'])
def hasil():
    if request.method == 'GET':
        return redirect(url_for('tes'))

    form = TesForm()

    if form.validate_on_submit():
        try:
            nama = form.nama.data
            nisn = form.nisn.data
            mtk = form.mtk.data
            bindo = form.bindo.data
            bing = form.bing.data
            peminatan = form.peminatan.data
            minat_logika = form.minat_logika.data
            minat_sosial = form.minat_sosial.data
            minat_kreatif = form.minat_kreatif.data
            minat_bahasa = form.minat_bahasa.data

            # Perubahan: IPA/IPS diganti peminatan
            hasil_rekomendasi, skor = hitung_rekomendasi(
                mtk, bindo, bing, peminatan,
                minat_logika, minat_sosial, minat_kreatif, minat_bahasa
            )

            data_minat = {
                'logika': minat_logika,
                'sosial': minat_sosial,
                'kreatif': minat_kreatif,
                'bahasa': minat_bahasa
            }

            top_3_list = [f"{idx+1}. {jurusan}" for idx, (jurusan, nilai) in enumerate(hasil_rekomendasi)]
            hasil_string = ", ".join(top_3_list)

            conn = None
            try:
                conn = get_connection()
                if conn:
                    cur = conn.cursor()

                    sql_query = """
                        INSERT INTO siswa (nisn, nama, nilai_mtk, nilai_bhs, nilai_bing, peminatan,
                                           minat_logika, minat_sosial, minat_kreatif, minat_bahasa, hasil_jurusan)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

                    sql_values = (
                        nisn, nama, mtk, bindo, bing, peminatan,
                        minat_logika, minat_sosial, minat_kreatif, minat_bahasa, hasil_string
                    )

                    cur.execute(sql_query, sql_values)
                    conn.commit()
                    cur.close()

            except MySQLError as e:
                if e.errno == 1062:
                    flash(f"NISN '{nisn}' sudah terdaftar.", "danger")
                    return redirect(url_for('tes'))
                else:
                    flash(f"Terjadi error database: {e}", "danger")
                    return redirect(url_for('tes'))
            finally:
                if conn:
                    conn.close()

            return render_template('hasil.html',
                                   nama=nama,
                                   hasil=hasil_rekomendasi,
                                   skor=skor,
                                   minat=data_minat)

        except Exception as e:
            print(f"Terjadi kesalahan non-DB: {e}")
            flash(f"Kesalahan internal: {e}", "error")
            return redirect(url_for('tes'))

    else:
        flash("Input tidak valid. Periksa kembali.", "error")
        return render_template('tes.html', form=form)

@app.route('/admin')
@auth.required
def admin():
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT nisn, nama, nilai_mtk, nilai_bhs, nilai_bing, peminatan,
                   minat_logika, minat_sosial, minat_kreatif, minat_bahasa, hasil_jurusan
            FROM siswa 
            ORDER BY waktu_tes DESC
        """)
        data_siswa = cur.fetchall()
        cur.close()
        return render_template('admin.html', data=data_siswa)

    except Exception as e:
        flash(f"Gagal memuat data siswa: {e}", "error")
        return redirect(url_for('index'))
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
