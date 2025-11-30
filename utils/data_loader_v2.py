"""
Improved Data Loader untuk dataset BPM yang lebih besar
Menghandle dataset dengan 40+ orang
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path

class DataLoaderV2:
    """Data loader untuk dataset BPM yang besar dan complex"""
    
    @staticmethod
    def load_dataset(filepath, sample_size=None, use_all=True):
        """
        Load dataset BPM dengan support untuk multiple persons
        
        Args:
            filepath: Path ke dataset JSON
            sample_size: Jumlah readings per person (default: all)
            use_all: Gunakan semua orang dalam dataset
            
        Returns:
            X, y: Features dan labels
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        features_list = []
        labels_list = []
        
        # Iterate semua orang dalam dataset
        for person_key, person_data in sorted(data.items()):
            timeline = person_data.get('timeline', [])
            
            if not timeline:
                continue
            
            # Extract BPM values dan classifications
            bpms = [reading['bpm'] for reading in timeline]
            classifications = [reading['classification'] for reading in timeline]
            
            if not bpms:
                continue
            
            # Limit sample size jika diperlukan
            if sample_size and len(bpms) > sample_size:
                indices = np.linspace(0, len(bpms)-1, sample_size, dtype=int)
                bpms = [bpms[i] for i in indices]
                classifications = [classifications[i] for i in indices]
            
            # Create features dari BPM readings
            features = DataLoaderV2._extract_features(bpms)
            
            # Create label (0 = normal/bradycardia, 1 = abnormal/tachycardia)
            label = 1 if 'tachycardia' in classifications else 0
            
            features_list.append(features)
            labels_list.append(label)
        
        X = np.array(features_list)
        y = np.array(labels_list)
        
        print(f"✓ Loaded {len(X)} samples with {X.shape[1]} features")
        print(f"  Class distribution: {np.sum(y==0)} normal, {np.sum(y==1)} abnormal")
        
        return X, y
    
    @staticmethod
    def _extract_features(bpms):
        """
        Extract statistical features dari BPM time series
        
        Args:
            bpms: List of BPM values
            
        Returns:
            features: Array of 18 features
        """
        bpms = np.array(bpms)
        
        features = [
            # Basic statistics (5)
            np.mean(bpms),
            np.std(bpms),
            np.min(bpms),
            np.max(bpms),
            np.percentile(bpms, 50),
            
            # Distribution (4)
            np.percentile(bpms, 25),
            np.percentile(bpms, 75),
            np.ptp(bpms),  # peak-to-peak
            
            # Variability (4)
            np.sqrt(np.mean(np.diff(bpms)**2)),  # RMS of changes
            np.mean(np.abs(np.diff(bpms))),  # Mean absolute change
            np.max(np.abs(np.diff(bpms))),  # Max change
            np.sum(np.abs(np.diff(bpms))),  # Total variation
            
            # Abnormal patterns (5)
            np.sum(bpms > 100) / len(bpms),  # Tachycardia ratio
            np.sum(bpms < 60) / len(bpms),  # Bradycardia ratio
            np.sum(np.abs(np.diff(bpms)) > 5) / len(bpms),  # Large jump ratio
            np.sum(bpms > 120) / len(bpms),  # High tachycardia ratio
            np.sum(bpms > 130) / len(bpms),  # Very high ratio
            np.sum(bpms < 50) / len(bpms),  # Critical low ratio
        ]
        
        return np.array(features)
    
    @staticmethod
    def get_person_bpm_data(filepath, person_name):
        """
        Get BPM timeline untuk specific person
        
        Args:
            filepath: Path ke dataset
            person_name: Nama person (e.g., 'orang_1')
            
        Returns:
            bpms, classifications: BPM values dan classifications
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if person_name not in data:
            return None, None
        
        timeline = data[person_name].get('timeline', [])
        bpms = [reading['bpm'] for reading in timeline]
        classifications = [reading['classification'] for reading in timeline]
        
        return bpms, classifications

# Backward compatibility
class DataLoader:
    """Original DataLoader - backward compatible"""
    
    @staticmethod
    def load_dataset(filepath):
        """Load dan convert dataset ke format lama (hanya 10 samples)"""
        X, y = DataLoaderV2.load_dataset(filepath)
        # Limit to first 10 samples untuk backward compatibility
        return X[:10], y[:10]
