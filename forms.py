from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class TesMinatForm(FlaskForm):
    nama = StringField('Nama Lengkap', validators=[DataRequired()])
    nisn = StringField('NISN', validators=[DataRequired(), Length(min=5, max=20)])

    mtk = IntegerField('Matematika (Wajib)', validators=[NumberRange(0, 100)])
    bindo = IntegerField('B. Indonesia', validators=[NumberRange(0, 100)])
    bing = IntegerField('B. Inggris', validators=[NumberRange(0, 100)])

    # INPUT BARU: RATA-RATA RUMPUN
    nilai_sains = IntegerField('Rata-rata Mapel Sains (Fisika/Kimia/Biologi)', 
                               validators=[NumberRange(0, 100)], default=0)
    
    nilai_sosial = IntegerField('Rata-rata Mapel Sosial (Eko/Sos/Geo)', 
                                validators=[NumberRange(0, 100)], default=0)

    minat_logika = IntegerField('Minat Logika', validators=[NumberRange(1, 5)], default=3)
    minat_sosial = IntegerField('Minat Sosial', validators=[NumberRange(1, 5)], default=3)
    minat_kreatif = IntegerField('Minat Kreatif', validators=[NumberRange(1, 5)], default=3)
    minat_bahasa = IntegerField('Minat Bahasa', validators=[NumberRange(1, 5)], default=3)

    submit = SubmitField('Lihat Rekomendasi')