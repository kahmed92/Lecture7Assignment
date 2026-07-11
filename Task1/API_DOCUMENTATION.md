# Transaction Analyzer - API Documentation

Complete API reference for programmatic use of the transaction analysis library.

## Table of Contents

1. [TransactionAnalyzer Class](#transactionanalyzer-class)
2. [Methods Reference](#methods-reference)
3. [Code Examples](#code-examples)
4. [Data Structures](#data-structures)

---

## TransactionAnalyzer Class

### Class Definition

```python
class TransactionAnalyzer:
    """Analyze transaction history from Excel files"""
    
    def __init__(self, excel_file: str)
```

### Constructor

#### Parameters
- **excel_file** (str): Path to Excel file with transaction data

#### Raises
- **FileNotFoundError**: If Excel file doesn't exist
- **Exception**: If Excel file cannot be read

#### Example
```python
from transaction_analyzer import TransactionAnalyzer

analyzer = TransactionAnalyzer('transactions.xlsx')
```

---

## Methods Reference

### 1. find_duplicate_transactions()

Identifies duplicate transactions within a configurable time window.

```python
def find_duplicate_transactions(self, time_window: int = 1) -> pd.DataFrame
```

#### Parameters
- **time_window** (int, default=1): Number of days to consider as "duplicate window"

#### Returns
- **pd.DataFrame**: DataFrame with columns:
  - Date1: First transaction date
  - Date2: Second transaction date
  - Description: Transaction description
  - Amount: Transaction amount
  - Days_Apart: Number of days between transactions

#### Example
```python
# Find duplicates within 1 day
duplicates = analyzer.find_duplicate_transactions(time_window=1)

if len(duplicates) > 0:
    print("Found duplicates:")
    print(duplicates)
else:
    print("No duplicates found")
```

---

### 2. identify_recurring_transactions()

Identifies transactions that occur regularly.

```python
def identify_recurring_transactions(self, min_occurrences: int = 3) -> dict
```

#### Parameters
- **min_occurrences** (int, default=3): Minimum number of times transaction must occur

#### Returns
- **dict**: Dictionary with format:
  ```python
  {
      'Description': {
          'count': int,              # Number of occurrences
          'amount': float,           # Average amount
          'interval_days': float,    # Average days between occurrences
          'total': float            # Total amount spent
      }
  }
  ```

#### Example
```python
# Find recurring transactions with 2+ occurrences
recurring = analyzer.identify_recurring_transactions(min_occurrences=2)

for description, data in recurring.items():
    print(f"\n{description}")
    print(f"  Occurrences: {data['count']}")
    print(f"  Average amount: ₹{data['amount']:.2f}")
    print(f"  Interval: {data['interval_days']:.1f} days")
    print(f"  Total: ₹{data['total']:.2f}")
```

---

### 3. calculate_monthly_totals()

Calculates income, expense, and net for each month.

```python
def calculate_monthly_totals(self) -> dict
```

#### Returns
- **dict**: Dictionary with format:
  ```python
  {
      'YYYY-MM': {
          'income': float,           # Total income that month
          'expense': float,          # Total expense that month
          'net': float,              # Income - Expense
          'transaction_count': int   # Number of transactions
      }
  }
  ```

#### Example
```python
monthly = analyzer.calculate_monthly_totals()

for month, data in monthly.items():
    print(f"{month}:")
    print(f"  Income: ₹{data['income']:>10,.2f}")
    print(f"  Expense: ₹{data['expense']:>10,.2f}")
    print(f"  Net: ₹{data['net']:>10,.2f}")
```

---

### 4. spending_by_category()

Groups expenses by category and provides statistics.

```python
def spending_by_category(self) -> pd.DataFrame
```

#### Returns
- **pd.DataFrame**: DataFrame with index as Category and columns:
  - Total: Sum of expenses in category
  - Average: Mean transaction amount
  - Count: Number of transactions

#### Example
```python
categories = analyzer.spending_by_category()

print(categories)
# Output:
#            Total    Average  Count
# Category
# Personal   15000       500       30
# Social      8500    283.33       30
# Official    5000   1666.67        3
```

---

### 5. spending_patterns()

Analyzes spending patterns by day of week, month, and other metrics.

```python
def spending_patterns(self) -> dict
```

#### Returns
- **dict**: Dictionary with format:
  ```python
  {
      'by_day_of_week': pd.DataFrame,    # Spending by day (sum, count, mean)
      'by_month': pd.DataFrame,           # Spending by month (sum, count, mean)
      'average_daily_expense': float,     # Average daily spending
      'daily_statistics': {
          'min': float,
          'max': float,
          'mean': float,
          'median': float
      }
  }
  ```

#### Example
```python
patterns = analyzer.spending_patterns()

print("Daily Statistics:")
for stat, value in patterns['daily_statistics'].items():
    print(f"  {stat}: ₹{value:.2f}")

print("\nSpending by Day of Week:")
print(patterns['by_day_of_week'])
```

---

### 6. generate_report()

Generates comprehensive text report and prints to console.

```python
def generate_report(self) -> None
```

#### Side Effects
- Prints detailed formatted report to console
- Calls all analysis methods to populate analysis_results

#### Example
```python
analyzer.generate_report()
# Output: Formatted report with all analyses
```

---

### 7. export_analysis_to_excel()

Exports analysis results to Excel file.

```python
def export_analysis_to_excel(self, output_file: str = 'transaction_analysis.xlsx') -> None
```

#### Parameters
- **output_file** (str): Path for output Excel file

#### Creates
- Excel file with multiple sheets:
  - Transactions: Original data
  - Duplicates: Duplicate transactions (if any)
  - By Category: Category breakdown
  - Monthly Summary: Monthly totals

#### Example
```python
analyzer.export_analysis_to_excel('my_analysis.xlsx')
# Creates: my_analysis.xlsx
```

---

### 8. get_summary()

Gets quick summary of all analyses.

```python
def get_summary(self) -> dict
```

#### Returns
- **dict**: Summary with keys:
  - total_transactions: Total transaction count
  - date_range: String "YYYY-MM-DD to YYYY-MM-DD"
  - total_income: Total income amount
  - total_expense: Total expense amount
  - duplicate_count: Number of duplicates found
  - recurring_count: Number of recurring transactions

#### Example
```python
summary = analyzer.get_summary()
print(f"Total transactions: {summary['total_transactions']}")
print(f"Date range: {summary['date_range']}")
print(f"Total income: ₹{summary['total_income']:,.2f}")
print(f"Total expense: ₹{summary['total_expense']:,.2f}")
```

---

## Code Examples

### Example 1: Basic Analysis

```python
from transaction_analyzer import TransactionAnalyzer

# Load transactions
analyzer = TransactionAnalyzer('transactions.xlsx')

# Get summary
summary = analyzer.get_summary()
print(f"Analyzed {summary['total_transactions']} transactions")

# Find duplicates
duplicates = analyzer.find_duplicate_transactions()
print(f"Found {len(duplicates)} duplicate(s)")

# Export results
analyzer.export_analysis_to_excel('results.xlsx')
```

### Example 2: Detailed Analysis

```python
from transaction_analyzer import TransactionAnalyzer

analyzer = TransactionAnalyzer('transactions.xlsx')

# Get all analyses
duplicates = analyzer.find_duplicate_transactions()
recurring = analyzer.identify_recurring_transactions(min_occurrences=2)
monthly = analyzer.calculate_monthly_totals()
categories = analyzer.spending_by_category()
patterns = analyzer.spending_patterns()

# Print findings
print("=== ANALYSIS RESULTS ===")
print(f"\nDuplicates: {len(duplicates)}")
print(f"Recurring transactions: {len(recurring)}")
print(f"\nMonthly breakdown:")
for month, data in monthly.items():
    print(f"  {month}: ₹{data['net']:,.2f} net")

print(f"\nTop spending categories:")
print(categories.nlargest(3, 'Total')[['Total']])

print(f"\nDaily spend range:")
stats = patterns['daily_statistics']
print(f"  Min: ₹{stats['min']:.2f}, Max: ₹{stats['max']:.2f}")
```

### Example 3: Budget Analysis

```python
from transaction_analyzer import TransactionAnalyzer

analyzer = TransactionAnalyzer('transactions.xlsx')
monthly = analyzer.calculate_monthly_totals()
categories = analyzer.spending_by_category()

# Calculate budget status
MONTHLY_BUDGET = 30000
total_spent = sum(m['expense'] for m in monthly.values())
avg_monthly = total_spent / len(monthly)

print(f"Monthly Budget: ₹{MONTHLY_BUDGET:,.2f}")
print(f"Average Spending: ₹{avg_monthly:,.2f}")
print(f"Budget Status: {'✓ Under' if avg_monthly < MONTHLY_BUDGET else '✗ Over'}")

# Category allocation
print("\nBudget by Category:")
for category, row in categories.iterrows():
    pct = (row['Total'] / total_spent) * 100
    print(f"  {category}: {pct:.1f}%")
```

### Example 4: Spending Trend Analysis

```python
from transaction_analyzer import TransactionAnalyzer
import matplotlib.pyplot as plt

analyzer = TransactionAnalyzer('transactions.xlsx')
monthly = analyzer.calculate_monthly_totals()

months = list(monthly.keys())
expenses = [monthly[m]['expense'] for m in months]
incomes = [monthly[m]['income'] for m in months]

plt.figure(figsize=(12, 5))
plt.plot(months, expenses, marker='o', label='Expense', color='red')
plt.plot(months, incomes, marker='s', label='Income', color='green')
plt.legend()
plt.xlabel('Month')
plt.ylabel('Amount (₹)')
plt.title('Monthly Income vs Expense Trend')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('trend.png')
```

### Example 5: Recurring Payment Forecast

```python
from transaction_analyzer import TransactionAnalyzer
from datetime import datetime, timedelta

analyzer = TransactionAnalyzer('transactions.xlsx')
recurring = analyzer.identify_recurring_transactions()

# Project next month's recurring expenses
next_month_recurring = 0
upcoming = []

for desc, data in recurring.items():
    next_month_recurring += data['amount']
    upcoming.append({
        'description': desc,
        'amount': data['amount'],
        'interval': data['interval_days']
    })

print(f"Projected recurring expenses next month: ₹{next_month_recurring:,.2f}")
print("\nUpcoming recurring payments:")
for item in upcoming:
    print(f"  • {item['description']}: ₹{item['amount']:.2f} (every {item['interval']:.0f} days)")
```

---

## Data Structures

### DataFrame: Analysis Results

When methods return pandas DataFrames, they follow these structures:

#### Duplicates DataFrame
```
Date1              Date2              Description  Amount  Days_Apart
2024-05-15         2024-05-16         Coffee        300      1
2024-06-01         2024-06-01         Rent         5000      0
```

#### Category Spending DataFrame
```
              Total    Average  Count
Category
Personal      15000    500.00    30
Social         8500    283.33    30
Official       5000   1666.67     3
```

#### Monthly Summary DataFrame
```
         income  expense      net  transaction_count
2024-05   50000    28500    21500                 45
2024-06   50000    27500    22500                 42
2024-07   50000    26800    23200                 40
```

---

## Error Handling

### Common Exceptions

```python
from transaction_analyzer import TransactionAnalyzer

try:
    analyzer = TransactionAnalyzer('transactions.xlsx')
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print(f"Error loading file: {str(e)}")

try:
    analyzer.generate_report()
except Exception as e:
    print(f"Error during analysis: {str(e)}")
```

---

## Performance Considerations

- **Large datasets**: Works efficiently with 10,000+ transactions
- **Memory**: Loads entire file into memory (typical Excel files < 100MB)
- **Time**: Analysis completes in <1 second for typical datasets
- **Optimization**: Use specific methods instead of `generate_report()` for large files

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-07 | Initial release |

---

## Support

For issues or questions:
1. Check `README_TRANSACTIONS.md` for general usage
2. Review code examples above
3. Check error messages in console output

---

**Last Updated**: July 2024
