import pandas as pd
import pickle
import glob
import os
from collections import defaultdict

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

# Ensure results directory exists
os.makedirs(RESULTS_DIR, exist_ok=True)

print("Calculating elite package turnover (Figure 8)...\n")

ecosystems = {
    'Maven': {
        'releases_file': os.path.join(DATA_DIR, 'releases', 'maven.gz'),
        'deps_glob': os.path.join(BASE_DIR, 'dependencies', 'maven', '*.csv.gz'),
        'color': '#D32F2F',
        'start_year': 2002
    },
    'npm': {
        'releases_file': os.path.join(DATA_DIR, 'releases', 'npm.gz'),
        'deps_glob': os.path.join(BASE_DIR, 'dependencies', 'npm', '*.csv.gz'),
        'color': '#E65100',
        'start_year': 2010
    },
    'Cargo': {
        'releases_file': os.path.join(DATA_DIR, 'releases', 'cargo.gz'),
        'deps_glob': os.path.join(BASE_DIR, 'dependencies', 'cargo', '*.csv.gz'),
        'color': '#F57C00',
        'start_year': 2015
    },
    'PyPI': {
        'releases_file': os.path.join(DATA_DIR, 'releases', 'pypi.gz'),
        'deps_glob': os.path.join(BASE_DIR, 'dependencies', 'pypi', '*.csv.gz'),
        'color': '#1976D2',
        'start_year': 2005
    },
    'Go': {
        'releases_file': os.path.join(DATA_DIR, 'releases', 'go.gz'),
        'deps_glob': os.path.join(BASE_DIR, 'dependencies', 'go', '*.csv.gz'),
        'color': '#00ACC1',
        'start_year': 2018
    },
    'NuGet': {
        'releases_file': os.path.join(DATA_DIR, 'releases', 'nuget.gz'),
        'deps_glob': os.path.join(BASE_DIR, 'dependencies', 'nuget', '*_resolved.csv.gz'),
        'color': '#7B1FA2',
        'start_year': 2011
    },
    'RubyGems': {
        'releases_file': os.path.join(DATA_DIR, 'releases', 'rubygems.gz'),
        'deps_glob': os.path.join(BASE_DIR, 'dependencies', 'rubygems', '*_resolved.csv.gz'),
        'color': '#388E3C',
        'start_year': 2009
    },
    'CRAN': {
        'releases_file': os.path.join(DATA_DIR, 'releases', 'cran.gz'),
        'deps_glob': os.path.join(BASE_DIR, 'dependencies', 'cran', '*.csv.gz'),
        'color': '#795548',
        'start_year': 1999
    },
    'CPAN': {
        'releases_file': os.path.join(DATA_DIR, 'releases', 'cpan.gz'),
        'deps_glob': os.path.join(BASE_DIR, 'dependencies', 'cpan', '*.csv.gz'),
        'color': '#607D8B',
        'start_year': 1995
    }
}

def process_ecosystem(eco_name, config):
    print(f"{'='*70}")
    print(f"Processing {eco_name}...")
    print(f"{'='*70}")

    # STEP 1: Count dependents per package per year
    print(f"  [1/3] Loading dependencies and counting dependents per year...")

    # Dictionary: year -> package -> count of dependents
    dependents_by_year = defaultdict(lambda: defaultdict(int))

    dep_files = glob.glob(config['deps_glob'])
    print(f"    {len(dep_files)} dependency files")

    for i, file in enumerate(dep_files, 1):
        if i % 20 == 0 or i == len(dep_files):
            print(f"    File {i}/{len(dep_files)}...", end='\r', flush=True)

        try:
            for chunk in pd.read_csv(file, chunksize=200000):
                if 'DependencyName' not in chunk.columns:
                    continue

                # Parse year from DependentPublishedAt
                if 'DependentPublishedAt' in chunk.columns and 'DependencyName' in chunk.columns:
                    chunk['Year'] = pd.to_datetime(chunk['DependentPublishedAt'], errors='coerce').dt.year
                    chunk = chunk.dropna(subset=['Year', 'DependencyName'])

                    for _, row in chunk[['Year', 'DependencyName']].iterrows():
                        year = int(row['Year'])
                        dep_name = row['DependencyName']
                        if year >= config['start_year'] and year <= 2025:
                            dependents_by_year[year][dep_name] += 1
        except Exception as e:
            print(f"\n    Error reading {file}: {e}")
            continue

    print(f"\n    Processed {len(dependents_by_year)} years")

    # STEP 2: For each year, rank packages by number of dependents
    print(f"  [2/3] Ranking packages by dependents for each year...")

    top_packages_by_year = {}
    for year in sorted(dependents_by_year.keys()):
        # Sort packages by dependent count (descending)
        sorted_packages = sorted(dependents_by_year[year].items(),
                                key=lambda x: x[1], reverse=True)
        top_packages_by_year[year] = [pkg for pkg, count in sorted_packages]

    print(f"    Ranked packages for {len(top_packages_by_year)} years")

    # STEP 3: Calculate turnover for top-10, top-100, top-500
    print(f"  [3/3] Calculating elite turnover...")

    turnover_data = {
        'top10': {},
        'top100': {},
        'top500': {}
    }

    years = sorted(top_packages_by_year.keys())

    for i in range(1, len(years)):
        prev_year = years[i-1]
        curr_year = years[i]

        prev_packages = top_packages_by_year[prev_year]
        curr_packages = top_packages_by_year[curr_year]

        # Top 10 - use actual cohort size (min of 10 and available packages)
        if len(prev_packages) > 0 and len(curr_packages) > 0:
            n10 = min(10, len(prev_packages), len(curr_packages))
            prev_top10 = set(prev_packages[:n10])
            curr_top10 = set(curr_packages[:n10])
            changed = len(curr_top10 - prev_top10)
            turnover_data['top10'][curr_year] = changed / float(n10) * 100

        # Top 100 - use actual cohort size (min of 100 and available packages)
        if len(prev_packages) > 0 and len(curr_packages) > 0:
            n100 = min(100, len(prev_packages), len(curr_packages))
            prev_top100 = set(prev_packages[:n100])
            curr_top100 = set(curr_packages[:n100])
            changed = len(curr_top100 - prev_top100)
            turnover_data['top100'][curr_year] = changed / float(n100) * 100

        # Top 500 - use actual cohort size (min of 500 and available packages)
        if len(prev_packages) > 0 and len(curr_packages) > 0:
            n500 = min(500, len(prev_packages), len(curr_packages))
            prev_top500 = set(prev_packages[:n500])
            curr_top500 = set(curr_packages[:n500])
            changed = len(curr_top500 - prev_top500)
            turnover_data['top500'][curr_year] = changed / float(n500) * 100

    # Print sample results
    if turnover_data['top10']:
        sample_years = sorted(turnover_data['top10'].keys())[:5]
        print(f"    Sample Top-10 turnover:")
        for year in sample_years:
            if year in turnover_data['top10']:
                print(f"      {year}: {turnover_data['top10'][year]:.1f}%")

    # Save results
    result = {
        'ecosystem': eco_name,
        'turnover': turnover_data,
        'color': config['color']
    }

    output_file = os.path.join(RESULTS_DIR, f"elite_turnover_{eco_name.lower()}.pkl")
    with open(output_file, 'wb') as f:
        pickle.dump(result, f)

    print(f"\n  Saved: {output_file}\n")
    return result

# Process all ecosystems
all_results = {}
for eco_name in ['Maven', 'Cargo', 'PyPI', 'NuGet', 'RubyGems', 'npm', 'Go', 'CRAN', 'CPAN']:
    if eco_name in ecosystems:
        try:
            result = process_ecosystem(eco_name, ecosystems[eco_name])
            all_results[eco_name] = result
        except Exception as e:
            print(f"\n  ERROR processing {eco_name}: {e}\n")
            continue

print("="*70)
print("All ecosystems completed!")
print("="*70)
