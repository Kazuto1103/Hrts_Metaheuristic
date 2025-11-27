"""
ACO (Ant Colony Optimization) Algorithm untuk BPM Feature Selection & Classification
Mengoptimalkan kombinasi fitur untuk klasifikasi terbaik
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
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score


class ACO:
    """Ant Colony Optimization untuk Feature Selection & BPM Classification"""
    
    def __init__(self, n_features=18, n_ants=15, n_iterations=50,
                 alpha=1.0, beta=2.0, rho=0.95, q=100):
        """
        Initialize ACO
        
        Args:
            n_features: Jumlah fitur total
            n_ants: Jumlah semut dalam colony
            n_iterations: Jumlah iterasi
            alpha: Pheromone influence
            beta: Heuristic influence (fitur importance)
            rho: Pheromone decay rate (evaporation)
            q: Pheromone deposit factor
        """
        self.n_features = n_features
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        
        # Initialize pheromone levels (setiap fitur mulai dengan nilai sama)
        self.pheromone = np.ones(n_features) * 0.5
        self.pheromone_history = []
        
        # Best solution tracking
        self.best_features = None
        self.best_fitness = -np.inf
        self.best_solutions = []
        self.fitness_history = []
        
        # Feature heuristic values (calculated later)
        self.heuristic = np.ones(n_features) * 0.5
    
    def calculate_feature_heuristic(self, X, y):
        """
        Calculate heuristic information (importance) untuk setiap fitur
        Menggunakan feature importance dari Random Forest
        
        Args:
            X: Feature matrix
            y: Labels
        """
        clf = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=5)
        clf.fit(X, y)
        
        # Normalize importance ke range [0.1, 1.0]
        importance = clf.feature_importances_
        min_imp, max_imp = np.min(importance), np.max(importance)
        self.heuristic = 0.1 + 0.9 * (importance - min_imp) / (max_imp - min_imp + 1e-10)
    
    def construct_solution(self, n_min_features=5):
        """
        Build feature selection dari satu semut
        Menggunakan probabilitas berdasarkan pheromone dan heuristic
        
        Args:
            n_min_features: Minimum jumlah fitur yang harus dipilih
        
        Returns:
            solution: binary array (1 = pilih fitur, 0 = tidak)
        """
        solution = np.zeros(self.n_features, dtype=int)
        
        for feature_idx in range(self.n_features):
            # Probability proportional to pheromone^alpha * heuristic^beta
            pheromone_effect = self.pheromone[feature_idx] ** self.alpha
            heuristic_effect = self.heuristic[feature_idx] ** self.beta
            probability = (pheromone_effect * heuristic_effect) / \
                         (np.sum(self.pheromone ** self.alpha * self.heuristic ** self.beta) + 1e-10)
            
            if np.random.rand() < probability:
                solution[feature_idx] = 1
        
        # Ensure minimum features selected
        if np.sum(solution) < n_min_features:
            # Randomly select additional features
            available = np.where(solution == 0)[0]
            n_to_add = n_min_features - np.sum(solution)
            selected = np.random.choice(available, min(n_to_add, len(available)), replace=False)
            solution[selected] = 1
        
        return solution
    
    def evaluate_solution(self, solution, X, y):
        """
        Evaluate kualitas feature selection
        
        Args:
            solution: binary array of features
            X: Feature matrix
            y: Labels
        
        Returns:
            fitness score (0-1)
        """
        # Minimum fitur yang valid
        if np.sum(solution) < 1:
            return 0.0
        
        try:
            # Select features
            X_selected = X[:, solution == 1]
            
            # Scaler
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_selected)
            
            # Cross-validation score
            clf = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=5)
            scores = cross_val_score(clf, X_scaled, y, cv=3, scoring='accuracy')
            fitness = np.mean(scores)
            
            # Penalty untuk terlalu banyak fitur
            feature_count = np.sum(solution)
            feature_penalty = 1.0 - (feature_count / self.n_features) * 0.2  # Max 20% penalty
            
            total_fitness = fitness * feature_penalty
            
            return total_fitness
        
        except Exception as e:
            return 0.0
    
    def update_pheromone(self, solutions, fitnesses):
        """
        Update pheromone levels berdasarkan quality dari solutions
        
        Args:
            solutions: List of ant solutions
            fitnesses: List of fitness values
        """
        # Evaporation
        self.pheromone = self.rho * self.pheromone
        
        # Deposit pheromone untuk best solutions
        best_idx = np.argmax(fitnesses)
        best_solution = solutions[best_idx]
        best_fitness = fitnesses[best_idx]
        
        # Update pheromone untuk selected features
        pheromone_deposit = self.q * best_fitness
        self.pheromone[best_solution == 1] += pheromone_deposit
        
        # Keep pheromone dalam range [0.1, 5.0]
        self.pheromone = np.clip(self.pheromone, 0.1, 5.0)
        
        self.pheromone_history.append(self.pheromone.copy())
    
    def optimize(self, X, y, verbose=True):
        """
        Run ACO optimization
        
        Args:
            X: Feature matrix
            y: Labels
            verbose: Print progress
        
        Returns:
            best_solution, best_fitness, solutions_history
        """
        if verbose:
            print_section("ACO OPTIMIZATION PROCESS")
            print(f"\n  Ants: {self.n_ants}")
            print(f"  Iterations: {self.n_iterations}")
            print(f"  Alpha (pheromone): {self.alpha}")
            print(f"  Beta (heuristic): {self.beta}")
            print(f"  Rho (evaporation): {self.rho}")
        
        # Calculate feature importance untuk heuristic
        print("\n📊 Calculating Feature Importance...")
        self.calculate_feature_heuristic(X, y)
        print(f"  ✓ Feature heuristic calculated")
        
        # Main ACO loop
        for iteration in range(self.n_iterations):
            solutions = []
            fitnesses = []
            
            # Construct solutions oleh setiap ant
            for ant in range(self.n_ants):
                solution = self.construct_solution()
                fitness = self.evaluate_solution(solution, X, y)
                
                solutions.append(solution)
                fitnesses.append(fitness)
                
                # Update best
                if fitness > self.best_fitness:
                    self.best_fitness = fitness
                    self.best_features = solution.copy()
            
            # Update pheromone
            self.update_pheromone(solutions, fitnesses)
            self.fitness_history.append(self.best_fitness)
            self.best_solutions.append(self.best_features.copy())
            
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
        
        return self.best_features, self.best_fitness, self.fitness_history
    
    def predict(self, X, y, features=None, n_splits=3):
        """Predict menggunakan selected features"""
        if features is None:
            features = self.best_features
        
        X_selected = X[:, features == 1]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_selected)
        
        clf = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=5)
        scores = cross_val_score(clf, X_scaled, y, cv=n_splits, scoring='accuracy')
        
        return scores


def run_aco_analysis():
    """
    Run complete ACO analysis untuk feature selection & BPM classification
    """
    print_section("ACO OPTIMIZATION - FEATURE SELECTION & BPM CLASSIFICATION")
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
    aco = ACO(n_features=X.shape[1], n_ants=15, n_iterations=50,
              alpha=1.0, beta=2.0, rho=0.95)
    best_features, best_fitness, fitness_history = aco.optimize(X, y, verbose=True)
    
    # Evaluate with selected features
    print("\n📈 Evaluation with Selected Features:")
    scaler = StandardScaler()
    X_selected = X[:, best_features == 1]
    X_scaled = scaler.fit_transform(X_selected)
    
    clf = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=5)
    from sklearn.model_selection import cross_val_predict
    y_pred = cross_val_predict(clf, X_scaled, y, cv=3)
    
    accuracy = MetricsCalculator.calculate_accuracy(y, y_pred)
    precision = MetricsCalculator.calculate_precision(y, y_pred)
    recall = MetricsCalculator.calculate_recall(y, y_pred)
    f1 = MetricsCalculator.calculate_f1(precision, recall)
    cm = MetricsCalculator.calculate_confusion_matrix(y, y_pred)
    
    print_metrics(accuracy, precision, recall, f1, cm)
    
    # Generate visualizations untuk setiap subject
    print("\n📊 Generating BPM Timeline Visualizations (ACO)...")
    results_dir = Path(__file__).parent / 'results'
    results_dir.mkdir(exist_ok=True)
    
    for i, (subject_key, subject_data) in enumerate(data.items(), 1):
        try:
            output_path = results_dir / f"{subject_key}_bpm_timeline.png"
            BPMVisualizer.plot_bpm_timeline(subject_key, subject_data, 'ACO', output_path)
            print(f"  ✓ {subject_key}: {output_path.name}")
        except Exception as e:
            print(f"  ✗ {subject_key}: Error - {e}")
    
    # Plot convergence
    print("\n📊 Generating Convergence Plot (ACO)...")
    convergence_path = results_dir / "aco_fitness_convergence.png"
    iterations = list(range(1, len(fitness_history) + 1))
    BPMVisualizer.plot_fitness_convergence(iterations, fitness_history, 'ACO', convergence_path)
    print(f"  ✓ Convergence plot saved: {convergence_path.name}")
    
    # Plot feature importance
    print("\n📊 Generating Feature Importance Plot...")
    feature_importance_path = results_dir / "aco_feature_importance.png"
    feature_names = [f"Feature {i+1}" for i in range(X.shape[1])]
    BPMVisualizer.plot_feature_importance(feature_names, aco.heuristic, 'ACO', 
                                         feature_importance_path)
    print(f"  ✓ Feature importance plot saved: {feature_importance_path.name}")
    
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
        'best_fitness': float(best_fitness),
        'total_iterations': len(fitness_history)
    }
    
    results_file = results_dir / 'aco_results.json'
    import json
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"  ✓ Results saved: {results_file.name}")
    
    print("\n" + "="*70)
    print("✅ ACO ANALYSIS COMPLETE!")
    print("="*70)
    
    return aco, best_features, results


if __name__ == "__main__":
    # Run ACO analysis
    aco, best_features, results = run_aco_analysis()
    
    print("\n" + "="*70)
    print("📁 Output Files:")
    print("="*70)
    results_dir = Path(__file__).parent / 'results'
    for file in sorted(results_dir.glob('*.png')):
        print(f"  📊 {file.name}")
    print(f"  📄 aco_results.json")
