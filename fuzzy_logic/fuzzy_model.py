import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

mtk = ctrl.Antecedent(np.arange(0, 101, 1), 'mtk')
bindo = ctrl.Antecedent(np.arange(0, 101, 1), 'bindo')
bing = ctrl.Antecedent(np.arange(0, 101, 1), 'bing')
ipa_ips = ctrl.Antecedent(np.arange(0, 101, 1), 'ipa_ips')

minat_logika = ctrl.Antecedent(np.arange(1, 6, 1), 'minat_logika')
minat_sosial = ctrl.Antecedent(np.arange(1, 6, 1), 'minat_sosial')
minat_kreatif = ctrl.Antecedent(np.arange(1, 6, 1), 'minat_kreatif')
minat_bahasa = ctrl.Antecedent(np.arange(1, 6, 1), 'minat_bahasa')

hasil = ctrl.Consequent(np.arange(0, 101, 1), 'hasil')

def set_membership_akademik(var):
    var['rendah'] = fuzz.trapmf(var.universe, [0, 0, 40, 55])
    var['sedang'] = fuzz.trimf(var.universe, [45, 65, 80])
    var['tinggi'] = fuzz.trapmf(var.universe, [75, 85, 100, 100])

for var in [mtk, bindo, bing, ipa_ips]:
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

rules = [
    # LOGIKA & TEKNIK
    ctrl.Rule(mtk['tinggi'] & minat_logika['tinggi'], hasil['tinggi']),
    ctrl.Rule(ipa_ips['tinggi'] & minat_logika['tinggi'], hasil['tinggi']),
    ctrl.Rule(mtk['tinggi'] & minat_logika['sedang'], hasil['sedang']),
    ctrl.Rule(mtk['sedang'] & minat_logika['tinggi'], hasil['sedang']),
    ctrl.Rule(mtk['sedang'] & minat_logika['sedang'], hasil['sedang']),

    # SOSIAL & KOMUNIKASI
    ctrl.Rule(bindo['tinggi'] & minat_sosial['tinggi'], hasil['tinggi']),
    ctrl.Rule(bing['tinggi'] & minat_sosial['tinggi'], hasil['tinggi']),
    ctrl.Rule(ipa_ips['tinggi'] & minat_sosial['tinggi'], hasil['tinggi']),
    ctrl.Rule(bindo['sedang'] & minat_sosial['sedang'], hasil['sedang']),
    ctrl.Rule(bing['sedang'] & minat_sosial['sedang'], hasil['sedang']),

    # KREATIF & DESAIN
    ctrl.Rule(minat_kreatif['tinggi'] & bing['tinggi'], hasil['tinggi']),
    ctrl.Rule(minat_kreatif['tinggi'] & bindo['tinggi'], hasil['tinggi']),
    ctrl.Rule(minat_kreatif['sedang'] & bing['sedang'], hasil['sedang']),

    # BAHASA
    ctrl.Rule(minat_bahasa['tinggi'] & bing['tinggi'], hasil['tinggi']),
    ctrl.Rule(minat_bahasa['tinggi'] & bindo['tinggi'], hasil['tinggi']),
    ctrl.Rule(minat_bahasa['sedang'] & bing['sedang'], hasil['sedang']),

    # HYBRID (Manajemen, Arsitektur)
    ctrl.Rule(minat_logika['tinggi'] & minat_sosial['tinggi'], hasil['tinggi']),
    ctrl.Rule(minat_logika['tinggi'] & minat_kreatif['tinggi'], hasil['tinggi']),
    ctrl.Rule(minat_logika['sedang'] & minat_sosial['sedang'], hasil['sedang']),
    ctrl.Rule(minat_logika['sedang'] & minat_kreatif['sedang'], hasil['sedang']),

    # ATURAN NEGATIF / RENDAH (PENTING)
    ctrl.Rule(mtk['rendah'] & minat_logika['rendah'], hasil['rendah']),
    ctrl.Rule(bindo['rendah'] & minat_sosial['rendah'], hasil['rendah']),
    ctrl.Rule(bing['rendah'] & minat_bahasa['rendah'], hasil['rendah']),
    ctrl.Rule(minat_kreatif['rendah'], hasil['rendah']), 
    
    # DEFAULT RULES
    ctrl.Rule(mtk['rendah'] & bindo['rendah'] & bing['rendah'], hasil['rendah']),
]

sistem_ctrl = ctrl.ControlSystem(rules)

def evaluasi_jurusan(mtk_v, bindo_v, bing_v, ipa_ips_v,
                     min_log, min_sos, min_kre, min_bah,
                     bobot_akademik, bobot_minat):

    sistem = ctrl.ControlSystemSimulation(sistem_ctrl)
    
    try:
        sistem.input['mtk'] = mtk_v
        sistem.input['bindo'] = bindo_v
        sistem.input['bing'] = bing_v
        sistem.input['ipa_ips'] = ipa_ips_v
        sistem.input['minat_logika'] = min_log
        sistem.input['minat_sosial'] = min_sos
        sistem.input['minat_kreatif'] = min_kre
        sistem.input['minat_bahasa'] = min_bah
        sistem.compute()
        skor_fuzzy = sistem.output['hasil']
    except Exception as e:
        print(f"Error pada komputasi fuzzy: {e}")
        skor_fuzzy = 50

    nilai_akademik = {'mtk': mtk_v, 'bindo': bindo_v, 'bing': bing_v, 'ipa_ips': ipa_ips_v}
    skor_akademik = sum(nilai_akademik[k] * bobot_akademik.get(k, 0) for k in nilai_akademik.keys())

    nilai_minat = {'logika': min_log, 'sosial': min_sos, 'kreatif': min_kre, 'bahasa': min_bah}
    skor_minat = sum((nilai_minat[k] / 5.0) * 100 * bobot_minat.get(k, 0) for k in nilai_minat.keys())

    skor_final = (0.4 * skor_fuzzy) + (0.3 * skor_akademik) + (0.3 * skor_minat)
    return round(skor_final, 2)

def hitung_rekomendasi(mtk_v, bindo_v, bing_v, ipa_ips_v,
                       min_log, min_sos, min_kre, min_bah):
    """
    Menghitung rekomendasi jurusan berbasis fuzzy
    Return: (skor_umum, list of tuples (jurusan, skor))
    """
    jurusan_config = {
        "Teknik Informatika": {
            'akademik': {'mtk': 0.5, 'ipa_ips': 0.3, 'bing': 0.2},
            'minat': {'logika': 0.7, 'kreatif': 0.2, 'sosial': 0.1}
        },
        "Sistem Informasi": {
            'akademik': {'mtk': 0.4, 'ipa_ips': 0.3, 'bindo': 0.15, 'bing': 0.15},
            'minat': {'logika': 0.5, 'sosial': 0.3, 'kreatif': 0.2}
        },
        "Ilmu Komunikasi": {
            'akademik': {'bindo': 0.4, 'bing': 0.3, 'ipa_ips': 0.3},
            'minat': {'sosial': 0.6, 'bahasa': 0.3, 'kreatif': 0.1}
        },
        "Psikologi": {
            'akademik': {'ipa_ips': 0.4, 'bindo': 0.3, 'bing': 0.3},
            'minat': {'sosial': 0.7, 'logika': 0.2, 'bahasa': 0.1}
        },
        "Desain Komunikasi Visual": {
            'akademik': {'bing': 0.3, 'mtk': 0.2, 'bindo': 0.25, 'ipa_ips': 0.25},
            'minat': {'kreatif': 0.7, 'logika': 0.2, 'bahasa': 0.1}
        },
        "Sastra Inggris": {
            'akademik': {'bing': 0.6, 'bindo': 0.3, 'ipa_ips': 0.1},
            'minat': {'bahasa': 0.7, 'kreatif': 0.2, 'sosial': 0.1}
        },
        "Sastra Indonesia": {
            'akademik': {'bindo': 0.6, 'bing': 0.2, 'ipa_ips': 0.2},
            'minat': {'bahasa': 0.6, 'kreatif': 0.3, 'sosial': 0.1}
        },
        "Manajemen": {
            'akademik': {'mtk': 0.3, 'ipa_ips': 0.3, 'bindo': 0.2, 'bing': 0.2},
            'minat': {'logika': 0.4, 'sosial': 0.4, 'kreatif': 0.2}
        },
        "Arsitektur": {
            'akademik': {'mtk': 0.35, 'ipa_ips': 0.35, 'bing': 0.15, 'bindo': 0.15},
            'minat': {'kreatif': 0.5, 'logika': 0.4, 'sosial': 0.1}
        },
        "Pendidikan Guru (PGSD)": {
            'akademik': {'bindo': 0.3, 'mtk': 0.25, 'ipa_ips': 0.25, 'bing': 0.2},
            'minat': {'sosial': 0.5, 'bahasa': 0.3, 'logika': 0.1, 'kreatif': 0.1}
        }
    }

    hasil_evaluasi = []
    for jurusan, config in jurusan_config.items():
        skor = evaluasi_jurusan(
            mtk_v, bindo_v, bing_v, ipa_ips_v,
            min_log, min_sos, min_kre, min_bah,
            config['akademik'],
            config['minat']
        )
        hasil_evaluasi.append((jurusan, skor))

    hasil_evaluasi = sorted(hasil_evaluasi, key=lambda x: x[1], reverse=True)
    
    top3 = hasil_evaluasi[:3]
    skor_rata = float(np.mean([x[1] for x in top3]))

    return top3, skor_rata