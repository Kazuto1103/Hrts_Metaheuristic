"""
ACO (Ant Colony Optimization) - FINAL OPTIMIZED VERSION
Feature Selection & BPM Classification dengan Timeline Visualization 1-40
"""

import numpy as np
import pandas as pd
from pathlib import Path
import sys
import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

sys.path.insert(0, str(Path(__file__).parent.parent / 'utils'))

from helper import (
    DataLoader, BPMVisualizer, MetricsCalculator,
    create_output_directory, print_section, print_metrics
)
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import confusion_matrix as sk_confusion_matrix


class ACO:
    """Ant Colony Optimization untuk Feature Selection & BPM Classification"""
    
    def __init__(self, n_features=18, n_ants=15, n_iterations=50,
                 alpha=1.0, beta=2.0, rho=0.95, q=100):
        self.n_features = n_features
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        
        self.pheromone = np.ones(n_features) * 0.5
        self.best_features = None
        self.best_fitness = -np.inf
        self.fitness_history = []
        self.heuristic = np.ones(n_features) * 0.5
    
    def calculate_feature_heuristic(self, X, y):
        """Calculate feature importance menggunakan Random Forest"""
        clf = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=5)
        clf.fit(X, y)
        
        importance = clf.feature_importances_
        min_imp, max_imp = np.min(importance), np.max(importance)
        self.heuristic = 0.1 + 0.9 * (importance - min_imp) / (max_imp - min_imp + 1e-10)
    
    def construct_solution(self, n_min_features=5):
        """Build feature selection dari semut"""
        solution = np.zeros(self.n_features, dtype=int)
        
        for feature_idx in range(self.n_features):
            pheromone_effect = self.pheromone[feature_idx] ** self.alpha
            heuristic_effect = self.heuristic[feature_idx] ** self.beta
            probability = (pheromone_effect * heuristic_effect) / \
                         (np.sum(self.pheromone ** self.alpha * self.heuristic ** self.beta) + 1e-10)
            
            if np.random.rand() < probability:
                solution[feature_idx] = 1
        
        if np.sum(solution) < n_min_features:
            available = np.where(solution == 0)[0]
            n_to_add = n_min_features - np.sum(solution)
            selected = np.random.choice(available, min(n_to_add, len(available)), replace=False)
            solution[selected] = 1
        
        return solution
    
    def evaluate_solution(self, solution, X, y):
        """Evaluate quality of feature selection"""
        if np.sum(solution) < 1:
            return 0.0
        
        try:
            X_selected = X[:, solution == 1]
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_selected)
            
            clf = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=5)
            scores = cross_val_score(clf, X_scaled, y, cv=3, scoring='accuracy')
            fitness = np.mean(scores)
            
            feature_count = np.sum(solution)
            feature_penalty = 1.0 - (feature_count / self.n_features) * 0.2
            total_fitness = fitness * feature_penalty
            
            return total_fitness
        
        except Exception as e:
            return 0.0
    
    def update_pheromone(self, solutions, fitnesses):
        """Update pheromone levels"""
        self.pheromone = self.rho * self.pheromone
        
        best_idx = np.argmax(fitnesses)
        best_solution = solutions[best_idx]
        best_fitness = fitnesses[best_idx]
        
        pheromone_deposit = self.q * best_fitness
        self.pheromone[best_solution == 1] += pheromone_deposit
        self.pheromone = np.clip(self.pheromone, 0.1, 5.0)
    
    def optimize(self, X, y, verbose=True):
        """Run ACO optimization"""
        if verbose:
            print_section("ACO OPTIMIZATION PROCESS")
            print(f"\n  Ants: {self.n_ants}")
            print(f"  Iterations: {self.n_iterations}")
            print(f"  Alpha: {self.alpha}, Beta: {self.beta}, Rho: {self.rho}")
        
        print("\n📊 Calculating Feature Importance...")
        self.calculate_feature_heuristic(X, y)
        
        for iteration in range(self.n_iterations):
            solutions = []
            fitnesses = []
            
            for ant in range(self.n_ants):
                solution = self.construct_solution()
                fitness = self.evaluate_solution(solution, X, y)
                
                solutions.append(solution)
                fitnesses.append(fitness)
                
                if fitness > self.best_fitness:
                    self.best_fitness = fitness
                    self.best_features = solution.copy()
            
            self.update_pheromone(solutions, fitnesses)
            self.fitness_history.append(self.best_fitness)
            
            if verbose and (iteration + 1) % 5 == 0:
                n_features_selected = np.sum(self.best_features)
                print(f"  Iteration {iteration+1:3d}/{self.n_iterations}: "
                      f"Fitness = {self.best_fitness:.4f}, "
                      f"Features = {n_features_selected:2d}")
        
        if verbose:
            print(f"\n  ✅ Optimization Complete!")
            print(f"  Final Best Fitness: {self.best_fitness:.4f}")
            n_features = np.sum(self.best_features)
            print(f"  Selected Features: {n_features}/{self.n_features}")
        
        return self.best_features, self.best_fitness


def run_aco_analysis():
    """Run complete ACO analysis"""
    print_section("ACO OPTIMIZATION - FINAL VERSION")
    print(f"\n  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load data
    print("\n📊 Loading Data...")
    data = DataLoader.load_optimized_dataset()
    df = DataLoader.load_feature_matrix()
    
    X = df.drop('label', axis=1).values
    y = df['label'].values
    
    print(f"  ✓ Loaded {X.shape[0]} samples with {X.shape[1]} features")
    print(f"  ✓ Classes: {np.sum(y==0)} normal, {np.sum(y==1)} abnormal")
    
    # Run ACO
    print("\n🐜 Running ACO Optimization...")
    aco = ACO(n_features=X.shape[1], n_ants=15, n_iterations=50)
    best_features, best_fitness = aco.optimize(X, y, verbose=True)
    
    # Evaluate
    print("\n📈 Evaluation with Selected Features:")
    scaler = StandardScaler()
    X_selected = X[:, best_features == 1]
    X_scaled = scaler.fit_transform(X_selected)
    
    clf = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=5)
    y_pred = cross_val_predict(clf, X_scaled, y, cv=3)
    
    accuracy = MetricsCalculator.calculate_accuracy(y, y_pred)
    precision = MetricsCalculator.calculate_precision(y, y_pred)
    recall = MetricsCalculator.calculate_recall(y, y_pred)
    f1 = MetricsCalculator.calculate_f1(precision, recall)
    cm = MetricsCalculator.calculate_confusion_matrix(y, y_pred)
    
    print_metrics(accuracy, precision, recall, f1, cm)
    
    # Generate visualizations untuk orang 1-40
    print("\n📊 Generating BPM Timeline Visualizations (1-40)...")
    results_dir = Path(__file__).parent / 'results'
    results_dir.mkdir(exist_ok=True)
    
    for i, (subject_key, subject_data) in enumerate(data.items(), 1):
        try:
            output_path = results_dir / f"{subject_key}_bpm_timeline.png"
            BPMVisualizer.plot_bpm_timeline(subject_key, subject_data, 'ACO', output_path)
            if i % 5 == 0 or i == len(data):
                print(f"  ✓ Generated {i}/{len(data)} timeline visualizations")
        except Exception as e:
            print(f"  ✗ {subject_key}: {e}")
    
    # Convergence plot
    print("\n📊 Generating Convergence Plot...")
    convergence_path = results_dir / "aco_fitness_convergence.png"
    iterations = list(range(1, len(aco.fitness_history) + 1))
    BPMVisualizer.plot_fitness_convergence(iterations, aco.fitness_history, 'ACO', convergence_path)
    print(f"  ✓ Saved: aco_fitness_convergence.png")
    
    # Feature importance plot
    print("\n📊 Generating Feature Importance Plot...")
    feature_importance_path = results_dir / "aco_feature_importance.png"
    feature_names = [f"Feature {i+1}" for i in range(X.shape[1])]
    BPMVisualizer.plot_feature_importance(feature_names, aco.heuristic, 'ACO', 
                                         feature_importance_path)
    print(f"  ✓ Saved: aco_feature_importance.png")
    
    # Save results
    print("\n💾 Saving Results...")
    selected_feature_indices = np.where(best_features == 1)[0].tolist()
    results = {
        'algorithm': 'ACO',
        'timestamp': datetime.now().isoformat(),
        'selected_features': selected_feature_indices,
        'n_selected_features': int(np.sum(best_features)),
        'total_features': X.shape[1],
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
        'best_fitness': float(best_fitness)
    }
    
    results_file = results_dir / 'aco_results.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"  ✓ Saved: aco_results.json")
    
    print("\n" + "="*75)
    print("✅ ACO ANALYSIS COMPLETE!")
    print("="*75)
    print(f"\n📁 Generated {len(list(results_dir.glob('orang_*_bpm_timeline.png')))} timeline visualizations")
    print(f"📊 Convergence & Feature importance plots generated")
    print(f"💾 Results saved to JSON\n")
    
    return aco, best_features, results


if __name__ == "__main__":
    aco, best_features, results = run_aco_analysis()
