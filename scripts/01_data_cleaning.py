"""
01_data_cleaning.py
Customer Churn & Retention Analysis — Data Cleaning & Preprocessing

Loads the raw Telco Customer Churn dataset, fixes data quality issues,
engineers a few analysis-ready columns, and writes a clean CSV that the
rest of the pipeline (EDA, SQL, modeling) reads from.
"""

import pandas as pd
import numpy as np

RAW_PATH = "../data/telco_churn.csv"
CLEAN_PATH = "../data/telco_churn_clean.csv"


def load_raw(path=RAW_PATH):
    return pd.read_csv(path)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # TotalCharges is read as object because 11 rows contain blank strings
    # for brand-new customers (tenure = 0). Coerce to numeric, then fill
    # those with 0 since no charge has been billed yet.
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    n_missing = df["TotalCharges"].isna().sum()
    df["TotalCharges"] = df["TotalCharges"].fillna(0)

    # Standardize target to binary
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

    # Senior citizen already 0/1 but stored as int64 with different dtype
    # than other flags — cast to a consistent Yes/No string for readability
    # in EDA, and keep a numeric version for modeling.
    df["SeniorCitizen_Label"] = df["SeniorCitizen"].map({1: "Yes", 0: "No"})

    # Feature engineering -----------------------------------------------
    # Tenure buckets — useful for cohort-style retention curves
    bins = [0, 6, 12, 24, 48, 72]
    labels = ["0-6 mo", "7-12 mo", "13-24 mo", "25-48 mo", "49-72 mo"]
    df["TenureGroup"] = pd.cut(df["tenure"], bins=bins, labels=labels, include_lowest=True)

    # Count of subscribed add-on services (signal for stickiness)
    service_cols = [
        "OnlineSecurity", "OnlineBackup", "DeviceProtection",
        "TechSupport", "StreamingTV", "StreamingMovies",
    ]
    df["NumAddonServices"] = (df[service_cols] == "Yes").sum(axis=1)

    # Average revenue per tenure month (helps spot high-value at-risk customers)
    df["AvgMonthlySpend"] = np.where(
        df["tenure"] > 0, df["TotalCharges"] / df["tenure"], df["MonthlyCharges"]
    )

    print(f"Rows: {len(df)} | Missing TotalCharges filled: {n_missing}")
    print(f"Churn rate: {df['Churn'].mean():.2%}")
    return df


if __name__ == "__main__":
    raw = load_raw()
    clean_df = clean(raw)
    clean_df.to_csv(CLEAN_PATH, index=False)
    print(f"Saved cleaned dataset -> {CLEAN_PATH}")
    print(clean_df.dtypes)
