import numpy as np

def get_bobot_gap(gap):
    if gap == 0: return 5.0
    elif gap == 1: return 4.5
    elif gap == 2: return 4.0
    elif gap >= 3: return 3.5
    elif gap == -1: return 3.0
    elif gap == -2: return 2.0
    elif gap == -3: return 1.5
    elif gap <= -4: return 1.0
    else: return 2.5

def konversi_nilai(nilai_asli):
    if nilai_asli >= 85: return 5
    elif nilai_asli >= 78: return 4
    elif nilai_asli >= 70: return 3
    elif nilai_asli >= 60: return 2
    else: return 1

def validate_input(mtk, bindo, bing, sains, sosial, min_log, min_sos, min_kre, min_bah):
    for nilai in [mtk, bindo, bing, sains, sosial]:
        if not (0 <= nilai <= 100):
            raise ValueError("Nilai harus 0-100")
    
    for minat in [min_log, min_sos, min_kre, min_bah]:
        if not (1 <= minat <= 5):
            raise ValueError("Minat harus 1-5")

def hitung_rekomendasi(mtk, bindo, bing, sains, sosial, min_log, min_sos, min_kre, min_bah):
    
    validate_input(mtk, bindo, bing, sains, sosial, min_log, min_sos, min_kre, min_bah)
    
    data_siswa = {
        'mtk': konversi_nilai(mtk),
        'bindo': konversi_nilai(bindo),
        'bing': konversi_nilai(bing),
        'sains': konversi_nilai(sains),
        'sosial': konversi_nilai(sosial),
        'logika': int(min_log),
        'sosial_minat': int(min_sos),
        'kreatif': int(min_kre),
        'bahasa': int(min_bah)
    }

    config_jurusan = {
        "Kedokteran Umum":      {'u': 'sains', 'd': 'bing', 'm': 'sosial_minat', 'target': {'u': 5, 'd': 4, 'm': 4}},
        "Farmasi":              {'u': 'sains', 'd': 'mtk', 'm': 'logika', 'target': {'u': 5, 'd': 4, 'm': 3}},
        "Teknik Sipil":         {'u': 'mtk', 'd': 'sains', 'm': 'logika', 'target': {'u': 4, 'd': 3, 'm': 3}},
        "Teknik Industri":      {'u': 'mtk', 'd': 'sains', 'm': 'logika', 'target': {'u': 4, 'd': 3, 'm': 3}},
        "Sains Data":           {'u': 'mtk', 'd': 'logika', 'm': 'logika', 'target': {'u': 5, 'd': 3, 'm': 4}},
        "Teknik Informatika":   {'u': 'mtk', 'd': 'bing', 'm': 'logika', 'target': {'u': 4, 'd': 3, 'm': 4}},
        "Sistem Informasi":     {'u': 'mtk', 'd': 'sosial', 'm': 'logika', 'target': {'u': 4, 'd': 3, 'm': 3}},
        "Teknik Komputer":      {'u': 'mtk', 'd': 'sains', 'm': 'logika', 'target': {'u': 4, 'd': 3, 'm': 4}},
        
        "Akuntansi":            {'u': 'sosial', 'd': 'mtk', 'm': 'logika', 'target': {'u': 5, 'd': 3, 'm': 3}},
        "Manajemen":            {'u': 'sosial', 'd': 'bing', 'm': 'sosial_minat', 'target': {'u': 4, 'd': 3, 'm': 4}},
        "Ilmu Hukum":           {'u': 'bindo', 'd': 'sosial', 'm': 'sosial_minat', 'target': {'u': 4, 'd': 4, 'm': 4}},
        "Psikologi":            {'u': 'sosial', 'd': 'bindo', 'm': 'sosial_minat', 'target': {'u': 4, 'd': 3, 'm': 5}},
        "Hubungan Internasional":{'u': 'bing', 'd': 'sosial', 'm': 'sosial_minat', 'target': {'u': 5, 'd': 4, 'm': 4}},
        "Ilmu Politik":         {'u': 'sosial', 'd': 'bindo', 'm': 'sosial_minat', 'target': {'u': 4, 'd': 3, 'm': 4}},
        "Ilmu Komunikasi":      {'u': 'sosial', 'd': 'bing', 'm': 'sosial_minat', 'target': {'u': 4, 'd': 3, 'm': 5}},
        "Administrasi Publik":  {'u': 'sosial', 'd': 'bing', 'm': 'sosial_minat', 'target': {'u': 3, 'd': 3, 'm': 3}},
        "Sosiologi":            {'u': 'sosial', 'd': 'bindo', 'm': 'sosial_minat', 'target': {'u': 4, 'd': 3, 'm': 4}},
        "Ekonomi Pembangunan":  {'u': 'sosial', 'd': 'mtk', 'm': 'logika', 'target': {'u': 4, 'd': 3, 'm': 3}},
        "Bisnis Digital":       {'u': 'mtk', 'd': 'sosial', 'm': 'kreatif', 'target': {'u': 3, 'd': 3, 'm': 4}},

        "Arsitektur":           {'u': 'mtk', 'd': 'kreatif', 'm': 'kreatif', 'target': {'u': 4, 'd': 4, 'm': 5}},
        "DKV":                  {'u': 'kreatif', 'd': 'bing', 'm': 'kreatif', 'target': {'u': 5, 'd': 3, 'm': 5}},
        "Sastra Inggris":       {'u': 'bing', 'd': 'bindo', 'm': 'bahasa', 'target': {'u': 5, 'd': 3, 'm': 4}},
        "Sastra Indonesia":     {'u': 'bindo', 'd': 'bing', 'm': 'bahasa', 'target': {'u': 5, 'd': 3, 'm': 4}},
        "Sastra Jepang":        {'u': 'bing', 'd': 'bindo', 'm': 'bahasa', 'target': {'u': 4, 'd': 3, 'm': 4}},
        "PGSD":                 {'u': 'sosial', 'd': 'bindo', 'm': 'sosial_minat', 'target': {'u': 3, 'd': 3, 'm': 4}},
        "Kesehatan Masyarakat": {'u': 'sains', 'd': 'sosial', 'm': 'sosial_minat', 'target': {'u': 3, 'd': 3, 'm': 4}}
    }

    hasil_akhir = []
    detail_perhitungan = []

    for jur, cfg in config_jurusan.items():
        target_u = cfg['target']['u']
        target_d = cfg['target']['d']
        target_m = cfg['target']['m']
        
        nilai_siswa_u = data_siswa.get(cfg['u'], 1)
        nilai_siswa_d = data_siswa.get(cfg['d'], 1)
        nilai_siswa_m = data_siswa.get(cfg['m'], 1)
        
        # --- HITUNG GAP ---
        gap_u = nilai_siswa_u - target_u
        gap_d = nilai_siswa_d - target_d
        gap_m = nilai_siswa_m - target_m

        # --- HITUNG BOBOT ---
        bobot_u = get_bobot_gap(gap_u)
        bobot_d = get_bobot_gap(gap_d)
        bobot_m = get_bobot_gap(gap_m)

        # --- HITUNG TOTAL ---
        avg_core = (bobot_u + bobot_m) / 2
        avg_secondary = bobot_d 
        nilai_total = (avg_core * 0.60) + (avg_secondary * 0.40)
        final_score = (nilai_total / 5.0) * 100

        penalty_log = []
        
        # Penalti
        if cfg['u'] == 'sains' and data_siswa['sains'] <= 2:
            final_score -= 35
            penalty_log.append("Nilai Sains Kurang (-35)")
        elif cfg['u'] == 'sosial' and data_siswa['sosial'] <= 2:
            final_score -= 35
            penalty_log.append("Nilai Sosial Kurang (-35)")
        elif cfg['u'] == 'kreatif' and data_siswa['kreatif'] <= 2:
            final_score -= 30
            penalty_log.append("Minat Kreatif Kurang (-30)")

        # Bonus
        bonus = 0
        if jur == "Kedokteran Umum" and data_siswa['sains'] == 5: bonus = 0.5
        elif jur == "Farmasi" and data_siswa['sains'] >= 4: bonus = 0.3
        elif jur == "Akuntansi" and data_siswa['sosial'] == 5: bonus = 0.3
        elif jur == "Sains Data" and data_siswa['mtk'] == 5: bonus = 0.3
        
        final_score = min(100, max(0, final_score + bonus))

        # === BAGIAN PENTING: MENYIMPAN DATA UNTUK DEBUGGING ===
        # Pastikan key 'gaps' dan 'bobots' ada di sini!
        detail_perhitungan.append({
            'jurusan': jur,
            'gaps': {'u': gap_u, 'd': gap_d, 'm': gap_m},       # INI HARUS ADA
            'bobots': {'u': bobot_u, 'd': bobot_d, 'm': bobot_m}, # INI JUGA
            'final_score': round(final_score, 2),
            'penalties': penalty_log
        })

        hasil_akhir.append((jur, round(final_score, 2)))

    hasil_akhir.sort(key=lambda x: x[1], reverse=True)
    
    top_3 = hasil_akhir[:3]
    rata_rata = float(np.mean([x[1] for x in top_3])) if top_3 else 0
    
    confidence = "Cukup Yakin" 
    if top_3[0][1] - top_3[1][1] > 2: confidence = "Sangat Yakin"
    elif top_3[0][1] < 60: confidence = "Kurang Yakin"

    detail_info = {
        'total_jurusan': len(hasil_akhir),
        'jurusan_layak': len(hasil_akhir), # Disederhanakan
        'detail_perhitungan': detail_perhitungan[:5] # Kirim 5 teratas saja
    }
    
    return top_3, rata_rata, confidence, detail_info