"""
04_modeling.py
Builds and evaluates churn prediction models:
  - Logistic Regression (interpretable baseline)
  - Random Forest (stronger predictive model + feature importance)

Outputs: metrics printed to console, ROC curve, confusion matrix, and
feature importance chart saved to ../charts/, plus a scored customer
list (churn probability) saved to ../outputs/ for the retention team
to act on.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_auc_score, roc_curve, classification_report,
    confusion_matrix, precision_recall_curve, f1_score
)

DATA_PATH = "../data/telco_churn_clean.csv"
CHART_DIR = "../charts"
OUT_DIR = "../outputs"

df = pd.read_csv(DATA_PATH)

# ---------------------------------------------------------------------------
# Feature preparation
# ---------------------------------------------------------------------------
target = "Churn"
drop_cols = ["customerID", target, "SeniorCitizen_Label", "TenureGroup", "AvgMonthlySpend"]
X = df.drop(columns=drop_cols)
y = df[target]

cat_cols = X.select_dtypes(include="object").columns.tolist()
num_cols = X.select_dtypes(exclude="object").columns.tolist()

X_encoded = pd.get_dummies(X, columns=cat_cols, drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ---------------------------------------------------------------------------
# Model 1: Logistic Regression (baseline, interpretable)
# ---------------------------------------------------------------------------
log_reg = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
log_reg.fit(X_train_scaled, y_train)
log_pred = log_reg.predict(X_test_scaled)
log_proba = log_reg.predict_proba(X_test_scaled)[:, 1]

# ---------------------------------------------------------------------------
# Model 2: Random Forest (higher capacity, feature importance)
# ---------------------------------------------------------------------------
rf = RandomForestClassifier(
    n_estimators=300, max_depth=8, min_samples_leaf=20,
    class_weight="balanced", random_state=42, n_jobs=-1
)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
rf_proba = rf.predict_proba(X_test)[:, 1]

# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------
print("=" * 60)
print("LOGISTIC REGRESSION")
print("=" * 60)
print(classification_report(y_test, log_pred, target_names=["Retained", "Churned"]))
print(f"ROC-AUC: {roc_auc_score(y_test, log_proba):.3f}")
print(f"F1 (churn class): {f1_score(y_test, log_pred):.3f}")

print("\n" + "=" * 60)
print("RANDOM FOREST")
print("=" * 60)
print(classification_report(y_test, rf_pred, target_names=["Retained", "Churned"]))
print(f"ROC-AUC: {roc_auc_score(y_test, rf_proba):.3f}")
print(f"F1 (churn class): {f1_score(y_test, rf_pred):.3f}")

# ROC curve comparison ------------------------------------------------------
plt.figure(figsize=(6, 5.5))
for name, proba, color in [("Logistic Regression", log_proba, "#2E86AB"), ("Random Forest", rf_proba, "#E4572E")]:
    fpr, tpr, _ = roc_curve(y_test, proba)
    auc = roc_auc_score(y_test, proba)
    plt.plot(fpr, tpr, label=f"{name} (AUC = {auc:.3f})", color=color, linewidth=2)
plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Random guess")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve — Churn Prediction Models")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/09_roc_curve.png", bbox_inches="tight")
plt.close()

# Confusion matrix (Random Forest, the stronger model) -----------------------
cm = confusion_matrix(y_test, rf_pred)
plt.figure(figsize=(5, 4.5))
import seaborn as sns
sns.heatmap(
    cm, annot=True, fmt="d", cmap="Blues",
    xticklabels=["Retained", "Churned"], yticklabels=["Retained", "Churned"]
)
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.title("Confusion Matrix — Random Forest")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/10_confusion_matrix.png", bbox_inches="tight")
plt.close()

# Feature importance (Random Forest) ------------------------------------------
importances = pd.Series(rf.feature_importances_, index=X_encoded.columns).sort_values(ascending=False).head(15)
plt.figure(figsize=(7, 6))
importances.sort_values().plot(kind="barh", color="#2E86AB")
plt.xlabel("Feature Importance")
plt.title("Top 15 Churn Drivers — Random Forest")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/11_feature_importance.png", bbox_inches="tight")
plt.close()

print("\nTop 10 churn drivers (Random Forest feature importance):")
print(importances.sort_values(ascending=False).head(10).to_string())

# ---------------------------------------------------------------------------
# Score the full customer base for a retention action list
# ---------------------------------------------------------------------------
full_proba = rf.predict_proba(X_encoded)[:, 1]
scored = df[["customerID", "Contract", "tenure", "MonthlyCharges", "InternetService"]].copy()
scored["churn_probability"] = full_proba
scored["risk_tier"] = pd.cut(
    scored["churn_probability"], bins=[0, 0.3, 0.6, 1.0],
    labels=["Low", "Medium", "High"], include_lowest=True
)
scored = scored.sort_values("churn_probability", ascending=False)
scored.to_csv(f"{OUT_DIR}/churn_risk_scores.csv", index=False)

print(f"\nRisk tier breakdown:\n{scored['risk_tier'].value_counts()}")
print(f"\nSaved scored customer list -> {OUT_DIR}/churn_risk_scores.csv")

# Save model metrics summary for the report
metrics_summary = pd.DataFrame({
    "model": ["Logistic Regression", "Random Forest"],
    "roc_auc": [roc_auc_score(y_test, log_proba), roc_auc_score(y_test, rf_proba)],
    "f1_churn": [f1_score(y_test, log_pred), f1_score(y_test, rf_pred)],
})
metrics_summary.to_csv(f"{OUT_DIR}/model_metrics.csv", index=False)
print(f"\n{metrics_summary}")
