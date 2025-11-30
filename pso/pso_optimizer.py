"""
PSO (Particle Swarm Optimization) - FINAL OPTIMIZED VERSION
Threshold Optimization & BPM Classification dengan Timeline Visualization 1-40
"""

import numpy as np
import pandas as pd
from pathlib import Path
import sys
import json
from datetime import datetime
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent.parent / 'utils'))

from helper import (
    DataLoader, BPMVisualizer, MetricsCalculator,
    create_output_directory, print_section, print_metrics
)
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix as sk_confusion_matrix


class PSO:
    """Particle Swarm Optimization untuk Threshold Optimization & BPM Classification"""
    
    def __init__(self, n_particles=20, n_iterations=100, w=0.7, c1=1.5, c2=1.5):
        self.n_particles = n_particles
        self.n_iterations = n_iterations
        self.w = w
        self.c1 = c1
        self.c2 = c2
        
        self.best_threshold = None
        self.best_fitness = -np.inf
        self.fitness_history = []
        self.threshold_history = []
    
    def initialize_particles(self, X, n_thresholds=2):
        """Initialize particles dengan threshold range dari data"""
        X_min, X_max = np.min(X), np.max(X)
        
        positions = []
        velocities = []
        
        for _ in range(self.n_particles):
            pos = np.array([
                np.random.uniform(X_min, (X_min + X_max) / 2),
                np.random.uniform((X_min + X_max) / 2, X_max)
            ])
            
            vel = np.random.uniform(-5, 5, n_thresholds)
            positions.append(pos)
            velocities.append(vel)
        
        return np.array(positions), np.array(velocities)
    
    def evaluate_threshold(self, thresholds, X, y):
        """Evaluate quality of threshold configuration"""
        try:
            y_pred = (X >= thresholds[1]).astype(int)
            
            acc = accuracy_score(y, y_pred)
            f1 = f1_score(y, y_pred, zero_division=0)
            
            fitness = 0.7 * f1 + 0.3 * acc
            return fitness
        
        except Exception as e:
            return 0.0
    
    def optimize(self, X, y, verbose=True):
        """Run PSO optimization"""
        if verbose:
            print_section("PSO OPTIMIZATION PROCESS")
            print(f"\n  Particles: {self.n_particles}")
            print(f"  Iterations: {self.n_iterations}")
            print(f"  W: {self.w}, C1: {self.c1}, C2: {self.c2}")
        
        positions, velocities = self.initialize_particles(X, n_thresholds=2)
        
        personal_best_pos = positions.copy()
        personal_best_fit = np.array([-np.inf] * self.n_particles)
        
        global_best_pos = None
        global_best_fit = -np.inf
        
        print("\n📊 Optimizing Thresholds...")
        
        for iteration in range(self.n_iterations):
            for i in range(self.n_particles):
                fitness = self.evaluate_threshold(positions[i], X, y)
                
                if fitness > personal_best_fit[i]:
                    personal_best_fit[i] = fitness
                    personal_best_pos[i] = positions[i].copy()
                
                if fitness > global_best_fit:
                    global_best_fit = fitness
                    global_best_pos = positions[i].copy()
            
            r1 = np.random.rand(self.n_particles, 2)
            r2 = np.random.rand(self.n_particles, 2)
            
            velocities = (self.w * velocities +
                         self.c1 * r1 * (personal_best_pos - positions) +
                         self.c2 * r2 * (global_best_pos - positions))
            
            positions = positions + velocities
            
            X_min, X_max = np.min(X), np.max(X)
            positions[:, 0] = np.clip(positions[:, 0], X_min, (X_min + X_max) / 2)
            positions[:, 1] = np.clip(positions[:, 1], (X_min + X_max) / 2, X_max)
            
            self.best_threshold = global_best_pos
            self.best_fitness = global_best_fit
            self.fitness_history.append(global_best_fit)
            self.threshold_history.append(global_best_pos.copy())
            
            if verbose and (iteration + 1) % 20 == 0:
                print(f"  Iteration {iteration+1:3d}/{self.n_iterations}: "
                      f"Fitness = {global_best_fit:.4f}")
        
        if verbose:
            print(f"\n  ✅ Optimization Complete!")
            print(f"  Final Best Fitness: {global_best_fit:.4f}")
        
        return global_best_pos, global_best_fit


def run_pso_analysis():
    """Run complete PSO analysis"""
    print_section("PSO OPTIMIZATION - FINAL VERSION")
    print(f"\n  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n📊 Loading Data...")
    data = DataLoader.load_optimized_dataset()
    df = DataLoader.load_feature_matrix()
    
    X = df.drop('label', axis=1).values
    y = df['label'].values
    
    print(f"  ✓ Loaded {X.shape[0]} samples with {X.shape[1]} features")
    print(f"  ✓ Classes: {np.sum(y==0)} normal, {np.sum(y==1)} abnormal")
    
    X_bpm = X[:, 0].reshape(-1, 1).flatten()
    
    print("\n⚡ Running PSO Optimization...")
    pso = PSO(n_particles=20, n_iterations=100)
    best_threshold, best_fitness = pso.optimize(X_bpm, y, verbose=True)
    
    print("\n📈 Evaluation with Optimized Thresholds:")
    y_pred = (X_bpm >= best_threshold[1]).astype(int)
    
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred, zero_division=0)
    recall = recall_score(y, y_pred, zero_division=0)
    f1 = f1_score(y, y_pred, zero_division=0)
    
    cm = sk_confusion_matrix(y, y_pred)
    cm_dict = {
        'TP': int(cm[1, 1]),
        'TN': int(cm[0, 0]),
        'FP': int(cm[0, 1]),
        'FN': int(cm[1, 0])
    }
    
    print(f"  Accuracy:  {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1-Score:  {f1:.4f}")
    print(f"\n  Optimized Thresholds:")
    print(f"    Normal Range:    < {best_threshold[0]:.2f}")
    print(f"    Abnormal Range:  >= {best_threshold[1]:.2f}")
    
    print("\n📊 Generating BPM Timeline Visualizations (1-40)...")
    results_dir = Path(__file__).parent / 'results'
    results_dir.mkdir(exist_ok=True)
    
    for i, (subject_key, subject_data) in enumerate(data.items(), 1):
        try:
            output_path = results_dir / f"{subject_key}_bpm_timeline.png"
            BPMVisualizer.plot_bpm_timeline(subject_key, subject_data, 'PSO', output_path)
            if i % 5 == 0 or i == len(data):
                print(f"  ✓ Generated {i}/{len(data)} timeline visualizations")
        except Exception as e:
            print(f"  ✗ {subject_key}: {e}")
    
    print("\n📊 Generating Convergence Plot...")
    convergence_path = results_dir / "pso_fitness_convergence.png"
    iterations = list(range(1, len(pso.fitness_history) + 1))
    BPMVisualizer.plot_fitness_convergence(iterations, pso.fitness_history, 'PSO', convergence_path)
    print(f"  ✓ Saved: pso_fitness_convergence.png")
    
    print("\n📊 Generating Threshold Distribution Plot...")
    threshold_path = results_dir / "pso_threshold_distribution.png"
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.hist(X_bpm[y == 0], bins=30, alpha=0.6, label='Normal', color='#95E1D3')
    ax.hist(X_bpm[y == 1], bins=30, alpha=0.6, label='Abnormal', color='#FF6B6B')
    ax.axvline(best_threshold[0], color='#4ECDC4', linestyle='--', linewidth=2.5, 
               label=f'Normal: {best_threshold[0]:.2f}')
    ax.axvline(best_threshold[1], color='#FF6B6B', linestyle='--', linewidth=2.5,
               label=f'Abnormal: {best_threshold[1]:.2f}')
    ax.set_xlabel('BPM (Mean)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax.set_title('BPM Distribution with Optimized Thresholds (PSO)', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(threshold_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: pso_threshold_distribution.png")
    
    print("\n💾 Saving Results...")
    results = {
        'algorithm': 'PSO',
        'timestamp': datetime.now().isoformat(),
        'optimized_thresholds': {
            'normal_upper': float(best_threshold[0]),
            'abnormal_lower': float(best_threshold[1])
        },
        'metrics': {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1)
        },
        'confusion_matrix': cm_dict,
        'best_fitness': float(best_fitness)
    }
    
    results_file = results_dir / 'pso_results.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"  ✓ Saved: pso_results.json")
    
    print("\n" + "="*75)
    print("✅ PSO ANALYSIS COMPLETE!")
    print("="*75)
    print(f"\n📁 Generated {len(list(results_dir.glob('orang_*_bpm_timeline.png')))} timeline visualizations")
    print(f"📊 Convergence & Threshold distribution plots generated")
    print(f"💾 Results saved to JSON\n")
    
    return pso, best_threshold, results


if __name__ == "__main__":
    pso, best_threshold, results = run_pso_analysis()
