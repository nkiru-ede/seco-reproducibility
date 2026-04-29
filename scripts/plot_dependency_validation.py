import matplotlib.pyplot as plt
import pandas as pd
import random
import numpy as np
import os

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
PLOTS_DIR = os.path.join(BASE_DIR, 'plots')

# Ensure plots directory exists
os.makedirs(PLOTS_DIR, exist_ok=True)

print("Plotting Dependency Validation: Jaccard Distance by Version Change Type\n")

# Sample size per ecosystem
SAMPLE_SIZE = 50000

ecosystems = {
    'npm': 'npm_dependency_results_batched.txt',
    'Maven': 'maven_dependency_results_batched.txt',
    'Go': 'go_dependency_results_batched.txt',
    'RubyGems': 'rubygems_dependency_results_batched.txt',
    'PyPI': 'pypi_dependency_results_batched.txt',
    'NuGet': 'nuget_dependency_results_batched.txt',
    'Cargo': 'cargo_dependency_results_batched.txt'
}

# Collect samples from all ecosystems
all_data = {'major': [], 'minor': [], 'patch': []}

for eco_name, filename in ecosystems.items():
    filepath = os.path.join(RESULTS_DIR, filename)

    # Check if file exists
    if not os.path.exists(filepath):
        print(f"  Warning: {filename} not found, skipping {eco_name}...")
        continue

    print(f"  Sampling from {eco_name}...")

    with open(filepath, 'r') as f:
        f.readline()  # Skip header

        lines = f.readlines()
        total_lines = len(lines)

        # Sample lines if too many
        if total_lines > SAMPLE_SIZE:
            sampled_lines = random.sample(lines, SAMPLE_SIZE)
        else:
            sampled_lines = lines

        for line in sampled_lines:
            parts = line.strip().split(',')
            if len(parts) == 4:
                change_type = parts[0]
                jaccard = float(parts[1])
                all_data[change_type].append(jaccard)

print()
print(f"Total samples - Major: {len(all_data['major'])}, Minor: {len(all_data['minor'])}, Patch: {len(all_data['patch'])}")
print()

# Calculate statistics
for change_type in ['major', 'minor', 'patch']:
    data = all_data[change_type]
    if len(data) == 0:
        print(f"{change_type.capitalize()}: No data available")
        continue

    print(f"{change_type.capitalize()}:")
    print(f"  Mean: {np.mean(data):.4f}")
    print(f"  Median: {np.median(data):.4f}")
    print(f"  Q1 (25%): {np.percentile(data, 25):.4f}")
    print(f"  Q3 (75%): {np.percentile(data, 75):.4f}")
    print(f"  95th percentile: {np.percentile(data, 95):.4f}")
    print()

# Create cleaner boxplot
fig, ax = plt.subplots(figsize=(10, 7))

data_to_plot = [all_data['major'], all_data['minor'], all_data['patch']]
labels = ['Major', 'Minor', 'Patch']
colors = ['#ff7f7f', '#7fbfff', '#7fff7f']  # Red, Blue, Green

# Create boxplot with limited outlier display
bp = ax.boxplot(data_to_plot,
                tick_labels=labels,
                patch_artist=True,
                widths=0.6,
                showfliers=True,  # Show outliers
                flierprops=dict(marker='o', markersize=2, alpha=0.3, markerfacecolor='gray'),
                medianprops=dict(color='black', linewidth=2.5),
                boxprops=dict(linewidth=1.5),
                whiskerprops=dict(linewidth=1.5),
                capprops=dict(linewidth=1.5))

# Color the boxes
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# Set y-axis limit to focus on the main distribution (up to 95th percentile)
max_95th = max([np.percentile(data, 95) for data in data_to_plot if len(data) > 0])
ax.set_ylim(0, min(0.5, max_95th * 1.2))

ax.set_ylabel('Jaccard Distance', fontsize=14, fontweight='bold')
ax.set_xlabel('Version Change Type', fontsize=14, fontweight='bold')
ax.set_title('Dependency Change Distribution Across All Ecosystems',
             fontsize=15, fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add mean annotations
for i, (label, data, color) in enumerate(zip(labels, data_to_plot, colors), 1):
    if len(data) == 0:
        continue
    mean_val = np.mean(data)
    # Add mean as a horizontal line
    ax.hlines(mean_val, i-0.3, i+0.3, colors='darkblue', linestyle='--', linewidth=2, alpha=0.8)
    # Annotate with mean value
    ax.text(i+0.35, mean_val, f'μ={mean_val:.3f}', va='center', fontsize=10,
            fontweight='bold', color='darkblue')

# Add subtitle with ecosystem info
ax.text(0.5, -0.12, 'Aggregated: npm, Maven, Go, RubyGems, PyPI, NuGet, Cargo',
        ha='center', va='top', transform=ax.transAxes, fontsize=10, style='italic', color='gray')

plt.tight_layout()
output_file = os.path.join(PLOTS_DIR, 'dependency_validation_jaccard.png')
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Boxplot saved to: {output_file}")

print("\nValidation plot complete!")
