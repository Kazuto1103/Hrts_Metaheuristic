"""
PSO (Particle Swarm Optimization) Algorithm untuk BPM Classification
Mengoptimalkan threshold untuk klasifikasi normal vs abnormal
"""

import numpy as np
import pandas as pd
from pathlib import Path
import sys
from datetime import datetime

# Add parent directory to path untuk import helper
sys.path.insert(0, str(Path(__file__).parent.parent / 'utils'))

from helper import (
    DataLoader, BPMVisualizer, MetricsCalculator, 
    create_output_directory, print_section, print_metrics
)


class PSO:
    """Particle Swarm Optimization untuk BPM Threshold Optimization"""
    
    def __init__(self, n_particles=20, n_dimensions=3, max_iterations=100,
                 w=0.7, c1=1.5, c2=1.5):
        """
        Initialize PSO
        
        Args:
            n_particles: Jumlah particles dalam swarm
            n_dimensions: Jumlah dimensi (parameter) yang dioptimalkan
            max_iterations: Jumlah iterasi maksimal
            w: Inertia weight (0.7 = bagus untuk balance exploration-exploitation)
            c1: Cognitive coefficient (particle's own best)
            c2: Social coefficient (swarm's global best)
        """
        self.n_particles = n_particles
        self.n_dimensions = n_dimensions
        self.max_iterations = max_iterations
        self.w = w
        self.c1 = c1
        self.c2 = c2
        
        # Initialize particles
        # Dimensi: [normal_min, normal_max, elevated_max]
        # Bounds: normal_min [40-70], normal_max [80-120], elevated_max [100-150]
        self.positions = np.random.uniform([40, 80, 100], [70, 120, 150], 
                                          size=(n_particles, n_dimensions))
        self.velocities = np.random.uniform(-10, 10, size=(n_particles, n_dimensions))
        
        # Best positions
        self.personal_best = self.positions.copy()
        self.personal_best_fitness = np.full(n_particles, -np.inf)
        self.global_best = None
        self.global_best_fitness = -np.inf
        
        # History untuk tracking
        self.fitness_history = []
        self.position_history = []
    
    def classify_bpm(self, bpm_value, thresholds):
        """
        Klasifikasi BPM berdasarkan thresholds
        
        Args:
            bpm_value: nilai BPM
            thresholds: [normal_min, normal_max, elevated_max]
        
        Returns:
            0: normal, 1: abnormal
        """
        normal_min, normal_max, elevated_max = thresholds
        
        # Ensure valid thresholds
        if normal_min > normal_max:
            normal_min, normal_max = normal_max, normal_min
        
        if (normal_min <= bpm_value <= normal_max):
            return 0  # normal
        else:
            return 1  # abnormal
    
    def fitness_function(self, thresholds, X_features, y_true, method='accuracy'):
        """
        Calculate fitness (accuracy) berdasarkan thresholds
        
        Args:
            thresholds: [normal_min, normal_max, elevated_max]
            X_features: Feature matrix (mean_bpm)
            y_true: True labels
            method: 'accuracy', 'f1', atau 'balanced'
        
        Returns:
            fitness score (0-1)
        """
        # Use mean_bpm sebagai primary feature (index 0)
        mean_bpms = X_features[:, 0]
        
        # Predict menggunakan thresholds
        y_pred = np.array([self.classify_bpm(bpm, thresholds) for bpm in mean_bpms])
        
        if method == 'accuracy':
            fitness = MetricsCalculator.calculate_accuracy(y_true, y_pred)
        elif method == 'f1':
            precision = MetricsCalculator.calculate_precision(y_true, y_pred)
            recall = MetricsCalculator.calculate_recall(y_true, y_pred)
            fitness = MetricsCalculator.calculate_f1(precision, recall)
        else:  # balanced
            # Weighted accuracy yang mempertimbangkan precision dan recall
            precision = MetricsCalculator.calculate_precision(y_true, y_pred)
            recall = MetricsCalculator.calculate_recall(y_true, y_pred)
            accuracy = MetricsCalculator.calculate_accuracy(y_true, y_pred)
            fitness = (accuracy + precision + recall) / 3
        
        return fitness
    
    def optimize(self, X_features, y_true, verbose=True):
        """
        Run PSO optimization
        
        Args:
            X_features: Feature matrix
            y_true: True labels
            verbose: Print progress
        
        Returns:
            best_thresholds, best_fitness, history
        """
        if verbose:
            print_section("PSO OPTIMIZATION PROCESS")
            print(f"\n  Particles: {self.n_particles}")
            print(f"  Max Iterations: {self.max_iterations}")
            print(f"  Inertia Weight (w): {self.w}")
            print(f"  Cognitive (c1): {self.c1}, Social (c2): {self.c2}")
        
        # Evaluate initial population
        for i in range(self.n_particles):
            fitness = self.fitness_function(self.positions[i], X_features, y_true)
            self.personal_best_fitness[i] = fitness
            
            if fitness > self.global_best_fitness:
                self.global_best_fitness = fitness
                self.global_best = self.positions[i].copy()
        
        if verbose:
            print(f"\n  Initial Best Fitness: {self.global_best_fitness:.4f}")
        
        # Main PSO loop
        for iteration in range(self.max_iterations):
            for i in range(self.n_particles):
                # Update velocity
                r1 = np.random.rand(self.n_dimensions)
                r2 = np.random.rand(self.n_dimensions)
                
                self.velocities[i] = (
                    self.w * self.velocities[i] +
                    self.c1 * r1 * (self.personal_best[i] - self.positions[i]) +
                    self.c2 * r2 * (self.global_best - self.positions[i])
                )
                
                # Update position
                self.positions[i] += self.velocities[i]
                
                # Apply bounds
                self.positions[i] = np.clip(self.positions[i], 
                                          [40, 80, 100], 
                                          [70, 120, 150])
                
                # Evaluate new position
                fitness = self.fitness_function(self.positions[i], X_features, y_true)
                
                # Update personal best
                if fitness > self.personal_best_fitness[i]:
                    self.personal_best_fitness[i] = fitness
                    self.personal_best[i] = self.positions[i].copy()
                
                # Update global best
                if fitness > self.global_best_fitness:
                    self.global_best_fitness = fitness
                    self.global_best = self.positions[i].copy()
            
            self.fitness_history.append(self.global_best_fitness)
            self.position_history.append(self.global_best.copy())
            
            if verbose and (iteration + 1) % 10 == 0:
                print(f"  Iteration {iteration+1:3d}/{self.max_iterations}: "
                      f"Best Fitness = {self.global_best_fitness:.4f}")
        
        if verbose:
            print(f"\n  ✅ Optimization Complete!")
            print(f"  Final Best Fitness: {self.global_best_fitness:.4f}")
            print(f"  Optimal Thresholds:")
            print(f"    Normal Range: {self.global_best[0]:.2f} - {self.global_best[1]:.2f} BPM")
            print(f"    Elevated Max: {self.global_best[2]:.2f} BPM")
        
        return self.global_best, self.global_best_fitness, self.fitness_history
    
    def predict(self, X_features, thresholds):
        """Predict menggunakan optimal thresholds"""
        mean_bpms = X_features[:, 0]
        y_pred = np.array([self.classify_bpm(bpm, thresholds) for bpm in mean_bpms])
        return y_pred


def run_pso_analysis(algorithm_type='standard'):
    """
    Run complete PSO analysis untuk semua subjects
    
    Args:
        algorithm_type: 'standard' atau 'adaptive'
    """
    print_section("PSO OPTIMIZATION - BPM CLASSIFICATION")
    print(f"\n  Algorithm Type: {algorithm_type}")
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load data
    print("\n📊 Loading Data...")
    data = DataLoader.load_optimized_dataset()
    df = DataLoader.load_feature_matrix()
    
    X = df.drop('label', axis=1).values
    y = df['label'].values
    
    print(f"  ✓ Loaded {X.shape[0]} samples with {X.shape[1]} features")
    print(f"  ✓ Classes: {np.sum(y==0)} normal, {np.sum(y==1)} abnormal")
    
    # Run PSO
    print("\n🔄 Running PSO Optimization...")
    pso = PSO(n_particles=20, max_iterations=100, w=0.7, c1=1.5, c2=1.5)
    best_thresholds, best_fitness, fitness_history = pso.optimize(X, y, verbose=True)
    
    # Evaluate
    print("\n📈 Evaluation Metrics:")
    y_pred = pso.predict(X, best_thresholds)
    accuracy = MetricsCalculator.calculate_accuracy(y, y_pred)
    precision = MetricsCalculator.calculate_precision(y, y_pred)
    recall = MetricsCalculator.calculate_recall(y, y_pred)
    f1 = MetricsCalculator.calculate_f1(precision, recall)
    cm = MetricsCalculator.calculate_confusion_matrix(y, y_pred)
    
    print_metrics(accuracy, precision, recall, f1, cm)
    
    # Generate visualizations untuk setiap subject
    print("\n📊 Generating BPM Timeline Visualizations...")
    results_dir = Path(__file__).parent / 'results'
    results_dir.mkdir(exist_ok=True)
    
    for i, (subject_key, subject_data) in enumerate(data.items(), 1):
        try:
            output_path = results_dir / f"{subject_key}_bpm_timeline.png"
            BPMVisualizer.plot_bpm_timeline(subject_key, subject_data, 'PSO', output_path)
            print(f"  ✓ {subject_key}: {output_path.name}")
        except Exception as e:
            print(f"  ✗ {subject_key}: Error - {e}")
    
    # Plot convergence
    print("\n📊 Generating Convergence Plot...")
    convergence_path = results_dir / "pso_fitness_convergence.png"
    generations = list(range(1, len(fitness_history) + 1))
    BPMVisualizer.plot_fitness_convergence(generations, fitness_history, 'PSO', convergence_path)
    print(f"  ✓ Convergence plot saved: {convergence_path.name}")
    
    # Save results
    print("\n💾 Saving Results...")
    results = {
        'algorithm': 'PSO',
        'timestamp': datetime.now().isoformat(),
        'best_thresholds': {
            'normal_min': float(best_thresholds[0]),
            'normal_max': float(best_thresholds[1]),
            'elevated_max': float(best_thresholds[2])
        },
        'metrics': {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1)
        },
        'confusion_matrix': {
            'TP': int(cm['TP']),
            'TN': int(cm['TN']),
            'FP': int(cm['FP']),
            'FN': int(cm['FN'])
        },
        'best_fitness': float(best_fitness),
        'total_iterations': len(fitness_history)
    }
    
    results_file = results_dir / 'pso_results.json'
    import json
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"  ✓ Results saved: {results_file.name}")
    
    print("\n" + "="*70)
    print("✅ PSO ANALYSIS COMPLETE!")
    print("="*70)
    
    return pso, best_thresholds, results


if __name__ == "__main__":
    # Run PSO analysis
    pso, best_thresholds, results = run_pso_analysis(algorithm_type='standard')
    
    print("\n" + "="*70)
    print("📁 Output Files:")
    print("="*70)
    results_dir = Path(__file__).parent / 'results'
    for file in sorted(results_dir.glob('*.png')):
        print(f"  📊 {file.name}")
    print(f"  📄 pso_results.json")
