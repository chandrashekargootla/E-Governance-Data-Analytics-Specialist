# E-Governance Data Analytics — Weeks 3 & 4

End-to-end data analytics project on a district-level e-governance
service-delivery dataset: exploratory analysis and visualization (Week 3)
followed by evaluative modeling, reporting, and policy recommendations
(Week 4).

## Contents

| File | Description |
|---|---|
| `EGov_EDA_Report.docx` | Week 3: EDA strategy, visualizations, insights |
| `EGov_Week4_Policy_Report.docx` | Week 4: Executive summary, methodology, key findings, analysis discussion, policy recommendations, conclusion |
| `01_generate_data.py` | Builds/cleans the dataset (`egov_raw_snapshot.csv` -> `egov_clean.csv`) |
| `02_eda.py` | Descriptive statistics + generates Figures 1-5 |
| `03_evaluation.py` | Standardized linear regression evaluating drivers of citizen satisfaction; generates Figures 6-7 |
| `egov_raw_snapshot.csv` | Raw data before cleaning |
| `egov_clean.csv` | Analysis-ready cleaned dataset |
| `descriptive_stats.csv` | Summary statistics table (mean, std, min/median/max, skew) |
| `model_coefficients.csv` | Standardized regression coefficients per indicator |
| `model_metrics.txt` | Held-out test R2 and MAE |
| `fig1_histograms.png` ... `fig5_state_bar.png` | Week 3 EDA visualizations |
| `fig6_coefficients.png`, `fig7_actual_vs_predicted.png` | Week 4 evaluation visualizations |

## Requirements

```
pip install pandas numpy matplotlib seaborn scikit-learn
```

## Usage

```bash
python 01_generate_data.py   # produces egov_clean.csv
python 02_eda.py             # produces descriptive_stats.csv + fig1-fig5
python 03_evaluation.py      # produces model_coefficients.csv, model_metrics.txt, fig6-fig7
```

## Key Finding

Across both weeks, citizen satisfaction is driven primarily by administrative
responsiveness (grievance redressal rate, service delivery speed) and digital
literacy -- not by raw internet penetration or e-governance budget per capita,
which show negligible independent effect once responsiveness is accounted for.
This points policy toward grievance-system modernization and rural
service-delivery reform over blanket digitization spending.
