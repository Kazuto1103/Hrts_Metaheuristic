# 02 - PROJECT OVERVIEW

**Dokumentasi Lengkap Struktur & Tujuan Proyek**

---

## 🎯 TUJUAN PROYEK

Mengoptimalkan klasifikasi detak jantung (BPM) normal/abnormal menggunakan dua algoritma metaheuristik dengan pendekatan berbeda:
- **PSO**: Menemukan threshold BPM optimal
- **ACO**: Memilih feature terbaik dari 18 features

---

## 📊 DATA

**Dataset Karakteristik:**
- 10 subjects
- 300 BPM readings per subject
- Total: 3,000 readings
- 18 features (15 statistical + 3 IoT metadata)
- Binary classification: Normal (0) vs Abnormal (1)

**Features (18 Total):**

*Statistical Features (15):*
- Mean, Std Dev, Variance
- Min, Max, Percentiles (25%, 50%, 75%)
- Range, IQR, Skewness, Kurtosis
- Energy, Entropy, Coefficient of Variation

*IoT Metadata (3):*
- Gender, Age, Device_ID

---

## 🗂️ STRUKTUR FOLDER

```
d:\Project\Heuristik\
│
├── 📂 docs/                    ← DOKUMENTASI (12 file)
│   ├── 00-START-HERE.md
│   ├── 01-QUICK-REFERENCE.md
│   ├── 02-PROJECT-OVERVIEW.md  ← Anda di sini
│   ├── 03-ALGORITHM-COMPARISON.md
│   ├── 04-RESULTS-SUMMARY.md
│   ├── 05-ACO-FEATURES.md
│   ├── 06-DATASET-DESCRIPTION.md
│   ├── 07-PSO-ALGORITHM.md
│   ├── 08-ACO-ALGORITHM.md
│   ├── 09-VISUALIZATION-GUIDE.md
│   ├── 10-COMPLETION-CHECKLIST.md
│   ├── 11-NAVIGATION-GUIDE.md
│   └── INDEX.md
│
├── 📂 datasets/                ← DATA FILES (3 file)
│   ├── dataset_bpm.json        (original raw data)
│   ├── dataset_bpm_optimized.json (18 features + metadata)
│   └── feature_matrix.csv      (ML-ready format)
│
├── 📂 pso/                     ← PSO ALGORITHM
│   ├── pso_optimizer.py        (313 lines)
│   └── results/                (12 files)
│       ├── 10 × timeline plots
│       ├── convergence plot
│       └── results.json
│
├── 📂 aco/                     ← ACO ALGORITHM
│   ├── aco_optimizer.py        (373 lines)
│   └── results/                (13 files)
│       ├── 10 × timeline plots
│       ├── convergence plot
│       ├── feature importance plot
│       └── results.json
│
└── 📂 utils/                   ← HELPER FUNCTIONS (3 file)
    ├── helper.py               (DataLoader, Visualizer, Metrics)
    ├── analyze_dataset.py
    └── optimize_dataset.py
```

**Total Files:**
- Dokumentasi: 12 markdown files
- Algoritma: 2 Python files (+ utility files)
- Data: 3 files (JSON + CSV)
- Visualisasi: 25 files (22 PNG + 2 JSON)
- **Grand Total: 44 files**

---

## 🚀 CARA MENJALANKAN

### Run PSO
```bash
cd d:\Project\Heuristik\pso
python pso_optimizer.py
```
**Output:** 12 files (10 plots + convergence + metrics.json)

### Run ACO
```bash
cd d:\Project\Heuristik\aco
python aco_optimizer.py
```
**Output:** 13 files (10 plots + convergence + importance + metrics.json)

---

## 📈 HASIL FINAL

### PSO: Threshold Optimization
```
Performance:
├─ Accuracy:  90%
├─ Precision: 100%
├─ Recall:    90%
└─ F1-Score:  0.947

Optimal Thresholds:
├─ Normal Min:   59.92 BPM
├─ Normal Max:   80.00 BPM
└─ Elevated Max: 122.80 BPM

Parameters:
├─ Particles:   20
├─ Iterations:  100
├─ Variables:   3 (threshold values)
└─ Convergence: 0.0 → 0.9
```

### ACO: Feature Selection
```
Performance:
├─ Accuracy:  100% ⭐
├─ Precision: 100%
├─ Recall:    100%
└─ F1-Score:  1.0

Selected Features: 5 from 18
├─ Feature 0: Mean BPM
├─ Feature 1: Std Deviation
├─ Feature 6: Median BPM
├─ Feature 9: IQR
└─ Feature 16: Age

Parameters:
├─ Ants:       15
├─ Iterations: 50
├─ Variables:  18 (feature selection)
└─ Convergence: ~0.944 (fast)
```

---

## 🎯 KEY DELIVERABLES

✅ **20 BPM Timeline Visualizations**
- 10 plots dari PSO (threshold-based)
- 10 plots dari ACO (feature-based)
- Color-coded: Green (normal) / Red (abnormal)

✅ **2 Convergence Plots**
- PSO: Menunjukkan gradual improvement
- ACO: Menunjukkan fast convergence

✅ **1 Feature Importance Plot**
- ACO: Ranking 5 fitur terpilih

✅ **2 Results JSON**
- PSO: Metrics + optimal thresholds
- ACO: Metrics + selected feature indices

✅ **Comprehensive Documentation**
- 12 markdown files
- Complete code explanation
- Usage guides

---

## 🔄 WORKFLOW SUMMARY

```
START
  ↓
[1] Load Data (10 subjects × 18 features)
  ├─→ PSO Path: Optimize 3 threshold variables
  │    ├─ Run 20 particles × 100 iterations
  │    ├─ Achieve 90% accuracy
  │    └─ Generate 12 outputs
  │
  └─→ ACO Path: Select 5 best features
       ├─ Run 15 ants × 50 iterations
       ├─ Achieve 100% accuracy
       └─ Generate 13 outputs
  ↓
[2] Generate Visualizations (20 plots total)
  ↓
[3] Create Documentation (12 markdown files)
  ↓
END: Project Complete!
```

---

## 💻 TECH STACK

**Language:** Python 3.x
**Libraries:**
- numpy (numerical computing)
- pandas (data manipulation)
- matplotlib (visualization)
- scikit-learn (ML utilities)
- scipy (statistical functions)

**Algorithms:**
- PSO: Custom implementation (313 lines)
- ACO: Custom implementation (373 lines)

**Data Format:**
- JSON (dataset storage)
- CSV (feature matrix)
- PNG (visualizations)

---

## 🎓 KONSEP PENTING

### PSO (Particle Swarm Optimization)
- Simulasi perilaku burung (flocking behavior)
- Particle bergerak di search space
- Setiap particle punya velocity & position
- Update berdasarkan personal best + global best

### ACO (Ant Colony Optimization)
- Simulasi perilaku semut mencari rute optimal
- Ants deposit pheromone saat menemukan solusi baik
- Pheromone menginduksi ants lain mengikuti rute baik
- Pheromone evaporation mencegah konvergensi prematur

### Feature Selection
- Dimensionality reduction: 18 → 5 (72% reduction)
- Meningkatkan: clarity, speed, generalization
- Mengurangi: overfitting, computation cost

---

## 📋 FILE YANG PERLU DIBACA

| Untuk... | Baca | Waktu |
|---------|------|-------|
| Mulai | 00-START-HERE.md | 5 min |
| Quick info | 01-QUICK-REFERENCE.md | 5 min |
| **Anda di sini** | 02-PROJECT-OVERVIEW.md | 10 min |
| Bandingkan | 03-ALGORITHM-COMPARISON.md | 15 min |
| Hasil | 04-RESULTS-SUMMARY.md | 10 min |
| Feature detail | 05-ACO-FEATURES.md | 15 min |
| Data | 06-DATASET-DESCRIPTION.md | 20 min |
| PSO deep dive | 07-PSO-ALGORITHM.md | 30 min |
| ACO deep dive | 08-ACO-ALGORITHM.md | 30 min |
| Baca grafik | 09-VISUALIZATION-GUIDE.md | 15 min |
| Verify | 10-COMPLETION-CHECKLIST.md | 10 min |
| Help | 11-NAVIGATION-GUIDE.md | 10 min |

---

## ✨ NEXT STEP

👉 **Baca**: 
- Untuk quick info → [01-QUICK-REFERENCE.md](01-QUICK-REFERENCE.md)
- Untuk compare → [03-ALGORITHM-COMPARISON.md](03-ALGORITHM-COMPARISON.md)
- Untuk detail → [06-DATASET-DESCRIPTION.md](06-DATASET-DESCRIPTION.md)

---

**Created:** 2025-11-27  
**Time to Read:** 10 minutes
