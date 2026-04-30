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

The analysis uses dependency data from [deps.dev](https://deps.dev/), accessed via Google BigQuery.

### Raw Dependency Data (CSV files)

Download from SharePoint: [Dependencies and Releases Data](https://vuw-my.sharepoint.com/:f:/g/personal/edenk_staff_vuw_ac_nz/IgA927qzIR9-RKDKOLxJh3fPAV2Ux1orJ4D4YLArjrqnIdA?e=VNXQsW)

Place the downloaded CSV files in the `dependencies/` directory:
```
dependencies/
├── maven/*.csv.gz
├── npm/*.csv.gz
├── pypi/*.csv.gz
├── cargo/*.csv.gz
├── go/*.csv.gz
├── nuget/*_resolved.csv.gz
└── rubygems/*_resolved.csv.gz
```

### Pre-Computed Results (PKL files)

Pre-computed analysis results are included in the [`data/`](data/) folder of this repository:

- **Gini Index**: `gini_cumulative_{ecosystem}.pkl` - Dependency concentration metrics for each ecosystem
- **Elite Turnover**: `elite_turnover_{ecosystem}.pkl` - Top package turnover rates for each ecosystem
- **Innovation Metrics**: `innovation_{ecosystem}.pkl` - InnovNEW and InnovUPD metrics for each ecosystem
- **Dependency Validation**: `{ecosystem}_batched_dependency_jaccard_results.pkl` - Dependency change analysis
- **API Validation**: `api_jaccard_results.pkl` - API surface change analysis

Alternative download: [Raw data on SharePoint](https://vuw-my.sharepoint.com/:f:/g/personal/edenk_staff_vuw_ac_nz/IgASd6cPmo8bQpNm2N7vJoihAeZ515cY3alDaVQdDfKio24?e=5KbeJE)

## Research Questions & Workflow

### RQ1: Growth Patterns/Evolution

**Metric**: Package growth, noise ratio (single-release packages with zero dependents)

| Script | Input | Output |
|--------|-------|--------|
| [`calculate_growth_metrics.py`](scripts/calculate_growth_metrics.py) | `dependencies/{ecosystem}/*.csv.gz` ([download](https://vuw-my.sharepoint.com/:f:/g/personal/edenk_staff_vuw_ac_nz/IgA927qzIR9-RKDKOLxJh3fPAV2Ux1orJ4D4YLArjrqnIdA?e=VNXQsW)) | `data/growth_metrics.pkl` |
| [`plot_figure2_growth.py`](scripts/plot_figure2_growth.py) | `data/growth_metrics.pkl` | [`figure_2_deps_dev.png`](plots/figure_2_deps_dev.png) |

### RQ2: Dependency Concentration (Gini Index)

**Metric**: Gini coefficient measuring inequality in dependency distribution

| Script | Input | Output |
|--------|-------|--------|
| [`calculate_gini_cumulative.py`](scripts/calculate_gini_cumulative.py) | `dependencies/{ecosystem}/*.csv.gz` ([download](https://vuw-my.sharepoint.com/:f:/g/personal/edenk_staff_vuw_ac_nz/IgA927qzIR9-RKDKOLxJh3fPAV2Ux1orJ4D4YLArjrqnIdA?e=VNXQsW)) | [`gini_cumulative_{ecosystem}.pkl`](data/) |
| [`plot_figure7_gini.py`](scripts/plot_figure7_gini.py) | [`gini_cumulative_*.pkl`](data/) | [`figure_7_gini_concentration.png`](plots/figure_7_gini_concentration.png) |

**Note**: The Gini index is calculated using cumulative dependencies: for each year *t*, we count ALL dependencies from packages released up to year *t* (not just those released in year *t*).

### RQ3: Elite Dynamism (Package Turnover)

**Metric**: Annual turnover rate in top-10/100/500 most-depended-upon packages

| Script | Input | Output |
|--------|-------|--------|
| [`calculate_elite_turnover.py`](scripts/calculate_elite_turnover.py) | `dependencies/{ecosystem}/*.csv.gz` ([download](https://vuw-my.sharepoint.com/:f:/g/personal/edenk_staff_vuw_ac_nz/IgA927qzIR9-RKDKOLxJh3fPAV2Ux1orJ4D4YLArjrqnIdA?e=VNXQsW)) | [`elite_turnover_{ecosystem}.pkl`](data/) |
| [`plot_figure10_turnover.py`](scripts/plot_figure10_turnover.py) | [`elite_turnover_*.pkl`](data/) | [`figure_10_elite_turnover.png`](plots/figure_10_elite_turnover.png) |

### RQ4: Innovation Pathways

**Metrics**:
- InnovNEW: Ratio of first-time packages to packages with last release in year *t*
- InnovUPD: Ratio of packages with major version bumps to packages with last release in year *t*

| Script | Input | Output |
|--------|-------|--------|
| [`calculate_innovation_metrics.py`](scripts/calculate_innovation_metrics.py) | `dependencies/{ecosystem}/*.csv.gz` ([download](https://vuw-my.sharepoint.com/:f:/g/personal/edenk_staff_vuw_ac_nz/IgA927qzIR9-RKDKOLxJh3fPAV2Ux1orJ4D4YLArjrqnIdA?e=VNXQsW)) | [`innovation_{ecosystem}.pkl`](data/) |
| [`plot_figures_20_21_innovation.py`](scripts/plot_figures_20_21_innovation.py) | [`innovation_*.pkl`](data/) | [`figures_20_21_innovation.png`](plots/figures_20_21_innovation.png) |

### Innovation Metric Validation

**Dependency Change Analysis**:
| Script | Input | Output |
|--------|-------|--------|
| [`analyze_dependency_changes.py`](scripts/analyze_dependency_changes.py) | `dependencies/{ecosystem}/*.csv.gz` ([download](https://vuw-my.sharepoint.com/:f:/g/personal/edenk_staff_vuw_ac_nz/IgA927qzIR9-RKDKOLxJh3fPAV2Ux1orJ4D4YLArjrqnIdA?e=VNXQsW)) | [`{ecosystem}_batched_dependency_jaccard_results.pkl`](data/) |
| [`plot_dependency_validation.py`](scripts/plot_dependency_validation.py) | [`*_batched_dependency_jaccard_results.pkl`](data/) | [`figure_22_dependency_changes.png`](plots/figure_22_dependency_changes.png) |

**API Surface Analysis**:
| Script | Input | Output |
|--------|-------|--------|
| [`analyze_api_changes.py`](scripts/analyze_api_changes.py) | Package artifacts from registries | [`api_jaccard_results.pkl`](data/api_jaccard_results.pkl) |
| [`plot_api_validation.py`](scripts/plot_api_validation.py) | [`api_jaccard_results.pkl`](data/api_jaccard_results.pkl) | [`figure_23_api_changes.png`](plots/figure_23_api_changes.png) |

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
│   ├── calculate_*.py    # Metric calculation scripts
│   └── plot_*.py         # Visualization scripts
├── data/                 # Pre-computed analysis results (PKL files)
│   ├── gini_cumulative_{ecosystem}.pkl       # Gini index data (7 files)
│   ├── elite_turnover_{ecosystem}.pkl        # Elite turnover data (7 files)
│   ├── innovation_{ecosystem}.pkl            # Innovation metrics (7 files)
│   ├── {eco}_batched_dependency_jaccard_results.pkl  # Dependency validation (7 files)
│   └── api_jaccard_results.pkl               # API surface validation
├── plots/                # Generated figures from the paper
│   ├── figure_1_complete_deps_dev.png
│   ├── figure_2_deps_dev.png
│   ├── figure_3_maven_gag_ratio_final.png
│   ├── figure_7_gini.png
│   ├── figure8_elite_turnover_all.png
│   ├── figure_10_babel_transition.png
│   ├── figure_11_cargo_serialization.png
│   ├── figure_12_maven_elite_change.png
│   ├── figure_13_maven_tech_trends.png
│   ├── figure_14_pypi_tech_trends.png
│   ├── figure_15_innovation_new.png
│   ├── figure_15_npm_tech_trends.png
│   ├── figure_16_innovation_update.png
│   ├── dependency_major_vs_nonmajor_full.png
│   ├── api_major_vs_nonmajor_boxplot.png
│   └── ... (and other supplementary figures)
├── dependencies/         # Raw dependency data (not included, download separately)
├── README.md             # This file
├── requirements.txt      # Python dependencies
└── LICENSE               # Apache 2.0 License
```

## Generated Figures

This repository includes all pre-generated figures from the paper:

**Main Analysis Figures**:
- **[Figure 1](plots/figure_1_complete_deps_dev.png)**: Complete dependency data overview
- **[Figure 2](plots/figure_2_deps_dev.png)**: Package growth across ecosystems
- **[Figure 3](plots/figure_3_maven_gag_ratio_final.png)**: Maven growth and noise ratio
- **[Figure 7](plots/figure_7_gini.png)**: Dependency concentration (Gini Index)
- **[Figure 8](plots/figure8_elite_turnover_all.png)**: Elite package turnover rates across ecosystems
- **[Figure 15](plots/figure_15_innovation_new.png)**: Innovation pathways - InnovNEW
- **[Figure 16](plots/figure_16_innovation_update.png)**: Innovation pathways - InnovUPD

**Case Study Figures**:
- **[Figure 10](plots/figure_10_babel_transition.png)**: Babel ecosystem transition (npm)
- **[Figure 11](plots/figure_11_cargo_serialization.png)**: Cargo serialization libraries
- **[Figure 12](plots/figure_12_maven_elite_change.png)**: Maven elite package changes
- **[Figure 13](plots/figure_13_maven_tech_trends.png)**: Maven technology trends
- **[Figure 14](plots/figure_14_pypi_tech_trends.png)**: PyPI technology trends
- **[Figure 15 (npm)](plots/figure_15_npm_tech_trends.png)**: npm technology trends

**Validation Figures**:
- **[Dependency Changes](plots/dependency_major_vs_nonmajor_full.png)**: Dependency change validation
- **[API Changes](plots/api_major_vs_nonmajor_boxplot.png)**: API surface change validation

**Supplementary Figures**:
- **[Hibernate](plots/hibernate.png)**: Hibernate transition analysis
- **[Spring Framework](plots/springframework.png)**: Spring Framework evolution
- **[RubyGems Auth](plots/figure_rubygems_auth.png)**: RubyGems authentication libraries
- **[RubyGems Jobs](plots/figure_rubygems_jobs.png)**: RubyGems job queue libraries
- **[Webrat/Capybara](plots/figure_rubygems_webrat_capybara.png)**: RubyGems testing frameworks
- **[Go HTTP Frameworks](plots/figure_go_http_framework.png)**: Go HTTP framework evolution
- **[Noise Ratio](plots/noise_ratio_y2_lag.png)**: Noise ratio analysis with lag

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
