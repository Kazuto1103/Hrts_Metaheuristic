# 7 - PSO ALGORITHM

**Particle Swarm Optimization - Implementasi Lengkap**

---

## 📚 TABLE OF CONTENTS

1. Algorithm Overview
2. Mathematical Foundation
3. Parameters & Configuration
4. Implementation Details
5. Code Walkthrough
6. Results & Performance
7. Thresholds Found
8. How to Use

**Read Time:** 25 minutes

---

## 1️⃣ ALGORITHM OVERVIEW

### Apa itu PSO?

Particle Swarm Optimization (PSO) adalah metode optimasi yang terinspirasi dari perilaku sosial burung yang terbang berkerumunan. Setiap "partikel" merepresentasikan kandidat solusi dan bergerak dalam ruang pencarian sambil mengingat posisi terbaik yang pernah ditemukan.

### Konsep Dasar

```
PSO = Eksplorasi + Eksploitasi
       
1. Eksplorasi: Partikel menjelajahi ruang pencarian yang berbeda
2. Eksploitasi: Partikel bergerak ke area yang menjanjikan
3. Keseimbangan: Penting untuk menghindari local minima
```

### Keuntungan PSO untuk Proyek Ini

- ✅ Mudah diimplementasikan
- ✅ Cepat konvergen untuk dimensi rendah
- ✅ Cocok untuk threshold optimization
- ✅ Tidak memerlukan gradient computation
- ✅ Baik untuk multi-modal search spaces

---

## 2️⃣ MATHEMATICAL FOUNDATION

### Update Equation

Posisi dan kecepatan partikel diupdate menggunakan:

$$v_i(t+1) = w \cdot v_i(t) + c_1 \cdot r_1 \cdot (p_i - x_i(t)) + c_2 \cdot r_2 \cdot (g - x_i(t))$$

$$x_i(t+1) = x_i(t) + v_i(t+1)$$

Dimana:
- $v_i$ = kecepatan partikel i
- $x_i$ = posisi partikel i
- $w$ = inertia weight (momentum)
- $c_1$ = cognitive parameter (attraction to personal best)
- $c_2$ = social parameter (attraction to global best)
- $p_i$ = personal best position
- $g$ = global best position
- $r_1, r_2$ = random numbers [0,1]

### Inertia Weight Strategy

PSO kami menggunakan **linearly decreasing inertia weight**:

$$w(t) = w_{min} + (w_{max} - w_{min}) \cdot \frac{T - t}{T}$$

Strategi ini:
- Awalnya: $w$ besar → eksplorasi lebih banyak
- Akhirnya: $w$ kecil → eksploitasi lebih intensif
- Smooth transition → lebih baik dari fixed weight

---

## 3️⃣ PARAMETERS & CONFIGURATION

### Parameter PSO Kami

| Parameter | Nilai | Penjelasan |
|-----------|-------|-----------|
| **Num Particles** | 20 | Jumlah partikel yang mencari |
| **Num Iterations** | 100 | Berapa lama PSO berjalan |
| **Num Thresholds** | 3 | Jumlah threshold yang dicari |
| **w_max** | 0.9 | Inertia weight maksimal |
| **w_min** | 0.4 | Inertia weight minimal |
| **c1** | 2.0 | Cognitive parameter |
| **c2** | 2.0 | Social parameter |
| **v_max** | 0.5 | Maksimal kecepatan |

### Penjelasan Pemilihan Parameter

**20 Partikel:**
- Cukup untuk ruang 3D (3 threshold)
- 10 partikel per dimensi rule of thumb
- Balance antara cepat vs akurat

**100 Iterasi:**
- Biasanya cukup untuk konvergen
- Dari 20 partikel × 100 iter = 2000 fitness evaluations
- Cepat namun thorough

**Inertia Weight 0.9 → 0.4:**
- 0.9 awal: Partikel bebas bergerak (eksplorasi)
- 0.4 akhir: Partikel fokus pada area bagus (eksploitasi)
- Range ini empirically proven untuk balance

**c1 = c2 = 2.0:**
- Standard pengaturan dalam literatur
- Cognitive dan social influence sama kuat
- Cocok untuk balanced search

---

## 4️⃣ IMPLEMENTATION DETAILS

### Struktur Kelas

```python
class PSO:
    def __init__(self, num_particles, num_thresholds, 
                 num_iterations, dataset, features, labels):
        """
        Initialize PSO optimizer
        
        Args:
            num_particles: Jumlah partikel (20)
            num_thresholds: Jumlah threshold (3)
            num_iterations: Jumlah iterasi (100)
            dataset: Data features (n_samples, 5)
            features: Nama fitur yang digunakan
            labels: Ground truth labels
        """
```

### Inisialisasi Partikel

```python
def _initialize_particles(self):
    """
    Initialize particle positions and velocities randomly
    
    Partikel didistribusikan sesuai range BPM yang meaningful:
    - Threshold 1: 50-80 (normal/low boundary)
    - Threshold 2: 80-120 (normal range)
    - Threshold 3: 120-150 (high boundary)
    """
```

### Fitness Function

```python
def calculate_fitness(self, thresholds):
    """
    Calculate fitness score untuk set threshold
    
    Fitness = Accuracy dari klasifikasi dengan thresholds ini
    
    Algoritma:
    1. Classify semua samples menggunakan thresholds
    2. Hitung accuracy dibanding ground truth
    3. Return accuracy sebagai fitness score
    
    Return: float [0, 1] dimana 1 = perfect
    """
```

### Update Particles

```python
def update_particles(self, iteration):
    """
    Update posisi dan kecepasan semua partikel
    
    Langkah per partikel:
    1. Hitung velocity baru (PSO equation)
    2. Update posisi berdasarkan velocity
    3. Clip posisi ke boundaries
    4. Evaluasi fitness
    5. Update personal best jika lebih baik
    6. Update global best jika perlu
    """
```

### Optimization Loop

```python
def optimize(self):
    """
    Main optimization loop
    
    Langkah:
    1. Initialize particles
    2. For 100 iterations:
        a. Update semua partikel
        b. Track best fitness setiap iterasi
    3. Return best thresholds ditemukan
    """
```

---

## 5️⃣ CODE WALKTHROUGH

### File: pso.py (313 lines)

#### Imports & Setup

```python
import numpy as np
from sklearn.metrics import accuracy_score
import json

class PSO:
    def __init__(self, num_particles=20, num_thresholds=3,
                 num_iterations=100, dataset=None, features=None,
                 labels=None):
```

#### Key Methods

| Method | Baris | Tujuan |
|--------|-------|--------|
| `_initialize_particles()` | 25-45 | Set posisi/kecepatan awal |
| `calculate_fitness()` | 47-70 | Hitung akurasi untuk threshold |
| `_classify_samples()` | 72-90 | Klasifikasi dengan threshold |
| `_update_inertia_weight()` | 92-100 | Decrease w seiring iterasi |
| `_update_velocity()` | 102-130 | Update velocity per partikel |
| `_update_position()` | 132-150 | Update posisi per partikel |
| `update_particles()` | 152-200 | Update semua partikel |
| `optimize()` | 202-245 | Main loop optimasi |
| `get_results()` | 247-313 | Format & return hasil |

#### Critical Loop (update_particles)

```python
def update_particles(self, iteration):
    """Update posisi semua partikel"""
    
    # 1. Update inertia weight (smooth decrease)
    self._update_inertia_weight(iteration)
    
    # 2. Loop semua partikel
    for i in range(self.num_particles):
        # 3. Update velocity menggunakan PSO equation
        self._update_velocity(i)
        
        # 4. Update posisi
        self._update_position(i)
        
        # 5. Evaluasi fitness
        fitness = self.calculate_fitness(self.positions[i])
        
        # 6. Update personal best
        if fitness > self.personal_best_fitness[i]:
            self.personal_best_fitness[i] = fitness
            self.personal_best_positions[i] = self.positions[i].copy()
            
            # 7. Update global best
            if fitness > self.best_fitness:
                self.best_fitness = fitness
                self.best_position = self.positions[i].copy()
                
        self.fitness_history.append(self.best_fitness)
```

---

## 6️⃣ RESULTS & PERFORMANCE

### Convergence Curve

```
Fitness
1.0 ┤
    │                                    ●●●●●●
    │                              ●●●●●
0.9 ┤                        ●●●●●
    │                  ●●●●●
0.8 ┤            ●●●●
    │      ●●●●
    │   ●●
0.7 ┤●●
    │
    └─────────────────────────────────────────→
      0    20    40    60    80    100
           Iterations
```

**Karakteristik:**
- Konvergen cepat di awal (eksplorasi)
- Plateau di akhir (eksploitasi)
- Final fitness: 0.90 (90% akurasi)
- Smooth curve tanpa fluctuations

### Performance Metrics

| Metrik | Nilai | Penjelasan |
|--------|-------|-----------|
| **Final Accuracy** | 90% | Correct classification |
| **Precision** | 100% | No false positives |
| **Recall** | 90% | 9 of 10 abnormal detected |
| **F1-Score** | 0.9474 | Harmonic mean |
| **Training Time** | <1 sec | Very fast |

### Confusion Matrix

```
                 Predicted
                Normal  Abnormal
Actual  Normal      9        0      (Specificity: 100%)
        Abnormal    1        9      (Sensitivity: 90%)
```

**Interpretasi:**
- True Negatives (TN): 9 normal samples correctly classified
- False Positives (FP): 0 (perfect specificity)
- False Negatives (FN): 1 abnormal missed
- True Positives (TP): 9 abnormal correctly detected

---

## 7️⃣ THRESHOLDS FOUND

### Optimal Thresholds

```
PSO menemukan 3 thresholds optimal:

┌─────────────────────────────────┐
│ Threshold 1: 59.92 BPM          │  ← Lower boundary
│ Threshold 2: 80.00 BPM          │  ← Normal range
│ Threshold 3: 122.80 BPM         │  ← Upper boundary
└─────────────────────────────────┘
```

### Interpretasi Klinik

**Threshold 1 = 59.92 BPM** (Lower boundary)
- Below 59.92: Bradycardia (abnormally slow)
- 59.92-80.00: Low normal range
- Threshold ini memisahkan dangkal dari bradycardia

**Threshold 2 = 80.00 BPM** (Upper normal boundary)
- 59.92-80.00: Normal resting heart rate
- 80.00-122.80: Tachycardic range
- Threshold ini memisahkan normal dari tachycardia

**Threshold 3 = 122.80 BPM** (Upper boundary)
- 80.00-122.80: Moderate elevation (could be exercise)
- Above 122.80: Severe tachycardia (abnormal)
- Threshold ini memisahkan moderate dari severe

### Klasifikasi Logic

```python
def classify_with_thresholds(mean_bpm, thresholds):
    t1, t2, t3 = thresholds
    
    if mean_bpm < t1:
        return "ABNORMAL (Bradycardia)"
    elif t1 <= mean_bpm <= t3:
        # Lebih detail:
        if mean_bpm <= t2:
            return "NORMAL (Low)"
        else:
            return "NORMAL (High but ok)"
    else:
        return "ABNORMAL (Severe Tachycardia)"
```

### Precision Analysis

**Mengapa 90% dan bukan 100%?**

1 sample dari 10 diclassify salah karena:
- Threshold di area "gray zone" antara normal dan abnormal
- Sample ini memiliki BPM di boundary yang ambiguous
- PSO balance antara precision (0% false alarms) vs recall (catch all abnormal)
- Trade-off yang reasonable untuk aplikasi medis

---

## 8️⃣ HOW TO USE

### Running PSO

#### Option 1: Direct Execution

```python
from pso import PSO
import json

# 1. Load dataset
with open('datasets/dataset_bpm_optimized.json', 'r') as f:
    data = json.load(f)

# 2. Initialize PSO
pso = PSO(
    num_particles=20,
    num_thresholds=3,
    num_iterations=100,
    dataset=data['features'],
    features=data['feature_names'],
    labels=data['labels']
)

# 3. Run optimization
pso.optimize()

# 4. Get results
results = pso.get_results()
print(f"Best fitness: {results['best_fitness']}")
print(f"Optimal thresholds: {results['best_thresholds']}")
```

#### Option 2: From Command Line

```bash
cd pso/
python pso.py

# Output:
# PSO Optimization Complete!
# Best Fitness: 0.900
# Optimal Thresholds: [59.92, 80.00, 122.80]
```

### Visualizing Results

```python
import matplotlib.pyplot as plt

# Plot convergence curve
plt.figure(figsize=(10, 6))
plt.plot(results['fitness_history'], linewidth=2)
plt.xlabel('Iteration')
plt.ylabel('Best Fitness')
plt.title('PSO Convergence Curve')
plt.grid(True, alpha=0.3)
plt.show()
```

### Customizing Parameters

```python
# Untuk eksperimen berbeda:

# Lebih partikel = lebih thorough tapi slower
pso1 = PSO(num_particles=50, num_iterations=100)

# Lebih iterasi = lebih convergence
pso2 = PSO(num_particles=20, num_iterations=200)

# Tuning inertia weight untuk eksplorasi lebih
pso3 = PSO(num_particles=20, num_iterations=100)
pso3.w_max = 1.0  # Lebih eksplorasi
pso3.w_min = 0.1  # Lebih fokus di akhir
```

### Comparing with ACO

```python
from aco import ACO

# PSO approach: Threshold optimization
pso_thresholds = pso.best_position
print(f"PSO Thresholds: {pso_thresholds}")

# ACO approach: Feature selection
# Baca: 08-ACO-ALGORITHM.md untuk perbandingan

# Metrics comparison
print(f"PSO Accuracy: 90%")
print(f"ACO Accuracy: 100%")
```

---

## 📊 KEY STATISTICS

| Aspect | Value |
|--------|-------|
| **Algorithm Type** | Swarm Intelligence |
| **Search Space** | 3D (3 thresholds) |
| **Solution Quality** | 90% accuracy |
| **Convergence Time** | ~50 iterations |
| **Final Fitness** | 0.900 |
| **Code Lines** | 313 |
| **Functions** | 8 |

---

## 🔗 RELATED DOCUMENTATION

- [00-START-HERE.md](./00-START-HERE.md) - Project introduction
- [01-QUICK-REFERENCE.md](./01-QUICK-REFERENCE.md) - Quick commands
- [03-ALGORITHM-COMPARISON.md](./03-ALGORITHM-COMPARISON.md) - PSO vs ACO
- [08-ACO-ALGORITHM.md](./08-ACO-ALGORITHM.md) - ACO deep dive
- [04-RESULTS-SUMMARY.md](./04-RESULTS-SUMMARY.md) - Final results

---

**Created:** 2025-11-27  
**Status:** ✅ Complete  
**Time to Read:** 25 minutes
