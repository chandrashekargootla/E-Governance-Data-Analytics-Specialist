import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", context="notebook")
PALETTE = "crest"

df = pd.read_csv("/home/claude/ega/egov_clean.csv")

numeric_cols = [
    "population_lakhs", "internet_penetration_pct", "digital_literacy_pct",
    "egov_budget_per_capita_inr", "digital_transactions_per_1000",
    "avg_service_delivery_days", "grievance_redressal_rate_pct",
    "citizen_satisfaction_score", "corruption_perception_index",
]

# ---------- 1. Descriptive statistics ----------
desc = df[numeric_cols].describe().T
desc["skew"] = df[numeric_cols].skew()
desc.to_csv("/home/claude/ega/descriptive_stats.csv")
print(desc.round(2))

# ---------- 2. Histograms (distribution) ----------
fig, axes = plt.subplots(2, 2, figsize=(11, 8))
hist_vars = ["digital_transactions_per_1000", "avg_service_delivery_days",
             "citizen_satisfaction_score", "internet_penetration_pct"]
titles = ["Digital Transactions per 1,000 Population", "Avg. Service Delivery Time (days)",
          "Citizen Satisfaction Score (1-10)", "Internet Penetration (%)"]
for ax, col, title in zip(axes.flat, hist_vars, titles):
    sns.histplot(df[col], kde=True, ax=ax, color="#2b6a7c", bins=22)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_xlabel("")
fig.suptitle("Figure 1. Distribution of Key E-Governance Metrics", fontsize=13, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig("/home/claude/ega/fig1_histograms.png", dpi=150)
plt.close(fig)

# ---------- 3. Box plots (spread & outliers by region type) ----------
fig, axes = plt.subplots(1, 2, figsize=(11, 5))
sns.boxplot(data=df, x="region_type", y="avg_service_delivery_days", ax=axes[0],
            palette=PALETTE, order=["Urban", "Semi-Urban", "Rural"])
axes[0].set_title("Service Delivery Time by Region Type", fontweight="bold")
axes[0].set_xlabel("")
axes[0].set_ylabel("Avg. Service Delivery Days")

sns.boxplot(data=df, x="region_type", y="citizen_satisfaction_score", ax=axes[1],
            palette=PALETTE, order=["Urban", "Semi-Urban", "Rural"])
axes[1].set_title("Citizen Satisfaction by Region Type", fontweight="bold")
axes[1].set_xlabel("")
axes[1].set_ylabel("Satisfaction Score (1-10)")
fig.suptitle("Figure 2. Spread and Outliers Across Region Types", fontsize=13, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig("/home/claude/ega/fig2_boxplots.png", dpi=150)
plt.close(fig)

# ---------- 4. Scatter plots (relationships) ----------
fig, axes = plt.subplots(1, 2, figsize=(11, 5))
sns.scatterplot(data=df, x="digital_transactions_per_1000", y="avg_service_delivery_days",
                 hue="region_type", ax=axes[0], palette="Set2", alpha=0.8)
axes[0].set_title("Digital Adoption vs. Service Delivery Time", fontweight="bold")
axes[0].set_xlabel("Digital Transactions per 1,000")
axes[0].set_ylabel("Avg. Service Delivery Days")

sns.scatterplot(data=df, x="grievance_redressal_rate_pct", y="citizen_satisfaction_score",
                 hue="region_type", ax=axes[1], palette="Set2", alpha=0.8, legend=False)
axes[1].set_title("Grievance Redressal vs. Citizen Satisfaction", fontweight="bold")
axes[1].set_xlabel("Grievance Redressal Rate (%)")
axes[1].set_ylabel("Satisfaction Score (1-10)")
fig.suptitle("Figure 3. Relationships Between Governance Performance Metrics", fontsize=13, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig("/home/claude/ega/fig3_scatterplots.png", dpi=150)
plt.close(fig)

# ---------- 5. Correlation heatmap ----------
fig, ax = plt.subplots(figsize=(9, 7))
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", center=0, ax=ax,
            cbar_kws={"label": "Pearson r"}, square=True, annot_kws={"size": 8})
ax.set_title("Figure 4. Correlation Matrix of Numeric E-Governance Indicators",
              fontsize=12, fontweight="bold")
plt.xticks(rotation=40, ha="right", fontsize=8)
plt.yticks(fontsize=8)
fig.tight_layout()
fig.savefig("/home/claude/ega/fig4_heatmap.png", dpi=150)
plt.close(fig)

# ---------- 6. Bar chart - state-level averages ----------
state_avg = df.groupby("state")["citizen_satisfaction_score"].mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 5.5))
sns.barplot(x=state_avg.values, y=state_avg.index, palette="crest", ax=ax)
ax.set_title("Figure 5. Average Citizen Satisfaction Score by State", fontsize=12, fontweight="bold")
ax.set_xlabel("Mean Satisfaction Score (1-10)")
ax.set_ylabel("")
fig.tight_layout()
fig.savefig("/home/claude/ega/fig5_state_bar.png", dpi=150)
plt.close(fig)

print("\nAll figures saved.")
print("\nTop correlations with citizen_satisfaction_score:")
print(corr["citizen_satisfaction_score"].sort_values(ascending=False))
