# Transaction Analysis Application

A comprehensive Python application for analyzing personal transaction history from Excel files. This tool helps identify spending patterns, recurring payments, duplicate transactions, and provides detailed financial insights.

## Features

### 1. **Duplicate Transaction Detection**
- Identifies duplicate transactions within a configurable time window
- Detects same description, amount, and date proximity
- Useful for catching billing errors or duplicate charges

### 2. **Recurring Transaction Identification**
- Automatically finds recurring transactions (subscriptions, bills, etc.)
- Calculates average intervals between occurrences
- Provides total spending on recurring items
- Filters by minimum occurrences (default: 3+)

### 3. **Monthly Analysis**
- Calculates total income and expenses per month
- Shows net income (income - expense)
- Tracks transaction count per month
- Identifies spending trends over time

### 4. **Category-Based Spending Analysis**
- Groups expenses by category
- Provides total, average, and count metrics per category
- Identifies top spending categories
- Sorted by total spending

### 5. **Spending Patterns**
- Daily spending statistics (min, max, mean, median)
- Spending patterns by day of week
- Spending patterns by month
- Average daily expense calculation

### 6. **Visualizations**
- Spending by category (bar chart)
- Monthly income vs expense comparison
- Daily spending trend with moving average
- Spending distribution by category (box plot)
- Top 10 transactions
- Expense distribution (pie chart)
- Category breakdown analysis

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Required Libraries
```bash
pip install pandas openpyxl matplotlib seaborn numpy
```

## Project Structure

```
.
├── sample_transactions.py        # Generate sample transaction data
├── transaction_analyzer.py       # Main analysis engine
├── visualize_transactions.py     # Visualization module
├── sample_transactions.xlsx      # Sample data (generated)
├── transaction_analysis.xlsx     # Analysis results (generated)
├── transaction_analysis.png      # Dashboard visualization (generated)
└── README_TRANSACTIONS.md        # This file
```

## Usage

### Step 1: Generate Sample Data

```bash
python sample_transactions.py
```

This creates `sample_transactions.xlsx` with 90 days of realistic transaction data including:
- Personal expenses (groceries, pharmacy, clothing)
- Social expenses (restaurants, movies, coffee)
- Official expenses (rent, utilities, bills)
- Salary income
- Recurring payments
- Duplicate transactions (for testing)

### Step 2: Analyze Transactions

#### Basic Analysis with Report
```bash
python transaction_analyzer.py sample_transactions.xlsx
```

This will:
- Load the Excel file
- Perform all analyses
- Print comprehensive report to console
- Export results to `transaction_analysis.xlsx`

#### Using as a Python Module

```python
from transaction_analyzer import TransactionAnalyzer

# Load and analyze transactions
analyzer = TransactionAnalyzer('sample_transactions.xlsx')

# Generate report with all analyses
analyzer.generate_report()

# Export analysis to Excel
analyzer.export_analysis_to_excel('results.xlsx')

# Get specific analyses
duplicates = analyzer.find_duplicate_transactions()
recurring = analyzer.identify_recurring_transactions()
monthly = analyzer.calculate_monthly_totals()
categories = analyzer.spending_by_category()
patterns = analyzer.spending_patterns()

# Get quick summary
summary = analyzer.get_summary()
print(summary)
```

### Step 3: Visualize Results

```bash
python visualize_transactions.py sample_transactions.xlsx
```

This generates:
- `transaction_analysis.png` - 6-panel dashboard
- `category_breakdown.png` - Detailed category analysis

## Excel File Format

Your input Excel file should have the following structure:

### Required Columns:
- **Date**: Transaction date (YYYY-MM-DD format)
- **Description**: Transaction description/merchant name
- **Amount**: Transaction amount (numeric)
- **Category**: Expense category (Personal, Social, Official, Income, etc.)
- **Type**: Transaction type (Debit for expenses, Credit for income)

### Example:
| Date       | Description | Amount | Category   | Type   |
|------------|-------------|--------|-----------|--------|
| 2024-05-01 | Salary      | 50000  | Income    | Credit |
| 2024-05-02 | Groceries   | 1200   | Personal  | Debit  |
| 2024-05-02 | Coffee      | 300    | Social    | Debit  |
| 2024-05-15 | Rent        | 5000   | Official  | Debit  |

## Output Files

### 1. transaction_analysis.xlsx
Multi-sheet Excel file containing:

- **Transactions**: Original data with formatting
- **Duplicates**: Detected duplicate transactions (if any)
- **By Category**: Spending breakdown by category
- **Monthly Summary**: Monthly income, expense, and net

### 2. transaction_analysis.png
6-panel dashboard showing:
1. Total spending by category (horizontal bar chart)
2. Monthly income vs expense comparison
3. Daily spending trend with area fill
4. Spending distribution by category (box plot)
5. Top 10 transactions
6. Expense distribution (pie chart)

### 3. Console Report
Detailed text report with:
- Duplicate transaction details
- Recurring transaction summary
- Monthly breakdown
- Category analysis
- Spending pattern statistics

## Configuration

### Duplicate Detection
Adjust time window in `transaction_analyzer.py`:
```python
duplicates = analyzer.find_duplicate_transactions(time_window=2)  # 2 days
```

### Recurring Transactions
Adjust minimum occurrences:
```python
recurring = analyzer.identify_recurring_transactions(min_occurrences=2)  # 2+ times
```

### Standard Deviation Threshold
In `transaction_analyzer.py`, line ~65:
```python
if np.std(amounts) < 0.1 * np.mean(amounts):  # 10% threshold
```
Lower = stricter (only identical amounts), Higher = more flexible

## Analysis Methods Explained

### Duplicate Detection
- Looks for transactions with same description and amount
- Within configurable time window (default: 1 day)
- Returns all matching pairs with date difference

### Recurring Transactions
- Groups by description
- Calculates if amount variance is < 10% of mean
- Computes average interval between occurrences
- Only includes items with 3+ occurrences (configurable)

### Monthly Totals
- Groups transactions by year-month
- Separates credits (income) and debits (expenses)
- Calculates net for each month
- Useful for budget planning

### Category Analysis
- Groups all debit transactions by category
- Calculates total, average, and count
- Helps identify biggest spending categories
- Useful for budget allocation

### Spending Patterns
- Daily statistics: min, max, mean, median transaction amounts
- Day-of-week analysis: which days you spend most
- Monthly comparison: seasonal spending variations
- Average daily expense for planning purposes

## Example Output

```
======================================================================
TRANSACTION ANALYSIS REPORT
======================================================================

1. DUPLICATE TRANSACTIONS
----------------------------------------------------------------------
No duplicate transactions found.

2. RECURRING TRANSACTIONS (3+ occurrences)
----------------------------------------------------------------------
  • Rent
    - Frequency: Every 30.0 days (~3 times)
    - Amount: ₹5000.00
    - Total: ₹15000.00
  
  • Coffee
    - Frequency: Every 7.2 days (~12 times)
    - Amount: ₹300.00
    - Total: ₹3600.00

3. MONTHLY SUMMARY
----------------------------------------------------------------------
  2024-05:
    - Income:       ₹50000.00
    - Expense:      ₹28500.00
    - Net:          ₹21500.00
    - Transactions: 45

4. SPENDING BY CATEGORY
----------------------------------------------------------------------
                Total    Average  Count
Category
Personal    15000.00  500.000000     30
Social      8500.00   283.333333     30
Official    5000.00  1666.666667      3

5. SPENDING PATTERNS
----------------------------------------------------------------------
  Daily Spending Statistics:
    - Min: ₹100.00
    - Max: ₹5000.00
    - Mean: ₹952.38
    - Median: ₹800.00
    - Average Daily: ₹952.38
```

## Tips & Best Practices

1. **Data Preparation**
   - Ensure consistent date format (YYYY-MM-DD)
   - Keep category names consistent
   - Use 'Income' for credit transactions
   - Round amounts to 2 decimal places

2. **Categorization**
   - Create meaningful category names
   - Use same categories consistently
   - Don't mix different concepts in one category

3. **Regular Analysis**
   - Run monthly for budget tracking
   - Compare month-over-month trends
   - Review recurring transactions annually

4. **Duplicate Handling**
   - Investigate duplicate alerts
   - Check with bank/merchant for errors
   - Keep evidence before disputing charges

5. **Budgeting**
   - Use monthly totals to plan budget
   - Compare actual vs planned spending
   - Adjust categories based on patterns

## Limitations

- Does not handle multi-currency transactions
- Date format must be consistent (YYYY-MM-DD preferred)
- Requires exact duplicate amounts (won't catch off-by-one errors)
- Cannot detect fraudulent transactions
- Doesn't account for pending/cleared status

## Troubleshooting

### FileNotFoundError
```
Error: File not found: sample_transactions.xlsx
```
**Solution**: Ensure Excel file exists in the same directory. Run `python sample_transactions.py` first.

### Module ImportError
```
ModuleNotFoundError: No module named 'pandas'
```
**Solution**: Install required packages:
```bash
pip install pandas openpyxl matplotlib seaborn numpy
```

### Date Format Error
```
ParserError: Unable to parse ... as a date
```
**Solution**: Ensure Date column is in YYYY-MM-DD format or Excel date format.

### Empty Analysis Results
**Solution**: Verify your data has:
- At least 2 columns with correct names
- Date values in the Date column
- Numeric values in Amount column
- Type column with "Credit" or "Debit" values

## Future Enhancements

- Budget vs actual comparison
- Predictive spending forecasts
- Anomaly detection (unusual transactions)
- Multi-currency support
- CSV file support
- Interactive dashboard (web interface)
- Export to PDF reports
- Savings goal tracking

## License

This project is open source and available for personal and educational use.

## Author

Created for personal financial analysis and learning purposes.

---

**Last Updated**: July 2024
**Version**: 1.0
