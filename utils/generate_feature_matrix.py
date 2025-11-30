"""
Generate Feature Matrix dari dataset_bpm_optimized.json untuk 40 orang
"""

import json
import numpy as np
import csv
from pathlib import Path
import sys

def calculate_features(timeline_data):
    """Calculate statistical features dari timeline"""
    bpms = [reading['bpm'] for reading in timeline_data]
    bpms = np.array(bpms)
    
    # HRV calculations
    bpm_diffs = np.diff(bpms)
    rmssd = np.sqrt(np.mean(bpm_diffs**2))
    nnxx = np.sum(np.abs(bpm_diffs) > 50) / len(bpm_diffs) * 100
    cvnn = np.std(bpms) / np.mean(bpms) if np.mean(bpms) > 0 else 0
    
    features = {
        'mean_bpm': np.mean(bpms),
        'std_dev_bpm': np.std(bpms),
        'min_bpm': np.min(bpms),
        'max_bpm': np.max(bpms),
        'median_bpm': np.median(bpms),
        'variance': np.var(bpms),
        'range_bpm': np.max(bpms) - np.min(bpms),
        'rmssd': rmssd,
        'nnxx': nnxx,
        'cvnn': cvnn,
        'skewness': float(calculate_skewness(bpms)),
        'kurtosis': float(calculate_kurtosis(bpms)),
        'q25': float(np.percentile(bpms, 25)),
        'q75': float(np.percentile(bpms, 75)),
        'iqr': float(np.percentile(bpms, 75) - np.percentile(bpms, 25))
    }
    
    return features

def calculate_skewness(data):
    """Calculate skewness"""
    n = len(data)
    mean = np.mean(data)
    std = np.std(data)
    if std == 0:
        return 0
    return np.sum(((data - mean) / std) ** 3) / n

def calculate_kurtosis(data):
    """Calculate kurtosis"""
    n = len(data)
    mean = np.mean(data)
    std = np.std(data)
    if std == 0:
        return 0
    return np.sum(((data - mean) / std) ** 4) / n - 3

def generate_feature_matrix():
    """Generate feature matrix untuk 40 orang"""
    print("\n" + "="*70)
    print("🧬 GENERATING FEATURE MATRIX FOR 40 PEOPLE")
    print("="*70)
    
    # Load dataset
    dataset_path = Path(__file__).parent.parent / 'datasets' / 'dataset_bpm_optimized.json'
    with open(dataset_path, 'r') as f:
        data = json.load(f)
    
    print(f"\n📊 Loaded {len(data)} subjects")
    
    # Feature list
    feature_names = [
        'mean_bpm', 'std_dev_bpm', 'min_bpm', 'max_bpm', 'median_bpm',
        'variance', 'range_bpm', 'rmssd', 'nnxx', 'cvnn', 'skewness', 'kurtosis',
        'q25', 'q75', 'iqr'
    ]
    
    feature_matrix = []
    labels = []
    
    print("\n📈 Processing subjects...")
    for i, (person_key, person_data) in enumerate(sorted(data.items()), 1):
        try:
            # Get timeline
            timeline = person_data.get('timeline', [])
            if not timeline:
                continue
            
            # Classify as abnormal if mean BPM > 100
            bpms = np.array([reading['bpm'] for reading in timeline])
            mean_bpm = np.mean(bpms)
            label = 1 if mean_bpm > 100 else 0
            
            # Calculate features
            features = calculate_features(timeline)
            
            # Append to matrix
            feature_row = [features[fname] for fname in feature_names]
            feature_matrix.append(feature_row)
            labels.append(label)
            
            if i % 10 == 0:
                print(f"  ✓ Processed {i}/{len(data)} subjects")
        
        except Exception as e:
            print(f"  ✗ Error processing {person_key}: {e}")
            continue
    
    print(f"\n✓ Processed {len(feature_matrix)} subjects successfully")
    print(f"  - Normal (label=0): {np.sum(np.array(labels)==0)}")
    print(f"  - Abnormal (label=1): {np.sum(np.array(labels)==1)}")
    
    # Save to CSV
    csv_path = Path(__file__).parent.parent / 'datasets' / 'feature_matrix.csv'
    print(f"\n💾 Saving to {csv_path}...")
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        header = feature_names + ['label']
        writer.writerow(header)
        for i, row in enumerate(feature_matrix):
            writer.writerow(row + [labels[i]])
    
    print(f"  ✓ Saved!")
    print(f"\n📊 Feature Matrix Shape: {len(feature_matrix)} × {len(feature_names)}")
    print("="*70 + "\n")
    
    return feature_matrix, labels

if __name__ == "__main__":
    generate_feature_matrix()
