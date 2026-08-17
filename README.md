# Customer Churn & Retention Analysis

An end-to-end data analytics project identifying why customers leave a telecom
provider, quantifying the revenue impact, and building a predictive model to
flag at-risk customers for proactive retention — combining Python/ML analysis,
SQL segmentation, and an interactive Power BI dashboard.

![Dashboard Overview](dashboard\p1.png)
![Dashboard Overview](dashboard\p2.png)
![Dashboard Overview](dashboard\p3.png)
![Dashboard Overview](dashboard\p4.png)

## Highlights
- **7,043 customers** analyzed (IBM Telco Customer Churn dataset)
- **26.5% churn rate**, ~**$1.67M** in annualized revenue at risk
- Random Forest churn prediction model: **0.844 ROC-AUC**, 78% recall on churners
- SQL-based segment analysis pinpointing the highest-risk customer cohorts
- 4-page interactive **Power BI dashboard** with AI-powered Key Influencers and a live risk-scoring action list
- Full customer base scored into **High / Medium / Low** risk tiers with an actionable output file

## Tech Stack
Python (pandas, NumPy, scikit-learn, matplotlib, seaborn) · SQL (SQLite) · Power BI (DAX, data modeling) · docx-js for reporting

## Project Structure
```
churn_project/
├── data/
│   ├── telco_churn.csv                    # raw source data
│   ├── telco_churn_clean.csv              # cleaned + feature-engineered
│   ├── churn.db                           # SQLite DB used for SQL analysis
│   └── eda_summary_stats.csv
├── scripts/
│   ├── 01_data_cleaning.py                # cleaning + feature engineering
│   ├── 02_eda.py                          # exploratory analysis + charts
│   ├── 03_sql_analysis.py                 # SQL cohort/segment queries
│   ├── 04_modeling.py                     # ML models + customer risk scoring
│   ├── 05_powerbi_export.py               # prepares the Power BI data model
│   └── build_report.js                    # generates the Word report
├── charts/                                # all generated PNG charts (11 total)
├── dashboard/
│   ├── Customer_Churn_Retention_Dashboard.pbix
│   └── PowerBI_Build_Guide.md             # how the dashboard was built (DAX, layout)
├── screenshots/                           # dashboard page exports for this README
└── outputs/
    ├── Customer_Churn_Retention_Analysis_Report.docx
    ├── churn_risk_scores.csv              # every customer scored + risk tier
    ├── churn_dashboard_data.xlsx          # Power BI source data
    └── model_metrics.csv
```

## How to Reproduce
```bash
cd scripts
python3 01_data_cleaning.py
python3 02_eda.py
python3 03_sql_analysis.py
python3 04_modeling.py
python3 05_powerbi_export.py
```
Then open `dashboard/Customer_Churn_Retention_Dashboard.pbix` in Power BI Desktop
(or import `outputs/churn_dashboard_data.xlsx` and follow `PowerBI_Build_Guide.md`
to rebuild it from scratch).

## Dashboard Pages
1. **Executive Overview** — KPI summary, churn by contract/tenure, and an AI-powered Key Influencers visual
2. **Segment Deep Dive** — Contract × Internet Service risk heatmap, payment method and add-on service analysis
3. **Cohort & Revenue Risk** — tenure-based cohort analysis and monthly revenue exposure
4. **Customer Risk Scoring** — live, filterable action list of customers ranked by churn probability

## Key Findings
1. **Contract type dominates churn risk** — month-to-month customers churn at 42.7% vs. 2.8% for two-year contracts.
2. **The first 6 months are the danger zone** — 52.9% of new customers churn before month 6.
3. **Fiber-optic customers churn more, despite paying more** — a signal of a value/quality gap worth investigating.
4. **Manual payment (electronic check) correlates with a 3x higher churn rate** than autopay methods.
5. **Add-on service adoption increases stickiness** — churn drops as customers subscribe to more services.
6. **The highest-risk segment**: month-to-month + fiber-optic customers (2,128 people, 54.6% churn rate).

## Business Recommendations
- Incentivize contract upgrades for month-to-month fiber customers (highest-risk segment)
- Build a 90-day onboarding/retention program targeting new customers
- Investigate the fiber-optic price-to-value gap
- Push electronic-check payers toward autopay
- Route the model's "High Risk" (2,101 customers) list to the retention team weekly via the dashboard's risk-scoring page
