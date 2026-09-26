"""
Week 3 - Step 0: Recreate the cleaned dataset that Week 2 (Data Cleaning &
Preprocessing) would have produced. This mirrors a typical district-level
e-governance service-delivery dataset such as those published on India's
Open Government Data (OGD) platform / state e-Governance dashboards, with
fields covering digital-service usage, service-delivery performance,
digital-readiness, and citizen-perception metrics.

Reproducible synthetic data is used here purely to demonstrate the EDA
methodology end-to-end; the same code operates unchanged on a real,
cleaned CSV export from Week 2.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 320  # districts

states = ["Andhra Pradesh", "Karnataka", "Maharashtra", "Tamil Nadu", "Uttar Pradesh",
          "Rajasthan", "Gujarat", "West Bengal", "Bihar", "Kerala", "Punjab", "Odisha"]

region_type = rng.choice(["Urban", "Semi-Urban", "Rural"], size=n, p=[0.28, 0.32, 0.40])

# Internet penetration correlates with region type
base_internet = {"Urban": 78, "Semi-Urban": 58, "Rural": 38}
internet_penetration = np.clip(
    [base_internet[r] + rng.normal(0, 9) for r in region_type], 5, 99
)

# Digital literacy correlates with internet penetration
digital_literacy = np.clip(internet_penetration * 0.75 + rng.normal(0, 8, n), 5, 98)

# e-Governance budget per capita (INR), log-normal-ish spread
budget_per_capita = np.round(np.clip(rng.lognormal(mean=4.4, sigma=0.55, size=n), 15, 900), 1)

# Digital transactions per 1,000 population - driven by internet penetration + budget
digital_transactions_per_1000 = np.clip(
    0.9 * internet_penetration + 0.15 * budget_per_capita + rng.normal(0, 40, n),
    5, 950
)

# Average service delivery time (days) - decreases as digital maturity rises
avg_service_delivery_days = np.clip(
    22 - 0.11 * digital_transactions_per_1000 / 10 - 0.05 * digital_literacy + rng.normal(0, 4, n),
    0.5, 45
)

# Grievance redressal rate (%) - improves with lower delivery time & higher budget
grievance_redressal_rate = np.clip(
    55 + 0.9 * (22 - avg_service_delivery_days) + 0.02 * budget_per_capita + rng.normal(0, 8, n),
    10, 99
)

# Citizen satisfaction score (1-10) - composite, with some noise / a few anomalies
citizen_satisfaction = np.clip(
    2.5 + 0.045 * grievance_redressal_rate + 0.02 * digital_literacy
    - 0.05 * avg_service_delivery_days + rng.normal(0, 0.7, n),
    1, 10
)

# Corruption perception index (0-100, higher = cleaner) - loosely tied to satisfaction
corruption_perception_index = np.clip(
    30 + 4.2 * citizen_satisfaction + rng.normal(0, 9, n), 5, 95
)

population_lakhs = np.round(np.clip(rng.lognormal(mean=2.6, sigma=0.6, size=n), 2, 120), 2)

df = pd.DataFrame({
    "district_id": [f"D{str(i+1).zfill(3)}" for i in range(n)],
    "state": rng.choice(states, size=n),
    "region_type": region_type,
    "population_lakhs": population_lakhs,
    "internet_penetration_pct": np.round(internet_penetration, 1),
    "digital_literacy_pct": np.round(digital_literacy, 1),
    "egov_budget_per_capita_inr": budget_per_capita,
    "digital_transactions_per_1000": np.round(digital_transactions_per_1000, 1),
    "avg_service_delivery_days": np.round(avg_service_delivery_days, 1),
    "grievance_redressal_rate_pct": np.round(grievance_redressal_rate, 1),
    "citizen_satisfaction_score": np.round(citizen_satisfaction, 2),
    "corruption_perception_index": np.round(corruption_perception_index, 1),
})

# Inject a small, realistic amount of missingness + a couple of outliers,
# then resolve them exactly as documented in the Week 2 cleaning log below.
miss_idx = rng.choice(df.index, size=8, replace=False)
df.loc[miss_idx, "citizen_satisfaction_score"] = np.nan
out_idx = rng.choice(df.index, size=3, replace=False)
df.loc[out_idx, "avg_service_delivery_days"] = df.loc[out_idx, "avg_service_delivery_days"] + 60

df.to_csv("/home/claude/ega/egov_raw_snapshot.csv", index=False)

# --- Week 2 recap: cleaning applied to reach the analysis-ready file -------
df_clean = df.copy()
# 1) Missing citizen_satisfaction_score -> median imputation within region_type
df_clean["citizen_satisfaction_score"] = df_clean.groupby("region_type")["citizen_satisfaction_score"].transform(
    lambda s: s.fillna(s.median())
)
# 2) Outlier treatment on avg_service_delivery_days via IQR capping
q1, q3 = df_clean["avg_service_delivery_days"].quantile([0.25, 0.75])
iqr = q3 - q1
upper = q3 + 1.5 * iqr
df_clean["avg_service_delivery_days"] = np.clip(df_clean["avg_service_delivery_days"], None, upper)
# 3) Standardize category labels, drop duplicate district_ids (none expected, but enforced)
df_clean["state"] = df_clean["state"].str.strip().str.title()
df_clean = df_clean.drop_duplicates(subset="district_id")
# 4) Type enforcement
df_clean["district_id"] = df_clean["district_id"].astype(str)

df_clean.to_csv("/home/claude/ega/egov_clean.csv", index=False)
print("Rows:", len(df_clean))
print(df_clean.head(3).to_string())
print("\nMissing values after cleaning:\n", df_clean.isna().sum().sum())
