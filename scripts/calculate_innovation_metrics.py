import pandas as pd
import pickle
import numpy as np
import os

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

# Ensure results directory exists
os.makedirs(RESULTS_DIR, exist_ok=True)

print("Calculating Innovation Metrics (Figures 15 & 16)...\n")

ecosystems = {
    'Maven': {'releases_file': os.path.join(DATA_DIR, 'releases', 'maven.gz'), 'start_year': 2002},
    'npm': {'releases_file': os.path.join(DATA_DIR, 'releases', 'npm.gz'), 'start_year': 2010},
    'Cargo': {'releases_file': os.path.join(DATA_DIR, 'releases', 'cargo.gz'), 'start_year': 2015},
    'PyPI': {'releases_file': os.path.join(DATA_DIR, 'releases', 'pypi.gz'), 'start_year': 2005},
    'Go': {'releases_file': os.path.join(DATA_DIR, 'releases', 'go.gz'), 'start_year': 2018},
    'NuGet': {'releases_file': os.path.join(DATA_DIR, 'releases', 'nuget.gz'), 'start_year': 2011},
    'RubyGems': {'releases_file': os.path.join(DATA_DIR, 'releases', 'rubygems.gz'), 'start_year': 2009}
}

def extract_major_version(version_str):
    """Extract major version from version string"""
    if pd.isna(version_str):
        return None
    version_str = str(version_str).strip()
    # Remove leading 'v' if present
    if version_str.startswith('v'):
        version_str = version_str[1:]
    # Split and get first part
    parts = version_str.split('.')
    if len(parts) > 0:
        try:
            return int(parts[0])
        except:
            return None
    return None

def process_ecosystem(eco_name, config):
    print(f"{'='*70}")
    print(f"Processing {eco_name}...")
    print(f"{'='*70}")

    # Load releases (FULL dataset through 2025 to properly identify LastPackage)
    print("  Loading releases...")
    all_data = []
    for chunk in pd.read_csv(config['releases_file'], chunksize=500000):
        chunk['Year'] = pd.to_datetime(chunk['UpstreamPublishedAt'], errors='coerce').dt.year
        chunk = chunk[(chunk['Year'] >= config['start_year']) & (chunk['Year'] <= 2025)]
        chunk = chunk.dropna(subset=['Year', 'Name', 'Version'])
        all_data.append(chunk[['Year', 'Name', 'Version']])

    df = pd.concat(all_data, ignore_index=True)
    print(f"    Loaded {len(df):,} releases (through 2025)")

    # Extract major versions
    print("  Extracting major versions...")
    df['MajorVersion'] = df['Version'].apply(extract_major_version)
    df = df.dropna(subset=['MajorVersion'])

    # Calculate metrics per year (only through 2023 to avoid right-censoring)
    print("  Calculating innovation metrics (analysis through 2023)...")
    innov_new = {}
    innov_upd = {}

    analysis_years = [y for y in sorted(df['Year'].unique()) if y <= 2023]
    for year in analysis_years:
        year_data = df[df['Year'] == year]

        # Get first release year for each package
        first_release = df.groupby('Name')['Year'].min().to_dict()

        # Packages new in this year
        new_packages = year_data[year_data['Name'].map(lambda n: first_release.get(n) == year)]

        # Existing packages (updated)
        existing_packages = year_data[year_data['Name'].map(lambda n: first_release.get(n) < year)]

        # Count major version bumps for new packages
        new_major_bumps = 0
        if len(new_packages) > 0:
            new_pkg_names = new_packages['Name'].unique()
            for pkg in new_pkg_names:
                pkg_data = new_packages[new_packages['Name'] == pkg]
                if pkg_data['MajorVersion'].nunique() > 1:
                    new_major_bumps += 1

        # Count major version bumps for existing packages
        existing_major_bumps = 0
        if len(existing_packages) > 0:
            existing_pkg_names = existing_packages['Name'].unique()
            for pkg in existing_pkg_names:
                pkg_data = existing_packages[existing_packages['Name'] == pkg]
                # Get previous year's max major version
                prev_data = df[(df['Name'] == pkg) & (df['Year'] < year)]
                if len(prev_data) > 0:
                    prev_max_major = prev_data['MajorVersion'].max()
                    curr_max_major = pkg_data['MajorVersion'].max()
                    if curr_max_major > prev_max_major:
                        existing_major_bumps += 1

        # LastPackage = packages with their last release in this year
        last_package = 0
        for pkg in year_data['Name'].unique():
            pkg_future = df[(df['Name'] == pkg) & (df['Year'] > year)]
            if len(pkg_future) == 0:
                last_package += 1

        # Innovation metrics (0-1 scale)
        if last_package > 0:
            innov_new[year] = new_major_bumps / last_package
            innov_upd[year] = existing_major_bumps / last_package
        else:
            innov_new[year] = 0
            innov_upd[year] = 0

        if year % 5 == 0 or year == config['start_year']:
            print(f"    {year}: InnovNEW={innov_new[year]:.4f}, InnovUPD={innov_upd[year]:.4f}")

    print()

    result = {
        'ecosystem': eco_name,
        'innov_new': innov_new,
        'innov_upd': innov_upd
    }

    output_file = os.path.join(RESULTS_DIR, f"innovation_{eco_name.lower()}.pkl")
    with open(output_file, 'wb') as f:
        pickle.dump(result, f)

    print(f"  Saved: {output_file}\n")
    return result

# Process all ecosystems
all_results = {}
for eco_name in ['Maven', 'Cargo', 'PyPI', 'NuGet', 'RubyGems', 'npm', 'Go']:
    try:
        result = process_ecosystem(eco_name, ecosystems[eco_name])
        if result:
            all_results[eco_name] = result
    except Exception as e:
        print(f"\n  ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        continue

print("="*70)
print("All ecosystems completed!")
print("="*70)
