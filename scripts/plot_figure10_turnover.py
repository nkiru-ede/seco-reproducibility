import pickle
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
PLOTS_DIR = os.path.join(BASE_DIR, 'plots')

# Ensure plots directory exists
os.makedirs(PLOTS_DIR, exist_ok=True)

print("Plotting Figure 10: Elite Package Turnover...\n")

ecosystems = ['Maven', 'Cargo', 'PyPI', 'NuGet', 'RubyGems', 'npm', 'Go']

# Create subdirectory for turnover plots
turnover_plots_dir = os.path.join(PLOTS_DIR, 'turnover')
os.makedirs(turnover_plots_dir, exist_ok=True)

# Colors for the 3 cohort sizes (same across all ecosystems)
cohort_colors = {
    'top10': '#D32F2F',    # Red
    'top100': '#1976D2',   # Blue
    'top500': '#388E3C'    # Green
}

for eco_name in ecosystems:
    pkl_file = os.path.join(RESULTS_DIR, f"elite_turnover_{eco_name.lower()}.pkl")

    with open(pkl_file, 'rb') as f:
        data = pickle.load(f)

    turnover = data['turnover']

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot top-10, top-100, top-500
    for cohort, label, marker in [
        ('top10', 'Top-10', 'o'),
        ('top100', 'Top-100', 's'),
        ('top500', 'Top-500', '^')
    ]:
        years = sorted(turnover[cohort].keys())
        values = [turnover[cohort][y] for y in years]

        ax.plot(years, values, marker=marker, linewidth=2.5,
                markersize=7, label=label, color=cohort_colors[cohort], alpha=0.8)

    ax.set_xlabel('Year', fontsize=14, fontweight='bold')
    ax.set_ylabel('Turnover Rate (%)', fontsize=14, fontweight='bold')
    ax.set_title(f'{eco_name}: Elite Package Turnover',
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(loc='best', fontsize=12, framealpha=0.95)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_ylim(0, 100)

    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=10))
    ax.tick_params(axis='both', labelsize=12)

    plt.tight_layout()
    output_file = os.path.join(turnover_plots_dir, f'{eco_name.lower()}_elite_turnover.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"  Saved: {eco_name} ({min(years)}-{max(years)})")
    plt.close()

print("\nAll Figure 10 plots completed!")
