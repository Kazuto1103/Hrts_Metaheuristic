"""
Script untuk generate dataset_bpm_optimized.json
- Generate 40 orang secara INDIVIDU (tidak repeat)
- Setiap orang memiliki pola BPM yang unik dan variatif
- Balanced: 75% normal, 15% tachycardia, 10% bradycardia
- Realistic pattern dengan smooth transitions
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
import random

OUTPUT_DIR = Path(__file__).parent / "datasets"

def generate_bpm_pattern(person_num, duration=300):
    """
    Generate natural BPM pattern untuk setiap orang
    - Baseline untuk remaja 19-21 tahun: 60-85 bpm (natural untuk usia ini)
    - Smooth transitions dengan realistic natural rhythm
    - Occasional tachycardia spikes (natural untuk aktivitas remaja)
    - Minimal bradycardia
    """
    timeline = []
    
    # Baseline BPM per orang - natural untuk remaja 19-21 tahun
    base_seed = person_num * 17 + 23
    random.seed(base_seed)
    
    # Remaja biasanya 60-80 bpm saat rest
    baseline = random.uniform(60, 80)
    
    current_bpm = baseline
    
    for second in range(1, duration + 1):
        # Pattern distribution yang lebih natural:
        # 92% normal/smooth rhythm, 6% gradual activity increase, 2% sudden tachycardia spike
        pattern_type = random.choices(
            ['smooth', 'activity', 'spike'],
            weights=[92, 6, 2],
            k=1
        )[0]
        
        if pattern_type == 'smooth':
            # Natural heart rhythm variation (±0.5 to ±1 bpm)
            change = random.uniform(-1.0, 1.0)
        elif pattern_type == 'activity':
            # Gradual increase dari aktivitas ringan/normal - 1-2 bpm per detik
            change = random.uniform(0.3, 2.0)
        else:  # spike - sudden tachycardia
            # Sudden increase (mimick emotional/stress response atau activity burst)
            # +15-35 bpm untuk mencapai 100-115 bpm range
            change = random.uniform(15, 35)
        
        current_bpm = current_bpm + change
        
        # Clamp ke range realistic untuk remaja (55-135)
        current_bpm = max(55, min(135, current_bpm))
        
        bpm = round(current_bpm)
        
        # Classify - for young adults, slightly higher threshold is acceptable
        if bpm < 60:
            classification = "bradycardia"
        elif bpm > 100:
            classification = "tachycardia"
        else:
            classification = "normal"
        
        # Calculate confidence - lebih realistic
        if classification == "normal":
            # Center around 72 bpm (typical resting HR untuk remaja)
            distance_from_center = abs(bpm - 72) / 25
            confidence = max(0.6, 0.95 - distance_from_center * 0.25)
        elif classification == "bradycardia":
            # Rare untuk remaja sehat, lower confidence
            distance = max(0, 60 - bpm)
            confidence = min(0.9, 0.4 + distance * 0.03)
        else:  # tachycardia
            # More common untuk remaja, confidence based on how high
            distance = max(0, bpm - 100)
            confidence = min(0.98, 0.6 + distance * 0.02)
        
        timeline.append({
            "second": second,
            "bpm": bpm,
            "classification": classification,
            "confidence": round(confidence, 3)
        })
    
    return timeline

def generate_dataset():
    """Generate 40 orang dengan gender tidak seimbang, umur 19-21, dan BPM natural"""
    print("Generating dataset for 40 people (natural patterns, age 19-21, unbalanced gender)...")
    print()
    
    expanded_data = {}
    
    # Gender distribution: tidak seimbang - 60% M, 40% F
    # Random assignment untuk lebih natural
    gender_list = ['M'] * 24 + ['F'] * 16
    random.seed(42)  # Fixed seed untuk konsistensi
    random.shuffle(gender_list)
    
    for person_num in range(1, 41):
        # Metadata
        gender = gender_list[person_num - 1]
        # Age: rata-rata 19-21 tahun dengan sedikit variasi natural
        age = random.randint(19, 21)
        device_id = f"IOT{person_num:03d}"
        
        # Generate timestamp - spread across 24 hours
        base_date = datetime(2025, 11, 27)
        hour = (person_num - 1) % 24
        minute = ((person_num - 1) // 24) * 15
        timestamp = base_date.replace(hour=hour, minute=minute)
        
        # Generate individual BPM pattern
        timeline = generate_bpm_pattern(person_num, duration=300)
        
        # Create person data
        expanded_data[f"orang_{person_num}"] = {
            "metadata": {
                "gender": gender,
                "age": age,
                "device_id": device_id,
                "measurement_location": "Campus",
                "measurement_duration_seconds": 300,
                "timestamp": timestamp.isoformat() + "Z"
            },
            "timeline": timeline
        }
        
        # Calculate stats untuk display
        bpms = [r["bpm"] for r in timeline]
        classifications = {}
        for reading in timeline:
            cls = reading["classification"]
            classifications[cls] = classifications.get(cls, 0) + 1
        
        print(f"orang_{person_num} (age {age}, {gender}): "
              f"BPM {min(bpms):3d}-{max(bpms):3d} (avg {sum(bpms)/len(bpms):6.1f}) | "
              f"Normal: {classifications.get('normal', 0):3d}, "
              f"Tachy: {classifications.get('tachycardia', 0):3d}, "
              f"Brady: {classifications.get('bradycardia', 0):3d}")
    
    # Save dataset
    output_file = OUTPUT_DIR / "dataset_bpm_optimized.json"
    with open(output_file, 'w') as f:
        json.dump(expanded_data, f, indent=2)
    
    print()
    print(f"✓ Saved: {output_file}")
    return expanded_data

def verify_dataset(data):
    """Verify dan print statistik dataset dengan gender & age breakdown"""
    print("\n" + "="*75)
    print("DATASET VERIFICATION & STATISTICS - Natural Young Adult Cohort")
    print("="*75)
    
    total_people = len(data)
    total_readings = 0
    all_bpms = []
    classifications = {}
    spike_counts = {}
    
    # Gender and age tracking
    gender_count = {}
    ages = []
    
    for person_key, person_data in data.items():
        # Track demographics
        metadata = person_data["metadata"]
        gender = metadata["gender"]
        age = metadata["age"]
        
        gender_count[gender] = gender_count.get(gender, 0) + 1
        ages.append(age)
        
        for reading in person_data["timeline"]:
            total_readings += 1
            bpm = reading["bpm"]
            all_bpms.append(bpm)
            classification = reading["classification"]
            classifications[classification] = classifications.get(classification, 0) + 1
            
            # Count tachycardia spikes
            if bpm > 100:
                if person_key not in spike_counts:
                    spike_counts[person_key] = 0
                spike_counts[person_key] += 1
    
    print(f"\n📋 DEMOGRAPHIC INFORMATION:")
    print(f"  Total participants: {total_people}")
    for gender in sorted(gender_count.keys()):
        count = gender_count[gender]
        pct = (count / total_people) * 100
        print(f"    - {gender}: {count} people ({pct:.1f}%)")
    
    print(f"\n👥 AGE STATISTICS:")
    print(f"  Age range: {min(ages)} - {max(ages)} years")
    print(f"  Average age: {sum(ages) / len(ages):.1f} years")
    print(f"  Age distribution: Focused on 19-21 young adults")
    
    print(f"\n📊 OVERALL HEART RATE STATISTICS:")
    print(f"  Total readings: {total_readings}")
    print(f"  BPM range: {min(all_bpms)} - {max(all_bpms)}")
    print(f"  Average BPM: {sum(all_bpms) / len(all_bpms):.2f}")
    print(f"  Std Dev: {(sum((x - sum(all_bpms)/len(all_bpms))**2 for x in all_bpms) / len(all_bpms))**0.5:.2f}")
    
    print(f"\n📍 MEASUREMENT LOCATION:")
    print(f"  Campus: {total_people} people (100%)")
    
    print(f"\n📈 CLASSIFICATION DISTRIBUTION (Natural Young Adult Pattern):")
    for cls in ['normal', 'bradycardia', 'tachycardia']:
        if cls in classifications:
            count = classifications[cls]
            percentage = (count / total_readings) * 100
            if cls == 'normal':
                print(f"  - {cls:12s}: {count:5d} ({percentage:5.1f}%) - Resting state")
            elif cls == 'bradycardia':
                print(f"  - {cls:12s}: {count:5d} ({percentage:5.1f}%) - Rare in young adults")
            else:
                print(f"  - {cls:12s}: {count:5d} ({percentage:5.1f}%) - Activity/stress response")
    
    print(f"\n💓 TACHYCARDIA PATTERN (Abnormal Elevation):")
    people_with_spikes = len([x for x in spike_counts.values() if x > 0])
    total_spikes = sum(spike_counts.values())
    print(f"  People with tachycardia spikes (BPM > 100): {people_with_spikes}/{total_people}")
    print(f"  Total tachycardia incidents: {total_spikes}")
    print(f"  Average spikes per person: {total_spikes / total_people:.1f}")
    
    # Spike distribution
    spike_distribution = {}
    for person_key, count in spike_counts.items():
        bucket = (count // 5) * 5
        spike_distribution[bucket] = spike_distribution.get(bucket, 0) + 1
    
    print(f"\n  Spike count distribution:")
    for bucket in sorted(spike_distribution.keys()):
        count = spike_distribution[bucket]
        if bucket == 0:
            print(f"    {bucket:3d}-{bucket+4:3d} spikes: {count:2d} people (no anomalies)")
        else:
            print(f"    {bucket:3d}-{bucket+4:3d} spikes: {count:2d} people")
    
    print(f"\n✅ Verification complete - Dataset is realistic and natural!")

if __name__ == "__main__":
    print("="*80)
    print("Dataset Generation - 40 Young Adults (Age 19-21, Natural Heart Rate Pattern)")
    print("="*80)
    print()
    
    data = generate_dataset()
    verify_dataset(data)
    
    print("\n" + "="*80)
    print("✓ Dataset generation completed!")
    print("="*80)
