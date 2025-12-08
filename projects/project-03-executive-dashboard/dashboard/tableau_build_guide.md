# Executive Finance Dashboard - Tableau Build Guide

## 1. Connect the Data (2 minutes)

1. Open **Tableau Public**
2. On the start screen, under Connect, click **Text File**
3. Browse to `superstore_tableau_ready.csv` and open it
4. Tableau should show you the data grid
5. Click **Sheet 1** at the bottom to start building views

**You'll see:**
- Left side: Data pane (Dimensions & Measures)
- Top middle: Columns / Rows shelves
- Directly under Columns/Rows on the left: Marks card (this is where you change from Automatic → Bar, Line, Area, etc.)

---

## 2. KPI Tiles (Revenue, Profit, Margin) – 3 Sheets (6–7 minutes)

We'll use:
- Revenue
- Profit
- Gross Margin % (already in your data)

### 2.1 KPI – Total Revenue

1. At the bottom, right-click **Sheet 1** → **Rename** → type: `KPI – Revenue`
2. In the Data pane:
   - Drag **Revenue** to **Text** on the Marks card
3. On the Marks card:
   - Click the dropdown where it says Automatic and leave it on **Text**
4. Right-click on the number in the view → **Format**:
   - Under Pane → Numbers, choose **Currency (Custom)** and set to 0 decimal places
5. Increase the font:
   - Click Format pane or click the Abc text → use the toolbar to set font size to **24–28, bold**

This gives you a big, clean Revenue number.

### 2.2 KPI – Total Profit

1. Right-click **KPI – Revenue** sheet tab → **Duplicate**
2. Rename the new one to `KPI – Profit`
3. On the duplicated sheet:
   - In the Marks card, replace Revenue with Profit:
   - Drag **Profit** from the Data pane onto **Text** (it will replace Revenue)
4. Right-click the number → **Format**:
   - Also format as Currency with 0 decimals
5. Optional: If Profit can be negative, keep the red parentheses default

### 2.3 KPI – Profit Margin %

1. Duplicate again: Right-click **KPI – Profit** → **Duplicate**
2. Rename to `KPI – Margin %`
3. On this sheet:
   - Drag **Gross Margin %** from the Data pane onto **Text** on the Marks card (replaces Profit)
4. Right-click the number → **Format**:
   - Under Numbers, choose **Percentage** (or Number Custom with 2 decimals)
5. Make sure the label looks like e.g. **18.7%**

**Now you have 3 KPI sheets ready.**

---

## 3. Monthly Revenue Trend – Area or Line (5 minutes)

We'll build a Revenue over Time chart.

1. At the bottom, click the **New Worksheet** icon
2. Rename this sheet: `Monthly Revenue`
3. From the Data pane:
   - Drag **Order Date** to **Columns**
   - Tableau will default to YEAR(Order Date)
4. Click the YEAR(Order Date) pill on Columns:
   - Choose **More → Custom** or simply click again and pick **MONTH** (the one that shows Mar 2016, not discrete)
   - You want a continuous time axis if possible
5. Drag **Revenue** to **Rows**
6. On the Marks card:
   - Click the dropdown (Automatic) → select **Area** or **Line** (your choice)
7. To apply color:
   - Click **Color** on the Marks card → choose a single professional color (blue/green)
8. To adjust opacity (for Area): Color → Opacity → ~50%
9. Clean axis:
   - Right-click the Revenue axis → **Format** → set Currency and abbreviate if you want (Display Units → Thousands or Millions)

This gives you a clean time trend.

---

## 4. Profit by Category – Bar Chart (4 minutes)

1. New sheet → rename `Profit by Category`
2. Drag **Category** to **Rows**
3. Drag **Profit** to **Columns**
4. On the Marks card, make sure it's **Bar**
5. Click the **Sort** icon on the toolbar (or right-click Category → Sort by Field → Profit, Descending)
6. Optional formatting:
   - Drag **Profit** onto **Label** on the Marks card to show values
   - Format Profit as Currency again

---

## 5. Sales vs Profit – Scatter Plot (5 minutes)

1. New sheet → rename `Sales vs Profit`
2. Drag **Sales** to **Columns**
3. Drag **Profit** to **Rows**
4. On the Marks card:
   - Change Automatic → **Circle**
5. Drag **Category** to **Color** on the Marks card
6. Drag **Sales** to **Size** on the Marks card
7. Optional:
   - Drag **Sub-Category** to **Detail** so hovering shows which product types they are
8. Right-click axes and **Format**:
   - Set Sales and Profit to Currency

Now you have a visual of high-Sales / low-Profit risk zones.

---

## 6. Filters (3–4 minutes)

We'll use:
- Year
- Region
- Category

1. Pick any sheet (e.g., Monthly Revenue) and do:
2. Drag **Year** to **Filters**:
   - Choose all years for now
3. Right-click the Year pill in Filters → **Show Filter**
4. Drag **Region** to **Filters**, then right-click → **Show Filter**
5. Drag **Category** to **Filters**, then right-click → **Show Filter**

You'll see filter cards appear on the right side of the sheet. We'll reuse them in the dashboard.

To make filters global on the dashboard later, we'll change them to apply to all related sheets.

---

## 7. Build the Dashboard (8–10 minutes)

1. Click **New Dashboard** (icon next to new worksheet)
2. On the left, under Size, choose:
   - **Automatic** or a fixed size like **1600 x 900**

### 7.1 Place KPI Tiles

From the Sheets list on the left, drag:
- KPI – Revenue
- KPI – Profit
- KPI – Margin %

Drop them across the top:
1. Drag the first sheet to the top
2. Then change the container to a horizontal layout if needed:
   - Right-click near them → **Add Horizontal Layout Container**
   - Drag all three KPI sheets inside so they sit side-by-side
3. Adjust each to be short in height and wide enough for the numbers

### 7.2 Place the Main Charts

Below the KPI row:
1. Drag **Monthly Revenue** under the KPI row (left side)
2. Drag **Profit by Category** next to it (right side)
3. Drag **Sales vs Profit** below them (centered or spanning the width)

You can also use horizontal/vertical containers if you want more control, but do not overthink it—just get all three visible.

### 7.3 Add Filters to Dashboard

1. Click the **Monthly Revenue** chart on the dashboard to select it
2. In the top-right of that chart's title area, click the small dropdown arrow → **Filters** → choose:
   - Year
   - Region
   - Category
3. The filter cards will appear on the right side of the dashboard
4. For each filter:
   - Click the dropdown on the filter card → **Apply to Worksheets** → **All Using This Data Source**

This makes the filter control all views on the dashboard.

Optionally, format filters as:
- Single value dropdowns
- Or multiple value dropdowns, whichever feels cleaner

---

## 8. Fixing a Squished Title (quick note)

If your dashboard title or sheet titles look squished:
1. Click the title area (top of the dashboard or worksheet)
2. In the toolbar, increase the font size and check **Wrap Text** or remove extra line breaks
3. You can also right-click the title → **Edit Title** and manually add line breaks or spacing

---

## 9. Final Polish (3 minutes)

**Change sheet titles to something executive-level:**
- Monthly Revenue → `Revenue Trend Over Time`
- Profit by Category → `Profit Contribution by Category`
- Sales vs Profit → `Sales vs Profit (Risk View)`

**For the dashboard title:**
1. Double-click the dashboard title → type:
   `Executive Revenue & Profitability Dashboard`

**Clean up:**
- Remove legends you don't need (right-click → Hide)

---

## Final Dashboard Layout

```
+------------------------------------------+
|  Executive Revenue & Profitability       |
|  Dashboard                               |
+------------+------------+----------------+
| Revenue    | Profit     | Margin %       |
| $2.3M      | $286K      | 12.5%          |
+------------+------------+----------------+
| Revenue Trend Over Time | Profit by      |
| (Area/Line Chart)       | Category (Bar) |
+-------------------------+----------------+
|     Sales vs Profit (Risk View)          |
|     (Scatter Plot)                       |
+------------------------------------------+
| Filters: Year | Region | Category        |
+------------------------------------------+
```

---

## Key Insights to Highlight

When presenting this dashboard, emphasize:

1. **Tables sub-category loses money** - recommend discontinuing or repricing
2. **High-Sales / Low-Profit products** visible in scatter plot - pricing issues
3. **Revenue trends** - identify seasonal patterns
4. **Category performance** - Technology most profitable

---

## Publish to Tableau Public

1. **File** → **Save to Tableau Public As...**
2. Sign in to your Tableau Public account
3. Name: `Executive Finance Dashboard`
4. Click **Save**
5. Copy the public URL for your portfolio
