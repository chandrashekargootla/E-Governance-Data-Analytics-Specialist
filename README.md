# E-Governance EDA — Week 3

Exploratory data analysis and visualization on a district-level e-governance
service-delivery dataset (digital adoption, service delivery time, grievance
redressal, citizen satisfaction, corruption perception).

## Contents

| File | Description |
|---|---|
| `EGov_EDA_Report.docx` | Full write-up: EDA strategy, visualizations, insights, policy implications |
| `01_generate_data.py` | Builds/cleans the dataset (`egov_raw_snapshot.csv` → `egov_clean.csv`) |
| `02_eda.py` | Descriptive statistics + generates all five figures |
| `egov_raw_snapshot.csv` | Raw data before cleaning |
| `egov_clean.csv` | Analysis-ready cleaned dataset |
| `descriptive_stats.csv` | Summary statistics table (mean, std, min/median/max, skew) |
| `fig1_histograms.png` | Distribution of key metrics |
| `fig2_boxplots.png` | Service delivery time & satisfaction by region type |
| `fig3_scatterplots.png` | Digital adoption vs. delivery time; grievance redressal vs. satisfaction |
| `fig4_heatmap.png` | Correlation matrix across all numeric indicators |
| `fig5_state_bar.png` | Average citizen satisfaction by state |

## Requirements

```
pip install pandas numpy matplotlib seaborn
```

## Usage

```bash
python 01_generate_data.py   # produces egov_clean.csv
python 02_eda.py             # produces descriptive_stats.csv + fig1–fig5 PNGs
```

## Key Finding

Grievance redressal rate correlates with citizen satisfaction more strongly
than digital transaction volume or e-governance budget per capita — pointing
to responsiveness, not just digitization spend, as the highest-leverage
policy lever.
