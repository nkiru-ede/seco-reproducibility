import pickle
import pandas as pd
import gzip
import glob
import os

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

# Ensure results directory exists
os.makedirs(RESULTS_DIR, exist_ok=True)

print("="*80)
print("DEPENDENCY CHANGE ANALYSIS")
print("="*80)
print()

# Load sampled npm pairs
print("Loading sampled npm version pairs...")
sampled_pairs_file = os.path.join(RESULTS_DIR, 'npm_sampled_pairs.pkl')
with open(sampled_pairs_file, 'rb') as f:
    sampled_pairs = pickle.load(f)

# Get unique packages we need
all_packages = set()
for pairs in sampled_pairs.values():
    for pair in pairs:
        all_packages.add(pair['package'])

print(f"Total unique packages to analyze: {len(all_packages)}")
print()

# Build a cache of dependencies for only the packages we need
print("Building dependency cache for sampled packages...")
npm_deps_pattern = os.path.join(BASE_DIR, 'dependencies', 'npm', '*.csv.gz')
npm_deps_files = sorted(glob.glob(npm_deps_pattern))
print(f"Found {len(npm_deps_files)} npm dependency files to search")

# Cache structure: {(package, version): set(dependency_names)}
dep_cache = {}
packages_found = set()

for i, file in enumerate(npm_deps_files):
    if i % 50 == 0:
        print(f"  Searching file {i+1}/{len(npm_deps_files)}... (found {len(packages_found)}/{len(all_packages)} packages)")

    try:
        with gzip.open(file, 'rt', encoding='utf-8') as f:
            # Read in chunks to save memory
            for chunk in pd.read_csv(f, chunksize=100000):
                # Filter for packages we care about
                relevant = chunk[chunk['DependentName'].isin(all_packages)]

                if len(relevant) > 0:
                    # Group by package and version
                    for (pkg, ver), group in relevant.groupby(['DependentName', 'DependentVersion']):
                        key = (pkg, ver)
                        if key not in dep_cache:
                            dep_cache[key] = set()
                        dep_cache[key].update(group['DependencyName'].unique())
                        packages_found.add(pkg)
    except Exception as e:
        print(f"    Warning: Error reading file {file}: {e}")
        continue

    # Early exit if we've found all packages
    if len(packages_found) == len(all_packages):
        print(f"  Found all {len(all_packages)} packages! Stopping search.")
        break

print(f"\nCache built: {len(dep_cache)} package-version combinations")
print(f"Packages found: {len(packages_found)}/{len(all_packages)}")
print()

def calculate_jaccard_distance(set_a, set_b):
    """Calculate Jaccard distance between two sets"""
    if len(set_a) == 0 and len(set_b) == 0:
        return 0.0

    intersection = len(set_a & set_b)
    union = len(set_a | set_b)

    if union == 0:
        return 0.0

    return 1.0 - (intersection / union)

def analyze_pair(pair):
    """Analyze a single version pair"""
    package = pair['package']
    old_version = pair['old_version']
    new_version = pair['new_version']

    print(f"  {package}: {old_version} -> {new_version}...", end=" ", flush=True)

    # Get dependencies from cache
    old_key = (package, old_version)
    new_key = (package, new_version)

    old_deps = dep_cache.get(old_key, set())
    new_deps = dep_cache.get(new_key, set())

    if len(old_deps) == 0 and len(new_deps) == 0:
        print("SKIP (no deps)")
        return None

    # Calculate Jaccard distance
    jaccard_dist = calculate_jaccard_distance(old_deps, new_deps)

    # Calculate added and removed dependencies
    added = len(new_deps - old_deps)
    removed = len(old_deps - new_deps)

    print(f"OK (old={len(old_deps)}, new={len(new_deps)}, added={added}, removed={removed}, jaccard={jaccard_dist:.3f})")

    return {
        'package': package,
        'old_version': old_version,
        'new_version': new_version,
        'old_deps_count': len(old_deps),
        'new_deps_count': len(new_deps),
        'added': added,
        'removed': removed,
        'jaccard_distance': jaccard_dist
    }

# Analyze all pairs
results = {'major': [], 'minor': [], 'patch': []}

for change_type in ['major', 'minor', 'patch']:
    pairs = sampled_pairs[change_type]
    print(f"\nAnalyzing {change_type.upper()} version changes ({len(pairs)} pairs):")
    print("-"*80)

    for pair in pairs:
        result = analyze_pair(pair)
        if result:
            results[change_type].append(result)

print()
print("="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print()

# Calculate statistics
print(f"{'Type':<8} {'n':>4} {'Jaccard Dist':>14} {'Added':>8} {'Removed':>8}")
print("-"*80)

for change_type in ['major', 'minor', 'patch']:
    data = results[change_type]
    if len(data) == 0:
        continue

    jaccard_vals = [r['jaccard_distance'] for r in data]
    added_vals = [r['added'] for r in data]
    removed_vals = [r['removed'] for r in data]

    avg_jaccard = sum(jaccard_vals) / len(data)
    avg_added = sum(added_vals) / len(data)
    avg_removed = sum(removed_vals) / len(data)

    print(f"{change_type:<8} {len(data):>4} {avg_jaccard:>14.3f} {avg_added:>8.1f} {avg_removed:>8.1f}")

print()

# Calculate ratios
major_avg = sum(r['jaccard_distance'] for r in results['major']) / len(results['major']) if results['major'] else 0
minor_avg = sum(r['jaccard_distance'] for r in results['minor']) / len(results['minor']) if results['minor'] else 0
patch_avg = sum(r['jaccard_distance'] for r in results['patch']) / len(results['patch']) if results['patch'] else 0

print("Jaccard Distance Ratios:")
if minor_avg > 0:
    print(f"  Major/Minor: {major_avg / minor_avg:.2f}x")
if patch_avg > 0:
    print(f"  Major/Patch: {major_avg / patch_avg:.2f}x")
if patch_avg > 0 and minor_avg > 0:
    print(f"  Minor/Patch: {minor_avg / patch_avg:.2f}x")
print()

# Save results
output_file = os.path.join(RESULTS_DIR, 'npm_dependency_jaccard_results.pkl')
with open(output_file, 'wb') as f:
    pickle.dump({
        'sampled_pairs': sampled_pairs,
        'results': results,
        'stats': {
            change_type: {
                'n': len(results[change_type]),
                'avg_jaccard': sum(r['jaccard_distance'] for r in results[change_type]) / len(results[change_type]) if results[change_type] else 0,
                'avg_added': sum(r['added'] for r in results[change_type]) / len(results[change_type]) if results[change_type] else 0,
                'avg_removed': sum(r['removed'] for r in results[change_type]) / len(results[change_type]) if results[change_type] else 0
            }
            for change_type in ['major', 'minor', 'patch']
        }
    }, f)

print(f"Results saved to: {output_file}")
