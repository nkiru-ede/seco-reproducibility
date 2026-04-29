import pickle
import os
import numpy as np
from scipy import stats

print("Calculating Mann-Kendall trend tests for all metrics...\n")

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def mann_kendall_test(data):
    """
    Perform Mann-Kendall trend test.
    Returns: (trend direction, p-value, tau statistic)
    """
    n = len(data)
    if n < 3:
        return 'insufficient data', None, None

    # Calculate S statistic
    s = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            s += np.sign(data[j] - data[i])

    # Calculate variance
    var_s = n * (n - 1) * (2 * n + 5) / 18

    # Calculate Z statistic
    if s > 0:
        z = (s - 1) / np.sqrt(var_s)
    elif s < 0:
        z = (s + 1) / np.sqrt(var_s)
    else:
        z = 0

    # Calculate p-value (two-tailed)
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    # Calculate Kendall's tau
    tau = s / (n * (n - 1) / 2)

    # Determine trend
    if p_value < 0.05:
        trend = 'increasing' if s > 0 else 'decreasing'
    else:
        trend = 'no significant trend'

    return trend, p_value, tau

print("="*80)
print("MANN-KENDALL TREND ANALYSIS (Table 6)")
print("="*80)

# Test 1: Gini Index Trends
print("\n1. GINI INDEX TRENDS")
print("-" * 80)

gini_files = [f for f in os.listdir(DATA_DIR) if f.startswith('gini_cumulative_') and f.endswith('.pkl')]
for gini_file in sorted(gini_files):
    with open(os.path.join(DATA_DIR, gini_file), 'rb') as f:
        data = pickle.load(f)

    eco_name = data['ecosystem']
    years = sorted(data['gini'].keys())
    gini_values = [data['gini'][y] for y in years]

    trend, p_val, tau = mann_kendall_test(gini_values)

    print(f"{eco_name:12} | Years: {years[0]}-{years[-1]} | "
          f"Trend: {trend:20} | p-value: {p_val:.4f if p_val else 'N/A':>6} | "
          f"tau: {tau:.4f if tau else 'N/A':>6}")

# Test 2: Innovation Metrics Trends
print("\n2. INNOVATION METRICS TRENDS")
print("-" * 80)

innov_files = [f for f in os.listdir(DATA_DIR) if f.startswith('innovation_') and f.endswith('.pkl')]
for innov_file in sorted(innov_files):
    with open(os.path.join(DATA_DIR, innov_file), 'rb') as f:
        data = pickle.load(f)

    if 'ecosystem' in data:
        eco_name = data['ecosystem']

        # InnovNEW trend
        if 'innov_new' in data:
            years = sorted(data['innov_new'].keys())
            values = [data['innov_new'][y] for y in years]
            trend, p_val, tau = mann_kendall_test(values)
            print(f"{eco_name:12} (InnovNEW) | Trend: {trend:20} | "
                  f"p-value: {p_val:.4f if p_val else 'N/A':>6}")

        # InnovUPD trend
        if 'innov_upd' in data:
            years = sorted(data['innov_upd'].keys())
            values = [data['innov_upd'][y] for y in years]
            trend, p_val, tau = mann_kendall_test(values)
            print(f"{eco_name:12} (InnovUPD) | Trend: {trend:20} | "
                  f"p-value: {p_val:.4f if p_val else 'N/A':>6}")

# Test 3: Elite Turnover Trends
print("\n3. ELITE TURNOVER TRENDS")
print("-" * 80)

turnover_files = [f for f in os.listdir(DATA_DIR) if f.startswith('elite_turnover_') and f.endswith('.pkl')]
for turnover_file in sorted(turnover_files):
    with open(os.path.join(DATA_DIR, turnover_file), 'rb') as f:
        data = pickle.load(f)

    if 'ecosystem' in data and 'top_100' in data:
        eco_name = data['ecosystem']
        years = sorted(data['top_100'].keys())
        turnover_rates = [data['top_100'][y] for y in years if data['top_100'][y] is not None]

        if len(turnover_rates) >= 3:
            trend, p_val, tau = mann_kendall_test(turnover_rates)
            print(f"{eco_name:12} (Top-100) | Trend: {trend:20} | "
                  f"p-value: {p_val:.4f if p_val else 'N/A':>6}")

print("\n" + "="*80)
print("Analysis complete. See Table 6 in the paper for detailed results.")
print("="*80)
