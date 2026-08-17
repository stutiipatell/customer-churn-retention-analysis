const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, AlignmentType, ImageRun, PageBreak,
  Header, Footer, PageNumber, LevelFormat, convertInchesToTwip
} = require("docx");

const CHARTS = "../charts";
const NAVY = "1F3864";
const ACCENT = "E4572E";
const LIGHTGREY = "F2F2F2";

function h1(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_1, spacing: { before: 300, after: 150 } });
}
function h2(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 120 } });
}
function body(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text, ...opts })],
    spacing: { after: 160 },
  });
}
function bullet(text, opts = {}) {
  return new Paragraph({
    text,
    bullet: { level: 0 },
    spacing: { after: 80 },
    ...opts,
  });
}
function img(path, width, height) {
  return new Paragraph({
    children: [new ImageRun({ data: fs.readFileSync(path), transformation: { width, height }, type: "png" })],
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
  });
}
function caption(text) {
  return new Paragraph({
    children: [new TextRun({ text, italics: true, size: 18, color: "595959" })],
    alignment: AlignmentType.CENTER,
    spacing: { after: 260 },
  });
}

function cell(text, opts = {}) {
  return new TableCell({
    width: { size: opts.width || 2000, type: WidthType.DXA },
    shading: opts.header ? { type: ShadingType.CLEAR, fill: NAVY } : undefined,
    children: [
      new Paragraph({
        children: [new TextRun({ text: String(text), bold: !!opts.header, color: opts.header ? "FFFFFF" : "000000", size: 20 })],
      }),
    ],
    verticalAlign: "center",
  });
}

function dataTable(headers, rows, colWidths) {
  const totalWidth = colWidths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: totalWidth, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [
      new TableRow({ children: headers.map((hh, i) => cell(hh, { header: true, width: colWidths[i] })) }),
      ...rows.map(
        (r) => new TableRow({ children: r.map((c, i) => cell(c, { width: colWidths[i] })) })
      ),
    ],
  });
}

const doc = new Document({
  styles: {
    default: {
      document: { run: { font: "Calibri", size: 22 } },
    },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, color: NAVY, font: "Calibri" },
        paragraph: { spacing: { before: 300, after: 150 }, border: { bottom: { color: NAVY, space: 4, style: BorderStyle.SINGLE, size: 8 } } },
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 25, bold: true, color: ACCENT, font: "Calibri" },
        paragraph: { spacing: { before: 240, after: 120 } },
      },
    ],
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 },
        },
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            alignment: AlignmentType.RIGHT,
            children: [new TextRun({ text: "Customer Churn & Retention Analysis", size: 16, color: "808080" })],
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: "Page ", size: 16, color: "808080" }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "808080" })],
          })],
        }),
      },
      children: [
        // ---------------- TITLE PAGE ----------------
        new Paragraph({ spacing: { before: 1200 }, children: [] }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "Customer Churn & Retention Analysis", bold: true, size: 52, color: NAVY })],
          spacing: { after: 200 },
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "Identifying At-Risk Customers and Revenue-Saving Interventions for a Telecom Provider", size: 26, color: "595959", italics: true })],
          spacing: { after: 600 },
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "Prepared using Python (pandas, scikit-learn), SQL, and statistical modeling", size: 20, color: "808080" })],
          spacing: { after: 100 },
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "Dataset: IBM Telco Customer Churn (7,043 customers, 21 features)", size: 20, color: "808080" })],
          spacing: { after: 100 },
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "August 2026", size: 20, color: "808080" })],
        }),
        new Paragraph({ children: [new PageBreak()] }),

        // ---------------- EXECUTIVE SUMMARY ----------------
        h1("Executive Summary"),
        body(
          "This project analyzes customer churn for a telecommunications provider using a real-world dataset of 7,043 customers. The goal was to identify which customers are at risk of leaving, understand the business drivers behind churn, and translate those insights into concrete retention actions. The analysis combines exploratory data analysis, SQL-based segmentation, and machine learning to produce a churn-risk score for every customer in the base."
        ),
        body("Headline findings:"),
        bullet("Overall churn rate is 26.5%, representing roughly $1.67M in annualized recurring revenue at risk."),
        bullet("Contract type is the single strongest churn driver: month-to-month customers churn at 42.7%, versus 11.3% for one-year and 2.8% for two-year contracts."),
        bullet("New customers are the highest-risk segment — 52.9% of customers in their first 6 months churn, more than 5x the rate of customers past 4 years of tenure."),
        bullet("Fiber-optic internet subscribers churn at 41.9%, more than double the DSL rate (19.0%), despite paying the highest average bills — suggesting a price-to-value or service-quality gap."),
        bullet("Customers paying by electronic check churn at 45.3%, nearly 3x the rate of customers on autopay (credit card or bank transfer)."),
        bullet("A Random Forest model predicts churn with 84.4% ROC-AUC and correctly flags 78% of customers who actually churn, enabling proactive, targeted retention outreach."),

        new Paragraph({ children: [new PageBreak()] }),

        // ---------------- OBJECTIVES / METHODOLOGY ----------------
        h1("Business Problem & Objectives"),
        body(
          "Customer acquisition costs far exceed retention costs in subscription businesses, making churn one of the most direct levers on profitability. The objectives of this analysis were to:"
        ),
        bullet("Quantify the scale and revenue impact of customer churn."),
        bullet("Identify which customer segments and behaviors are associated with higher churn risk."),
        bullet("Build a predictive model that scores every customer's likelihood of churning."),
        bullet("Translate findings into specific, actionable retention recommendations for the business."),

        h1("Data & Methodology"),
        body("Dataset: IBM Telco Customer Churn — 7,043 customers across demographics, account information, subscribed services, billing details, and churn status (26.5% churned)."),
        body("Tools & techniques:"),
        bullet("Python (pandas, NumPy) for data cleaning and feature engineering"),
        bullet("SQL (SQLite) for cohort- and segment-level aggregation queries"),
        bullet("Matplotlib / Seaborn for exploratory visualization"),
        bullet("Scikit-learn for predictive modeling (Logistic Regression, Random Forest)"),
        body("Data cleaning steps: converted TotalCharges to numeric (11 blank values from brand-new customers were set to 0), encoded the churn target as binary, and engineered three new features: tenure cohort buckets, count of subscribed add-on services, and average monthly spend."),

        new Paragraph({ children: [new PageBreak()] }),

        // ---------------- EDA SECTION ----------------
        h1("Exploratory Analysis: Who Is Churning, and Why"),

        h2("Overall Churn Rate"),
        img(`${CHARTS}/01_overall_churn_rate.png`, 320, 320),
        caption("Figure 1. 26.5% of the customer base has churned."),

        h2("Contract Type Is the Dominant Driver"),
        img(`${CHARTS}/02_churn_by_contract.png`, 420, 300),
        caption("Figure 2. Churn falls sharply as contract commitment length increases."),
        body("Month-to-month customers have no switching cost and churn at more than 3.7x the rate of annual contract holders, and over 15x the rate of two-year contract holders. Contract length is the clearest lever available for reducing churn."),

        h2("Tenure: The First 6 Months Are Critical"),
        img(`${CHARTS}/03_churn_by_tenure.png`, 440, 300),
        caption("Figure 3. Churn risk decreases steadily the longer a customer stays."),
        body("Over half of customers who are less than 6 months in churn within that window. This 'early churn cliff' suggests onboarding and early-lifecycle engagement is where retention investment has the highest leverage."),

        h2("Pricing and Service Type"),
        img(`${CHARTS}/04_monthly_charges_dist.png`, 420, 300),
        caption("Figure 4. Churned customers skew toward higher monthly bills."),
        img(`${CHARTS}/05_churn_by_internet_service.png`, 420, 300),
        caption("Figure 5. Fiber-optic customers churn at more than double the DSL rate."),
        body("Fiber customers pay the most on average but also churn the most, which points to a perceived value gap rather than a pure affordability issue — worth validating with customer satisfaction or NPS data if available."),

        h2("Service Adoption Increases Stickiness"),
        img(`${CHARTS}/06_churn_by_addons.png`, 440, 300),
        caption("Figure 6. Customers with 5-6 add-on services churn at a fraction of the rate of those with 1 add-on."),
        body("Customers with zero add-ons churn at a moderate 21.4%, but the highest-risk group is customers with just one add-on service (45.8% churn) — a segment that has started engaging but hasn't yet built enough switching cost to stay. Churn falls consistently from there as service adoption deepens."),

        h2("Payment Method"),
        img(`${CHARTS}/07_churn_by_payment.png`, 420, 300),
        caption("Figure 7. Manual electronic check payers churn nearly 3x more than autopay customers."),

        h2("Feature Correlations"),
        img(`${CHARTS}/08_correlation_heatmap.png`, 380, 320),
        caption("Figure 8. Tenure is negatively correlated with churn; monthly charges are positively correlated."),

        new Paragraph({ children: [new PageBreak()] }),

        // ---------------- SQL SECTION ----------------
        h1("SQL Segment Analysis"),
        body("Cohort- and segment-level queries were run against the cleaned dataset (loaded into SQLite) to quantify risk and revenue exposure by segment."),

        h2("Churn Rate by Contract x Internet Service"),
        dataTable(
          ["Contract", "Internet Service", "Customers", "Churn Rate", "Avg. Monthly Charge"],
          [
            ["Month-to-month", "Fiber optic", "2,128", "54.6%", "$87.02"],
            ["Month-to-month", "DSL", "1,223", "32.2%", "$50.22"],
            ["One year", "Fiber optic", "539", "19.3%", "$98.78"],
            ["Month-to-month", "No internet", "524", "18.9%", "$20.41"],
            ["One year", "DSL", "570", "9.3%", "$61.40"],
            ["Two year", "Fiber optic", "429", "7.2%", "$104.57"],
          ],
          [2600, 2400, 1600, 1600, 2400]
        ),
        body(" "),
        body("The highest-risk segment by far is month-to-month customers with fiber-optic internet — 2,128 customers churning at 54.6%. This single segment should be the top priority for a retention campaign.", { bold: true }),

        h2("Revenue at Risk by Tenure Cohort"),
        dataTable(
          ["Tenure Cohort", "Customers", "Churn Rate", "Monthly Revenue at Risk"],
          [
            ["0-6 months", "1,481", "52.9%", "$49,896"],
            ["7-12 months", "705", "35.9%", "$19,058"],
            ["13-24 months", "1,024", "28.7%", "$23,082"],
            ["25-48 months", "1,594", "20.4%", "$27,463"],
            ["49-72 months", "2,239", "9.5%", "$19,632"],
          ],
          [2600, 2200, 2200, 2600]
        ),
        body(" "),
        body("New customers (0-6 months) represent the single largest pool of at-risk monthly revenue (~$50K/month) despite having the smallest average bills — driven purely by volume and churn rate, reinforcing the case for an onboarding-focused retention program."),

        new Paragraph({ children: [new PageBreak()] }),

        // ---------------- MODELING SECTION ----------------
        h1("Predictive Modeling"),
        body("Two classification models were trained to predict churn probability for each customer, using an 80/20 train-test split stratified on the target. Class weights were balanced to account for the 26.5% / 73.5% class imbalance."),

        h2("Model Performance"),
        dataTable(
          ["Model", "ROC-AUC", "F1-Score (Churn)", "Recall (Churn)"],
          [
            ["Logistic Regression", "0.841", "0.614", "78%"],
            ["Random Forest", "0.844", "0.621", "78%"],
          ],
          [3000, 2200, 2600, 2200]
        ),
        body(" "),
        body("The Random Forest model was selected as the production model — it edges out logistic regression on every metric while still offering interpretable feature importances. It correctly identifies 78% of customers who will actually churn, which is what matters most for a proactive retention program (missing an at-risk customer is more costly than a false alarm)."),

        h2("ROC Curve"),
        img(`${CHARTS}/09_roc_curve.png`, 380, 340),
        caption("Figure 9. Both models substantially outperform random guessing (AUC = 0.5)."),

        h2("Confusion Matrix (Random Forest)"),
        img(`${CHARTS}/10_confusion_matrix.png`, 340, 300),
        caption("Figure 10. The model prioritizes catching true churners (recall) over avoiding false alarms, by design."),

        h2("Top Churn Drivers"),
        img(`${CHARTS}/11_feature_importance.png`, 440, 380),
        caption("Figure 11. Tenure, two-year contracts, total charges, and fiber-optic service are the strongest predictors."),
        body("The model's top drivers align closely with the exploratory findings: how long a customer has been with the company, whether they're locked into a long-term contract, their total spend to date, and whether they subscribe to fiber internet."),

        h2("Deliverable: Customer Risk Scores"),
        body("Every customer in the dataset was scored with a churn probability and assigned to a risk tier, producing a ready-to-use action list for the retention/customer success team:"),
        dataTable(
          ["Risk Tier", "Probability Range", "Customer Count", "Suggested Action"],
          [
            ["High", "> 60%", "2,101", "Proactive outreach, retention offer, contract upgrade incentive"],
            ["Medium", "30-60%", "1,939", "Targeted email campaign, service value messaging"],
            ["Low", "< 30%", "3,003", "Standard engagement, upsell opportunities"],
          ],
          [1800, 2400, 2200, 3600]
        ),

        new Paragraph({ children: [new PageBreak()] }),

        // ---------------- RECOMMENDATIONS ----------------
        h1("Business Recommendations"),
        bullet("Incentivize contract upgrades: offer month-to-month fiber customers a discount or perk to move to a one- or two-year contract — this is the single highest-leverage lever, given the 3-15x churn rate gap by contract length."),
        bullet("Build a 90-day onboarding program: since over half of new customers churn within 6 months, invest in proactive check-ins, welcome offers, and early support for this cohort specifically."),
        bullet("Investigate the fiber-optic value gap: fiber customers pay the most and churn the most — a targeted customer satisfaction survey or competitive pricing review is warranted."),
        bullet("Migrate electronic check payers to autopay: offer a small discount or incentive to switch, since manual payment correlates with a 3x higher churn rate (likely a proxy for lower engagement/commitment)."),
        bullet("Promote add-on service adoption early: customers with multiple add-ons churn far less; bundling 2-3 services into a starter package could improve stickiness from day one."),
        bullet("Operationalize the risk score: route the 2,101 'High Risk' customers to the retention team weekly, prioritized by monthly revenue, to focus effort where it saves the most revenue."),

        h1("Project Files & Reproducibility"),
        body("This analysis is fully reproducible. The project includes:"),
        bullet("01_data_cleaning.py — data loading, cleaning, and feature engineering"),
        bullet("02_eda.py — exploratory analysis and chart generation"),
        bullet("03_sql_analysis.py — SQLite-based segment and cohort queries"),
        bullet("04_modeling.py — model training, evaluation, and customer risk scoring"),
        bullet("churn_risk_scores.csv — final scored output for all 7,043 customers"),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("../outputs/Customer_Churn_Retention_Analysis_Report.docx", buf);
  console.log("Report written.");
});
