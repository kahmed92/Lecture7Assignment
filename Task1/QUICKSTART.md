# Quick Start Guide - Transaction Analysis

Get up and running in 3 simple steps!

## Step 1: Install Dependencies

```bash
pip install pandas openpyxl matplotlib seaborn numpy
```

## Step 2: Generate Sample Data

Create 90 days of realistic transaction data:

```bash
python sample_transactions.py
```

**Output**: `sample_transactions.xlsx` (Excel file with transactions)

## Step 3: Run Analysis

Analyze the transactions and generate report:

```bash
python transaction_analyzer.py
```

**Outputs**:
- Console report with detailed analysis
- `transaction_analysis.xlsx` (results in Excel)

### Bonus: Create Visualizations

Generate visual dashboard:

```bash
python visualize_transactions.py
```

**Outputs**:
- `transaction_analysis.png` (6-panel dashboard)
- `category_breakdown.png` (detailed category charts)

---

## Using Your Own Data

1. **Prepare Excel file** with columns:
   - Date (YYYY-MM-DD)
   - Description
   - Amount (numeric)
   - Category
   - Type (Credit/Debit)

2. **Run analysis**:
   ```bash
   python transaction_analyzer.py your_file.xlsx
   python visualize_transactions.py your_file.xlsx
   ```

---

## What You'll Get

✓ **Duplicate Transaction Detection** - Find billing errors  
✓ **Recurring Payment Identification** - Track subscriptions  
✓ **Monthly Summaries** - See income vs expenses  
✓ **Category Breakdown** - Understand spending habits  
✓ **Visual Dashboards** - Charts and graphs  
✓ **Detailed Report** - Console and Excel exports  

---

## Sample Output Preview

```
MONTHLY SUMMARY
  2024-05:
    - Income:       ₹50,000.00
    - Expense:      ₹28,500.00
    - Net:          ₹21,500.00
    - Transactions: 45

SPENDING BY CATEGORY
  Personal:    ₹15,000.00
  Social:      ₹8,500.00
  Official:    ₹5,000.00

RECURRING TRANSACTIONS
  • Rent (Monthly): ₹5,000.00
  • Coffee (Weekly): ₹300.00
  • Internet (Monthly): ₹1,500.00
```

---

## Need Help?

See `README_TRANSACTIONS.md` for detailed documentation.

---

**Time to complete**: < 5 minutes  
**No setup required**: Just run the commands!
