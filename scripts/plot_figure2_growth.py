import pickle
import matplotlib.pyplot as plt
import os

print("Creating Figure 2: Package Growth Across Ecosystems...\n")

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PLOTS_DIR = os.path.join(BASE_DIR, 'plots')

# Load growth metrics
metrics_file = os.path.join(DATA_DIR, 'growth_metrics.pkl')
with open(metrics_file, 'rb') as f:
    all_data = pickle.load(f)

print(f"Loaded growth metrics for {len(all_data)} ecosystems")

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Plot all ecosystems
for eco_name, data in sorted(all_data.items()):
    if data['metrics']:
        years = sorted(data['metrics'].keys())
        total_packages = [data['metrics'][y]['total_packages'] for y in years]
        ax.plot(years, total_packages, marker='o', markersize=6, linewidth=2.5,
                label=eco_name, color=data['color'], alpha=0.8)

ax.set_xlabel('Year', fontsize=13, fontweight='bold')
ax.set_ylabel('Total Packages', fontsize=13, fontweight='bold')
ax.set_title('Figure 2: Package Growth Across Ecosystems',
             fontsize=14, fontweight='bold')
ax.legend(loc='best', fontsize=11)
ax.grid(True, alpha=0.3, linestyle='--')

# Make tick labels bolder
ax.tick_params(labelsize=11, width=1.5)
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontweight('bold')

plt.tight_layout()

# Save figure
os.makedirs(PLOTS_DIR, exist_ok=True)
output_png = os.path.join(PLOTS_DIR, 'figure_2_growth.png')
plt.savefig(output_png, dpi=300, bbox_inches='tight')
print(f"\nFigure 2 PNG saved to: {output_png}")

output_pdf = os.path.join(PLOTS_DIR, 'figure_2_growth.pdf')
plt.savefig(output_pdf, bbox_inches='tight')
print(f"Figure 2 PDF saved to: {output_pdf}")

print(f"\nEcosystems included: {', '.join(sorted(all_data.keys()))}")
