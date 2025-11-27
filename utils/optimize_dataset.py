import json
import numpy as np
from datetime import datetime
from scipy import stats

def calculate_statistical_features(bpm_values):
    """
    Menghitung fitur statistik dari nilai BPM untuk machine learning
    """
    bpm_array = np.array(bpm_values)
    
    # Calculate successive differences (RR intervals)
    rr_intervals = np.diff(bpm_array)
    
    features = {
        "mean_bpm": float(np.mean(bpm_array)),
        "std_dev_bpm": float(np.std(bpm_array)),
        "min_bpm": float(np.min(bpm_array)),
        "max_bpm": float(np.max(bpm_array)),
        "median_bpm": float(np.median(bpm_array)),
        "variance": float(np.var(bpm_array)),
        "range_bpm": float(np.max(bpm_array) - np.min(bpm_array)),
        
        # Heart Rate Variability features
        "rmssd": float(np.sqrt(np.mean(rr_intervals ** 2))),  # Root Mean Square of Successive Differences
        "nnxx": float(np.sum(np.abs(rr_intervals) > 5) / len(rr_intervals) * 100),  # % successive differences > 5
        "cvnn": float(np.std(bpm_array) / np.mean(bpm_array)) if np.mean(bpm_array) > 0 else 0,  # Coefficient of Variation
        
        # Distribution features
        "skewness": float(stats.skew(bpm_array)),  # Asimetri distribusi
        "kurtosis": float(stats.kurtosis(bpm_array)),  # Keruncingan distribusi
        
        # Quantiles
        "q25": float(np.percentile(bpm_array, 25)),
        "q75": float(np.percentile(bpm_array, 75)),
        "iqr": float(np.percentile(bpm_array, 75) - np.percentile(bpm_array, 25)),
    }
    
    return features

def classify_bpm_reading(bpm_value):
    """
    Klasifikasi BPM reading berdasarkan nilai standar medis
    """
    if bpm_value < 60:
        return "bradycardia"
    elif 60 <= bpm_value <= 100:
        return "normal"
    elif 100 < bpm_value <= 120:
        return "elevated"
    else:
        return "tachycardia"

def load_and_optimize_dataset():
    """
    Memuat dataset lama dan mengoptimalkannya dengan fitur baru
    """
    with open('dataset_bpm.json', 'r') as f:
        old_data = json.load(f)
    
    # Metadata realistis dari IoT (simulasi pengumpulan real)
    persons_metadata = {
        "orang_1": {"gender": "M", "age": 20, "device_id": "IOT001", "location": "Home"},
        "orang_2": {"gender": "F", "age": 22, "device_id": "IOT002", "location": "Office"},
        "orang_3": {"gender": "M", "age": 25, "device_id": "IOT003", "location": "Gym"},
        "orang_4": {"gender": "F", "age": 28, "device_id": "IOT004", "location": "Home"},
        "orang_5": {"gender": "M", "age": 30, "device_id": "IOT005", "location": "Office"},
        "orang_6": {"gender": "F", "age": 23, "device_id": "IOT006", "location": "Home"},
        "orang_7": {"gender": "M", "age": 26, "device_id": "IOT007", "location": "Gym"},
        "orang_8": {"gender": "F", "age": 24, "device_id": "IOT008", "location": "Office"},
        "orang_9": {"gender": "M", "age": 21, "device_id": "IOT009", "location": "Home"},
        "orang_10": {"gender": "F", "age": 27, "device_id": "IOT010", "location": "Home"},
    }
    
    optimized_data = {}
    
    for person_key, person_data in old_data.items():
        print(f"Processing {person_key}...")
        
        metadata = persons_metadata.get(person_key, {})
        
        # Extract timeline BPM values
        timeline = person_data.get("timeline", [])
        bpm_values = [reading["bpm"] for reading in timeline]
        
        # Extract normal dan abnormal
        normal_bpm = person_data.get("normal_bpm", [])
        abnormal_bpm = person_data.get("abnormal_bpm", [])
        
        normal_bpm_values = [reading["bpm"] for reading in normal_bpm]
        abnormal_bpm_values = [reading["bpm"] for reading in abnormal_bpm]
        
        # Calculate features
        overall_features = calculate_statistical_features(bpm_values)
        normal_features = calculate_statistical_features(normal_bpm_values) if normal_bpm_values else {}
        abnormal_features = calculate_statistical_features(abnormal_bpm_values) if abnormal_bpm_values else {}
        
        # Enhance timeline dengan classification dan confidence
        enhanced_timeline = []
        for i, reading in enumerate(timeline):
            bpm_val = reading["bpm"]
            classification = classify_bpm_reading(bpm_val)
            
            # Calculate confidence based on how far from boundaries
            if classification == "normal":
                confidence = 1.0 - (min(abs(bpm_val - 60), abs(bpm_val - 100)) / 40)
            elif classification == "bradycardia":
                confidence = min(1.0, (60 - bpm_val) / 60)
            elif classification == "tachycardia":
                confidence = min(1.0, (bpm_val - 100) / 100)
            else:  # elevated
                confidence = 1.0 - (bpm_val - 100) / 20
            
            enhanced_timeline.append({
                "second": reading["second"],
                "bpm": bpm_val,
                "classification": classification,
                "confidence": max(0, min(1.0, float(confidence)))
            })
        
        # Enhance abnormal BPM dengan duration dan severity
        enhanced_abnormal = []
        for i, abnormal_reading in enumerate(abnormal_bpm):
            bpm_val = abnormal_reading["bpm"]
            second_val = abnormal_reading["second"]
            
            # Tentukan severity berdasarkan deviation dari normal range
            if bpm_val < 60:
                deviation = 60 - bpm_val
                severity = min(100, (deviation / 60) * 100)
                type_abnormal = "bradycardia"
            else:
                deviation = bpm_val - 100
                severity = min(100, (deviation / 100) * 100)
                type_abnormal = "tachycardia"
            
            enhanced_abnormal.append({
                "second": second_val,
                "bpm": bpm_val,
                "type": type_abnormal,
                "severity_percentage": float(severity),
                "deviation_from_normal": float(deviation)
            })
        
        # Build optimized person data
        optimized_data[person_key] = {
            # Metadata IoT
            "metadata": {
                "gender": metadata.get("gender"),
                "age": person_data.get("age"),
                "device_id": metadata.get("device_id"),
                "measurement_location": metadata.get("location"),
                "measurement_duration_seconds": 300,
                "timestamp": "2025-11-27T" + f"{8 + int(person_key[-1]) % 8}:{int(person_key[-1]) * 6 % 60:02d}:00Z"
            },
            
            # Timeline dengan enhanced features
            "timeline": enhanced_timeline,
            
            # Aggregated features untuk ML
            "statistics": {
                "overall": overall_features,
                "normal_period": normal_features,
                "abnormal_period": abnormal_features,
                "data_quality": {
                    "total_readings": len(timeline),
                    "normal_count": len(normal_bpm),
                    "abnormal_count": len(abnormal_bpm),
                    "abnormal_percentage": float((len(abnormal_bpm) / len(timeline) * 100) if timeline else 0)
                }
            },
            
            # Classification results
            "classifications": {
                "normal_bpm_readings": normal_bpm,
                "abnormal_bpm_readings": enhanced_abnormal
            }
        }
    
    return optimized_data

def save_optimized_dataset(data, filename):
    """
    Simpan dataset yang sudah dioptimalkan
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✓ Optimized dataset saved to {filename}")

if __name__ == "__main__":
    print("🔄 Optimizing BPM Dataset...")
    print("=" * 50)
    
    optimized = load_and_optimize_dataset()
    save_optimized_dataset(optimized, 'dataset_bpm_optimized.json')
    
    # Show sample dari hasil
    print("\n📊 Sample dari optimized data (orang_1):")
    print(json.dumps(optimized["orang_1"], indent=2)[:1500] + "\n...")
    
    print("\n✓ Optimization Complete!")
