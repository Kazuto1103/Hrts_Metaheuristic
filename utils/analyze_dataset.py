import json
import numpy as np
from collections import defaultdict

def analyze_optimized_dataset():
    """
    Analisis dataset yang sudah dioptimalkan untuk memberikan insights
    """
    with open('dataset_bpm_optimized.json', 'r') as f:
        data = json.load(f)
    
    print("=" * 70)
    print("📊 ANALISIS DATASET BPM TEROPTIMALKAN")
    print("=" * 70)
    
    # Summary statistics
    all_bpm = []
    all_abnormal = []
    gender_distribution = defaultdict(int)
    location_distribution = defaultdict(int)
    classification_count = defaultdict(int)
    
    for person_key, person_data in data.items():
        print(f"\n👤 {person_key.upper()}")
        print("-" * 70)
        
        metadata = person_data["metadata"]
        stats = person_data["statistics"]
        
        # Basic info
        print(f"  Gender: {metadata['gender']} | Age: {metadata['age']} | Location: {metadata['measurement_location']}")
        print(f"  Device: {metadata['device_id']} | Time: {metadata['timestamp']}")
        
        # Statistics
        overall = stats["overall"]
        print(f"\n  📈 BPM Statistics:")
        print(f"     Mean: {overall['mean_bpm']:.2f} | Std Dev: {overall['std_dev_bpm']:.2f}")
        print(f"     Range: {overall['min_bpm']:.0f} - {overall['max_bpm']:.0f} (Range: {overall['range_bpm']:.0f})")
        print(f"     Median: {overall['median_bpm']:.0f} | IQR: {overall['iqr']:.0f}")
        
        # HRV features
        print(f"\n  ❤️  Heart Rate Variability:")
        print(f"     RMSSD: {overall['rmssd']:.2f} | NNxx: {overall['nnxx']:.2f}% | CV: {overall['cvnn']:.4f}")
        
        # Distribution
        print(f"\n  📉 Distribution Shape:")
        print(f"     Skewness: {overall['skewness']:.3f} | Kurtosis: {overall['kurtosis']:.3f}")
        
        # Data quality
        quality = stats["data_quality"]
        print(f"\n  ✓ Data Quality:")
        print(f"     Total: {quality['total_readings']} readings | Normal: {quality['normal_count']} | Abnormal: {quality['abnormal_count']}")
        print(f"     Abnormal %: {quality['abnormal_percentage']:.2f}%")
        
        # Abnormal details
        abnormal = person_data["classifications"]["abnormal_bpm_readings"]
        if abnormal:
            print(f"\n  ⚠️  Abnormal Readings Detected:")
            for abn in abnormal:
                print(f"     Second {abn['second']}: {abn['bpm']} BPM ({abn['type']}) - Severity: {abn['severity_percentage']:.1f}%")
        
        # Collect statistics
        for reading in person_data["timeline"]:
            all_bpm.append(reading["bpm"])
            classification_count[reading["classification"]] += 1
        
        all_abnormal.extend([abn["bpm"] for abn in abnormal])
        gender_distribution[metadata["gender"]] += 1
        location_distribution[metadata["measurement_location"]] += 1
    
    # Overall summary
    print("\n" + "=" * 70)
    print("📋 OVERALL SUMMARY")
    print("=" * 70)
    
    print(f"\n👥 Subject Distribution:")
    print(f"   Male: {gender_distribution['M']} | Female: {gender_distribution['F']}")
    
    print(f"\n📍 Measurement Location:")
    for loc, count in location_distribution.items():
        print(f"   {loc}: {count} subjects")
    
    print(f"\n📊 Classification Distribution:")
    for cls, count in sorted(classification_count.items(), key=lambda x: x[1], reverse=True):
        pct = (count / len(all_bpm)) * 100
        print(f"   {cls.capitalize()}: {count} readings ({pct:.2f}%)")
    
    all_bpm = np.array(all_bpm)
    print(f"\n📈 Global BPM Statistics:")
    print(f"   Mean: {np.mean(all_bpm):.2f} | Std Dev: {np.std(all_bpm):.2f}")
    print(f"   Min: {np.min(all_bpm):.0f} | Max: {np.max(all_bpm):.0f}")
    print(f"   Median: {np.median(all_bpm):.0f} | IQR: {np.percentile(all_bpm, 75) - np.percentile(all_bpm, 25):.0f}")
    
    if all_abnormal:
        print(f"\n⚠️  Abnormal Findings:")
        print(f"   Total abnormal readings: {len(all_abnormal)}")
        print(f"   Mean abnormal BPM: {np.mean(all_abnormal):.2f}")
        print(f"   Type distribution: {[abn for abn in all_abnormal]}")

def compare_normal_vs_abnormal():
    """
    Perbandingan fitur normal vs abnormal untuk feature importance
    """
    with open('dataset_bpm_optimized.json', 'r') as f:
        data = json.load(f)
    
    print("\n" + "=" * 70)
    print("🔍 FEATURE COMPARISON: NORMAL vs ABNORMAL")
    print("=" * 70)
    
    print(f"\n{'Feature':<25} {'Normal Avg':<15} {'Abnormal Avg':<15} {'Difference':<15}")
    print("-" * 70)
    
    features_to_compare = [
        'mean_bpm', 'std_dev_bpm', 'variance', 'rmssd', 'nnxx', 'cvnn', 'skewness', 'kurtosis'
    ]
    
    normal_values = defaultdict(list)
    abnormal_values = defaultdict(list)
    
    for person_data in data.values():
        stats = person_data["statistics"]
        
        for feature in features_to_compare:
            if feature in stats["normal_period"]:
                normal_values[feature].append(stats["normal_period"][feature])
            
            if feature in stats["abnormal_period"]:
                abnormal_values[feature].append(stats["abnormal_period"][feature])
    
    for feature in features_to_compare:
        normal_avg = np.mean(normal_values[feature]) if normal_values[feature] else 0
        abnormal_avg = np.mean(abnormal_values[feature]) if abnormal_values[feature] else 0
        diff = abs(normal_avg - abnormal_avg)
        
        marker = "🔴" if diff > normal_avg * 0.3 else "🟡" if diff > normal_avg * 0.1 else "🟢"
        print(f"{feature:<25} {normal_avg:<15.2f} {abnormal_avg:<15.2f} {diff:<14.2f} {marker}")
    
    print("\nKeterangan:")
    print("🔴 Red: Difference > 30% (High importance)")
    print("🟡 Yellow: Difference 10-30% (Medium importance)")
    print("🟢 Green: Difference < 10% (Low importance)")

def generate_feature_matrix():
    """
    Buat feature matrix untuk training PSO/ACO
    """
    with open('dataset_bpm_optimized.json', 'r') as f:
        data = json.load(f)
    
    print("\n" + "=" * 70)
    print("🧬 GENERATING FEATURE MATRIX FOR ML")
    print("=" * 70)
    
    feature_matrix = []
    labels = []
    
    features_list = [
        'mean_bpm', 'std_dev_bpm', 'min_bpm', 'max_bpm', 'median_bpm',
        'variance', 'range_bpm', 'rmssd', 'nnxx', 'cvnn', 'skewness', 'kurtosis',
        'q25', 'q75', 'iqr'
    ]
    
    for person_key, person_data in data.items():
        metadata = person_data["metadata"]
        stats = person_data["statistics"]["overall"]
        quality = person_data["statistics"]["data_quality"]
        
        feature_row = []
        
        # Add statistical features
        for feature in features_list:
            feature_row.append(stats[feature])
        
        # Add metadata features (normalized)
        feature_row.append(1 if metadata["gender"] == "M" else 0)  # Gender (0=F, 1=M)
        feature_row.append(metadata["age"] / 50)  # Age (normalized by 50)
        feature_row.append(quality["abnormal_percentage"])  # Abnormal percentage
        
        feature_matrix.append(feature_row)
        
        # Label: 1 if has abnormal, 0 otherwise
        label = 1 if quality["abnormal_count"] > 0 else 0
        labels.append(label)
    
    print(f"\n✓ Feature Matrix Generated!")
    print(f"  Shape: {len(feature_matrix)} samples × {len(feature_matrix[0])} features")
    print(f"\n  Features: {features_list + ['gender', 'age_norm', 'abnormal_pct']}")
    print(f"\n  Labels: {np.sum(labels)}/{len(labels)} abnormal cases")
    
    # Save to CSV
    import csv
    with open('feature_matrix.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        header = features_list + ['gender', 'age_norm', 'abnormal_pct', 'label']
        writer.writerow(header)
        for i, row in enumerate(feature_matrix):
            writer.writerow(row + [labels[i]])
    
    print(f"  ✓ Saved to: feature_matrix.csv")
    
    return feature_matrix, labels

if __name__ == "__main__":
    analyze_optimized_dataset()
    compare_normal_vs_abnormal()
    generate_feature_matrix()
    
    print("\n" + "=" * 70)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 70)
