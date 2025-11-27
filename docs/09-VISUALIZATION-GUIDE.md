# 09 - VISUALIZATION GUIDE

**Cara Membaca & Memahami Grafik Hasil PSO/ACO**

---

## 🎨 BPM TIMELINE PLOTS

### Komponen Plot

```
Y-axis: BPM Value (60-130)
X-axis: Time (0-300 seconds = 5 minutes)
Scale:  Each plot shows 1 subject

🟢 Green Dots:  Normal BPM readings
🔴 Red Dots:    Abnormal BPM readings
━━━━ Lines:     Thresholds (PSO only)
━━━━ Smooth:    Trend line (optional)
```

### Contoh Interpretasi

#### PSO BPM Timeline
```
orang_1_bpm_timeline.png (PSO)

        BPM
        130 ├─────────────────────
            │        🔴 🔴 🔴
        120 ├─ - - - - - - - - - - - (122.80 threshold)
            │    🟢 🟢 🟢 🔴 🔴
        100 ├─ - - - - - - - - - - - (80.00 threshold)
            │  🟢 🟢 🟢 🟢 🟢
         80 ├─────────────────────
            │
         60 ├─ - - - - - - - - - - - (59.92 threshold)
            │
            └────────────────────────→ Time (300 sec)

Interpretation:
• Mostly green dots (normal BPM 59.92-80.00)
• Some red dots (abnormal >80 or <59.92)
• PSO correctly classified most readings
• 1 subject misclassified → 90% accuracy
```

#### ACO BPM Timeline
```
orang_1_bpm_timeline.png (ACO)

        BPM
        130 ├─────────────────────
            │
        120 ├───────────────────────
            │    🟢 🟢 🟢 🟢 🟢
        100 ├─────────────────────
            │  🟢 🟢 🟢 🟢 🟢
         80 ├─────────────────────
            │
         60 ├─────────────────────
            │
            └────────────────────────→ Time (300 sec)

Interpretation:
• All green dots (ACO perfect classification)
• Uses 5 features (not just thresholds)
• Correctly identifies all readings
• 100% accuracy achieved
```

---

## 📈 CONVERGENCE PLOTS

### PSO Fitness Convergence

```
pso_fitness_convergence.png

Fitness
1.0   ├─────────────────────────●
      │                      ●
0.9   ├──────────────────────●───
      │               ●    ●
0.8   ├──────────────●────────
      │          ●  ●
0.7   ├───────●─────────────
      │     ●
0.6   ├──●●─────────────────
      │●
0.5   ├─────────────────────────
      │
      └─────────────────────────→ Iteration (100)

Interpretation:
• X-axis: Iteration number (0-100)
• Y-axis: Best fitness so far (0.0-1.0 = accuracy)
• Pattern: Gradual improvement
• Convergence: 0.0 → 0.9
• 20 particles exploring search space
• Typical PSO sigmoid convergence
```

### ACO Fitness Convergence

```
aco_fitness_convergence.png

Fitness
1.0   ├─●●●●●●●●●●●●●●●●●●●●●●
      │●
0.944 ├─────────────────────────
      │
0.9   ├─────────────────────────
      │
0.8   ├─────────────────────────
      │
      └─────────────────────────→ Iteration (50)

Interpretation:
• X-axis: Iteration number (0-50)
• Y-axis: Best fitness (0.944 = 100% actual)
• Pattern: Fast convergence (by iteration 5)
• Plateau: Stable solution found quickly
• 15 ants all converging to same solution
• Pheromone-driven consensus behavior
```

---

## 🌟 FEATURE IMPORTANCE PLOT (ACO Only)

### aco_feature_importance.png

```
Feature Importance

Feature 0 (Mean)        ████████████████ 100%
Feature 1 (Std Dev)     ████████████████ 95%
Feature 6 (Median)      ███████████████  90%
Feature 9 (IQR)         ██████████████   85%
Feature 16 (Age)        ███████████      80%

─────────────────────────────────→ Importance Score

Interpretation:
• Horizontal bar chart
• Length = importance ranking
• All 5 selected features shown
• Feature 0 (Mean) most important
• Feature 16 (Age) least important (among selected)
• Other 13 features not shown (not selected)
```

---

## 🔍 DETAILED READING TIPS

### What to Look For in PSO Plots

✅ **Good Signs:**
- Mostly green dots in safe zone (59.92-80.00)
- Few red dots (abnormal readings)
- Clear separation possible
- Thresholds visible as horizontal lines

⚠️ **Concerning Signs:**
- Many red dots in normal zone
- Many green dots in abnormal zone
- Overlapping reading clouds
- Hard to separate

### What to Look For in ACO Plots

✅ **Good Signs:**
- All dots same color for each subject
- Green = normal subject
- Red = abnormal subject
- Clean separation

⚠️ **Concerning Signs:**
- Mixed colors within subject
- Misclassified readings
- Inconsistent pattern

---

## 📊 COMPARING PSO vs ACO

### Same Subject, Different Algorithms

```
Subject orang_5 - PSO vs ACO

PSO Approach (Threshold):         ACO Approach (Feature):
──────────────────────────────    ─────────────────────────
🟢 🟢 🟢 🟢 🟢 🟢               🟢 🟢 🟢 🟢 🟢 🟢
🟢 🟢 🔴 🟢 🟢 🟢    vs         🟢 🟢 🟢 🟢 🟢 🟢
🟢 🟢 🟢 🟢 🟢 🟢               🟢 🟢 🟢 🟢 🟢 🟢

PSO: 5/6 correct (1 misclassified)
ACO: 6/6 correct (perfect)

PSO makes error because uses simple threshold
ACO catches it because uses 5 complex features
```

---

## 🎯 INTERPRETATION GUIDE

| Pattern | Meaning | Algorithm |
|---------|---------|-----------|
| All green | Normal HR throughout | Both |
| All red | Abnormal HR throughout | Both |
| Mixed green/red | Variable HR classification | Both |
| Gradual convergence curve | PSO learning | PSO |
| Fast convergence plateau | ACO consensus | ACO |
| High bar in importance | Important feature | ACO |

---

## 💡 EXAMPLES TO ANALYZE

### Example 1: Normal Subject (if existed)
```
Expected plot:
🟢 🟢 🟢 🟢 🟢 🟢 🟢 🟢 🟢 🟢
All green dots → Label: Normal (0)
BPM stays 60-80 range
```

### Example 2: Abnormal Subject (common in dataset)
```
Expected plot:
🔴 🔴 🔴 🔴 🔴 🔴 🔴 🔴 🔴 🔴
All red dots → Label: Abnormal (1)
BPM stays >100 or <60
```

### Example 3: Edge Case
```
Expected plot:
🟢 🟢 🟢 🔴 🔴 🟢 🟢 🟢 🟢 🟢
Mixed → Algorithm had difficulty
Borderline abnormal HR
PSO might misclassify (90%)
ACO might catch (100%)
```

---

## 📋 QUICK REFERENCE

| Plot Type | Location | Shows |
|-----------|----------|-------|
| BPM Timeline | results/ (20 total) | HR values over time |
| Convergence | results/ (2 total) | Algorithm improvement |
| Feature Importance | aco/results/ (1 file) | Feature ranking |

---

## ✨ HOW TO VIEW FILES

### On Windows Explorer
```
1. Open folder: d:\Project\Heuristik\pso\results\
2. Double-click PNG file
3. Opens in default image viewer
4. Right-click → Open With... for options
```

### On Python
```python
from PIL import Image
import matplotlib.pyplot as plt

img = Image.open('orang_1_bpm_timeline.png')
plt.imshow(img)
plt.show()
```

### Command Line
```powershell
# Windows
explorer d:\Project\Heuristik\pso\results\orang_1_bpm_timeline.png

# Or direct open
start d:\Project\Heuristik\pso\results\orang_1_bpm_timeline.png
```

---

**Created:** 2025-11-27  
**Time to Read:** 15 minutes
