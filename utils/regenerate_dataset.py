"""
Script untuk regenerate dataset_bpm_optimized.json
- Expand dari pattern 10 orang pertama
- Duplicate pattern ke orang 11-40
- Set semua measurement_location ke "Campus"
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
import copy

OUTPUT_DIR = Path(__file__).parent / "datasets"

def expand_dataset_from_pattern():
    """Regenerate dataset dengan pattern dari 10 orang pertama"""
    
    print("Loading original dataset...")
    original_file = OUTPUT_DIR / "dataset_bpm_optimized.json"
    
    with open(original_file, 'r') as f:
        original_data = json.load(f)
    
    # Ambil data dari 10 orang pertama yang akan menjadi template
    template_data = {}
    for i in range(1, 11):
        key = f"orang_{i}"
        if key in original_data:
            template_data[key] = original_data[key]
    
    print(f"Found {len(template_data)} people as template")
    
    # Expand ke 40 orang dengan pattern yang sama tapi modified
    expanded_data = {}
    
    for person_num in range(1, 41):
        # Pilih template dari 10 orang pertama
        template_idx = ((person_num - 1) % 10) + 1
        template_key = f"orang_{template_idx}"
        
        # Deep copy template
        person_data = copy.deepcopy(template_data[template_key])
        
        # Update metadata
        person_data["metadata"]["device_id"] = f"IOT{person_num:03d}"
        person_data["metadata"]["measurement_location"] = "Campus"  # Always Campus
        
        # Update timestamp - spread across 24 hours
        base_time = datetime(2025, 11, 27)
        hour = (person_num - 1) % 24
        minute = ((person_num - 1) // 24) * 15  # 0, 15, 30, 45 minutes
        new_timestamp = base_time.replace(hour=hour, minute=minute)
        person_data["metadata"]["timestamp"] = new_timestamp.isoformat() + "Z"
        
        # Add slight variation to BPM dalam timeline (jangan ubah classification/confidence)
        if person_num > 10:
            # Untuk orang 11-40, tambahkan sedikit noise pada BPM
            variation_factor = 1 + ((person_num - 11) / 30) * 0.05  # 0% sampai 5% variation
            
            for reading in person_data["timeline"]:
                # Vary BPM slightly
                old_bpm = reading["bpm"]
                new_bpm = int(old_bpm * variation_factor)
                
                # Clamp ke range realistic
                new_bpm = max(55, min(130, new_bpm))
                reading["bpm"] = new_bpm
                
                # Update classification based on new BPM
                if new_bpm < 60:
                    reading["classification"] = "bradycardia"
                elif new_bpm > 100:
                    reading["classification"] = "tachycardia"
                else:
                    reading["classification"] = "normal"
                
                # Adjust confidence based on new classification
                if reading["classification"] == "normal":
                    distance_from_center = abs(new_bpm - 80) / 20
                    reading["confidence"] = round(max(0.5, 1.0 - distance_from_center * 0.25), 3)
                elif reading["classification"] == "bradycardia":
                    distance = max(0, 60 - new_bpm)
                    reading["confidence"] = round(min(1.0, 0.5 + distance * 0.05), 3)
                else:  # tachycardia
                    distance = max(0, new_bpm - 100)
                    reading["confidence"] = round(min(1.0, 0.5 + distance * 0.03), 3)
        
        expanded_data[f"orang_{person_num}"] = person_data
        print(f"Generated orang_{person_num} from template orang_{template_idx} - Campus - {person_data['metadata']['timestamp']}")
    
    # Save expanded dataset
    output_file = OUTPUT_DIR / "dataset_bpm_optimized.json"
    with open(output_file, 'w') as f:
        json.dump(expanded_data, f, indent=2)
    
    print(f"\n✓ Saved: {output_file}")
    print(f"Total people: {len(expanded_data)}")
    
    return expanded_data

def verify_dataset(data):
    """Verify dataset"""
    print("\n" + "="*60)
    print("VERIFICATION RESULTS")
    print("="*60)
    
    total_people = len(data)
    total_readings = 0
    all_locations = set()
    all_bpms = []
    classifications = {}
    
    for person_key, person_data in data.items():
        location = person_data["metadata"]["measurement_location"]
        all_locations.add(location)
        
        for reading in person_data["timeline"]:
            total_readings += 1
            all_bpms.append(reading["bpm"])
            classification = reading["classification"]
            classifications[classification] = classifications.get(classification, 0) + 1
    
    print(f"\n📊 Dataset Statistics:")
    print(f"  Total people: {total_people}")
    print(f"  Total readings: {total_readings}")
    print(f"  BPM range: {min(all_bpms)} - {max(all_bpms)}")
    print(f"  Average BPM: {sum(all_bpms) / len(all_bpms):.2f}")
    print(f"  Unique locations: {all_locations}")
    
    print(f"\n📍 Measurement Locations:")
    for location in sorted(all_locations):
        count = sum(1 for p in data.values() if p["metadata"]["measurement_location"] == location)
        print(f"  - {location}: {count} people")
    
    print(f"\n📈 Classification Distribution:")
    for cls in sorted(classifications.keys()):
        count = classifications[cls]
        percentage = (count / total_readings) * 100
        print(f"  - {cls}: {count} ({percentage:.1f}%)")
    
    print("\n✅ Verification complete!")

if __name__ == "__main__":
    print("="*60)
    print("Dataset Regeneration - Pattern-based Expansion")
    print("="*60)
    print()
    
    data = expand_dataset_from_pattern()
    verify_dataset(data)
    
    print("\n" + "="*60)
    print("✓ Dataset regeneration completed!")
    print("="*60)
