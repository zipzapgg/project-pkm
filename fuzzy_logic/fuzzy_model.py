import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# 1. Definisikan Variabel
mtk = ctrl.Antecedent(np.arange(0, 101, 1), 'mtk')
bindo = ctrl.Antecedent(np.arange(0, 101, 1), 'bindo')
bing = ctrl.Antecedent(np.arange(0, 101, 1), 'bing')

minat_logika = ctrl.Antecedent(np.arange(1, 6, 1), 'minat_logika')
minat_sosial = ctrl.Antecedent(np.arange(1, 6, 1), 'minat_sosial')
minat_kreatif = ctrl.Antecedent(np.arange(1, 6, 1), 'minat_kreatif')
minat_bahasa = ctrl.Antecedent(np.arange(1, 6, 1), 'minat_bahasa')

hasil = ctrl.Consequent(np.arange(0, 101, 1), 'hasil')

# 2. Membership Functions (Himpunan Fuzzy)
def set_membership_akademik(var):
    var['rendah'] = fuzz.trapmf(var.universe, [0, 0, 40, 55])
    var['sedang'] = fuzz.trimf(var.universe, [45, 65, 80])
    var['tinggi'] = fuzz.trapmf(var.universe, [75, 85, 100, 100])

for var in [mtk, bindo, bing]:
    set_membership_akademik(var)

def set_membership_minat(var):
    var['rendah'] = fuzz.trapmf(var.universe, [1, 1, 2, 3])
    var['sedang'] = fuzz.trimf(var.universe, [2, 3, 4])
    var['tinggi'] = fuzz.trapmf(var.universe, [3, 4, 5, 5])

for var in [minat_logika, minat_sosial, minat_kreatif, minat_bahasa]:
    set_membership_minat(var)

hasil['rendah'] = fuzz.trapmf(hasil.universe, [0, 0, 25, 45])
hasil['sedang'] = fuzz.trimf(hasil.universe, [35, 55, 75])
hasil['tinggi'] = fuzz.trapmf(hasil.universe, [65, 80, 100, 100])

# 3. Aturan Fuzzy (Diperbarui agar lebih lengkap)
rules = [
    # --- KELOMPOK 1: POSITIF (Sangat Cocok) ---
    ctrl.Rule(mtk['tinggi'] & minat_logika['tinggi'], hasil['tinggi']),
    ctrl.Rule(bindo['tinggi'] & minat_sosial['tinggi'], hasil['tinggi']),
    ctrl.Rule(bing['tinggi'] & minat_bahasa['tinggi'], hasil['tinggi']),
    ctrl.Rule(minat_kreatif['tinggi'] & bing['tinggi'], hasil['tinggi']),

    # --- KELOMPOK 2: MODERAT (Cukup Cocok) ---
    # Bakat tinggi tapi minat biasa aja -> Sedang
    ctrl.Rule(mtk['tinggi'] & minat_logika['sedang'], hasil['sedang']),
    ctrl.Rule(bindo['tinggi'] & minat_sosial['sedang'], hasil['sedang']),
    ctrl.Rule(bing['tinggi'] & minat_bahasa['sedang'], hasil['sedang']),
    
    # Minat tinggi tapi bakat biasa aja -> Sedang (Bisa dikejar dengan belajar)
    ctrl.Rule(mtk['sedang'] & minat_logika['tinggi'], hasil['sedang']),
    ctrl.Rule(bindo['sedang'] & minat_sosial['tinggi'], hasil['sedang']),
    ctrl.Rule(bing['sedang'] & minat_bahasa['tinggi'], hasil['sedang']),
    
    # Dua-duanya sedang
    ctrl.Rule(mtk['sedang'] & minat_logika['sedang'], hasil['sedang']),
    ctrl.Rule(bindo['sedang'] & minat_sosial['sedang'], hasil['sedang']),
    ctrl.Rule(bing['sedang'] & minat_bahasa['sedang'], hasil['sedang']),

    # --- KELOMPOK 3: KONFLIK (Kurang Cocok) ---
    # Nilai Tinggi tapi TIDAK MINAT -> Rendah (Jangan dipaksa)
    ctrl.Rule(mtk['tinggi'] & minat_logika['rendah'], hasil['rendah']),
    ctrl.Rule(bindo['tinggi'] & minat_sosial['rendah'], hasil['rendah']),
    ctrl.Rule(bing['tinggi'] & minat_bahasa['rendah'], hasil['rendah']),
    
    # Minat Tinggi tapi Nilai Jeblok -> Rendah (Realistis)
    ctrl.Rule(mtk['rendah'] & minat_logika['tinggi'], hasil['rendah']),
    ctrl.Rule(bindo['rendah'] & minat_sosial['tinggi'], hasil['rendah']),

    # --- KELOMPOK 4: NEGATIF (Tidak Cocok) ---
    ctrl.Rule(mtk['rendah'] & minat_logika['rendah'], hasil['rendah']),
    ctrl.Rule(bindo['rendah'] & minat_sosial['rendah'], hasil['rendah']),
    ctrl.Rule(bing['rendah'] & minat_bahasa['rendah'], hasil['rendah']),
    ctrl.Rule(minat_kreatif['rendah'], hasil['rendah']),
    
    # --- HYBRID (Manajemen, Arsitektur dll) ---
    ctrl.Rule(minat_logika['tinggi'] & minat_sosial['tinggi'], hasil['tinggi']),
    ctrl.Rule(minat_logika['tinggi'] & minat_kreatif['tinggi'], hasil['tinggi']),
]

sistem_ctrl = ctrl.ControlSystem(rules)

def evaluasi_jurusan(mtk_v, bindo_v, bing_v, peminatan,
                     min_log, min_sos, min_kre, min_bah,
                     bobot_akademik, bobot_minat, bobot_peminatan):

    sistem = ctrl.ControlSystemSimulation(sistem_ctrl)
    
    # Default score jika fuzzy gagal
    skor_fuzzy = 50 
    
    try:
        sistem.input['mtk'] = mtk_v
        sistem.input['bindo'] = bindo_v
        sistem.input['bing'] = bing_v
        sistem.input['minat_logika'] = min_log
        sistem.input['minat_sosial'] = min_sos
        sistem.input['minat_kreatif'] = min_kre
        sistem.input['minat_bahasa'] = min_bah
        
        sistem.compute()
        skor_fuzzy = sistem.output['hasil']
    except Exception as e:
        # Log error tapi jangan crash aplikasi
        print(f"Warning: Fuzzy compute error (Rules incomplete for this input): {e}")
        skor_fuzzy = 40 # Nilai aman (rendah) jika tidak masuk rules manapun

    # Hitung skor komponen lain
    nilai_akademik = {'mtk': mtk_v, 'bindo': bindo_v, 'bing': bing_v}
    skor_akademik = sum(nilai_akademik[k] * bobot_akademik.get(k, 0) for k in nilai_akademik.keys())

    nilai_minat = {'logika': min_log, 'sosial': min_sos, 'kreatif': min_kre, 'bahasa': min_bah}
    skor_minat = sum((nilai_minat[k] / 5.0) * 100 * bobot_minat.get(k, 0) for k in nilai_minat.keys())

    skor_peminatan = bobot_peminatan.get(peminatan, 0) * 100

    # Bobot Akhir: Fuzzy (35%) + Akademik (25%) + Minat (25%) + Peminatan (15%)
    skor_final = (0.35 * skor_fuzzy) + (0.25 * skor_akademik) + (0.25 * skor_minat) + (0.15 * skor_peminatan)
    return round(skor_final, 2)

def hitung_rekomendasi(mtk_v, bindo_v, bing_v, peminatan,
                       min_log, min_sos, min_kre, min_bah):
    
    # Konfigurasi Bobot tiap Jurusan
    jurusan_config = {
        "Teknik Informatika": {
            'akademik': {'mtk': 0.5, 'bing': 0.3, 'bindo': 0.2},
            'minat': {'logika': 0.7, 'kreatif': 0.2, 'sosial': 0.1},
            'peminatan': {'MIPA': 1.0, 'IPS': 0.3, 'Bahasa': 0.2, 'Vokasi': 0.6}
        },
        "Sistem Informasi": {
            'akademik': {'mtk': 0.4, 'bindo': 0.3, 'bing': 0.3},
            'minat': {'logika': 0.5, 'sosial': 0.3, 'kreatif': 0.2},
            'peminatan': {'MIPA': 0.9, 'IPS': 0.6, 'Bahasa': 0.3, 'Vokasi': 0.5}
        },
        "Ilmu Komunikasi": {
            'akademik': {'bindo': 0.4, 'bing': 0.4, 'mtk': 0.2},
            'minat': {'sosial': 0.6, 'bahasa': 0.3, 'kreatif': 0.1},
            'peminatan': {'MIPA': 0.2, 'IPS': 1.0, 'Bahasa': 0.8, 'Vokasi': 0.4}
        },
        "Psikologi": {
            'akademik': {'bindo': 0.4, 'bing': 0.3, 'mtk': 0.3},
            'minat': {'sosial': 0.7, 'logika': 0.2, 'bahasa': 0.1},
            'peminatan': {'MIPA': 0.5, 'IPS': 1.0, 'Bahasa': 0.6, 'Vokasi': 0.3}
        },
        "Desain Komunikasi Visual": {
            'akademik': {'bing': 0.3, 'bindo': 0.3, 'mtk': 0.4},
            'minat': {'kreatif': 0.7, 'logika': 0.2, 'bahasa': 0.1},
            'peminatan': {'MIPA': 0.4, 'IPS': 0.5, 'Bahasa': 0.6, 'Vokasi': 1.0}
        },
        "Sastra Inggris": {
            'akademik': {'bing': 0.6, 'bindo': 0.3, 'mtk': 0.1},
            'minat': {'bahasa': 0.7, 'kreatif': 0.2, 'sosial': 0.1},
            'peminatan': {'MIPA': 0.2, 'IPS': 0.6, 'Bahasa': 1.0, 'Vokasi': 0.3}
        },
        "Sastra Indonesia": {
            'akademik': {'bindo': 0.6, 'bing': 0.2, 'mtk': 0.2},
            'minat': {'bahasa': 0.6, 'kreatif': 0.3, 'sosial': 0.1},
            'peminatan': {'MIPA': 0.2, 'IPS': 0.7, 'Bahasa': 1.0, 'Vokasi': 0.3}
        },
        "Manajemen": {
            'akademik': {'mtk': 0.3, 'bindo': 0.3, 'bing': 0.4},
            'minat': {'logika': 0.4, 'sosial': 0.4, 'kreatif': 0.2},
            'peminatan': {'MIPA': 0.5, 'IPS': 1.0, 'Bahasa': 0.4, 'Vokasi': 0.6}
        },
        "Arsitektur": {
            'akademik': {'mtk': 0.4, 'bing': 0.3, 'bindo': 0.3},
            'minat': {'kreatif': 0.5, 'logika': 0.4, 'sosial': 0.1},
            'peminatan': {'MIPA': 0.8, 'IPS': 0.4, 'Bahasa': 0.3, 'Vokasi': 0.9}
        },
        "Pendidikan Guru (PGSD)": {
            'akademik': {'bindo': 0.35, 'mtk': 0.35, 'bing': 0.3},
            'minat': {'sosial': 0.5, 'bahasa': 0.3, 'logika': 0.1, 'kreatif': 0.1},
            'peminatan': {'MIPA': 0.5, 'IPS': 0.8, 'Bahasa': 0.9, 'Vokasi': 0.6}
        }
    }

    hasil_evaluasi = []
    for jurusan, config in jurusan_config.items():
        skor = evaluasi_jurusan(
            mtk_v, bindo_v, bing_v, peminatan,
            min_log, min_sos, min_kre, min_bah,
            config['akademik'],
            config['minat'],
            config['peminatan']
        )
        hasil_evaluasi.append((jurusan, skor))

    # Urutkan dari skor tertinggi
    hasil_evaluasi = sorted(hasil_evaluasi, key=lambda x: x[1], reverse=True)
    
    top3 = hasil_evaluasi[:3]
    skor_rata = float(np.mean([x[1] for x in top3]))

    return top3, skor_rata