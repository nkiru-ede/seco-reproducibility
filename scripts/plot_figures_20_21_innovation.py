import pickle
import matplotlib.pyplot as plt
import numpy as np
import os

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
PLOTS_DIR = os.path.join(BASE_DIR, 'plots')

# Ensure plots directory exists
os.makedirs(PLOTS_DIR, exist_ok=True)

print("Plotting Figures 20 & 21: Innovation Metrics\n")

# Load all innovation data
ecosystems = {
    'Maven': {'start': 2002, 'color': '#1f77b4'},
    'PyPI': {'start': 2005, 'color': '#ff7f0e'},
    'RubyGems': {'start': 2009, 'color': '#2ca02c'},
    'npm': {'start': 2010, 'color': '#d62728'},
    'NuGet': {'start': 2011, 'color': '#9467bd'},
    'Cargo': {'start': 2015, 'color': '#8c564b'},
    'Go': {'start': 2018, 'color': '#e377c2'}
}

all_data = {}
for eco in ecosystems.keys():
    pkl_file = os.path.join(RESULTS_DIR, f"innovation_{eco.lower()}.pkl")
    try:
        with open(pkl_file, 'rb') as f:
            all_data[eco] = pickle.load(f)
        print(f"Loaded {eco}: {len(all_data[eco]['innov_new'])} years")
    except Exception as e:
        print(f"Error loading {eco}: {e}")

print(f"\nTotal ecosystems: {len(all_data)}")
print()

# ============================================================================
# Figure 20: InnovNEW (New Package Innovation)
# ============================================================================

fig, ax = plt.subplots(figsize=(12, 7))

for eco in ['Maven', 'PyPI', 'RubyGems', 'npm', 'NuGet', 'Cargo', 'Go']:
    if eco in all_data:
        data = all_data[eco]
        innov_new = data['innov_new']

        years = sorted(innov_new.keys())
        values = [innov_new[y] for y in years]

        ax.plot(years, values,
                marker='o',
                linewidth=2,
                markersize=4,
                label=eco,
                color=ecosystems[eco]['color'])

ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Ratio', fontsize=12, fontweight='bold')
ax.set_title('InnovNEW (FirstPackage/LastPackage)', fontsize=14, fontweight='bold')
ax.legend(loc='best', frameon=True, fontsize=10)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlim(2000, 2024)
ax.set_ylim(0, max([max(all_data[e]['innov_new'].values()) for e in all_data]) * 1.1)

# Add horizontal line at 0
ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.3)

# Add horizontal dotted line at y=1 (equilibrium)
ax.axhline(y=1, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)

# Explicitly show 2023 on x-axis
ax.set_xticks([2000, 2005, 2010, 2015, 2020, 2023])
ax.set_xticklabels([2000, 2005, 2010, 2015, 2020, 2023])

plt.tight_layout()
output_file = os.path.join(PLOTS_DIR, 'figure_20_innovation_new.png')
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print("Saved: figure_20_innovation_new.png")

# ============================================================================
# Figure 21: InnovUPD (Existing Package Innovation)
# ============================================================================

fig, ax = plt.subplots(figsize=(12, 7))

for eco in ['Maven', 'PyPI', 'RubyGems', 'npm', 'NuGet', 'Cargo', 'Go']:
    if eco in all_data:
        data = all_data[eco]
        innov_upd = data['innov_upd']

        years = sorted(innov_upd.keys())
        values = [innov_upd[y] for y in years]

        ax.plot(years, values,
                marker='s',
                linewidth=2,
                markersize=4,
                label=eco,
                color=ecosystems[eco]['color'])

ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Ratio', fontsize=12, fontweight='bold')
ax.set_title('InnovUPD (MajorReleasePackage/LastPackage)', fontsize=14, fontweight='bold')
ax.legend(loc='best', frameon=True, fontsize=10)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlim(2000, 2024)
ax.set_ylim(0, max([max(all_data[e]['innov_upd'].values()) for e in all_data]) * 1.1)

# Add horizontal line at 0
ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.3)

# Explicitly show 2023 on x-axis
ax.set_xticks([2000, 2005, 2010, 2015, 2020, 2023])
ax.set_xticklabels([2000, 2005, 2010, 2015, 2020, 2023])

plt.tight_layout()
output_file = os.path.join(PLOTS_DIR, 'figure_21_innovation_update.png')
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print("Saved: figure_21_innovation_update.png")

# ============================================================================
# Combined Figure: Both Metrics Side-by-Side
# ============================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

# Left panel: InnovNEW
for eco in ['Maven', 'PyPI', 'RubyGems', 'npm', 'NuGet', 'Cargo', 'Go']:
    if eco in all_data:
        data = all_data[eco]
        innov_new = data['innov_new']

        years = sorted(innov_new.keys())
        values = [innov_new[y] for y in years]

        ax1.plot(years, values,
                marker='o',
                linewidth=2,
                markersize=4,
                label=eco,
                color=ecosystems[eco]['color'])

ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
ax1.set_ylabel('Ratio', fontsize=12, fontweight='bold')
ax1.set_title('(a) InnovNEW (FirstPackage/LastPackage)', fontsize=13, fontweight='bold')
ax1.legend(loc='best', frameon=True, fontsize=9)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xlim(2000, 2024)
ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.3)
ax1.axhline(y=1, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)
ax1.set_xticks([2000, 2005, 2010, 2015, 2020, 2023])
ax1.set_xticklabels([2000, 2005, 2010, 2015, 2020, 2023])

# Right panel: InnovUPD
for eco in ['Maven', 'PyPI', 'RubyGems', 'npm', 'NuGet', 'Cargo', 'Go']:
    if eco in all_data:
        data = all_data[eco]
        innov_upd = data['innov_upd']

        years = sorted(innov_upd.keys())
        values = [innov_upd[y] for y in years]

        ax2.plot(years, values,
                marker='s',
                linewidth=2,
                markersize=4,
                label=eco,
                color=ecosystems[eco]['color'])

ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
ax2.set_ylabel('Ratio', fontsize=12, fontweight='bold')
ax2.set_title('(b) InnovUPD (MajorReleasePackage/LastPackage)', fontsize=13, fontweight='bold')
ax2.legend(loc='best', frameon=True, fontsize=9)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.set_xlim(2000, 2024)
ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.3)
ax2.set_xticks([2000, 2005, 2010, 2015, 2020, 2023])
ax2.set_xticklabels([2000, 2005, 2010, 2015, 2020, 2023])

plt.suptitle('Innovation Metrics',
             fontsize=14, fontweight='bold', y=1.00)
plt.tight_layout()
output_file = os.path.join(PLOTS_DIR, 'figures_20_21_innovation_combined.png')
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print("Saved: figures_20_21_innovation_combined.png")

# ============================================================================
# Summary Statistics
# ============================================================================

print("\n" + "="*70)
print("INNOVATION METRICS SUMMARY")
print("="*70)

for eco in ['Maven', 'PyPI', 'RubyGems', 'npm', 'NuGet', 'Cargo', 'Go']:
    if eco in all_data:
        data = all_data[eco]
        innov_new = data['innov_new']
        innov_upd = data['innov_upd']

        years = sorted(innov_new.keys())

        print(f"\n{eco} ({min(years)}-{max(years)}):")
        print(f"  InnovNEW:")
        print(f"    Start: {innov_new[min(years)]:.4f}")
        print(f"    End:   {innov_new[max(years)]:.4f}")
        print(f"    Change: {innov_new[max(years)] - innov_new[min(years)]:.4f}")
        print(f"  InnovUPD:")
        print(f"    Start: {innov_upd[min(years)]:.4f}")
        print(f"    End:   {innov_upd[max(years)]:.4f}")
        print(f"    Change: {innov_upd[max(years)] - innov_upd[min(years)]:.4f}")

print("\n" + "="*70)
print("KEY FINDINGS:")
print("="*70)

# Calculate trend direction for each ecosystem
declining_new = []
increasing_upd = []

for eco in all_data:
    innov_new = all_data[eco]['innov_new']
    innov_upd = all_data[eco]['innov_upd']

    years = sorted(innov_new.keys())
    if len(years) >= 3:
        # Simple trend check: first third vs last third
        first_third = np.mean([innov_new[y] for y in years[:len(years)//3]])
        last_third = np.mean([innov_new[y] for y in years[-len(years)//3:]])

        if last_third < first_third * 0.8:  # Decline > 20%
            declining_new.append(eco)

        first_third_upd = np.mean([innov_upd[y] for y in years[:len(years)//3]])
        last_third_upd = np.mean([innov_upd[y] for y in years[-len(years)//3:]])

        if last_third_upd > first_third_upd * 1.5:  # Increase > 50%
            increasing_upd.append(eco)

print(f"\nEcosystems with declining InnovNEW (>20%): {len(declining_new)}/7")
for eco in declining_new:
    print(f"  - {eco}")

print(f"\nEcosystems with increasing InnovUPD (>50%): {len(increasing_upd)}/7")
for eco in increasing_upd:
    print(f"  - {eco}")

print("\n" + "="*70)
print("PLOTTING COMPLETE")
print("="*70)
print("\nGenerated files:")
print("  1. figure_20_innovation_new.png")
print("  2. figure_21_innovation_update.png")
print("  3. figures_20_21_innovation_combined.png")
