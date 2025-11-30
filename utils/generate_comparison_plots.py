"""
Generate Comparison Plots - ACO vs PSO
Visualisasi perbandingan kedua algoritma optimasi
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def load_results():
    """Load hasil dari ACO dan PSO"""
    aco_path = Path(__file__).parent.parent / "aco" / "results" / "aco_results.json"
    pso_path = Path(__file__).parent.parent / "pso" / "results" / "pso_results.json"
    
    with open(aco_path, 'r') as f:
        aco_results = json.load(f)
    
    with open(pso_path, 'r') as f:
        pso_results = json.load(f)
    
    return aco_results, pso_results

def create_metrics_comparison(aco_results, pso_results):
    """Buat perbandingan metrics ACO vs PSO"""
    print("  Creating metrics comparison plot...")
    
    algorithms = ['ACO', 'PSO']
    aco_metrics = aco_results.get('metrics', aco_results)  # Handle both old and new format
    pso_metrics = pso_results.get('metrics', pso_results)
    
    accuracy = [aco_metrics['accuracy'], pso_metrics['accuracy']]
    precision = [aco_metrics['precision'], pso_metrics['precision']]
    recall = [aco_metrics['recall'], pso_metrics['recall']]
    f1 = [aco_metrics['f1_score'], pso_metrics['f1_score']]
    
    x = np.arange(len(algorithms))
    width = 0.2
    
    fig, ax = plt.subplots(figsize=(11, 6))
    
    rects1 = ax.bar(x - 1.5*width, accuracy, width, label='Accuracy', color='#FF6B6B', alpha=0.8)
    rects2 = ax.bar(x - 0.5*width, precision, width, label='Precision', color='#4ECDC4', alpha=0.8)
    rects3 = ax.bar(x + 0.5*width, recall, width, label='Recall', color='#95E1D3', alpha=0.8)
    rects4 = ax.bar(x + 1.5*width, f1, width, label='F1-Score', color='#FFE66D', alpha=0.8)
    
    ax.set_ylabel('Score', fontsize=12, fontweight='bold')
    ax.set_title('Performance Metrics Comparison - ACO vs PSO (40 People Dataset)', 
                 fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, fontsize=11, fontweight='bold')
    ax.legend(fontsize=11, loc='upper left')
    ax.set_ylim([0, 1.1])
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for rects in [rects1, rects2, rects3, rects4]:
        for rect in rects:
            height = rect.get_height()
            if height > 0:
                ax.text(rect.get_x() + rect.get_width()/2., height,
                       f'{height:.3f}',
                       ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(Path(__file__).parent.parent / "results" / "aco_pso_metrics_comparison.png", 
                dpi=150, bbox_inches='tight')
    print("  ✓ Metrics comparison saved")
    plt.close()

def create_convergence_comparison(aco_results, pso_results):
    """Buat perbandingan konvergensi ACO vs PSO"""
    print("  Creating convergence comparison plot...")
    
    # Check if fitness_history exists
    if 'fitness_history' not in aco_results or 'fitness_history' not in pso_results:
        print("  ⚠ Fitness history not available in results")
        return
    
    aco_history = aco_results['fitness_history']
    pso_history = pso_results['fitness_history']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # ACO convergence
    ax1.plot(aco_history, linewidth=2.5, color='#FF6B6B', marker='o', markersize=3)
    ax1.fill_between(range(len(aco_history)), aco_history, alpha=0.2, color='#FF6B6B')
    ax1.set_xlabel('Iteration', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Best Fitness', fontsize=11, fontweight='bold')
    ax1.set_title(f'ACO Fitness Convergence\n(Final: {aco_history[-1]:.4f})', 
                  fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # PSO convergence
    ax2.plot(pso_history, linewidth=2.5, color='#4ECDC4', marker='s', markersize=3)
    ax2.fill_between(range(len(pso_history)), pso_history, alpha=0.2, color='#4ECDC4')
    ax2.set_xlabel('Iteration', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Best Fitness', fontsize=11, fontweight='bold')
    ax2.set_title(f'PSO Fitness Convergence\n(Final: {pso_history[-1]:.4f})', 
                  fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--')
    
    fig.suptitle('Convergence Behavior Comparison - 40 People (12,000 BPM Readings)', 
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(Path(__file__).parent.parent / "results" / "aco_pso_convergence_comparison.png", 
                dpi=150, bbox_inches='tight')
    print("  ✓ Convergence comparison saved")
    plt.close()

def create_summary_report(aco_results, pso_results):
    """Buat ringkasan report dalam bentuk visualisasi"""
    print("  Creating summary report visualization...")
    
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.4, wspace=0.3)
    
    # Title
    fig.suptitle('ACO vs PSO Optimization Results - 40 People Dataset (12,000 BPM Readings)', 
                 fontsize=14, fontweight='bold', y=0.98)
    
    # 1. Algorithm Info
    ax1 = fig.add_subplot(gs[0, :])
    ax1.axis('off')
    
    info_text = f"""
    DATASET INFORMATION
    ├─ Total Samples: 40 people
    ├─ Total BPM Readings: 12,000
    ├─ Normal: 3,625 (30.2%)
    └─ Tachycardia: 8,375 (69.8%)
    
    ACO RESULTS
    ├─ Ants: 20 | Iterations: 50
    ├─ Features Selected: {aco_results['selected_features']}/{aco_results['total_features']}
    ├─ Best Fitness: {aco_results['best_fitness']:.4f}
    ├─ Accuracy: {aco_results['accuracy']:.4f}
    ├─ F1-Score: {aco_results['f1_score']:.4f}
    └─ Time Complexity: O(ants × iterations × features)
    
    PSO RESULTS
    ├─ Particles: 25 | Iterations: 100
    ├─ Optimal Threshold: {pso_results['optimal_threshold_bpm']:.2f} bpm
    ├─ Best Fitness: {pso_results['best_fitness']:.4f}
    ├─ Accuracy: {pso_results['accuracy']:.4f}
    ├─ F1-Score: {pso_results['f1_score']:.4f}
    └─ Time Complexity: O(particles × iterations)
    """
    
    ax1.text(0.02, 0.5, info_text, fontsize=10, family='monospace',
            verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    # 2. Accuracy Comparison
    ax2 = fig.add_subplot(gs[1, 0])
    algorithms = ['ACO', 'PSO']
    accuracies = [aco_results['accuracy'], pso_results['accuracy']]
    colors = ['#FF6B6B', '#4ECDC4']
    bars = ax2.bar(algorithms, accuracies, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Accuracy', fontsize=11, fontweight='bold')
    ax2.set_title('Accuracy Comparison', fontsize=11, fontweight='bold')
    ax2.set_ylim([0, 1.1])
    ax2.grid(axis='y', alpha=0.3)
    for i, (bar, acc) in enumerate(zip(bars, accuracies)):
        ax2.text(bar.get_x() + bar.get_width()/2, acc + 0.02, f'{acc:.4f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 3. F1-Score Comparison
    ax3 = fig.add_subplot(gs[1, 1])
    f1_scores = [aco_results['f1_score'], pso_results['f1_score']]
    bars = ax3.bar(algorithms, f1_scores, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax3.set_ylabel('F1-Score', fontsize=11, fontweight='bold')
    ax3.set_title('F1-Score Comparison', fontsize=11, fontweight='bold')
    ax3.set_ylim([0, 1.1])
    ax3.grid(axis='y', alpha=0.3)
    for i, (bar, f1) in enumerate(zip(bars, f1_scores)):
        ax3.text(bar.get_x() + bar.get_width()/2, f1 + 0.02, f'{f1:.4f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 4. Recommendation
    ax4 = fig.add_subplot(gs[2, :])
    ax4.axis('off')
    
    if aco_results['accuracy'] >= pso_results['accuracy']:
        winner = "ACO"
        reason = f"ACO achieves {aco_results['accuracy']:.1%} accuracy with {aco_results['selected_features']} selected features"
    else:
        winner = "PSO"
        reason = f"PSO achieves {pso_results['accuracy']:.1%} accuracy with optimal threshold {pso_results['optimal_threshold_bpm']:.2f} bpm"
    
    rec_text = f"""
    RECOMMENDATION
    
    ✓ Winner: {winner}
    
    Reason: {reason}
    
    ✓ Best Algorithm for Feature Selection: ACO ({aco_results['selected_features']}/{aco_results['total_features']} features)
    ✓ Best Algorithm for Threshold Optimization: PSO (Optimal: {pso_results['optimal_threshold_bpm']:.2f} bpm)
    
    Next Steps:
    ├─ Deploy optimized model with {winner}'s parameters
    ├─ Validate on additional test dataset
    └─ Monitor model performance in production
    """
    
    ax4.text(0.02, 0.5, rec_text, fontsize=10, family='monospace',
            verticalalignment='center', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.2))
    
    plt.savefig(Path(__file__).parent.parent / "results" / "aco_pso_summary_report.png", 
                dpi=150, bbox_inches='tight')
    print("  ✓ Summary report saved")
    plt.close()

def main():
    print("="*75)
    print("  ACO vs PSO COMPARISON PLOTS GENERATOR")
    print("="*75)
    print()
    
    print("📊 Loading Results...")
    aco_results, pso_results = load_results()
    
    aco_metrics = aco_results.get('metrics', aco_results)
    pso_metrics = pso_results.get('metrics', pso_results)
    
    print(f"  ✓ ACO Results loaded: Accuracy = {aco_metrics['accuracy']:.4f}")
    print(f"  ✓ PSO Results loaded: Accuracy = {pso_metrics['accuracy']:.4f}")
    print()
    
    print("📈 Generating Comparison Plots...")
    print()
    
    output_dir = Path(__file__).parent.parent / "results"
    output_dir.mkdir(exist_ok=True)
    
    create_metrics_comparison(aco_results, pso_results)
    create_convergence_comparison(aco_results, pso_results)
    
    print()
    print("="*75)
    print("✅ COMPARISON PLOTS GENERATED!")
    print("="*75)
    print()
    print(f"📁 Output Directory: {output_dir}")
    print(f"   ├─ aco_pso_metrics_comparison.png")
    print(f"   ├─ aco_pso_convergence_comparison.png")
    print(f"   └─ aco_pso_summary_report.png")
    print()

if __name__ == "__main__":
    main()
