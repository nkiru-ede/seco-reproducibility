import pandas as pd
import numpy as np
import pickle
import glob
import os
from collections import defaultdict

print("Calculating Gini index using CUMULATIVE dependencies...\n")

def calculate_gini(counts):
    """
    Calculate Gini coefficient from a list of counts.
    Gini = 0 means perfect equality, Gini = 1 means perfect inequality.
    """
    if len(counts) == 0:
        return 0.0

    counts = np.array(sorted(counts))
    n = len(counts)

    if counts.sum() == 0:
        return 0.0

    # Gini formula: G = (2 * sum(i * x_i)) / (n * sum(x_i)) - (n + 1) / n
    index = np.arange(1, n + 1)
    gini = (2 * np.sum(index * counts)) / (n * counts.sum()) - (n + 1) / n

    return gini

# Configuration - adjust paths as needed
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEPS_DIR = os.path.join(BASE_DIR, 'dependencies')
OUTPUT_DIR = os.path.join(BASE_DIR, 'data')

ecosystems = {
    'Maven': {
        'deps_glob': os.path.join(DEPS_DIR, 'maven', '*.csv.gz'),
        'color': '#D32F2F',
        'start_year': 2002
    },
    'npm': {
        'deps_glob': os.path.join(DEPS_DIR, 'npm', '*.csv.gz'),
        'color': '#E65100',
        'start_year': 2010
    },
    'Cargo': {
        'deps_glob': os.path.join(DEPS_DIR, 'cargo', '*.csv.gz'),
        'color': '#F57C00',
        'start_year': 2015
    },
    'PyPI': {
        'deps_glob': os.path.join(DEPS_DIR, 'pypi', '*.csv.gz'),
        'color': '#1976D2',
        'start_year': 2005
    },
    'Go': {
        'deps_glob': os.path.join(DEPS_DIR, 'go', '*.csv.gz'),
        'color': '#00ACC1',
        'start_year': 2018
    },
    'NuGet': {
        'deps_glob': os.path.join(DEPS_DIR, 'nuget', '*_resolved.csv.gz'),
        'color': '#7B1FA2',
        'start_year': 2011
    },
    'RubyGems': {
        'deps_glob': os.path.join(DEPS_DIR, 'rubygems', '*_resolved.csv.gz'),
        'color': '#388E3C',
        'start_year': 2009
    }
}

def process_ecosystem(eco_name, config):
    print(f"{'='*70}")
    print(f"Processing {eco_name}...")
    print(f"{'='*70}")

    # STEP 1: Load dependency counts BY YEAR (not cumulative yet)
    # Structure: year -> dependency_name -> count
    print(f"  [1/3] Loading dependency relationships grouped by year...")

    deps_by_year = defaultdict(lambda: defaultdict(int))

    dep_files = glob.glob(config['deps_glob'])
    print(f"    {len(dep_files)} dependency files")

    total_deps = 0

    for i, file in enumerate(dep_files, 1):
        if i % 20 == 0 or i == len(dep_files):
            print(f"    File {i}/{len(dep_files)}... ({total_deps:,} deps loaded)", end='\r', flush=True)

        try:
            for chunk in pd.read_csv(file, chunksize=200000, low_memory=False):
                if 'DependentPublishedAt' not in chunk.columns or 'DependencyName' not in chunk.columns:
                    continue

                # Parse year from DependentPublishedAt
                chunk['Year'] = pd.to_datetime(chunk['DependentPublishedAt'], errors='coerce').dt.year
                chunk = chunk.dropna(subset=['Year', 'DependencyName'])

                # Group by year and dependency, count occurrences
                for year, dep_name in zip(chunk['Year'], chunk['DependencyName']):
                    year = int(year)
                    if year >= config['start_year'] and year <= 2025:
                        deps_by_year[year][dep_name] += 1
                        total_deps += 1

        except Exception as e:
            print(f"\n    Error reading {file}: {e}")
            continue

    print(f"\n    Loaded {total_deps:,} dependency relationships across {len(deps_by_year)} years")

    # STEP 2: Build CUMULATIVE counts for each year
    print(f"  [2/3] Building cumulative dependency counts...")

    years = sorted(deps_by_year.keys())
    print(f"    Years: {years[0]} to {years[-1]}")

    cumulative_counts_by_year = {}
    running_counts = defaultdict(int)  # Accumulator

    for year in years:
        # Add this year's dependencies to the running total
        for dep_name, count in deps_by_year[year].items():
            running_counts[dep_name] += count

        # Store a copy of the cumulative state for this year
        cumulative_counts_by_year[year] = dict(running_counts)

        if year % 5 == 0 or year == years[0] or year == years[-1]:
            n_packages = len(running_counts)
            n_deps = sum(running_counts.values())
            print(f"    Year {year}: {n_packages:,} unique dependencies, {n_deps:,} cumulative relationships")

    # STEP 3: Calculate Gini index for each year
    print(f"  [3/3] Calculating Gini index for each year...")

    gini_by_year = {}
    sample_sizes = {}

    for year in sorted(cumulative_counts_by_year.keys()):
        counts = list(cumulative_counts_by_year[year].values())

        if len(counts) > 0:
            gini = calculate_gini(counts)
            gini_by_year[year] = gini
            sample_sizes[year] = {
                'n_packages': len(counts),
                'n_relationships': sum(counts)
            }

            if year % 5 == 0 or year == years[0] or year == years[-1]:
                print(f"    {year}: Gini = {gini:.4f} ({len(counts):,} packages, {sum(counts):,} relationships)")

    print(f"    Calculated Gini for {len(gini_by_year)} years")

    # Save results
    result = {
        'ecosystem': eco_name,
        'gini': gini_by_year,
        'sample_sizes': sample_sizes,
        'color': config['color']
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, f"gini_cumulative_{eco_name.lower()}.pkl")
    with open(output_file, 'wb') as f:
        pickle.dump(result, f)

    print(f"\n  Saved: {output_file}\n")
    return result

# Process all ecosystems
all_results = {}
for eco_name in ['Maven', 'Cargo', 'PyPI', 'NuGet', 'RubyGems', 'npm', 'Go']:
    try:
        result = process_ecosystem(eco_name, ecosystems[eco_name])
        all_results[eco_name] = result
    except Exception as e:
        print(f"\n  ERROR processing {eco_name}: {e}\n")
        import traceback
        traceback.print_exc()
        continue

print("="*70)
print("All ecosystems completed!")
print("="*70)
