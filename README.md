# 🫀 BPM Heart Rate Classification - PSO vs ACO Optimization

Proyek machine learning untuk klasifikasi detak jantung normal/abnormal menggunakan dua algoritma metaheuristik: **Particle Swarm Optimization (PSO)** dan **Ant Colony Optimization (ACO)**.

**👉 START HERE:** [`docs/00-START-HERE.md`](./docs/00-START-HERE.md) (3 min quickstart)

---

## 📁 Struktur Folder

```
d:\Project\Heuristik\
├── 📄 README.md                          # File dokumentasi ini (top-level entry)
│
├── 📂 docs/                              # 📚 DOKUMENTASI LENGKAP (13 files organized)
│   ├── 📄 INDEX.md                       # Master navigation hub
│   ├── 📄 00-START-HERE.md               # Entry point (3 min)
│   ├── 📄 01-QUICK-REFERENCE.md          # Cheat sheet (5 min)
│   ├── 📄 02-PROJECT-OVERVIEW.md         # Project structure (10 min)
│   ├── 📄 03-ALGORITHM-COMPARISON.md     # PSO vs ACO (15 min)
│   ├── 📄 04-RESULTS-SUMMARY.md          # Final results (10 min)
│   ├── 📄 05-ACO-FEATURES.md             # Feature analysis (15 min)
│   ├── 📄 06-DATASET-DESCRIPTION.md      # Data details (20 min)
│   ├── 📄 07-PSO-ALGORITHM.md            # PSO deep dive (25 min)
│   ├── 📄 08-ACO-ALGORITHM.md            # ACO deep dive (30 min)
│   ├── 📄 09-VISUALIZATION-GUIDE.md      # Plot guide (15 min)
│   ├── 📄 10-COMPLETION-CHECKLIST.md     # Verification (10 min)
│   └── 📄 11-NAVIGATION-GUIDE.md         # Navigation guide (5-10 min)
│
├── 📂 datasets/                          # Dataset & Feature Matrix
│   ├── dataset_bpm.json                 # Dataset original (raw sensor data)
│   ├── dataset_bpm_optimized.json       # Dataset optimized (dengan 18 fitur + metadata)
│   └── feature_matrix.csv               # Format ML-ready (10 samples × 18 features)
│
├── 📂 pso/                               # Particle Swarm Optimization
│   ├── pso_optimizer.py                 # Implementasi PSO algorithm
│   └── results/                         # Output visualisasi & hasil PSO
│       ├── orang_1_bpm_timeline.png     # Timeline BPM individual (1-10)
│       ├── orang_2_bpm_timeline.png
│       ├── ... (8 files lebih)
│       ├── orang_10_bpm_timeline.png
│       ├── pso_fitness_convergence.png  # Grafik konvergensi fitness
│       └── pso_results.json             # Hasil metrics & optimal thresholds
│
├── 📂 aco/                               # Ant Colony Optimization
│   ├── aco_optimizer.py                 # Implementasi ACO algorithm
│   └── results/                         # Output visualisasi & hasil ACO
│       ├── orang_1_bpm_timeline.png     # Timeline BPM individual (1-10)
│       ├── orang_2_bpm_timeline.png
│       ├── ... (8 files lebih)
│       ├── orang_10_bpm_timeline.png
│       ├── aco_fitness_convergence.png  # Grafik konvergensi fitness ACO
│       ├── aco_feature_importance.png   # Fitur terpilih ACO
│       └── aco_results.json             # Hasil metrics & selected features
│
└── 📂 utils/                             # Utility Functions
    ├── helper.py                        # DataLoader, BPMVisualizer, MetricsCalculator
    ├── analyze_dataset.py               # Analisis dataset
    └── optimize_dataset.py              # Fungsi optimisasi dataset
```

---

## 🚀 Cara Menjalankan

### 1️⃣ **Jalankan PSO Optimizer**
```bash
cd d:\Project\Heuristik\pso
python pso_optimizer.py
```

**Output yang dihasilkan:**
- 10 BPM timeline plots dengan threshold optimal
- Fitness convergence plot (0.0 → 0.9)
- Results JSON dengan optimal thresholds

**Hasil PSO:**
- **Accuracy:** 90%
- **Precision:** 100%
- **Recall:** 90%
- **F1-Score:** 0.9474
- **Optimal Thresholds:** Normal 59.92-80.00 BPM, Elevated max 122.80 BPM

---

### 2️⃣ **Jalankan ACO Optimizer**
```bash
cd d:\Project\Heuristik\aco
python aco_optimizer.py
```

**Output yang dihasilkan:**
- 10 BPM timeline plots dengan fitur terpilih
- Fitness convergence plot (menunjukkan pheromone dynamics)
- Feature importance plot (5 fitur terbaik dari 18)
- Results JSON dengan selected features

**Hasil ACO:**
- **Accuracy:** 100% ✨
- **Precision:** 100%
- **Recall:** 100%
- **F1-Score:** 1.0
- **Selected Features:** 5/18 (dimensionality reduction)

---

## 📊 Membaca Visualisasi

### 🟢 BPM Timeline Plot
- **Warna Hijau:** BPM normal (dalam range optimal)
- **Warna Merah:** BPM abnormal (di luar range optimal)
- **Garis Horizontal:** Threshold batas

**PSO Timeline:** Menunjukkan klasifikasi berdasarkan **threshold optimal**
**ACO Timeline:** Menunjukkan klasifikasi berdasarkan **fitur terpilih**

### 📈 Fitness Convergence Plot
- **X-axis:** Iterasi
- **Y-axis:** Fitness (accuracy)
- **PSO:** Konvergensi 100 particles ⟶ 20 particles menuju 0.9
- **ACO:** Konvergensi 50 iterations dengan pheromone update ⟶ 0.9444

### 🎯 Feature Importance Plot (ACO Only)
- Menampilkan ranking 5 fitur terbaik yang dipilih ACO
- Skala kepentingan pheromone

---

## 🔄 Perbandingan PSO vs ACO

| Aspek | PSO | ACO |
|-------|-----|-----|
| **Strategi** | Threshold Optimization | Feature Selection |
| **Variabel Optimasi** | 3 (normal_min, normal_max, elevated_max) | 18 (feature selection: yes/no) |
| **Particles/Ants** | 20 particles | 15 ants |
| **Iterasi** | 100 | 50 |
| **Fitness Akhir** | 0.9000 (90%) | 0.9444 (100% accuracy actual) |
| **Precision** | 100% | 100% |
| **Recall** | 90% | 100% |
| **F1-Score** | 0.9474 | 1.0000 |
| **Output Utama** | Optimal thresholds | Selected 5 features |
| **Keunikan** | Menemukan boundary BPM | Mengurangi dimensi fitur |

---

## 📚 Fitur yang Dioptimalkan

Setiap subject memiliki 18 fitur statistik yang diekstrak dari 300 reading BPM dalam 5 menit:

**Statistical Features (15):**
- Mean, Std Dev, Variance, Min, Max
- 25th, 50th, 75th Percentile
- Range, IQR, Skewness, Kurtosis
- Energy, Entropy, Coefficient of Variation

**IoT Metadata (3):**
- Gender, Age, Device ID
- Location, Timestamp

---

## 🎯 Hasil Akhir

✅ **PSO:** Menghasilkan threshold optimal untuk klasifikasi BPM
- Normal Range: **59.92 - 80.00 BPM**
- Elevated Max: **122.80 BPM**
- Akurasi: **90%** (9/10 subjects benar)

✅ **ACO:** Memilih 5 fitur terbaik dari 18 untuk klasifikasi
- **100% Accuracy** pada test set
- Dimensionality reduction: 18 → 5 fitur
- F1-Score: **1.0** (perfect classification)

---

## 🛠️ Requirements

```txt
numpy
pandas
matplotlib
scikit-learn
scipy
```

Install dengan:
```bash
pip install numpy pandas matplotlib scikit-learn scipy
```

---

## 📝 Catatan Pengembangan

### Folder Semantic Organization
- **docs/**: Dokumentasi lengkap untuk referensi
- **datasets/**: Data untuk training & evaluation
- **pso/**: Kode PSO terpisah dari ACO
- **aco/**: Kode ACO terpisah dari PSO
- **utils/**: Helper functions yang dipakai kedua algoritma

### Visualization Differences
- PSO timeline: scatter plot dengan threshold boundaries
- ACO timeline: scatter plot dari predictions menggunakan selected features
- Convergence plots: menunjukkan dinamika berbeda (velocity vs pheromone)

### Next Steps (Optional)
- [ ] Gabungkan PSO + ACO (use PSO thresholds dengan ACO features)
- [ ] Cross-validation dengan k-fold
- [ ] Export model untuk production
- [ ] Real-time monitoring dengan IoT sensor

---

**Created:** 2025-11-27  
**Last Updated:** 2025-11-27  
**Status:** ✅ Complete - PSO & ACO successfully optimized and visualized
