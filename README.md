# Charting the Dynamics of Popularity and Innovation in Multiple Open-Source Software Ecosystems

This repository contains the scripts, data, and analysis code for reproducing the results presented in the paper:

> **Charting the dynamics of popularity and innovation in multiple open-source software ecosystems**
> Nkiru Ede, Jens Dietrich, Ulrich Zülicke
> *Submitted to Journal of Systems and Software (JSS)*, under review

## Overview

This study examines growth patterns, dependency concentration, elite package stability, and innovation pathways across seven major software package ecosystems: Maven, npm, PyPI, Cargo, NuGet, RubyGems, and Go.

## Prerequisites

- Python 3.8 or higher
- Required Python packages (see `requirements.txt`)
- Access to deps.dev dataset (see Data Sources below)

## Installation

```bash
git clone https://github.com/nkiru-ede/seco-reproducibility.git
cd seco-reproducibility
pip install -r requirements.txt
```

## Data Sources

The analysis uses dependency data from [deps.dev](https://deps.dev/), accessed via Google BigQuery. The processed datasets are available at:

1. **Dependency Data** (CSV files): [SharePoint Link 1](https://vuw-my.sharepoint.com/:f:/g/personal/edenk_staff_vuw_ac_nz/IgA927qzIR9-RKDKOLxJh3fPAV2Ux1orJ4D4YLArjrqnIdA?e=VNXQsW)
2. **Processed Results** (PKL files): [SharePoint Link 2](https://vuw-my.sharepoint.com/:f:/g/personal/edenk_staff_vuw_ac_nz/IgASd6cPmo8bQpNm2N7vJoihAeZ515cY3alDaVQdDfKio24?e=5KbeJE)

Download the data files and place them in the appropriate directories as indicated in the workflow below.

## Research Questions & Workflow

### RQ1: Growth Patterns/Evolution

**Metric**: Package growth, noise ratio (single-release packages with zero dependents)

| Script | Input | Output |
|--------|-------|--------|
| `scripts/calculate_growth_metrics.py` | `dependencies/{ecosystem}/*.csv.gz` | `data/growth_metrics.pkl` |
| `scripts/plot_figure2_growth.py` | `data/growth_metrics.pkl` | `plots/figure_2_growth.png` |

### RQ2: Dependency Concentration (Gini Index)

**Metric**: Gini coefficient measuring inequality in dependency distribution

| Script | Input | Output |
|--------|-------|--------|
| `scripts/calculate_gini_cumulative.py` | `dependencies/{ecosystem}/*.csv.gz` | `data/gini_cumulative_{ecosystem}.pkl` |
| `scripts/plot_figure7_gini.py` | `data/gini_cumulative_*.pkl` | `plots/figure_7_gini_concentration.png` |

**Note**: The Gini index is calculated using cumulative dependencies: for each year *t*, we count ALL dependencies from packages released up to year *t* (not just those released in year *t*).

### RQ3: Elite Dynamism (Package Turnover)

**Metric**: Annual turnover rate in top-10/100/500 most-depended-upon packages

| Script | Input | Output |
|--------|-------|--------|
| `scripts/calculate_elite_turnover.py` | `dependencies/{ecosystem}/*.csv.gz` | `data/elite_turnover_{ecosystem}.pkl` |
| `scripts/plot_figure10_turnover.py` | `data/elite_turnover_*.pkl` | `plots/figure_10_elite_turnover.png` |

### RQ4: Innovation Pathways

**Metrics**:
- InnovNEW: Ratio of first-time packages to packages with last release in year *t*
- InnovUPD: Ratio of packages with major version bumps to packages with last release in year *t*

| Script | Input | Output |
|--------|-------|--------|
| `scripts/calculate_innovation_metrics.py` | `dependencies/{ecosystem}/*.csv.gz` | `data/innovation_{ecosystem}.pkl` |
| `scripts/plot_figures_20_21_innovation.py` | `data/innovation_*.pkl` | `plots/figure_20_innov_new.png`, `plots/figure_21_innov_upd.png` |

### Innovation Metric Validation

**Dependency Change Analysis**:
| Script | Input | Output |
|--------|-------|--------|
| `scripts/analyze_dependency_changes.py` | `dependencies/{ecosystem}/*.csv.gz` | `data/dependency_jaccard_results.pkl` |
| `scripts/plot_dependency_validation.py` | `data/dependency_jaccard_results.pkl` | `plots/figure_22_dependency_changes.png` |

**API Surface Analysis**:
| Script | Input | Output |
|--------|-------|--------|
| `scripts/analyze_api_changes.py` | Package artifacts from registries | `data/api_jaccard_results.pkl` |
| `scripts/plot_api_validation.py` | `data/api_jaccard_results.pkl` | `plots/figure_23_api_changes.png` |

## Reproducibility Instructions

### Step 1: Download Data

Download dependency data from the SharePoint links above and organize as:
```
seco-reproducibility/
├── dependencies/
│   ├── maven/*.csv.gz
│   ├── npm/*.csv.gz
│   ├── pypi/*.csv.gz
│   ├── cargo/*.csv.gz
│   ├── go/*.csv.gz
│   ├── nuget/*_resolved.csv.gz
│   └── rubygems/*_resolved.csv.gz
```

### Step 2: Run Analysis Pipeline

Execute scripts in order:

```bash
# RQ1: Growth patterns
python scripts/calculate_growth_metrics.py
python scripts/plot_figure2_growth.py

# RQ2: Dependency concentration
python scripts/calculate_gini_cumulative.py
python scripts/plot_figure7_gini.py

# RQ3: Elite turnover
python scripts/calculate_elite_turnover.py
python scripts/plot_figure10_turnover.py

# RQ4: Innovation pathways
python scripts/calculate_innovation_metrics.py
python scripts/plot_figures_20_21_innovation.py

# Validation analyses
python scripts/analyze_dependency_changes.py
python scripts/plot_dependency_validation.py
python scripts/analyze_api_changes.py
python scripts/plot_api_validation.py
```

### Step 3: Statistical Trend Analysis

To reproduce the Mann-Kendall trend tests reported in Table 6:

```bash
python scripts/calculate_mann_kendall_trends.py
```

## Key Findings

- **RQ1**: Ecosystem growth patterns diverge: Go shows declining noise (20.9%→14.9%), while most ecosystems show increasing noise alongside steady package growth
- **RQ2**: Dependency concentration increases across all ecosystems (Gini indices converge to 0.93-0.99), indicating preferential attachment dynamics
- **RQ3**: Elite package turnover decreases and stabilizes over time, showing transition from rapid displacement to consolidation
- **RQ4**: Innovation pathways shift from replacement (InnovNEW declining) to enhancement (InnovUPD increasing), validated through dependency and API change analyses

## Repository Structure

```
seco-reproducibility/
├── scripts/              # Analysis and visualization scripts
├── data/                 # Intermediate results (PKL files)
├── plots/                # Generated figures
├── dependencies/         # Raw dependency data (not included, download separately)
├── README.md             # This file
├── requirements.txt      # Python dependencies
└── LICENSE               # Apache 2.0 License
```

## Citation

If you use this code or data, please cite:

```bibtex
@article{ede2026charting,
  title={Charting the dynamics of popularity and innovation in multiple open-source software ecosystems},
  author={Ede, Nkiru and Dietrich, Jens and Z{\"u}licke, Ulrich},
  journal={Journal of Systems and Software},
  note={Manuscript under review},
  year={2026}
}
```

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Contact

- Nkiru Ede - nkiru.ede@vuw.ac.nz
- Jens Dietrich - jens.dietrich@vuw.ac.nz
- Ulrich Zülicke - uli.zuelicke@vuw.ac.nz

## Acknowledgments

This work was funded partly by the New Zealand CoREs Fund through Te Pūnaha Matatini Centre of Research Excellence in Complex Systems.
