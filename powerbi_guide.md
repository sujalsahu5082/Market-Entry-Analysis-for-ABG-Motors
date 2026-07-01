# Power BI Integration Guide - ABG Motors

This guide walks you through importing the pre-processed data or raw scripts into **Power BI Desktop** and designing a premium dark-themed dashboard to present the Market Entry Analysis.

---

## 📅 Data Loading Options

### Option A: Using Pre-computed Predictions (Recommended & Fastest)
We generated a consolidated dataset containing predictions from all three models.
1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Excel Workbook**.
3. Choose the generated workbook: `cleaned_indian_with_predictions.xlsx`.
4. Select the sheet/table, click **Load**.

### Option B: Running Python ML Scripts directly in Power Query
To dynamically train the models every time Power BI refreshes:
1. Load the raw `IN_Data.xlsx` file.
2. In Power Query Editor, go to the **Transform** tab and click **Run Python Script**.
3. Copy and paste the code from [powerbi_powerquery_script.py](file:///c:/Users/Sujal%20Sahu/Downloads/Market-Entry-Analysis-for-ABG-Motors-in-India---CAPSTONE-PROJECT--main/powerbi_powerquery_script.py).
4. Click **OK**, expand the output table, and click **Close & Apply**.

---

## 🧮 DAX Measures to Add

Create a new table (e.g., `_Measures`) or add these directly to your main table:

```dax
// 1. Total predicted buyers based on the Random Forest model
Total Predicted Buyers (RF) = SUM(cleaned_indian_with_predictions[RF_PREDICTION])

// 2. The break-even sales benchmark set by the company
Sales Target = 12000

// 3. Margin threshold comparison percentage
Sales Margin % = DIVIDE([Total Predicted Buyers (RF)] - [Sales Target], [Sales Target])

// 4. Conditional text verdict for display cards
Market Entry Verdict = 
IF(
    [Sales Margin %] >= 0, 
    "✅ PROCEED WITH MARKET ENTRY", 
    "❌ DO NOT ENTER MARKET"
)
```

---

## 🎨 Dashboard Design System & Styling

To match the premium look of our web app, configure these background and formatting details:

* **Canvas Background**: Solid Color `#0B0F19` (Dark Slate/Blue) with 0% Transparency.
* **Card & Visual Backgrounds**: Solid Color `#161E31` with 15% Transparency, with white borders at 8% transparency.
* **Text Theme**: 
  - Callout values: `#FFFFFF` (White)
  - Category labels & text: `#94A3B8` (Muted Gray)
* **Accent Colors**:
  - Blue accent (Logistic Regression): `#3B82F6`
  - Green accent (Decision Tree / Positive values): `#10B981`
  - Purple accent (Random Forest): `#8B5CF6`
  - Orange accent (Target / Warning values): `#F59E0B`

---

## 📊 Visual Layout Recommendations

### 1. Executive Summary Panel (Top Row)
* **Visual Type: Card (New)**
  - Add `Total Predicted Buyers (RF)` (format as integer, e.g., `13,285`).
  - Add `Sales Target` (format as integer, e.g., `12,000`).
  - Add `Sales Margin %` (format as percentage, e.g., `10.7%`).
  - Add `Market Entry Verdict` (large text visual).

### 2. Model Performance Comparatives
* **Visual Type: Clustered Column Chart**
  - **X-axis**: Value names (Target, Logistic Regression, Decision Tree, Random Forest)
  - **Y-axis**: Buyers Count
  - Add `Sales Target` (12,000) and the sum of `LR_PREDICTION`, `DT_PREDICTION`, and `RF_PREDICTION`.

### 3. Customer Demographic Insights (EDA)
* **Visual Type: Line and Stacked Column Chart**
  - **X-axis**: Age Groups (create groups/bins on `CURR_AGE` with size 10, i.e., 20-30, 30-40, 40-50, etc.).
  - **Column y-axis**: Count of IDs (to show population volume).
  - **Line y-axis**: Average of `RF_PROBABILITY` (to show purchase rate by age).
* **Visual Type: Area Chart**
  - **X-axis**: Annual Income (`ANN_INCOME`).
  - **Y-axis**: Average of `RF_PROBABILITY`.
  - This displays the correlation curve showing how purchase likelihood spikes as annual income increases.

### 4. Interactive Profile Tester
* **Visual Type: Slicers**
  - Add slicers for `CURR_AGE`, `GENDER` (mapped to Male/Female), and `ANN_INCOME` to filter the table and view the average buyer probabilities interactively.
