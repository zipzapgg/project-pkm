import numpy as np

# 1. TABEL BOBOT GAP (Standar Profile Matching)
def get_bobot_gap(gap):
    # Mapping standar: Semakin dekat gap dengan 0, semakin tinggi nilainya
    mapping = {
        0: 5.0,   # Kompetensi pas
        1: 4.5,   # Kelebihan 1 tingkat
        -1: 4.0,  # Kekurangan 1 tingkat
        2: 3.5,   # Kelebihan 2 tingkat
        -2: 3.0,  # Kekurangan 2 tingkat
        3: 2.5,   # Kelebihan 3 tingkat
        -3: 2.0,  # Kekurangan 3 tingkat
        4: 1.5,   # Kelebihan 4 tingkat
        -4: 1.0   # Kekurangan 4 tingkat
    }
    # Handle gap yang lebih besar dari 4 atau lebih kecil dari -4
    if gap in mapping:
        return mapping[gap]
    elif gap > 4:
        return 1.5
    else: # gap < -4
        return 1.0

def konversi_nilai(nilai_asli):
    if nilai_asli >= 85: return 5
    elif nilai_asli >= 78: return 4
    elif nilai_asli >= 70: return 3
    elif nilai_asli >= 60: return 2
    else: return 1

def validate_input(mtk, bindo, bing, sains, sosial, min_log, min_sos, min_kre, min_bah):
    inputs = {
        'Nilai Akademik': [mtk, bindo, bing, sains, sosial],
        'Minat': [min_log, min_sos, min_kre, min_bah]
    }
    
    for val in inputs['Nilai Akademik']:
        if not (0 <= val <= 100): raise ValueError(f"Nilai Akademik {val} tidak valid (0-100)")
            
    for val in inputs['Minat']:
        if not (1 <= val <= 5): raise ValueError(f"Nilai Minat {val} tidak valid (1-5)")

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

    # === KONFIGURASI JURUSAN LENGKAP (35 JURUSAN) ===
    config_jurusan = {
        # --- KESEHATAN ---
        "Kedokteran Umum":      {'u': 'sains', 'd': 'bing', 'm': 'sosial_minat', 'target': {'u': 5, 'd': 4, 'm': 4}},
        "Farmasi":              {'u': 'sains', 'd': 'mtk', 'm': 'logika', 'target': {'u': 5, 'd': 4, 'm': 3}},
        "Ilmu Gizi":            {'u': 'sains', 'd': 'sains', 'm': 'sosial_minat', 'target': {'u': 4, 'd': 4, 'm': 4}},
        "Kesehatan Masyarakat": {'u': 'sains', 'd': 'sosial', 'm': 'sosial_minat', 'target': {'u': 3, 'd': 3, 'm': 4}},
        "Keperawatan":          {'u': 'sains', 'd': 'sosial', 'm': 'sosial_minat', 'target': {'u': 3, 'd': 3, 'm': 5}},

        # --- TEKNIK & SAINTEK ---
        "Teknik Sipil":         {'u': 'mtk', 'd': 'sains', 'm': 'logika', 'target': {'u': 4, 'd': 3, 'm': 3}},
        "Teknik Industri":      {'u': 'mtk', 'd': 'sains', 'm': 'logika', 'target': {'u': 4, 'd': 3, 'm': 3}},
        "Teknik Mesin":         {'u': 'sains', 'd': 'mtk', 'm': 'logika', 'target': {'u': 5, 'd': 4, 'm': 4}},
        "Teknik Elektro":       {'u': 'mtk', 'd': 'sains', 'm': 'logika', 'target': {'u': 5, 'd': 4, 'm': 5}},
        "Arsitektur":           {'u': 'mtk', 'd': 'kreatif', 'm': 'kreatif', 'target': {'u': 4, 'd': 4, 'm': 5}},
        "Agroteknologi":        {'u': 'sains', 'd': 'mtk', 'm': 'logika', 'target': {'u': 4, 'd': 3, 'm': 3}},

        # --- KOMPUTER & DATA ---
        "Sains Data":           {'u': 'mtk', 'd': 'logika', 'm': 'logika', 'target': {'u': 5, 'd': 3, 'm': 4}},
        "Teknik Informatika":   {'u': 'mtk', 'd': 'bing', 'm': 'logika', 'target': {'u': 4, 'd': 3, 'm': 4}},
        "Sistem Informasi":     {'u': 'mtk', 'd': 'sosial', 'm': 'logika', 'target': {'u': 4, 'd': 3, 'm': 3}},
        "Teknik Komputer":      {'u': 'mtk', 'd': 'sains', 'm': 'logika', 'target': {'u': 4, 'd': 3, 'm': 4}},

        # --- EKONOMI & BISNIS ---
        "Akuntansi":            {'u': 'sosial', 'd': 'mtk', 'm': 'logika', 'target': {'u': 5, 'd': 3, 'm': 3}},
        "Manajemen":            {'u': 'sosial', 'd': 'bing', 'm': 'sosial_minat', 'target': {'u': 4, 'd': 3, 'm': 4}},
        "Ekonomi Pembangunan":  {'u': 'sosial', 'd': 'mtk', 'm': 'logika', 'target': {'u': 4, 'd': 3, 'm': 3}},
        "Bisnis Digital":       {'u': 'mtk', 'd': 'sosial', 'm': 'kreatif', 'target': {'u': 3, 'd': 3, 'm': 4}},
        "Pariwisata":           {'u': 'bing', 'd': 'sosial', 'm': 'bahasa', 'target': {'u': 4, 'd': 4, 'm': 5}},
        "Perhotelan":           {'u': 'sosial', 'd': 'bing', 'm': 'sosial_minat', 'target': {'u': 4, 'd': 3, 'm': 5}},

        # --- SOSIAL & HUKUM ---
        "Ilmu Hukum":           {'u': 'bindo', 'd': 'sosial', 'm': 'sosial_minat', 'target': {'u': 4, 'd': 4, 'm': 4}},
        "Psikologi":            {'u': 'sosial', 'd': 'bindo', 'm': 'sosial_minat', 'target': {'u': 4, 'd': 3, 'm': 5}},
        "Hubungan Internasional":{'u': 'bing', 'd': 'sosial', 'm': 'sosial_minat', 'target': {'u': 5, 'd': 4, 'm': 4}},
        "Ilmu Politik":         {'u': 'sosial', 'd': 'bindo', 'm': 'sosial_minat', 'target': {'u': 4, 'd': 3, 'm': 4}},
        "Ilmu Komunikasi":      {'u': 'sosial', 'd': 'bing', 'm': 'sosial_minat', 'target': {'u': 4, 'd': 3, 'm': 5}},
        "Humas / PR":           {'u': 'sosial', 'd': 'bindo', 'm': 'sosial_minat', 'target': {'u': 5, 'd': 4, 'm': 5}},
        "Administrasi Publik":  {'u': 'sosial', 'd': 'bing', 'm': 'sosial_minat', 'target': {'u': 3, 'd': 3, 'm': 3}},
        "Sosiologi":            {'u': 'sosial', 'd': 'bindo', 'm': 'sosial_minat', 'target': {'u': 4, 'd': 3, 'm': 4}},
        "PGSD":                 {'u': 'sosial', 'd': 'bindo', 'm': 'sosial_minat', 'target': {'u': 3, 'd': 3, 'm': 4}},

        # --- BAHASA & SENI ---
        "DKV":                  {'u': 'kreatif', 'd': 'bing', 'm': 'kreatif', 'target': {'u': 5, 'd': 3, 'm': 5}},
        "Sastra Inggris":       {'u': 'bing', 'd': 'bindo', 'm': 'bahasa', 'target': {'u': 5, 'd': 3, 'm': 4}},
        "Sastra Indonesia":     {'u': 'bindo', 'd': 'bing', 'm': 'bahasa', 'target': {'u': 5, 'd': 3, 'm': 4}},
        "Sastra Jepang":        {'u': 'bing', 'd': 'bindo', 'm': 'bahasa', 'target': {'u': 4, 'd': 3, 'm': 4}},
    }

    hasil_akhir = []
    detail_perhitungan = []

    for jur, cfg in config_jurusan.items():
        # --- 1. GAP ANALYSIS ---
        val_u = data_siswa.get(cfg['u'], 1)
        val_d = data_siswa.get(cfg['d'], 1)
        val_m = data_siswa.get(cfg['m'], 1)
        
        target_u = cfg['target']['u']
        target_d = cfg['target']['d']
        target_m = cfg['target']['m']
        
        gap_u = val_u - target_u
        gap_d = val_d - target_d
        gap_m = val_m - target_m

        # --- 2. BOBOT NILAI (WEIGHTING) ---
        bobot_u = get_bobot_gap(gap_u)
        bobot_d = get_bobot_gap(gap_d)
        bobot_m = get_bobot_gap(gap_m)

        # --- 3. TOTAL SCORE CALCULATION ---
        avg_core = (bobot_u + bobot_m) / 2
        avg_secondary = bobot_d 
        nilai_total_pm = (avg_core * 0.60) + (avg_secondary * 0.40)
        final_score = (nilai_total_pm / 5.0) * 100

        penalty_log = []
        
        # --- 4. PENALTY & BONUS (RULE BASED OVERLAY) ---
        if val_u <= 2: 
            final_score -= 25 # Dikurangi dari 35 biar lebih rasional
            penalty_log.append(f"Nilai Utama ({cfg['u']}) Rendah (-25)")

        # Bonus: Diperbaiki skalanya agar terasa efeknya
        bonus = 0
        if jur == "Kedokteran Umum" and data_siswa['sains'] == 5: bonus = 5
        elif jur == "Farmasi" and data_siswa['sains'] >= 4: bonus = 3
        elif jur == "Akuntansi" and data_siswa['sosial'] == 5: bonus = 3
        elif jur == "Sains Data" and data_siswa['mtk'] == 5: bonus = 3
        
        if bonus > 0:
            penalty_log.append(f"Bonus Prestasi (+{bonus})")

        final_score = min(100, max(0, final_score + bonus))

        # Simpan Detail
        detail_perhitungan.append({
            'jurusan': jur,
            'gaps': {'u': gap_u, 'd': gap_d, 'm': gap_m},
            'bobots': {'u': bobot_u, 'd': bobot_d, 'm': bobot_m},
            'scores': {'core': avg_core, 'secondary': avg_secondary},
            'final_score': round(final_score, 2),
            'notes': penalty_log
        })

        hasil_akhir.append((jur, round(final_score, 2)))

    # Sort dari nilai tertinggi
    hasil_akhir.sort(key=lambda x: x[1], reverse=True)
    
    top_3 = hasil_akhir[:3]
    
    # Hitung Confidence Level sederhana
    confidence = "Cukup Yakin"
    if not top_3:
        confidence = "Data Tidak Cukup"
    else:
        selisih_1_2 = top_3[0][1] - top_3[1][1]
        if top_3[0][1] < 50: confidence = "Tidak Yakin (Nilai Rendah)"
        elif selisih_1_2 > 5: confidence = "Sangat Yakin" # Margin dominan
        elif selisih_1_2 < 1: confidence = "Kurang Yakin (Persaingan Ketat)"

    detail_info = {
        'total_jurusan': len(hasil_akhir),
        'detail_perhitungan': sorted(detail_perhitungan, key=lambda x: x['final_score'], reverse=True)[:5]
    }
    
    # PERBAIKAN: Mengambil skor asli dari top_3 (bukan 0.0 dummy)
    skor_tertinggi = top_3[0][1] if top_3 else 0

    return top_3, skor_tertinggi, confidence, detail_info