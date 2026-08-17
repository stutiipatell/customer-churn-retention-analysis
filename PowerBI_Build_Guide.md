# Power BI Dashboard Build Guide — Customer Churn & Retention

Data file: `churn_dashboard_data.xlsx` (sheets: `Customers`, `TenureGroupSort`, `RiskTierSort`)

---

## 1. Import & Set Up Relationships

1. Power BI Desktop → **Get Data → Excel Workbook** → select `churn_dashboard_data.xlsx`.
2. Load all three sheets: `Customers`, `TenureGroupSort`, `RiskTierSort`.
3. Go to **Model view** and create two relationships (both One-to-Many, single direction, from the sort table to Customers):
   - `TenureGroupSort[TenureGroup]` → `Customers[TenureGroup]`
   - `RiskTierSort[RiskTier]` → `Customers[RiskTier]`
4. In **Data view**, select `Customers[TenureGroup]` column → **Column tools → Sort by column** → `TenureGroupSort[SortOrder]` (do the same trick for `RiskTier` → `RiskTierSort[SortOrder]`). This makes charts display "0-6 mo, 7-12 mo, 13-24 mo…" and "Low, Medium, High" in the right order instead of alphabetically.

## 2. Create DAX Measures

Right-click `Customers` table → **New measure**. Add these one at a time:

```dax
Total Customers = COUNTROWS(Customers)

Churned Customers = CALCULATE(COUNTROWS(Customers), Customers[Churn] = 1)

Churn Rate = DIVIDE([Churned Customers], [Total Customers], 0)

Monthly Revenue at Risk = CALCULATE(SUM(Customers[MonthlyCharges]), Customers[Churn] = 1)

Annual Revenue at Risk = [Monthly Revenue at Risk] * 12

Total Monthly Revenue = SUM(Customers[MonthlyCharges])

Avg Monthly Charge = AVERAGE(Customers[MonthlyCharges])

Avg Tenure (Months) = AVERAGE(Customers[tenure])

High Risk Customers = CALCULATE(COUNTROWS(Customers), Customers[RiskTier] = "High")

High Risk Revenue = CALCULATE(SUM(Customers[MonthlyCharges]), Customers[RiskTier] = "High")

Avg Churn Probability = AVERAGE(Customers[ChurnProbability])
```

Format `Churn Rate` and `Avg Churn Probability` as **Percentage, 1 decimal**. Format the revenue measures as **Currency**.

## 3. Build 4 Report Pages

### Page 1 — Executive Overview
| Visual | Fields | Notes |
|---|---|---|
| 4 Card visuals | `[Total Customers]`, `[Churn Rate]`, `[Annual Revenue at Risk]`, `[High Risk Customers]` | Top row KPI strip |
| Donut chart | Legend: `ChurnLabel`, Values: `[Total Customers]` | Retained vs. Churned split |
| Bar chart | Axis: `Contract`, Values: `[Churn Rate]` | Sort descending |
| Line/column chart | Axis: `TenureGroup` (sorted), Values: `[Churn Rate]` | The "retention curve" |
| Slicers (top of page) | `Contract`, `InternetService`, `PaymentMethod` | Let viewers filter the whole page |

### Page 2 — Segment Deep Dive
| Visual | Fields | Notes |
|---|---|---|
| Matrix | Rows: `Contract`, Columns: `InternetService`, Values: `[Total Customers]`, `[Churn Rate]` | Conditional formatting (color scale) on Churn Rate |
| Bar chart | Axis: `PaymentMethod`, Values: `[Churn Rate]` | Sort descending |
| Bar chart | Axis: `NumAddonServices`, Values: `[Churn Rate]` | Shows the "stickiness" effect |
| Scatter chart | X: `[Avg Monthly Charge]`, Y: `[Churn Rate]`, Legend: `InternetService`, Details: `Contract` | Value-vs-risk view |

### Page 3 — Cohort & Revenue Risk
| Visual | Fields | Notes |
|---|---|---|
| Column chart | Axis: `TenureGroup` (sorted), Values: `[Total Customers]`, `[Churned Customers]` | Clustered columns |
| Column chart | Axis: `TenureGroup` (sorted), Values: `[Monthly Revenue at Risk]` | Revenue exposure by cohort |
| Card | `[Avg Tenure (Months)]` | |
| Table | `TenureGroup`, `[Total Customers]`, `[Churn Rate]`, `[Monthly Revenue at Risk]` | Sorted by TenureGroup sort order |

### Page 4 — Customer Risk Scoring (actionable list)
| Visual | Fields | Notes |
|---|---|---|
| 3 Cards | Count of customers per `RiskTier` (use a measure filtered per tier, or a Card visual with `RiskTier` filter) | High / Medium / Low counts |
| Stacked bar | Axis: `RiskTier` (sorted), Values: `[Total Customers]`, Legend: `ChurnLabel` | |
| Table | `customerID`, `Contract`, `tenure`, `MonthlyCharges`, `InternetService`, `ChurnProbability`, `RiskTier` | Sort by `ChurnProbability` descending; this is the retention team's action list — add a slicer for `RiskTier = High` |
| Conditional formatting | On `ChurnProbability` column in the table | Red = high, green = low (Format → Conditional formatting → Background color, field-based) |

## 4. Styling Tips
- Theme: **View → Themes** → pick a clean theme, or set custom colors: Navy `#1F3864` for retained/neutral, Orange/Red `#E4572E` for churn/risk.
- Add a text box header per page with the page title (e.g., "Executive Overview") and a **date/refresh** note.
- Use **Bookmarks** if you want a guided walkthrough (Overview → Segment → Cohort → Risk List).
- Publish to **Power BI Service** if you want a shareable link for your resume/portfolio — include the link in your resume or a QR code on the file.

## 5. What to Put On Your Resume
> *Designed an interactive Power BI dashboard visualizing churn drivers across 7,000+ telecom customers — contract type, tenure, payment method, and service mix — with a live risk-scoring page prioritizing $200K+ in monthly at-risk revenue for the retention team.*
