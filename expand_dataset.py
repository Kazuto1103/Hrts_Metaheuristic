"""
Script untuk memperluas dataset BPM dari 10 orang menjadi 40 orang
Mengikuti pola atribut yang sudah ada dengan variasi yang realistis
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Konfigurasi
PEOPLE_COUNT = 40
TIMELINE_SECONDS = 300
OUTPUT_DIR = Path(__file__).parent / "datasets"

# Data untuk variasi
GENDERS = ["M", "F"]
LOCATIONS = ["Campus", "Home", "Gym", "Office", "Hospital", "Park"]
AGES = list(range(18, 70))

# Pola BPM berdasarkan kondisi
BPM_PATTERNS = {
    "normal": {"min": 60, "max": 100, "mean": 75},
    "athletic": {"min": 55, "max": 95, "mean": 65},
    "high_stress": {"min": 80, "max": 130, "mean": 100},
    "resting": {"min": 50, "max": 75, "mean": 62},
}

# Classification rules
def classify_bpm(bpm):
    if bpm < 60:
        return "bradycardia"
    elif bpm > 100:
        return "tachycardia"
    else:
        return "normal"

def calculate_confidence(bpm, classification):
    """Hitung confidence score berdasarkan BPM dan klasifikasi"""
    if classification == "normal":
        # Semakin dekat ke tengah range (60-100), semakin tinggi confidence
        distance_from_center = abs(bpm - 80) / 20
        confidence = max(0.5, 1.0 - distance_from_center * 0.25)
    elif classification == "bradycardia":
        # Semakin jauh dari 60, semakin tinggi confidence
        distance = max(0, 60 - bpm)
        confidence = min(1.0, 0.5 + distance * 0.05)
    else:  # tachycardia
        # Semakin jauh dari 100, semakin tinggi confidence
        distance = max(0, bpm - 100)
        confidence = min(1.0, 0.5 + distance * 0.03)
    
    return round(confidence, 3)

def generate_timeline(person_num, age):
    """Generate timeline untuk satu orang dengan pola BPM realistis"""
    timeline = []
    
    # Pilih pola berdasarkan age
    if age < 25:
        pattern = BPM_PATTERNS["athletic"]
    elif age > 60:
        pattern = BPM_PATTERNS["high_stress"]
    else:
        pattern = BPM_PATTERNS["normal"]
    
    # Generate BPM values dengan variasi smooth
    current_bpm = pattern["mean"]
    base_noise = random.uniform(-5, 5)
    
    for second in range(1, TIMELINE_SECONDS + 1):
        # Tambahkan trend dan noise untuk membuat pattern lebih realistis
        trend = random.uniform(-0.3, 0.3)
        noise = random.uniform(-3, 3)
        
        current_bpm = current_bpm + trend + noise
        current_bpm = max(pattern["min"], min(pattern["max"], current_bpm))
        
        bpm = round(current_bpm)
        classification = classify_bpm(bpm)
        confidence = calculate_confidence(bpm, classification)
        
        timeline.append({
            "second": second,
            "bpm": bpm,
            "classification": classification,
            "confidence": confidence
        })
    
    return timeline

def generate_metadata(person_num):
    """Generate metadata untuk satu orang"""
    gender = random.choice(GENDERS)
    age = random.choice(AGES)
    
    # Generate device ID
    device_id = f"IOT{person_num:03d}"
    
    # Generate timestamp
    base_date = datetime(2025, 11, 27)
    random_hours = random.randint(0, 23)
    random_minutes = random.randint(0, 59)
    timestamp = base_date.replace(hour=random_hours, minute=random_minutes)
    
    return {
        "gender": gender,
        "age": age,
        "device_id": device_id,
        "measurement_location": random.choice(LOCATIONS),
        "measurement_duration_seconds": TIMELINE_SECONDS,
        "timestamp": timestamp.isoformat() + "Z"
    }

def expand_dataset_simple():
    """Expand dataset_bpm.json (simple version - hanya age dan timeline)"""
    print("Expanding dataset_bpm.json...")
    
    expanded_data = {}
    
    for person_num in range(1, PEOPLE_COUNT + 1):
        # Generate metadata dengan age saja
        age = random.choice(AGES)
        
        # Generate timeline
        timeline = generate_timeline(person_num, age)
        
        # Buat struktur sederhana (seperti original)
        expanded_data[f"orang_{person_num}"] = {
            "age": age,
            "timeline": [{"second": item["second"], "bpm": item["bpm"]} for item in timeline]
        }
        
        print(f"Generated orang_{person_num} (age {age})")
    
    # Save ke file
    output_file = OUTPUT_DIR / "dataset_bpm.json"
    with open(output_file, "w") as f:
        json.dump(expanded_data, f, indent=4)
    
    print(f"✓ Saved: {output_file}")
    return output_file

def expand_dataset_optimized():
    """Expand dataset_bpm_optimized.json (dengan metadata lengkap)"""
    print("\nExpanding dataset_bpm_optimized.json...")
    
    expanded_data = {}
    
    for person_num in range(1, PEOPLE_COUNT + 1):
        # Generate metadata lengkap
        metadata = generate_metadata(person_num)
        
        # Generate timeline
        timeline = generate_timeline(person_num, metadata["age"])
        
        # Buat struktur lengkap (seperti original)
        expanded_data[f"orang_{person_num}"] = {
            "metadata": metadata,
            "timeline": timeline
        }
        
        print(f"Generated orang_{person_num} (age {metadata['age']}, gender {metadata['gender']})")
    
    # Save ke file
    output_file = OUTPUT_DIR / "dataset_bpm_optimized.json"
    with open(output_file, "w") as f:
        json.dump(expanded_data, f, indent=2)
    
    print(f"✓ Saved: {output_file}")
    return output_file

def print_statistics(filename):
    """Print statistik dari file yang di-generate"""
    print(f"\n📊 Statistics for {filename.name}:")
    
    with open(filename, "r") as f:
        data = json.load(f)
    
    total_people = len(data)
    total_bpm_points = 0
    all_bpms = []
    all_classifications = {}
    age_distribution = {}
    
    for person_key, person_data in data.items():
        if "metadata" in person_data:
            age = person_data["metadata"]["age"]
            timeline = person_data["timeline"]
        else:
            age = person_data["age"]
            timeline = person_data["timeline"]
        
        age_distribution[age] = age_distribution.get(age, 0) + 1
        
        for entry in timeline:
            bpm = entry["bpm"]
            all_bpms.append(bpm)
            total_bpm_points += 1
            
            if "classification" in entry:
                classification = entry["classification"]
                all_classifications[classification] = all_classifications.get(classification, 0) + 1
    
    # Hitung statistik
    min_bpm = min(all_bpms)
    max_bpm = max(all_bpms)
    avg_bpm = sum(all_bpms) / len(all_bpms)
    
    print(f"  Total people: {total_people}")
    print(f"  Total BPM measurements: {total_bpm_points}")
    print(f"  Age range: {min(age_distribution.keys())} - {max(age_distribution.keys())}")
    print(f"  BPM range: {min_bpm} - {max_bpm}")
    print(f"  Average BPM: {avg_bpm:.2f}")
    
    if all_classifications:
        print(f"  Classifications:")
        for cls, count in sorted(all_classifications.items()):
            percentage = (count / total_bpm_points) * 100
            print(f"    - {cls}: {count} ({percentage:.1f}%)")

if __name__ == "__main__":
    print("=" * 60)
    print("Dataset Expansion Script - 10 to 40 People")
    print("=" * 60)
    
    # Expand both datasets
    file1 = expand_dataset_simple()
    file2 = expand_dataset_optimized()
    
    # Print statistics
    print_statistics(file1)
    print_statistics(file2)
    
    print("\n" + "=" * 60)
    print("✓ Dataset expansion completed!")
    print("=" * 60)
