"""
Helper Functions untuk PSO & ACO Optimization
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os


class DataLoader:
    """Load dan manage dataset"""
    
    @staticmethod
    def load_optimized_dataset():
        """Load optimized dataset dari JSON"""
        dataset_path = Path(__file__).parent.parent / 'datasets' / 'dataset_bpm_optimized.json'
        with open(dataset_path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def load_feature_matrix():
        """Load feature matrix dari CSV"""
        csv_path = Path(__file__).parent.parent / 'datasets' / 'feature_matrix.csv'
        return pd.read_csv(csv_path)
    
    @staticmethod
    def get_subject_data(data, subject_key):
        """Extract data untuk satu subject"""
        subject = data[subject_key]
        X = []
        
        # Extract features
        stats = subject['statistics']['overall']
        features = [
            stats['mean_bpm'], stats['std_dev_bpm'], stats['min_bpm'],
            stats['max_bpm'], stats['median_bpm'], stats['variance'],
            stats['range_bpm'], stats['rmssd'], stats['nnxx'], stats['cvnn'],
            stats['skewness'], stats['kurtosis'], stats['q25'],
            stats['q75'], stats['iqr']
        ]
        
        return features, subject


class BPMVisualizer:
    """Visualisasi BPM data dengan normal/abnormal highlighting"""
    
    @staticmethod
    def plot_bpm_timeline(subject_key, subject_data, algorithm_name, save_path):
        """
        Plot BPM timeline dengan warna berbeda untuk normal/abnormal
        
        Args:
            subject_key: identifier subject (orang_1, dll)
            subject_data: data subject dari JSON
            algorithm_name: nama algoritma (PSO/ACO)
            save_path: path untuk save figure
        """
        timeline = subject_data['timeline']
        
        # Extract data
        seconds = [reading['second'] for reading in timeline]
        bpms = [reading['bpm'] for reading in timeline]
        classifications = [reading['classification'] for reading in timeline]
        
        # Create figure dengan ukuran yang bagus
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Separate normal dan abnormal berdasarkan classification di timeline
        normal_seconds, normal_bpms = [], []
        abnormal_s, abnormal_b = [], []
        
        for sec, bpm, classification in zip(seconds, bpms, classifications):
            if classification == 'abnormal' or classification == 'tachycardia' or classification == 'bradycardia':
                abnormal_s.append(sec)
                abnormal_b.append(bpm)
            else:
                normal_seconds.append(sec)
                normal_bpms.append(bpm)
        
        # Plot normal (hijau) dan abnormal (merah)
        ax.scatter(normal_seconds, normal_bpms, color='#2ecc71', s=50, 
                  label='Normal', alpha=0.7, edgecolors='darkgreen', linewidth=0.5)
        ax.scatter(abnormal_s, abnormal_b, color='#e74c3c', s=100, 
                  label='Abnormal', alpha=0.8, edgecolors='darkred', linewidth=1)
        
        # Plot line
        ax.plot(seconds, bpms, color='#95a5a6', alpha=0.3, linewidth=1, zorder=1)
        
        # Add reference lines
        ax.axhline(y=60, color='orange', linestyle='--', alpha=0.5, linewidth=1, label='Bradycardia Threshold')
        ax.axhline(y=100, color='blue', linestyle='--', alpha=0.5, linewidth=1, label='Tachycardia Threshold')
        
        # Formatting
        ax.set_xlabel('Time (seconds)', fontsize=12, fontweight='bold')
        ax.set_ylabel('BPM (Beats Per Minute)', fontsize=12, fontweight='bold')
        ax.set_title(f'{subject_key} - BPM Timeline ({algorithm_name} Analysis)', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
        ax.legend(loc='best', fontsize=10, framealpha=0.95)
        
        # Set Y-axis limits dengan margin
        min_bpm, max_bpm = min(bpms), max(bpms)
        margin = (max_bpm - min_bpm) * 0.1
        ax.set_ylim(min_bpm - margin, max_bpm + margin)
        ax.set_xlim(0, 301)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    @staticmethod
    def plot_fitness_convergence(generations, fitness_history, algorithm_name, save_path):
        """
        Plot fitness convergence history
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(generations, fitness_history, linewidth=2.5, color='#3498db', marker='o', 
               markersize=4, label='Fitness Score')
        ax.fill_between(generations, fitness_history, alpha=0.3, color='#3498db')
        
        ax.set_xlabel('Iteration', fontsize=12, fontweight='bold')
        ax.set_ylabel('Fitness Score (Accuracy)', fontsize=12, fontweight='bold')
        ax.set_title(f'{algorithm_name} - Fitness Convergence', fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
        ax.legend(loc='best', fontsize=11)
        
        # Add best fitness annotation
        best_idx = np.argmax(fitness_history)
        best_fitness = fitness_history[best_idx]
        ax.annotate(f'Best: {best_fitness:.4f}', 
                   xy=(generations[best_idx], best_fitness),
                   xytext=(10, 10), textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
    
    @staticmethod
    def plot_feature_importance(features, importances, algorithm_name, save_path):
        """
        Plot feature importance bars
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Sort by importance
        indices = np.argsort(importances)[::-1][:15]  # Top 15
        top_features = [features[i] for i in indices]
        top_importances = [importances[i] for i in indices]
        
        colors = plt.cm.viridis(np.linspace(0, 1, len(top_features)))
        bars = ax.barh(range(len(top_features)), top_importances, color=colors, edgecolor='black', linewidth=1.5)
        
        ax.set_yticks(range(len(top_features)))
        ax.set_yticklabels(top_features, fontsize=10)
        ax.set_xlabel('Importance Score', fontsize=12, fontweight='bold')
        ax.set_title(f'{algorithm_name} - Top 15 Feature Importance', fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='x', linestyle=':', linewidth=0.5)
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, top_importances)):
            ax.text(val, i, f' {val:.4f}', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()


class MetricsCalculator:
    """Calculate classification metrics"""
    
    @staticmethod
    def calculate_accuracy(y_true, y_pred):
        """Calculate accuracy"""
        return np.mean(y_true == y_pred)
    
    @staticmethod
    def calculate_precision(y_true, y_pred):
        """Calculate precision"""
        true_positives = np.sum((y_true == 1) & (y_pred == 1))
        predicted_positives = np.sum(y_pred == 1)
        return true_positives / predicted_positives if predicted_positives > 0 else 0
    
    @staticmethod
    def calculate_recall(y_true, y_pred):
        """Calculate recall"""
        true_positives = np.sum((y_true == 1) & (y_pred == 1))
        actual_positives = np.sum(y_true == 1)
        return true_positives / actual_positives if actual_positives > 0 else 0
    
    @staticmethod
    def calculate_f1(precision, recall):
        """Calculate F1 score"""
        if precision + recall == 0:
            return 0
        return 2 * (precision * recall) / (precision + recall)
    
    @staticmethod
    def calculate_confusion_matrix(y_true, y_pred):
        """Generate confusion matrix"""
        tn = np.sum((y_true == 0) & (y_pred == 0))
        fp = np.sum((y_true == 0) & (y_pred == 1))
        fn = np.sum((y_true == 1) & (y_pred == 0))
        tp = np.sum((y_true == 1) & (y_pred == 1))
        return {'TP': tp, 'TN': tn, 'FP': fp, 'FN': fn}


def create_output_directory(algorithm_name, subject_key):
    """Buat direktori output untuk hasil"""
    base_path = Path(__file__).parent.parent / algorithm_name.lower() / 'results'
    output_dir = base_path / subject_key
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def print_section(title):
    """Print formatted section title"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def print_metrics(accuracy, precision, recall, f1, cm):
    """Print classification metrics"""
    print(f"\n  Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1-Score:  {f1:.4f}")
    print(f"\n  Confusion Matrix:")
    print(f"    TP: {cm['TP']:<3} | FN: {cm['FN']:<3}")
    print(f"    FP: {cm['FP']:<3} | TN: {cm['TN']:<3}")
