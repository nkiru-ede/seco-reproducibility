import pickle
import matplotlib.pyplot as plt
import glob
import os

print("Creating Figure 7: Gini Index of Dependency Concentration...\n")

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PLOTS_DIR = os.path.join(BASE_DIR, 'plots')

# Load all Gini files
gini_files = glob.glob(os.path.join(DATA_DIR, 'gini_cumulative_*.pkl'))

print(f"Found {len(gini_files)} completed ecosystems:")

all_gini_data = {}

# Define ecosystem colors
eco_colors = {
    'Maven': '#D32F2F',
    'npm': '#E65100',
    'Cargo': '#F57C00',
    'PyPI': '#1976D2',
    'Go': '#00ACC1',
    'NuGet': '#7B1FA2',
    'RubyGems': '#388E3C'
}

for file in gini_files:
    with open(file, 'rb') as f:
        data = pickle.load(f)
    eco_name = data['ecosystem']
    # Add color if not present
    if 'color' not in data:
        data['color'] = eco_colors.get(eco_name, '#000000')
    all_gini_data[eco_name] = data
    print(f"  {eco_name}: {len(data['gini'])} years of data")

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Plot all ecosystems
for eco_name, data in sorted(all_gini_data.items()):
    if data['gini']:
        years = sorted(data['gini'].keys())
        gini_values = [data['gini'][y] for y in years]
        ax.plot(years, gini_values, marker='o', markersize=6, linewidth=2.5,
                label=eco_name, color=data['color'], alpha=0.8)

ax.set_xlabel('Year', fontsize=13, fontweight='bold')
ax.set_ylabel('Gini Index', fontsize=13, fontweight='bold')
ax.set_title('Figure 7: Dependency Concentration (Gini Index)',
             fontsize=14, fontweight='bold')
ax.legend(loc='best', fontsize=11)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_ylim(0, 1)

# Set x-axis to start from 2002 (Maven's start year)
ax.set_xlim(2002 - 0.5, 2025.5)

# Force integer years and ensure 2002 and 2025 are shown
from matplotlib.ticker import MaxNLocator
ax.xaxis.set_major_locator(MaxNLocator(integer=True, prune=None))

# Ensure 2002 is in the tick labels
current_ticks = list(ax.get_xticks())
if 2002 not in current_ticks:
    current_ticks.append(2002)
if 2025 not in current_ticks:
    current_ticks.append(2025)
current_ticks = sorted([int(t) for t in current_ticks if 2002 <= t <= 2025])
ax.set_xticks(current_ticks)

# Rotate x-axis labels to prevent overlap
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Make tick labels bolder
ax.tick_params(labelsize=11, width=1.5)
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontweight('bold')

plt.tight_layout()

# Save figure
os.makedirs(PLOTS_DIR, exist_ok=True)
output_png = os.path.join(PLOTS_DIR, 'figure_7_gini_concentration.png')
plt.savefig(output_png, dpi=300, bbox_inches='tight')
print(f"\nFigure 7 PNG saved to: {output_png}")

output_pdf = os.path.join(PLOTS_DIR, 'figure_7_gini_concentration.pdf')
plt.savefig(output_pdf, bbox_inches='tight')
print(f"Figure 7 PDF saved to: {output_pdf}")

# Print summary statistics
print(f"\nEcosystems included: {', '.join(sorted(all_gini_data.keys()))}")
print("\n" + "="*70)
print("SUMMARY: Final Gini values (most recent year)")
print("="*70)
for eco_name, data in sorted(all_gini_data.items()):
    if data['gini']:
        years = sorted(data['gini'].keys())
        final_year = years[-1]
        final_gini = data['gini'][final_year]
        if 'sample_sizes' in data and final_year in data['sample_sizes']:
            n_pkgs = data['sample_sizes'][final_year]['n_packages']
            n_rels = data['sample_sizes'][final_year]['n_relationships']
            print(f"{eco_name:12} | {final_year} | Gini: {final_gini:.4f} | {n_pkgs:,} packages | {n_rels:,} relationships")
        else:
            print(f"{eco_name:12} | {final_year} | Gini: {final_gini:.4f}")

print("\nNote: Gini index calculated using ALL active dependencies:")
print("  - Population: All packages released up to year t")
print("  - Wealth distribution: Number of times each package is depended upon")
print("  - by all packages released up to year t")
