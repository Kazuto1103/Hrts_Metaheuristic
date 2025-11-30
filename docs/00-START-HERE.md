# 🎯 START HERE - Panduan Pertama

**Selamat datang!** Ini adalah halaman pertama untuk memahami proyek BPM Classification.

---

## ⚡ 30 Detik Summary

```
Apa itu?
→ Machine learning klasifikasi detak jantung (BPM) remaja stabil
  menggunakan 2 algoritma metaheuristik: PSO & ACO
  Dataset: 40 orang (12,000 reading) dengan realistic jumpscare patterns

Hasil apa?
→ PSO: 100% accuracy (threshold optimization: 68.44 < X < 96.59 bpm)
  ACO: 100% accuracy (5 features selected: Mean, Max, Median, Skewness, Q75)

Mana yang MENANG?
→ ACCURACY: TIED 🤝 (both 100% on 40-person realistic dataset)
  TRAINING: ACO WINS ⚡ (2x faster convergence)
  DEPLOYMENT: PSO WINS ⚡ (simpler & faster inference)

File apa saja?
→ 40 timeline per algoritma (80 total visualizations)
  + convergence plots + feature importance plot
  + hasil metrics (JSON) dengan clear efficiency comparison
```

---

## 🚀 QUICK START (5 menit)

### Langkah 1: Lihat Hasil
```powershell
# PSO results
explorer d:\Project\Heuristik\pso\results\

# ACO results
explorer d:\Project\Heuristik\aco\results\
```

### Langkah 2: Jalankan Ulang (Optional)
```bash
# Run PSO
cd d:\Project\Heuristik\pso
python pso_optimizer.py

# Run ACO
cd d:\Project\Heuristik\aco
python aco_optimizer.py
```

### Langkah 3: Baca Dokumentasi
→ **Lanjut ke:** [01-QUICK-REFERENCE.md](01-QUICK-REFERENCE.md)

---

## 📊 HASIL RINGKAS

| Algoritma | Accuracy | Strategy | Keunggulan | Efficiency |
|-----------|----------|----------|-----------|-----------|
| **PSO** | 100% ✓ | Threshold Optimization | Simpler, faster deployment | Deployment ⚡ |
| **ACO** | 100% ✓ | Feature Selection | More features, 2x faster training | Training ⚡ |

---

## 🗂️ STRUKTUR FOLDER

```
d:\Project\Heuristik\
├── docs/          ← Dokumentasi (12 file)
├── datasets/      ← Data (3 file)
├── pso/           ← PSO algorithm + 12 results
├── aco/           ← ACO algorithm + 13 results
└── utils/         ← Helper functions
```

---

## 🎯 PILIH JALUR MEMBACA

### Saya butuh... **Overview cepat** (5-10 min)
1. Ini: **00-START-HERE.md** ✓
2. Lalu: **01-QUICK-REFERENCE.md**
→ Selesai!

### Saya butuh... **Memahami algoritma** (45 min)
1. **02-PROJECT-OVERVIEW.md**
2. **07-PSO-ALGORITHM.md**
3. **08-ACO-ALGORITHM.md**
→ Mengerti!

### Saya butuh... **Membandingkan hasil** (20 min)
1. **03-ALGORITHM-COMPARISON.md**
2. **04-RESULTS-SUMMARY.md**
→ Clear!

### Saya butuh... **Mengerti fitur ACO** (20 min)
1. **06-DATASET-DESCRIPTION.md**
2. **05-ACO-FEATURES.md**
→ Jelas!

### Saya butuh... **Verifikasi semua selesai** (15 min)
1. **10-COMPLETION-CHECKLIST.md**
→ ✅ Complete!

---

## 📞 HUBUNGI BANTUAN

| Jika... | Baca |
|--------|------|
| "Mana algoritma yang MENANG?" | 03-ALGORITHM-COMPARISON.md |
| "Algoritma mana lebih EFFICIENT?" | 03-ALGORITHM-COMPARISON.md (FINAL VERDICT) |
| "Apa arti grafik hijau/merah?" | 09-VISUALIZATION-GUIDE.md |
| "Data seperti apa (realistic)?" | 06-DATASET-DESCRIPTION.md |
| "Berapa akurasi kedua?" | 04-RESULTS-SUMMARY.md |
| "Konvergensi mana lebih cepat?" | 03-ALGORITHM-COMPARISON.md (Convergence Analysis) |
| "Mau lihat file mana?" | 11-NAVIGATION-GUIDE.md |

---

## ✨ NEXT STEP

👉 **Baca**: [01-QUICK-REFERENCE.md](01-QUICK-REFERENCE.md) (5 menit)

---

**Created:** 2025-11-27  
**Time to Read:** 3-5 minutes
