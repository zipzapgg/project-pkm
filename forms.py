from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError
import re

def validate_nisn(form, field):
    if not re.match(r'^\d{5,20}$', field.data):
        raise ValidationError('NISN harus berupa angka 5-20 digit')

class TesMinatForm(FlaskForm):
    nama = StringField('Nama Lengkap', validators=[
        DataRequired(message="Nama wajib diisi"),
        Length(min=3, max=100, message="Nama harus 3-100 karakter")
    ])
    
    nisn = StringField('NISN', validators=[
        DataRequired(message="NISN wajib diisi"),
        Length(min=5, max=20, message="NISN harus 5-20 karakter"),
        validate_nisn
    ])

    mtk = IntegerField('Matematika (Wajib)', validators=[
        DataRequired(message="Nilai Matematika wajib diisi"),
        NumberRange(min=0, max=100, message="Nilai harus 0-100")
    ])
    
    bindo = IntegerField('B. Indonesia', validators=[
        DataRequired(message="Nilai B. Indonesia wajib diisi"),
        NumberRange(min=0, max=100, message="Nilai harus 0-100")
    ])
    
    bing = IntegerField('B. Inggris', validators=[
        DataRequired(message="Nilai B. Inggris wajib diisi"),
        NumberRange(min=0, max=100, message="Nilai harus 0-100")
    ])

    nilai_sains = IntegerField('Rata-rata Mapel Sains (Fisika/Kimia/Biologi)', 
                               validators=[
                                   NumberRange(min=0, max=100, message="Nilai harus 0-100")
                               ], 
                               default=0)
    
    nilai_sosial = IntegerField('Rata-rata Mapel Sosial (Eko/Sos/Geo)', 
                                validators=[
                                    NumberRange(min=0, max=100, message="Nilai harus 0-100")
                                ], 
                                default=0)

    minat_logika = IntegerField('Minat Logika', validators=[
        NumberRange(min=1, max=5, message="Minat harus 1-5")
    ], default=3)
    
    minat_sosial = IntegerField('Minat Sosial', validators=[
        NumberRange(min=1, max=5, message="Minat harus 1-5")
    ], default=3)
    
    minat_kreatif = IntegerField('Minat Kreatif', validators=[
        NumberRange(min=1, max=5, message="Minat harus 1-5")
    ], default=3)
    
    minat_bahasa = IntegerField('Minat Bahasa', validators=[
        NumberRange(min=1, max=5, message="Minat harus 1-5")
    ], default=3)

    submit = SubmitField('Lihat Rekomendasi')