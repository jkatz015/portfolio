# Executive Finance Dashboard - Tableau Build Guide

## Setup

1. Open **Tableau Public**
2. Connect → Text File → select `C:\Users\jkatz\Downloads\superstore_tableau_ready.csv`
3. Verify data types loaded correctly (dates as dates, numbers as numbers)
4. Click **Sheet 1** to begin

---

## Calculated Fields to Create First

Before building, create these calculated fields (Analysis → Create Calculated Field):

```
Name: Profit Margin %
Formula: SUM([Profit])/SUM([Revenue])

Name: Order Count
Formula: COUNTD([Order Id])

Name: Avg Order Value
Formula: SUM([Revenue])/COUNTD([Order Id])

Name: YoY Revenue Growth
Formula: (SUM([Revenue]) - LOOKUP(SUM([Revenue]), -1)) / ABS(LOOKUP(SUM([Revenue]), -1))

Name: Prior Year Revenue
Formula: LOOKUP(SUM([Revenue]), -4)  // 4 quarters back

Name: Variance to Budget
Formula: SUM([Revenue]) - SUM([Budget])

Name: Variance %
Formula: (SUM([Revenue]) - SUM([Budget])) / SUM([Budget])
```

---

# PAGE 1: EXECUTIVE SUMMARY

## Sheet 1.1: KPI Card - Total Revenue

1. New Worksheet → Rename to "KPI Revenue"
2. Drag `Revenue` to **Text** (Marks card)
3. Click on the pill → Format → Currency (Custom) → $#,##0,,"M" for millions or $#,##0,"K" for thousands
4. Click Text on Marks card → Edit → Center align, make font large (28pt+)
5. Right-click sheet title → Edit Title → "Total Revenue"
6. Format → Shading → Light gray background
7. Hide all gridlines, row/column dividers

## Sheet 1.2: KPI Card - Total Profit

1. New Worksheet → Rename to "KPI Profit"
2. Drag `Profit` to **Text**
3. Format as currency: $#,##0,"K"
4. Large centered font
5. Title: "Total Profit"

## Sheet 1.3: KPI Card - Profit Margin

1. New Worksheet → Rename to "KPI Margin"
2. Drag `Profit Margin %` (calculated field) to **Text**
3. Format as Percentage (1 decimal)
4. Large centered font
5. Title: "Profit Margin"

## Sheet 1.4: KPI Card - Total Orders

1. New Worksheet → Rename to "KPI Orders"
2. Drag `Order Count` (calculated field) to **Text**
3. Format as Number (no decimals, with comma separator)
4. Large centered font
5. Title: "Total Orders"

## Sheet 1.5: Revenue & Profit Trend

1. New Worksheet → Rename to "Revenue Trend"
2. Drag `Year-Month` to **Columns** (right-click → Discrete)
3. Drag `Revenue` to **Rows**
4. Drag `Profit` to **Rows** (creates second row)
5. Right-click second axis → **Dual Axis**
6. Right-click axis → **Synchronize Axis**
7. Click Revenue marks → Change to **Area** (light blue, 50% opacity)
8. Click Profit marks → Change to **Line** (dark green, thicker)
9. Title: "Revenue & Profit Trend"
10. Format axes: Currency, abbreviate to K/M

## Sheet 1.6: Revenue by Category (Pie)

1. New Worksheet → Rename to "Revenue by Category"
2. Drag `Category` to **Color**
3. Drag `Revenue` to **Angle**
4. Drag `Revenue` to **Label** → Quick Table Calc → Percent of Total
5. Change mark type to **Pie**
6. Title: "Revenue by Category"

## Sheet 1.7: Revenue by Region (Bar)

1. New Worksheet → Rename to "Revenue by Region"
2. Drag `Region` to **Rows**
3. Drag `Revenue` to **Columns**
4. Sort descending
5. Add `Revenue` to **Label**
6. Color: Single professional color (blue/green)
7. Title: "Revenue by Region"

## Dashboard 1: Executive Summary

1. New Dashboard → Rename to "Executive Summary"
2. Set size: Automatic or 1200x800
3. Layout:
   ```
   +------------------------------------------+
   |  TITLE: Executive Finance Dashboard      |
   +----------+----------+----------+---------+
   | Revenue  | Profit   | Margin   | Orders  |
   | $2.3M    | $286K    | 12.5%    | 5,009   |
   +----------+----------+----------+---------+
   |         Revenue & Profit Trend           |
   |         (area/line chart)                |
   +--------------------+---------------------+
   | Revenue by Category | Revenue by Region  |
   | (pie chart)        | (bar chart)        |
   +--------------------+---------------------+
   ```
4. Drag sheets onto dashboard
5. Add filters: Year, Region (apply to all worksheets)
6. Add title text box at top

---

# PAGE 2: REVENUE DEEP DIVE

## Sheet 2.1: Revenue Map

1. New Worksheet → Rename to "Revenue Map"
2. Double-click `State` (auto-generates map)
3. Drag `Revenue` to **Color**
4. Color palette: Sequential blue or green
5. Drag `Revenue` to **Label** (optional)
6. Title: "Revenue by State"

## Sheet 2.2: Monthly Revenue YoY Comparison

1. New Worksheet → Rename to "Revenue YoY"
2. Drag `Month Name` to **Columns**
3. Drag `Year` to **Color**
4. Drag `Revenue` to **Rows**
5. Change mark to **Line**
6. This shows each year's monthly pattern overlaid
7. Title: "Monthly Revenue by Year"

## Sheet 2.3: Revenue by Sub-Category

1. New Worksheet → Rename to "Revenue Sub-Category"
2. Drag `Sub-Category` to **Rows**
3. Drag `Revenue` to **Columns**
4. Sort descending
5. Add `Revenue` to **Label**
6. Title: "Revenue by Sub-Category"
7. Color by `Category` for grouping visual

## Sheet 2.4: Top 10 Customers

1. New Worksheet → Rename to "Top Customers"
2. Drag `Customer Name` to **Rows**
3. Drag `Revenue` to **Columns**
4. Right-click `Customer Name` → Filter → Top → By Field → Top 10 by Revenue
5. Sort descending
6. Add `Revenue` and `Order Count` to **Label**
7. Title: "Top 10 Customers by Revenue"

## Sheet 2.5: Revenue by Segment

1. New Worksheet → Rename to "Revenue Segment"
2. Drag `Segment` to **Rows**
3. Drag `Revenue` to **Columns**
4. Add `Profit Margin %` to **Color**
5. Title: "Revenue & Margin by Segment"

## Dashboard 2: Revenue Deep Dive

1. New Dashboard → Rename to "Revenue Deep Dive"
2. Layout:
   ```
   +------------------------------------------+
   |  TITLE: Revenue Deep Dive                |
   +------------------------------------------+
   |            Revenue Map (large)           |
   +--------------------+---------------------+
   | Monthly YoY        | Revenue by Segment  |
   +--------------------+---------------------+
   | Sub-Category       | Top 10 Customers    |
   +--------------------+---------------------+
   ```
3. Add filters: Year, Region, Category

---

# PAGE 3: PROFITABILITY ANALYSIS

## Sheet 3.1: Margin by Category

1. New Worksheet → Rename to "Margin by Category"
2. Drag `Category` to **Rows**
3. Drag `Profit Margin %` to **Columns**
4. Drag `Revenue` to **Size** (shows volume)
5. Sort by margin
6. Color: Green/Red diverging based on margin
7. Title: "Profit Margin by Category"

## Sheet 3.2: Margin by Sub-Category (Key Insight!)

1. New Worksheet → Rename to "Margin Sub-Category"
2. Drag `Sub-Category` to **Rows**
3. Drag `Profit Margin %` to **Columns**
4. Drag `Revenue` to **Size**
5. Add `Profit` to **Color** (diverging red-green)
6. Sort by `Profit Margin %`
7. Title: "Profitability by Sub-Category"
8. **This will show Tables has NEGATIVE margin - key insight!**

## Sheet 3.3: Profit Trend

1. New Worksheet → Rename to "Profit Trend"
2. Drag `Year-Month` to **Columns**
3. Drag `Profit` to **Rows**
4. Change to **Area** chart
5. Color by whether positive/negative:
   - Create calc: IF SUM([Profit]) >= 0 THEN "Positive" ELSE "Negative" END
6. Title: "Profit Trend Over Time"

## Sheet 3.4: Profit by Region & Category (Heatmap)

1. New Worksheet → Rename to "Profit Heatmap"
2. Drag `Region` to **Columns**
3. Drag `Category` to **Rows**
4. Drag `Profit` to **Color**
5. Drag `Profit` to **Label**
6. Color: Diverging Red-Green (red = loss, green = profit)
7. Title: "Profit by Region & Category"

## Sheet 3.5: Discount Impact Analysis

1. New Worksheet → Rename to "Discount Impact"
2. Create bins for Discount: Right-click Discount → Create → Bins (size 0.1)
3. Drag `Discount (bin)` to **Columns**
4. Drag `Profit Margin %` to **Rows**
5. Drag `Order Count` to **Size**
6. Title: "How Discounts Impact Margin"
7. **Key insight: Higher discounts correlate with lower/negative margins**

## Sheet 3.6: Cost Breakdown

1. New Worksheet → Rename to "Cost Breakdown"
2. Drag `Category` to **Rows**
3. Drag `Cost` to **Columns**
4. Drag `Sub-Category` to **Rows** (nested)
5. Title: "Cost by Category & Sub-Category"

## Dashboard 3: Profitability Analysis

1. New Dashboard → Rename to "Profitability Analysis"
2. Layout:
   ```
   +------------------------------------------+
   |  TITLE: Profitability Analysis           |
   +------------------------------------------+
   |    Margin by Sub-Category (full width)   |
   |    (sorted bar - shows winners/losers)   |
   +--------------------+---------------------+
   | Profit Heatmap     | Discount Impact     |
   | (Region x Category)| (scatter)           |
   +--------------------+---------------------+
   |         Profit Trend Over Time           |
   +------------------------------------------+
   ```
3. Add insight text boxes:
   - "Tables sub-category has -8.5% margin"
   - "Discounts >20% destroy profitability"

---

# PAGE 4: VARIANCE ANALYSIS

## Sheet 4.1: Actual vs Budget by Month

1. New Worksheet → Rename to "Actual vs Budget"
2. Drag `Year-Month` to **Columns**
3. Drag `Revenue` to **Rows** (rename to "Actual")
4. Drag `Budget` to **Rows**
5. Right-click → Dual Axis → Synchronize
6. Actual = solid line, Budget = dashed line
7. Title: "Actual vs Budget Revenue"

## Sheet 4.2: Variance Bars

1. New Worksheet → Rename to "Variance Bars"
2. Drag `Year-Month` to **Columns**
3. Drag `Variance to Budget` to **Rows**
4. Color by positive/negative:
   - Create calc: IF SUM([Variance to Budget]) >= 0 THEN "Favorable" ELSE "Unfavorable" END
   - Green for favorable, Red for unfavorable
5. Title: "Monthly Variance to Budget"

## Sheet 4.3: Variance by Region

1. New Worksheet → Rename to "Variance Region"
2. Drag `Region` to **Rows**
3. Drag `Variance to Budget` to **Columns**
4. Drag `Variance %` to **Label**
5. Color by Favorable/Unfavorable
6. Title: "Variance by Region"

## Sheet 4.4: Variance by Category

1. New Worksheet → Rename to "Variance Category"
2. Drag `Category` to **Rows**
3. Drag `Variance to Budget` to **Columns**
4. Drag `Variance %` to **Label**
5. Color by Favorable/Unfavorable
6. Title: "Variance by Category"

## Sheet 4.5: Variance Waterfall (Advanced)

1. New Worksheet → Rename to "Variance Waterfall"
2. This requires Gantt chart technique:
   - Create calculated field `Negative Variance`: -[Variance to Budget]
   - Drag dimension (Category or Region) to Columns
   - Drag `Variance to Budget` to Rows
   - Change to Gantt Bar
   - Drag `Negative Variance` to Size
3. Alternative: Use grouped bar chart for simplicity
4. Title: "Variance Waterfall"

## Sheet 4.6: YoY Growth by Quarter

1. New Worksheet → Rename to "YoY Growth"
2. Drag `Quarter` to **Columns**
3. Drag `Year` to **Color**
4. Drag `Revenue` to **Rows**
5. Add Table Calc: Percent Difference From → Previous (compute using Year)
6. Title: "Year-over-Year Revenue Growth"

## Dashboard 4: Variance Analysis

1. New Dashboard → Rename to "Variance Analysis"
2. Layout:
   ```
   +------------------------------------------+
   |  TITLE: Variance Analysis                |
   +------------------------------------------+
   |      Actual vs Budget Trend (large)      |
   +------------------------------------------+
   |      Monthly Variance Bars               |
   +--------------------+---------------------+
   | Variance by Region | Variance by Category|
   +--------------------+---------------------+
   ```
3. Add filter: Year
4. Add text insights

---

# FINAL STEPS

## Create Navigation

1. On each dashboard, add navigation buttons
2. Objects → Button → Navigate to Dashboard
3. Or use a floating horizontal container with text links

## Apply Consistent Formatting

1. Format → Workbook Theme → Select professional theme
2. Colors: Use 3-4 colors max
   - Primary: Dark blue (#1f77b4)
   - Secondary: Green (#2ca02c)
   - Accent: Orange (#ff7f0e)
   - Negative: Red (#d62728)
3. Fonts:
   - Titles: Bold, 14-16pt
   - Labels: Regular, 10-12pt
   - KPIs: Bold, 24-32pt
4. Remove all unnecessary gridlines
5. Clean white/light gray backgrounds

## Add Interactivity

1. Dashboard Actions:
   - Dashboard → Actions → Add Action → Filter
   - Select a chart → filters other charts
2. Highlight Actions:
   - Hovering highlights related data
3. Tooltips:
   - Customize to show relevant metrics

## Publish to Tableau Public

1. File → Save to Tableau Public
2. Sign in to your Tableau Public account
3. Name: "Executive Finance Dashboard"
4. Add tags: finance, dashboard, KPI, executive
5. Copy the public URL for your portfolio

---

# KEY INSIGHTS TO HIGHLIGHT

When presenting this dashboard, emphasize these findings:

1. **Tables sub-category loses money** (-8.5% margin) - recommend discontinuing or repricing
2. **West region most profitable** - consider expansion strategy
3. **Consumer segment dominates** but Corporate has better margins
4. **High discounts (>20%) destroy profitability** - need discount policy review
5. **Technology category has best margins** - product mix opportunity
6. **Seasonal patterns** - Q4 strongest (holiday effect)

---

# SCREENSHOT CHECKLIST

Save these screenshots for your portfolio:

- [ ] Full Executive Summary dashboard
- [ ] Revenue Map zoomed
- [ ] Profitability by Sub-Category (showing Tables negative)
- [ ] Discount Impact scatter plot
- [ ] Actual vs Budget comparison
- [ ] Mobile/tablet responsive view

Save to: `dashboard/screenshots/`
