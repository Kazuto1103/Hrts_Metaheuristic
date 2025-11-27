# 11 - NAVIGATION GUIDE

**Panduan Navigasi & Pencarian File**

---

## 🗺️ STRUCTURE MASTER

```
Heuristik/
├── 📁 docs/              ← Anda di sini (dokumentasi utama)
│   ├── 📄 INDEX.md
│   ├── 📄 00-START-HERE.md
│   ├── 📄 01-QUICK-REFERENCE.md
│   ├── 📄 02-PROJECT-OVERVIEW.md
│   ├── 📄 03-ALGORITHM-COMPARISON.md
│   ├── 📄 04-RESULTS-SUMMARY.md
│   ├── 📄 05-ACO-FEATURES.md
│   ├── 📄 06-DATASET-DESCRIPTION.md
│   ├── 📄 07-PSO-ALGORITHM.md
│   ├── 📄 08-ACO-ALGORITHM.md
│   ├── 📄 09-VISUALIZATION-GUIDE.md
│   ├── 📄 10-COMPLETION-CHECKLIST.md
│   └── 📄 11-NAVIGATION-GUIDE.md (ini)
│
├── 📁 datasets/          ← Data files
│   ├── dataset_bpm.json
│   ├── dataset_bpm_optimized.json
│   └── feature_matrix.csv
│
├── 📁 pso/              ← Algoritma & hasil PSO
│   ├── pso.py
│   ├── 12 visualization files
│   └── pso_results.json
│
├── 📁 aco/              ← Algoritma & hasil ACO
│   ├── aco.py
│   ├── 13 visualization files
│   └── aco_results.json
│
└── 📁 utils/            ← Helper files
    ├── helper.py
    ├── analyze_dataset.py
    └── optimize_dataset.py
```

---

## 🔍 QUICK FINDER

### ❓ Saya ingin tahu...

#### ...apa itu proyek ini?
→ **START:** [00-START-HERE.md](./00-START-HERE.md) (3 min)
→ **NEXT:** [02-PROJECT-OVERVIEW.md](./02-PROJECT-OVERVIEW.md) (10 min)

#### ...cara menjalankan algoritma
→ **START:** [01-QUICK-REFERENCE.md](./01-QUICK-REFERENCE.md) (5 min)
→ **REFERENCE:** Bagian "How to Run"

#### ...perbedaan PSO vs ACO
→ **DIRECT:** [03-ALGORITHM-COMPARISON.md](./03-ALGORITHM-COMPARISON.md) (15 min)
→ **OPTIONAL:** [07-PSO-ALGORITHM.md](./07-PSO-ALGORITHM.md) vs [08-ACO-ALGORITHM.md](./08-ACO-ALGORITHM.md)

#### ...data apa yang digunakan
→ **DIRECT:** [06-DATASET-DESCRIPTION.md](./06-DATASET-DESCRIPTION.md) (20 min)
→ **QUICK:** [01-QUICK-REFERENCE.md](./01-QUICK-REFERENCE.md) - Bagian "Datasets"

#### ...hasil akhir proyek
→ **DIRECT:** [04-RESULTS-SUMMARY.md](./04-RESULTS-SUMMARY.md) (10 min)
→ **VERIFICATION:** [10-COMPLETION-CHECKLIST.md](./10-COMPLETION-CHECKLIST.md)

#### ...cara membaca visualisasi
→ **DIRECT:** [09-VISUALIZATION-GUIDE.md](./09-VISUALIZATION-GUIDE.md) (15 min)

#### ...fitur yang dipilih ACO
→ **DIRECT:** [05-ACO-FEATURES.md](./05-ACO-FEATURES.md) (15 min)

#### ...detail implementasi PSO/ACO
→ **PSO:** [07-PSO-ALGORITHM.md](./07-PSO-ALGORITHM.md) (25 min)
→ **ACO:** [08-ACO-ALGORITHM.md](./08-ACO-ALGORITHM.md) (30 min)

#### ...status proyek lengkap
→ **DIRECT:** [10-COMPLETION-CHECKLIST.md](./10-COMPLETION-CHECKLIST.md) (10 min)

---

## 👥 ROLE-BASED READING PATHS

### 👔 Project Manager
**Goal:** Understand deliverables and status

1. [00-START-HERE.md](./00-START-HERE.md) - 3 min
2. [02-PROJECT-OVERVIEW.md](./02-PROJECT-OVERVIEW.md) - 10 min
3. [04-RESULTS-SUMMARY.md](./04-RESULTS-SUMMARY.md) - 10 min
4. [10-COMPLETION-CHECKLIST.md](./10-COMPLETION-CHECKLIST.md) - 10 min
5. [03-ALGORITHM-COMPARISON.md](./03-ALGORITHM-COMPARISON.md) - 15 min

**Total Time:** ~48 minutes
**Key Takeaways:** Deliverables ✓, Metrics ✓, Status ✓

---

### 💻 Developer
**Goal:** Understand code and run it

1. [00-START-HERE.md](./00-START-HERE.md) - 3 min
2. [01-QUICK-REFERENCE.md](./01-QUICK-REFERENCE.md) - 5 min
3. [07-PSO-ALGORITHM.md](./07-PSO-ALGORITHM.md) - 25 min
4. [08-ACO-ALGORITHM.md](./08-ACO-ALGORITHM.md) - 30 min
5. [02-PROJECT-OVERVIEW.md](./02-PROJECT-OVERVIEW.md) - 10 min

**Total Time:** ~73 minutes
**Key Takeaways:** Code ✓, How to run ✓, Implementation ✓

---

### 📊 Data Scientist
**Goal:** Understand data and features

1. [00-START-HERE.md](./00-START-HERE.md) - 3 min
2. [01-QUICK-REFERENCE.md](./01-QUICK-REFERENCE.md) - 5 min
3. [06-DATASET-DESCRIPTION.md](./06-DATASET-DESCRIPTION.md) - 20 min
4. [05-ACO-FEATURES.md](./05-ACO-FEATURES.md) - 15 min
5. [03-ALGORITHM-COMPARISON.md](./03-ALGORITHM-COMPARISON.md) - 15 min

**Total Time:** ~58 minutes
**Key Takeaways:** Data ✓, Features ✓, Analysis ✓

---

### 🏥 Medical Professional
**Goal:** Understand results in medical context

1. [00-START-HERE.md](./00-START-HERE.md) - 3 min
2. [01-QUICK-REFERENCE.md](./01-QUICK-REFERENCE.md) - 5 min
3. [04-RESULTS-SUMMARY.md](./04-RESULTS-SUMMARY.md) - 10 min
4. [09-VISUALIZATION-GUIDE.md](./09-VISUALIZATION-GUIDE.md) - 15 min
5. [03-ALGORITHM-COMPARISON.md](./03-ALGORITHM-COMPARISON.md) - 15 min

**Total Time:** ~48 minutes
**Key Takeaways:** Results ✓, Visualization ✓, Comparison ✓

---

## 📂 FILE LOCATION QUICK REFERENCE

| Arti | Lokasi | File |
|------|--------|------|
| **Entry Point** | docs/ | [00-START-HERE.md](./00-START-HERE.md) |
| **Cheat Sheet** | docs/ | [01-QUICK-REFERENCE.md](./01-QUICK-REFERENCE.md) |
| **Project Info** | docs/ | [02-PROJECT-OVERVIEW.md](./02-PROJECT-OVERVIEW.md) |
| **Algorithm Comparison** | docs/ | [03-ALGORITHM-COMPARISON.md](./03-ALGORITHM-COMPARISON.md) |
| **Results** | docs/ | [04-RESULTS-SUMMARY.md](./04-RESULTS-SUMMARY.md) |
| **Features (ACO)** | docs/ | [05-ACO-FEATURES.md](./05-ACO-FEATURES.md) |
| **Data Details** | docs/ | [06-DATASET-DESCRIPTION.md](./06-DATASET-DESCRIPTION.md) |
| **PSO Deep Dive** | docs/ | [07-PSO-ALGORITHM.md](./07-PSO-ALGORITHM.md) |
| **ACO Deep Dive** | docs/ | [08-ACO-ALGORITHM.md](./08-ACO-ALGORITHM.md) |
| **Plot Guide** | docs/ | [09-VISUALIZATION-GUIDE.md](./09-VISUALIZATION-GUIDE.md) |
| **Verification** | docs/ | [10-COMPLETION-CHECKLIST.md](./10-COMPLETION-CHECKLIST.md) |
| **Navigation** | docs/ | [11-NAVIGATION-GUIDE.md](./11-NAVIGATION-GUIDE.md) (ini) |
| **Master Index** | docs/ | [INDEX.md](./INDEX.md) |
| --- | --- | --- |
| **Raw Data** | datasets/ | dataset_bpm.json |
| **Optimized Data** | datasets/ | dataset_bpm_optimized.json |
| **Feature Matrix** | datasets/ | feature_matrix.csv |
| --- | --- | --- |
| **PSO Code** | pso/ | pso.py |
| **PSO Results** | pso/ | pso_results.json |
| **PSO Plots** | pso/ | 12 PNG files |
| --- | --- | --- |
| **ACO Code** | aco/ | aco.py |
| **ACO Results** | aco/ | aco_results.json |
| **ACO Plots** | aco/ | 13 PNG files |
| --- | --- | --- |
| **Helpers** | utils/ | helper.py |
| **Analysis** | utils/ | analyze_dataset.py |
| **Optimization** | utils/ | optimize_dataset.py |

---

## 🔗 CROSS-REFERENCE MAP

```
00-START-HERE
├── → 01-QUICK-REFERENCE
├── → 02-PROJECT-OVERVIEW
└── → Choose your role (Manager/Dev/DS/Medical)

01-QUICK-REFERENCE
├── → 04-RESULTS-SUMMARY (Results)
├── → 06-DATASET-DESCRIPTION (Datasets)
└── → 07-PSO-ALGORITHM or 08-ACO-ALGORITHM (Code)

02-PROJECT-OVERVIEW
├── → 04-RESULTS-SUMMARY (Results)
├── → 06-DATASET-DESCRIPTION (Data)
└── → 03-ALGORITHM-COMPARISON (Comparison)

03-ALGORITHM-COMPARISON
├── → 07-PSO-ALGORITHM (PSO Details)
├── → 08-ACO-ALGORITHM (ACO Details)
└── → 05-ACO-FEATURES (Features)

04-RESULTS-SUMMARY
├── → 09-VISUALIZATION-GUIDE (How to read plots)
├── → 05-ACO-FEATURES (Selected features)
└── → 10-COMPLETION-CHECKLIST (Verification)

05-ACO-FEATURES
├── → 06-DATASET-DESCRIPTION (Feature details)
├── → 08-ACO-ALGORITHM (Feature selection logic)
└── → 09-VISUALIZATION-GUIDE (Feature importance plot)

06-DATASET-DESCRIPTION
├── → 05-ACO-FEATURES (Feature list)
├── → 07-PSO-ALGORITHM (Threshold values)
└── → 08-ACO-ALGORITHM (Feature selection)

07-PSO-ALGORITHM
├── → 03-ALGORITHM-COMPARISON (vs ACO)
├── → 01-QUICK-REFERENCE (How to run)
└── → 04-RESULTS-SUMMARY (Results)

08-ACO-ALGORITHM
├── → 03-ALGORITHM-COMPARISON (vs PSO)
├── → 05-ACO-FEATURES (Selected features)
└── → 01-QUICK-REFERENCE (How to run)

09-VISUALIZATION-GUIDE
├── → 04-RESULTS-SUMMARY (Files)
├── → pso/ folder (BPM plots)
└── → aco/ folder (BPM plots)

10-COMPLETION-CHECKLIST
└── → All other files (References)

11-NAVIGATION-GUIDE (ini)
└── → All files (Master index)

INDEX.md (Master)
└── → All files (Central hub)
```

---

## 🎯 SEARCH PATTERNS

### Jika Anda mencari...

#### ...hasil akurasi
→ Cari di: [03-ALGORITHM-COMPARISON.md](./03-ALGORITHM-COMPARISON.md) - "Metrics"
→ Atau: [04-RESULTS-SUMMARY.md](./04-RESULTS-SUMMARY.md) - "Performance"

#### ...informasi BPM threshold
→ Cari di: [07-PSO-ALGORITHM.md](./07-PSO-ALGORITHM.md) - "Thresholds"
→ Atau: [01-QUICK-REFERENCE.md](./01-QUICK-REFERENCE.md) - "PSO Results"

#### ...nama fitur yang dipilih
→ Cari di: [05-ACO-FEATURES.md](./05-ACO-FEATURES.md) - "5 Selected Features"
→ Atau: [01-QUICK-REFERENCE.md](./01-QUICK-REFERENCE.md) - "ACO Features"

#### ...cara membaca plot BPM
→ Cari di: [09-VISUALIZATION-GUIDE.md](./09-VISUALIZATION-GUIDE.md) - "BPM Timeline"

#### ...data format/struktur
→ Cari di: [06-DATASET-DESCRIPTION.md](./06-DATASET-DESCRIPTION.md) - "Data Structure"

#### ...parameter algoritma
→ PSO: [07-PSO-ALGORITHM.md](./07-PSO-ALGORITHM.md) - "Parameters"
→ ACO: [08-ACO-ALGORITHM.md](./08-ACO-ALGORITHM.md) - "Parameters"

#### ...cara menjalankan kode
→ Cari di: [01-QUICK-REFERENCE.md](./01-QUICK-REFERENCE.md) - "How to Run"
→ Atau: [02-PROJECT-OVERVIEW.md](./02-PROJECT-OVERVIEW.md) - "Running"

#### ...confusion matrix
→ Cari di: [03-ALGORITHM-COMPARISON.md](./03-ALGORITHM-COMPARISON.md) - "Confusion Matrix"

#### ...file output yang tersedia
→ Cari di: [10-COMPLETION-CHECKLIST.md](./10-COMPLETION-CHECKLIST.md) - "Output Files"

---

## 📖 RECOMMENDED READING ORDER

### Level 1: Quick Overview (5-15 min)
1. [00-START-HERE.md](./00-START-HERE.md)
2. [01-QUICK-REFERENCE.md](./01-QUICK-REFERENCE.md)

### Level 2: Detailed Understanding (30-60 min)
Add to Level 1:
3. [02-PROJECT-OVERVIEW.md](./02-PROJECT-OVERVIEW.md)
4. [03-ALGORITHM-COMPARISON.md](./03-ALGORITHM-COMPARISON.md)
5. [04-RESULTS-SUMMARY.md](./04-RESULTS-SUMMARY.md)

### Level 3: Deep Dive (2+ hours)
Add to Level 2:
6. [05-ACO-FEATURES.md](./05-ACO-FEATURES.md)
7. [06-DATASET-DESCRIPTION.md](./06-DATASET-DESCRIPTION.md)
8. [07-PSO-ALGORITHM.md](./07-PSO-ALGORITHM.md)
9. [08-ACO-ALGORITHM.md](./08-ACO-ALGORITHM.md)
10. [09-VISUALIZATION-GUIDE.md](./09-VISUALIZATION-GUIDE.md)

### Level 4: Complete (2.5+ hours)
Add to Level 3:
11. [10-COMPLETION-CHECKLIST.md](./10-COMPLETION-CHECKLIST.md)

---

## 🚀 GETTING STARTED

### Langkah 1: Pahami Proyek
→ Baca: [00-START-HERE.md](./00-START-HERE.md) (3 min)

### Langkah 2: Lihat Overview
→ Baca: [02-PROJECT-OVERVIEW.md](./02-PROJECT-OVERVIEW.md) (10 min)

### Langkah 3: Lihat Hasil
→ Baca: [04-RESULTS-SUMMARY.md](./04-RESULTS-SUMMARY.md) (10 min)

### Langkah 4: Pilih Path Anda
- **Ingin tahu perbedaan?** → [03-ALGORITHM-COMPARISON.md](./03-ALGORITHM-COMPARISON.md)
- **Ingin analisa data?** → [06-DATASET-DESCRIPTION.md](./06-DATASET-DESCRIPTION.md)
- **Ingin baca code?** → [07-PSO-ALGORITHM.md](./07-PSO-ALGORITHM.md)
- **Ingin lihat plot?** → [09-VISUALIZATION-GUIDE.md](./09-VISUALIZATION-GUIDE.md)

### Langkah 5: Deep Dive (Opsional)
→ Baca file-file spesifik sesuai kebutuhan

---

## 💡 TIPS

1. **Start small**: Jangan baca semuanya sekaligus. Mulai dengan [00-START-HERE.md](./00-START-HERE.md)

2. **Follow links**: Setiap file memiliki link ke file lain yang relevan di bagian bawah

3. **Use INDEX**: [INDEX.md](./INDEX.md) memiliki tabel navigasi lengkap dengan read times

4. **Check Checklist**: [10-COMPLETION-CHECKLIST.md](./10-COMPLETION-CHECKLIST.md) menunjukkan apa saja yang sudah selesai

5. **Role-based**: Pilih reading path sesuai role Anda untuk efisiensi maksimal

6. **Bookmark**: Bookmark file yang sering Anda akses untuk akses cepat

---

## 📞 QUICK LINKS

- **Master Index:** [INDEX.md](./INDEX.md)
- **Start Here:** [00-START-HERE.md](./00-START-HERE.md)
- **Quick Ref:** [01-QUICK-REFERENCE.md](./01-QUICK-REFERENCE.md)
- **Results:** [04-RESULTS-SUMMARY.md](./04-RESULTS-SUMMARY.md)
- **Checklist:** [10-COMPLETION-CHECKLIST.md](./10-COMPLETION-CHECKLIST.md)

---

**Created:** 2025-11-27  
**Status:** ✅ All 12 Files Complete  
**Time to Read:** 5-10 minutes
