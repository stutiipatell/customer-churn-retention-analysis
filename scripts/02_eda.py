"""
02_eda.py
Exploratory analysis of churn drivers. Saves each chart as a PNG to
../charts/ so they can be dropped into the report / dashboard.
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["figure.dpi"] = 140

DATA_PATH = "../data/telco_churn_clean.csv"
CHART_DIR = "../charts"

df = pd.read_csv(DATA_PATH)
df["TenureGroup"] = pd.Categorical(
    df["TenureGroup"], categories=["0-6 mo", "7-12 mo", "13-24 mo", "25-48 mo", "49-72 mo"], ordered=True
)

COLOR_CHURN = "#E4572E"
COLOR_STAY = "#2E86AB"


def savefig(name):
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/{name}.png", bbox_inches="tight")
    plt.close()


# 1. Overall churn rate ------------------------------------------------
plt.figure(figsize=(5, 5))
counts = df["Churn"].value_counts().sort_index()
plt.pie(
    counts, labels=["Retained", "Churned"], autopct="%1.1f%%",
    colors=[COLOR_STAY, COLOR_CHURN], startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 2},
)
plt.title("Overall Churn Rate (n=7,043 customers)")
savefig("01_overall_churn_rate")

# 2. Churn rate by contract type ---------------------------------------
plt.figure(figsize=(6, 4.5))
rate = df.groupby("Contract")["Churn"].mean().sort_values() * 100
ax = rate.plot(kind="barh", color=COLOR_CHURN)
plt.xlabel("Churn Rate (%)")
plt.title("Churn Rate by Contract Type")
for i, v in enumerate(rate):
    ax.text(v + 0.5, i, f"{v:.1f}%", va="center")
savefig("02_churn_by_contract")

# 3. Churn rate by tenure group (retention curve) -----------------------
plt.figure(figsize=(6.5, 4.5))
rate = df.groupby("TenureGroup", observed=True)["Churn"].mean() * 100
ax = rate.plot(kind="bar", color=COLOR_CHURN)
plt.ylabel("Churn Rate (%)")
plt.xlabel("Tenure")
plt.title("Churn Rate by Customer Tenure")
plt.xticks(rotation=0)
for i, v in enumerate(rate):
    ax.text(i, v + 0.5, f"{v:.1f}%", ha="center")
savefig("03_churn_by_tenure")

# 4. Monthly charges distribution: churned vs retained -------------------
plt.figure(figsize=(6.5, 4.5))
sns.kdeplot(df[df.Churn == 0]["MonthlyCharges"], label="Retained", fill=True, color=COLOR_STAY, alpha=0.4)
sns.kdeplot(df[df.Churn == 1]["MonthlyCharges"], label="Churned", fill=True, color=COLOR_CHURN, alpha=0.4)
plt.xlabel("Monthly Charges ($)")
plt.title("Monthly Charges: Churned vs Retained Customers")
plt.legend()
savefig("04_monthly_charges_dist")

# 5. Churn rate by internet service type ---------------------------------
plt.figure(figsize=(6, 4.5))
rate = df.groupby("InternetService")["Churn"].mean().sort_values() * 100
ax = rate.plot(kind="barh", color=COLOR_CHURN)
plt.xlabel("Churn Rate (%)")
plt.title("Churn Rate by Internet Service Type")
for i, v in enumerate(rate):
    ax.text(v + 0.5, i, f"{v:.1f}%", va="center")
savefig("05_churn_by_internet_service")

# 6. Churn rate by number of add-on services ------------------------------
plt.figure(figsize=(6.5, 4.5))
rate = df.groupby("NumAddonServices")["Churn"].mean() * 100
ax = rate.plot(kind="bar", color=COLOR_CHURN)
plt.ylabel("Churn Rate (%)")
plt.xlabel("Number of Add-on Services Subscribed")
plt.title("Churn Rate vs. Add-on Service Adoption")
plt.xticks(rotation=0)
for i, v in enumerate(rate):
    ax.text(i, v + 0.5, f"{v:.1f}%", ha="center")
savefig("06_churn_by_addons")

# 7. Churn rate by payment method -----------------------------------------
plt.figure(figsize=(6.5, 4.5))
rate = df.groupby("PaymentMethod")["Churn"].mean().sort_values() * 100
ax = rate.plot(kind="barh", color=COLOR_CHURN)
plt.xlabel("Churn Rate (%)")
plt.title("Churn Rate by Payment Method")
for i, v in enumerate(rate):
    ax.text(v + 0.5, i, f"{v:.1f}%", va="center")
savefig("07_churn_by_payment")

# 8. Correlation heatmap of numeric features -------------------------------
plt.figure(figsize=(6.5, 5.5))
num_cols = ["tenure", "MonthlyCharges", "TotalCharges", "NumAddonServices", "AvgMonthlySpend", "Churn"]
corr = df[num_cols].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, vmin=-1, vmax=1)
plt.title("Correlation Matrix — Numeric Features")
savefig("08_correlation_heatmap")

# Print key summary stats for the report ------------------------------------
summary = {
    "overall_churn_rate": df["Churn"].mean(),
    "month_to_month_churn": df[df.Contract == "Month-to-month"]["Churn"].mean(),
    "two_year_churn": df[df.Contract == "Two year"]["Churn"].mean(),
    "fiber_churn": df[df.InternetService == "Fiber optic"]["Churn"].mean(),
    "dsl_churn": df[df.InternetService == "DSL"]["Churn"].mean(),
    "first_6mo_churn": df[df.TenureGroup == "0-6 mo"]["Churn"].mean(),
    "electronic_check_churn": df[df.PaymentMethod == "Electronic check"]["Churn"].mean(),
    "zero_addon_churn": df[df.NumAddonServices == 0]["Churn"].mean(),
    "avg_monthly_charge_churned": df[df.Churn == 1]["MonthlyCharges"].mean(),
    "avg_monthly_charge_retained": df[df.Churn == 0]["MonthlyCharges"].mean(),
    "estimated_annual_revenue_at_risk": (df[df.Churn == 1]["MonthlyCharges"].sum()) * 12,
}
for k, v in summary.items():
    print(f"{k}: {v:.3f}" if isinstance(v, float) else f"{k}: {v}")

pd.Series(summary).to_csv("../data/eda_summary_stats.csv")
print("\nCharts saved to ../charts/, summary stats saved to ../data/eda_summary_stats.csv")
