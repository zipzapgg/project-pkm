import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# === 1. DEFINISI VARIABEL FUZZY ===
# Input Generik (Bisa dipakai untuk mapel apapun)
nilai_relevan = ctrl.Antecedent(np.arange(0, 101, 1), 'nilai_relevan')
nilai_pendukung = ctrl.Antecedent(np.arange(0, 101, 1), 'nilai_pendukung')
minat_relevan = ctrl.Antecedent(np.arange(1, 6, 1), 'minat_relevan')
# Output
hasil = ctrl.Consequent(np.arange(0, 101, 1), 'hasil')

# === 2. MEMBERSHIP FUNCTIONS ===
# Kurva Akademik
for var in [nilai_relevan, nilai_pendukung]:
    var['buruk'] = fuzz.trapmf(var.universe, [0, 0, 50, 60])
    var['cukup'] = fuzz.trimf(var.universe, [50, 70, 85])
    var['bagus'] = fuzz.trapmf(var.universe, [75, 85, 100, 100])

# Kurva Minat
minat_relevan['rendah'] = fuzz.trapmf(minat_relevan.universe, [1, 1, 2, 3])
minat_relevan['sedang'] = fuzz.trimf(minat_relevan.universe, [2, 3, 4])
minat_relevan['tinggi'] = fuzz.trapmf(minat_relevan.universe, [3, 4, 5, 5])

# Kurva Hasil
hasil['tidak_cocok'] = fuzz.trapmf(hasil.universe, [0, 0, 40, 50])
hasil['pertimbangkan'] = fuzz.trimf(hasil.universe, [40, 60, 80])
hasil['sangat_cocok'] = fuzz.trapmf(hasil.universe, [70, 85, 100, 100])

# === 3. ATURAN (RULES) ===
rules = [
    # Logika Murni Fuzzy
    ctrl.Rule(nilai_relevan['bagus'] & minat_relevan['tinggi'], hasil['sangat_cocok']),
    ctrl.Rule(nilai_relevan['bagus'] & nilai_pendukung['bagus'], hasil['sangat_cocok']),
    
    ctrl.Rule(nilai_relevan['bagus'] & minat_relevan['sedang'], hasil['sangat_cocok']),
    ctrl.Rule(nilai_relevan['cukup'] & minat_relevan['tinggi'], hasil['sangat_cocok']),
    
    ctrl.Rule(nilai_relevan['cukup'] & minat_relevan['sedang'], hasil['pertimbangkan']),
    ctrl.Rule(nilai_relevan['bagus'] & minat_relevan['rendah'], hasil['pertimbangkan']),
    
    ctrl.Rule(nilai_relevan['buruk'] & minat_relevan['tinggi'], hasil['pertimbangkan']),
    ctrl.Rule(nilai_relevan['cukup'] & minat_relevan['rendah'], hasil['tidak_cocok']),
    ctrl.Rule(nilai_relevan['buruk'], hasil['tidak_cocok']),
]

sistem_ctrl = ctrl.ControlSystem(rules)
simulasi = ctrl.ControlSystemSimulation(sistem_ctrl)

def hitung_rekomendasi(mtk, bindo, bing, peminatan, min_log, min_sos, min_kre, min_bah):
    # Data dictionary
    nilai = {'mtk': mtk, 'bindo': bindo, 'bing': bing}
    minat = {'logika': min_log, 'sosial': min_sos, 'kreatif': min_kre, 'bahasa': min_bah}

    # Konfigurasi Jurusan (Syarat Masuk)
    config_jurusan = {
        "Teknik Informatika":   {'u': 'mtk', 'd': 'bing', 'm': 'logika', 'p': ['MIPA', 'Vokasi']},
        "Sistem Informasi":     {'u': 'mtk', 'd': 'bindo', 'm': 'logika', 'p': ['MIPA', 'IPS']},
        "Bisnis Digital":       {'u': 'mtk', 'd': 'bing', 'm': 'sosial', 'p': ['IPS', 'MIPA']},
        "Arsitektur":           {'u': 'mtk', 'd': 'bing', 'm': 'kreatif', 'p': ['MIPA', 'Vokasi']},
        "Ilmu Hukum":           {'u': 'bindo', 'd': 'bing', 'm': 'sosial', 'p': ['IPS', 'Bahasa']},
        "Hubungan Internasional":{'u': 'bing', 'd': 'bindo', 'm': 'sosial', 'p': ['Bahasa', 'IPS']},
        "Ilmu Komunikasi":      {'u': 'bindo', 'd': 'bing', 'm': 'sosial', 'p': ['IPS', 'Bahasa']},
        "Psikologi":            {'u': 'bindo', 'd': 'mtk', 'm': 'sosial', 'p': ['IPS', 'MIPA']},
        "Kriminologi":          {'u': 'bindo', 'd': 'mtk', 'm': 'logika', 'p': ['IPS', 'MIPA']},
        "Administrasi Publik":  {'u': 'bindo', 'd': 'bing', 'm': 'sosial', 'p': ['IPS', 'Bahasa']},
        "Manajemen":            {'u': 'mtk', 'd': 'bing', 'm': 'sosial', 'p': ['IPS', 'MIPA']},
        "Akuntansi":            {'u': 'mtk', 'd': 'bindo', 'm': 'logika', 'p': ['IPS', 'MIPA']},
        "Ekonomi Pembangunan":  {'u': 'mtk', 'd': 'bing', 'm': 'logika', 'p': ['IPS', 'MIPA']},
        "Sastra Inggris":       {'u': 'bing', 'd': 'bindo', 'm': 'bahasa', 'p': ['Bahasa', 'IPS']},
        "Sastra Indonesia":     {'u': 'bindo', 'd': 'bing', 'm': 'bahasa', 'p': ['Bahasa', 'IPS']},
        "Sastra Jepang":        {'u': 'bing', 'd': 'bindo', 'm': 'bahasa', 'p': ['Bahasa', 'IPS']},
        "DKV":                  {'u': 'bing', 'd': 'mtk', 'm': 'kreatif', 'p': ['Vokasi', 'IPS', 'MIPA']},
        "PGSD":                 {'u': 'bindo', 'd': 'mtk', 'm': 'sosial', 'p': ['IPS', 'Bahasa']}
    }

    hasil_akhir = []

    for jur, cfg in config_jurusan.items():
        # 1. Hitung Fuzzy Score
        try:
            simulasi.input['nilai_relevan'] = nilai[cfg['u']]
            simulasi.input['nilai_pendukung'] = nilai[cfg['d']]
            simulasi.input['minat_relevan'] = minat[cfg['m']]
            simulasi.compute()
            skor = simulasi.output['hasil']
        except:
            skor = 0
            
        # 2. Contextual Penalty (Lintas Jurusan)
        if peminatan not in cfg['p']:
            skor = max(0, skor - 10)

        # 3. Tie-Breaker (Hitung Nilai Mentah untuk memecah nilai kembar)
        raw_score = nilai[cfg['u']] + nilai[cfg['d']] + (minat[cfg['m']] * 20)
        
        hasil_akhir.append((jur, round(skor, 1), raw_score))

    # Sort: Prioritas Fuzzy, lalu Raw Score
    hasil_akhir.sort(key=lambda x: (x[1], x[2]), reverse=True)
    
    top3 = [(x[0], x[1]) for x in hasil_akhir[:3]]
    rata = float(np.mean([x[1] for x in top3])) if top3 else 0
    
    return top3, rata