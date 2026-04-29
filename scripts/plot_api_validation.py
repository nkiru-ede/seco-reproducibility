import pickle
import matplotlib.pyplot as plt
import numpy as np
import os

print("Creating Figure 23: API Surface Change Validation...\n")

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PLOTS_DIR = os.path.join(BASE_DIR, 'plots')

# Load API Jaccard results
results_file = os.path.join(DATA_DIR, 'api_jaccard_results.pkl')

if not os.path.exists(results_file):
    print(f"API analysis results not found at: {results_file}")
    print("Please run analyze_api_changes.py first.")
    exit(1)

with open(results_file, 'rb') as f:
    api_data = pickle.load(f)

print(f"Loaded API analysis for {len(api_data)} ecosystems")

# Create figure
fig, ax = plt.subplots(figsize=(12, 6))

ecosystems = sorted(api_data.keys())
x_pos = np.arange(len(ecosystems))

major_means = [np.mean(api_data[eco]['major']) for eco in ecosystems]
nonmajor_means = [np.mean(api_data[eco]['non_major']) for eco in ecosystems]

width = 0.35
ax.bar(x_pos - width/2, major_means, width, label='Major Version Changes', alpha=0.8)
ax.bar(x_pos + width/2, nonmajor_means, width, label='Non-Major Version Changes', alpha=0.8)

ax.set_xlabel('Ecosystem', fontsize=13, fontweight='bold')
ax.set_ylabel('Mean Jaccard Distance', fontsize=13, fontweight='bold')
ax.set_title('Figure 23: API Surface Changes by Version Type',
             fontsize=14, fontweight='bold')
ax.set_xticks(x_pos)
ax.set_xticklabels(ecosystems)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, linestyle='--', axis='y')

# Make tick labels bolder
ax.tick_params(labelsize=11, width=1.5)
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontweight('bold')

plt.tight_layout()

# Save figure
os.makedirs(PLOTS_DIR, exist_ok=True)
output_png = os.path.join(PLOTS_DIR, 'figure_23_api_changes.png')
plt.savefig(output_png, dpi=300, bbox_inches='tight')
print(f"\nFigure 23 PNG saved to: {output_png}")

output_pdf = os.path.join(PLOTS_DIR, 'figure_23_api_changes.pdf')
plt.savefig(output_pdf, bbox_inches='tight')
print(f"Figure 23 PDF saved to: {output_pdf}")
