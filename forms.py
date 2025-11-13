from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import InputRequired, NumberRange, DataRequired, Length, Regexp

class TesForm(FlaskForm):
    """
    Form untuk tes rekomendasi dengan validasi server-side.
    """
    nama = StringField('Nama Siswa', 
        validators=[DataRequired(message="Nama tidak boleh kosong.")])

    nisn = StringField('NISN (Nomor Induk Siswa Nasional)',
        validators=[
            DataRequired(message="NISN tidak boleh kosong."),
            Length(min=10, max=10, message="NISN harus 10 digit."),
            Regexp('^[0-9]+$', message="NISN hanya boleh berisi angka.")
        ])
    
    mtk = FloatField('Matematika', 
        validators=[
            InputRequired(message="Nilai tidak boleh kosong."), 
            NumberRange(min=0, max=100, message="Nilai harus antara 0 dan 100.")
        ])
    bindo = FloatField('Bahasa Indonesia', 
        validators=[
            InputRequired(message="Nilai tidak boleh kosong."), 
            NumberRange(min=0, max=100, message="Nilai harus antara 0 dan 100.")
        ])
    bing = FloatField('Bahasa Inggris', 
        validators=[
            InputRequired(message="Nilai tidak boleh kosong."), 
            NumberRange(min=0, max=100, message="Nilai harus antara 0 dan 100.")
        ])
    ipa_ips = FloatField('IPA / IPS', 
        validators=[
            InputRequired(message="Nilai tidak boleh kosong."), 
            NumberRange(min=0, max=100, message="Nilai harus antara 0 dan 100.")
        ])

    minat_logika = FloatField('Logika / Analisis', 
        validators=[
            InputRequired(message="Minat tidak boleh kosong."), 
            NumberRange(min=1, max=5, message="Minat harus antara 1 dan 5.")
        ])
    minat_sosial = FloatField('Sosial / Komunikasi', 
        validators=[
            InputRequired(message="Minat tidak boleh kosong."), 
            NumberRange(min=1, max=5, message="Minat harus antara 1 dan 5.")
        ])
    minat_kreatif = FloatField('Kreatif / Desain', 
        validators=[
            InputRequired(message="Minat tidak boleh kosong."), 
            NumberRange(min=1, max=5, message="Minat harus antara 1 dan 5.")
        ])
    minat_bahasa = FloatField('Bahasa / Literasi', 
        validators=[
            InputRequired(message="Minat tidak boleh kosong."), 
            NumberRange(min=1, max=5, message="Minat harus antara 1 dan 5.")
        ])

    submit = SubmitField('🔍 Lihat Hasil')