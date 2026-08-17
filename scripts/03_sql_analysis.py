"""
03_sql_analysis.py
Loads the cleaned data into a local SQLite database and runs SQL queries
for cohort- and segment-level retention analysis — the kind of querying
a data analyst would be expected to write against a warehouse table.
"""

import sqlite3
import pandas as pd

DATA_PATH = "../data/telco_churn_clean.csv"
DB_PATH = "../data/churn.db"

df = pd.read_csv(DATA_PATH)

conn = sqlite3.connect(DB_PATH)
df.to_sql("customers", conn, if_exists="replace", index=False)


def run(label, query):
    print(f"\n--- {label} ---")
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))
    return result


# 1. High-value customers at risk: top monthly spenders who churned
q1 = run(
    "Top 10 highest-value churned customers (revenue leakage)",
    """
    SELECT customerID, Contract, tenure, MonthlyCharges, InternetService, PaymentMethod
    FROM customers
    WHERE Churn = 1
    ORDER BY MonthlyCharges DESC
    LIMIT 10;
    """,
)

# 2. Segment risk table: churn rate & customer count by contract x internet service
q2 = run(
    "Churn rate by Contract x InternetService segment",
    """
    SELECT Contract, InternetService,
           COUNT(*) AS customers,
           ROUND(100.0 * SUM(Churn) / COUNT(*), 1) AS churn_rate_pct,
           ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges
    FROM customers
    GROUP BY Contract, InternetService
    ORDER BY churn_rate_pct DESC;
    """,
)

# 3. Retention by cohort (tenure group) with revenue at risk
q3 = run(
    "Revenue at risk by tenure cohort",
    """
    SELECT TenureGroup,
           COUNT(*) AS customers,
           ROUND(100.0 * SUM(Churn) / COUNT(*), 1) AS churn_rate_pct,
           ROUND(SUM(CASE WHEN Churn = 1 THEN MonthlyCharges ELSE 0 END), 0) AS monthly_revenue_at_risk
    FROM customers
    GROUP BY TenureGroup
    ORDER BY
        CASE TenureGroup
            WHEN '0-6 mo' THEN 1 WHEN '7-12 mo' THEN 2 WHEN '13-24 mo' THEN 3
            WHEN '25-48 mo' THEN 4 WHEN '49-72 mo' THEN 5 END;
    """,
)

# 4. Impact of add-on services on retention (stickiness effect)
q4 = run(
    "Retention by number of add-on services",
    """
    SELECT NumAddonServices,
           COUNT(*) AS customers,
           ROUND(100.0 * SUM(Churn) / COUNT(*), 1) AS churn_rate_pct
    FROM customers
    GROUP BY NumAddonServices
    ORDER BY NumAddonServices;
    """,
)

# 5. Payment method risk ranking
q5 = run(
    "Churn rate by payment method",
    """
    SELECT PaymentMethod,
           COUNT(*) AS customers,
           ROUND(100.0 * SUM(Churn) / COUNT(*), 1) AS churn_rate_pct
    FROM customers
    GROUP BY PaymentMethod
    ORDER BY churn_rate_pct DESC;
    """,
)

conn.close()
print(f"\nSQLite DB saved -> {DB_PATH} (table: customers)")
