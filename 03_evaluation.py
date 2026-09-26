"""
Week 4 - Evaluation step.
Builds on the Week 3 cleaned dataset (egov_clean.csv) to move from purely
descriptive EDA to a light evaluative model: how well do the governance
indicators explain citizen satisfaction, and which indicators matter most?
This uses scikit-learn's LinearRegression as an interpretable evaluation
tool (not a black-box predictive deployment) so that coefficients can be
read directly as policy-relevant effect sizes.
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error

sns.set_theme(style="whitegrid", context="notebook")

df = pd.read_csv("/home/claude/ega/egov_clean.csv")

features = [
    "internet_penetration_pct", "digital_literacy_pct", "egov_budget_per_capita_inr",
    "digital_transactions_per_1000", "avg_service_delivery_days",
    "grievance_redressal_rate_pct", "corruption_perception_index",
]
target = "citizen_satisfaction_score"

X = df[features].values
y = df[target].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

model = LinearRegression()
model.fit(X_train_s, y_train)
y_pred = model.predict(X_test_s)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
print(f"Test R^2: {r2:.3f}")
print(f"Test MAE: {mae:.3f}")

coef_df = pd.DataFrame({"feature": features, "standardized_coef": model.coef_}).sort_values(
    "standardized_coef", key=abs, ascending=False
)
coef_df.to_csv("/home/claude/ega/model_coefficients.csv", index=False)
print(coef_df)

with open("/home/claude/ega/model_metrics.txt", "w") as f:
    f.write(f"r2={r2:.3f}\nmae={mae:.3f}\nn_train={len(y_train)}\nn_test={len(y_test)}\n")

# ---- Figure 6: standardized coefficients (feature importance / effect size) ----
fig, ax = plt.subplots(figsize=(9, 5))
colors = ["#c0392b" if v < 0 else "#1f6f8b" for v in coef_df["standardized_coef"]]
sns.barplot(data=coef_df, x="standardized_coef", y="feature", palette=colors, ax=ax)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_title("Figure 6. Standardized Effect of Each Indicator on Citizen Satisfaction",
              fontsize=12, fontweight="bold")
ax.set_xlabel("Standardized Regression Coefficient")
ax.set_ylabel("")
fig.tight_layout()
fig.savefig("/home/claude/ega/fig6_coefficients.png", dpi=150)
plt.close(fig)

# ---- Figure 7: actual vs predicted (model evaluation) ----
fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(y_test, y_pred, alpha=0.7, color="#1f6f8b", edgecolor="white")
lims = [min(y_test.min(), y_pred.min()) - 0.3, max(y_test.max(), y_pred.max()) + 0.3]
ax.plot(lims, lims, "--", color="gray", linewidth=1)
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel("Actual Satisfaction Score")
ax.set_ylabel("Predicted Satisfaction Score")
ax.set_title(f"Figure 7. Model Evaluation: Actual vs. Predicted\n(Test R\u00b2 = {r2:.2f}, MAE = {mae:.2f})",
             fontsize=12, fontweight="bold")
fig.tight_layout()
fig.savefig("/home/claude/ega/fig7_actual_vs_predicted.png", dpi=150)
plt.close(fig)

print("Done.")
