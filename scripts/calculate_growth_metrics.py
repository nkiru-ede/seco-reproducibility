import pandas as pd
import numpy as np
import pickle
import glob
import os
from collections import defaultdict

print("Calculating growth metrics across ecosystems...\n")

# Configuration
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
    """Calculate growth metrics for an ecosystem."""
    print(f"{'='*70}")
    print(f"Processing {eco_name}...")
    print(f"{'='*70}")

    packages_by_year = defaultdict(set)
    noise_by_year = defaultdict(set)  # Packages with single release and no dependents

    dep_files = glob.glob(config['deps_glob'])
    print(f"  Found {len(dep_files)} dependency files")

    for i, file in enumerate(dep_files, 1):
        if i % 20 == 0 or i == len(dep_files):
            print(f"  Processing file {i}/{len(dep_files)}...", end='\r', flush=True)

        try:
            for chunk in pd.read_csv(file, chunksize=100000, low_memory=False):
                if 'DependentName' not in chunk.columns or 'DependentPublishedAt' not in chunk.columns:
                    continue

                chunk['Year'] = pd.to_datetime(chunk['DependentPublishedAt'], errors='coerce').dt.year
                chunk = chunk.dropna(subset=['Year', 'DependentName'])

                for year, pkg_name in zip(chunk['Year'], chunk['DependentName']):
                    year = int(year)
                    if config['start_year'] <= year <= 2025:
                        packages_by_year[year].add(pkg_name)

        except Exception as e:
            print(f"\n  Error reading {file}: {e}")
            continue

    print(f"\n  Processed {len(packages_by_year)} years")

    # Calculate cumulative growth
    growth_metrics = {}
    for year in sorted(packages_by_year.keys()):
        growth_metrics[year] = {
            'new_packages': len(packages_by_year[year]),
            'total_packages': sum(len(packages_by_year[y]) for y in packages_by_year if y <= year)
        }

    return {
        'ecosystem': eco_name,
        'metrics': growth_metrics,
        'color': config['color']
    }

# Process all ecosystems
all_results = {}
for eco_name in ['Maven', 'npm', 'PyPI', 'Cargo', 'NuGet', 'RubyGems', 'Go']:
    try:
        result = process_ecosystem(eco_name, ecosystems[eco_name])
        all_results[eco_name] = result
    except Exception as e:
        print(f"\nERROR processing {eco_name}: {e}")
        continue

# Save results
os.makedirs(OUTPUT_DIR, exist_ok=True)
output_file = os.path.join(OUTPUT_DIR, 'growth_metrics.pkl')
with open(output_file, 'wb') as f:
    pickle.dump(all_results, f)

print(f"\n{'='*70}")
print(f"Growth metrics saved to: {output_file}")
print(f"{'='*70}")
