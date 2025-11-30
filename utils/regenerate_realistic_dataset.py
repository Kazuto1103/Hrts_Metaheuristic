"""
Regenerate Realistic BPM Dataset untuk 40 Remaja (19-21 tahun)
- Baseline stabil 60-75 bpm (resting heart rate remaja)
- Variasi natural smooth ±0.5-1 bpm per detik
- Beberapa spike abnormal (jumpscare moments) - 5-10 kali per orang
- Smooth recovery setelah spike
"""

import json
import random
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np

OUTPUT_DIR = Path(__file__).parent.parent / 'datasets'

def generate_realistic_bpm_pattern(person_num, duration=300):
    """
    Generate realistic BPM pattern untuk remaja stabil dengan abnormal spikes
    
    Karakteristik:
    - Baseline: 60-75 bpm (remaja normal saat istirahat)
    - 90% waktu: smooth rhythm dengan variasi ±0.5-1 bpm
    - 10% waktu: beberapa spike abnormal (80-120 bpm) akibat kejutan
    - Recovery: gradual turun kembali ke baseline
    """
    timeline = []
    
    # Unique seed per person
    random.seed(person_num * 42 + 100)
    np.random.seed(person_num * 42 + 100)
    
    # Baseline untuk setiap orang (60-75 bpm)
    baseline = random.uniform(60, 75)
    
    # Tentukan 3-5 jumpscare moments (times ketika ada spike abnormal)
    n_spikes = random.randint(3, 5)
    spike_times = sorted(random.sample(range(50, duration - 30), n_spikes))
    
    current_bpm = baseline
    spike_recovery_end = 0  # Track kapan selesai recovery dari spike
    
    for second in range(1, duration + 1):
        # Determine current phase
        if second in spike_times and second > spike_recovery_end:
            # JUMPSCARE SPIKE - sudden increase (startled reaction)
            # Naik 30-50 bpm dalam 1-2 detik
            if random.random() < 0.5:
                change = random.uniform(30, 50)
            else:
                change = random.uniform(20, 35)
            
            spike_peak = current_bpm + change
            current_bpm = spike_peak
            spike_recovery_end = second + random.randint(5, 15)  # Recovery duration: 5-15 detik
            
        elif second <= spike_recovery_end:
            # RECOVERY phase - gradual decrease back to baseline
            # Turun smooth kembali ke baseline
            remaining_recovery = spike_recovery_end - second
            if remaining_recovery > 0:
                target = baseline + random.uniform(-2, 2)  # Slight overshoot atau undershoot
                change = (target - current_bpm) / remaining_recovery
                change = np.clip(change, -3, -0.5)  # Controlled decrease
            else:
                change = random.uniform(-1, 0.5)
            
            current_bpm = current_bpm + change
        
        else:
            # BASELINE phase - smooth natural variation
            # Realistic HRV (heart rate variability)
            # Most of time: ±0.5-1 bpm
            # Occasionally: slightly higher variation ±1-2 bpm
            if random.random() < 0.15:
                # Occasional slightly bigger variation (breathing, movement, etc)
                change = random.uniform(-2, 2)
            else:
                # Normal smooth variation
                change = random.uniform(-1, 1)
            
            current_bpm = current_bpm + change
        
        # Clamp ke realistic range untuk remaja (55-130 bpm)
        current_bpm = max(55, min(130, current_bpm))
        
        # Round ke integer
        bpm = round(current_bpm)
        
        # Classify based on bpm value
        if bpm < 60:
            classification = 'bradycardia'
        elif bpm > 100:
            classification = 'abnormal'  # tachycardia
        else:
            classification = 'normal'
        
        timeline.append({
            'second': second,
            'bpm': bpm,
            'classification': classification,
            'confidence': round(random.uniform(0.85, 0.99), 2)
        })
    
    return timeline


def generate_metadata(person_num):
    """Generate metadata untuk setiap orang"""
    genders = ['M', 'F']
    locations = ['Campus', 'Dormitory', 'Lab']
    devices = [f'IOT{str(i).zfill(3)}' for i in range(1, 41)]
    
    random.seed(person_num * 17)
    
    return {
        'gender': random.choice(genders),
        'age': random.randint(19, 21),
        'device_id': devices[person_num - 1],
        'measurement_location': random.choice(locations),
        'measurement_duration_seconds': 300,
        'timestamp': (datetime.now() - timedelta(days=person_num)).isoformat() + 'Z'
    }


def generate_realistic_dataset():
    """Generate complete dataset untuk 40 orang dengan realistic BPM patterns"""
    print("\n" + "="*75)
    print("🧬 REGENERATING REALISTIC BPM DATASET FOR 40 PEOPLE")
    print("="*75)
    
    dataset = {}
    
    print("\n📊 Generating realistic BPM patterns...")
    print("   Baseline: 60-75 bpm (remaja stabil)")
    print("   Variasi: ±0.5-1 bpm smooth variation")
    print("   Abnormal: 3-5 spike moments (jumpscare effect)\n")
    
    stats_summary = {
        'total_samples': 0,
        'normal_count': 0,
        'abnormal_count': 0,
        'bradycardia_count': 0,
        'baseline_ranges': []
    }
    
    for person_num in range(1, 41):
        person_key = f'orang_{person_num}'
        
        # Generate timeline
        timeline = generate_realistic_bpm_pattern(person_num)
        
        # Calculate statistics
        bpms = [reading['bpm'] for reading in timeline]
        baseline_bpm = np.mean([b for b in bpms if 55 < b < 100])  # Exclude spikes
        
        # Classify person as abnormal if has significant abnormal readings
        abnormal_readings = [r for r in timeline if r['classification'] != 'normal']
        person_is_abnormal = len(abnormal_readings) > 30  # More than 10% abnormal
        person_label = 1 if person_is_abnormal else 0
        
        # Store in dataset
        dataset[person_key] = {
            'metadata': generate_metadata(person_num),
            'timeline': timeline,
            'person_label': person_label,
            'statistics': {
                'baseline_bpm': round(baseline_bpm, 2),
                'mean_bpm': round(np.mean(bpms), 2),
                'std_dev': round(np.std(bpms), 2),
                'min_bpm': min(bpms),
                'max_bpm': max(bpms),
                'abnormal_percentage': round(len(abnormal_readings) / len(timeline) * 100, 2)
            }
        }
        
        # Update summary
        stats_summary['total_samples'] += len(timeline)
        normal_count = len([r for r in timeline if r['classification'] == 'normal'])
        abnormal_count = len([r for r in timeline if r['classification'] in ['abnormal', 'bradycardia']])
        bradycardia_count = len([r for r in timeline if r['classification'] == 'bradycardia'])
        
        stats_summary['normal_count'] += normal_count
        stats_summary['abnormal_count'] += abnormal_count
        stats_summary['bradycardia_count'] += bradycardia_count
        stats_summary['baseline_ranges'].append(round(baseline_bpm, 1))
        
        if person_num % 5 == 0:
            print(f"  ✓ Generated {person_num}/40 people")
            print(f"    {person_key}: baseline={baseline_bpm:.1f}bpm, "
                  f"abnormal_readings={len(abnormal_readings)}, label={person_label}")
    
    # Save dataset
    output_file = OUTPUT_DIR / 'dataset_bpm_optimized.json'
    with open(output_file, 'w') as f:
        json.dump(dataset, f, indent=2)
    
    print(f"\n✓ Dataset saved to: {output_file}")
    
    # Print summary
    print("\n" + "="*75)
    print("📊 DATASET SUMMARY")
    print("="*75)
    print(f"\nTotal BPM Readings: {stats_summary['total_samples']:,}")
    print(f"  - Normal: {stats_summary['normal_count']:,} ({stats_summary['normal_count']/stats_summary['total_samples']*100:.1f}%)")
    print(f"  - Abnormal (Tachycardia): {stats_summary['abnormal_count'] - stats_summary['bradycardia_count']:,}")
    print(f"  - Bradycardia: {stats_summary['bradycardia_count']:,}")
    
    print(f"\nBaseline BPM Range per Person: {min(stats_summary['baseline_ranges']):.1f} - {max(stats_summary['baseline_ranges']):.1f} bpm")
    print(f"Average Baseline: {np.mean(stats_summary['baseline_ranges']):.1f} bpm")
    
    print(f"\n✅ Dataset regenerated with realistic patterns!")
    print("="*75 + "\n")
    
    return dataset


if __name__ == "__main__":
    generate_realistic_dataset()
