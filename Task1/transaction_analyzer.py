import pandas as pd
import numpy as np
from datetime import datetime
import os


class TransactionAnalyzer:
    """Analyze transaction history from Excel files"""

    def __init__(self, excel_file):
        """Initialize with Excel file path"""
        if not os.path.exists(excel_file):
            raise FileNotFoundError(f"File not found: {excel_file}")
        self.file_path = excel_file
        self.df = None
        self.analysis_results = {}
        self._load_data()

    def _load_data(self):
        """Load transaction data from Excel file"""
        try:
            self.df = pd.read_excel(self.file_path, sheet_name='Transactions')
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            print(f"✓ Loaded {len(self.df)} transactions from {self.file_path}")
        except Exception as e:
            raise Exception(f"Error loading Excel file: {str(e)}")

    def find_duplicate_transactions(self, time_window=1):
        """
        Identify duplicate transactions within time window (in days)
        Returns DataFrame of potential duplicates
        """
        duplicates = []

        for i in range(len(self.df)):
            for j in range(i + 1, len(self.df)):
                row1 = self.df.iloc[i]
                row2 = self.df.iloc[j]

                date_diff = abs((row1['Date'] - row2['Date']).days)

                if (date_diff <= time_window and
                    row1['Amount'] == row2['Amount'] and
                    row1['Description'] == row2['Description']):
                    duplicates.append({
                        'Date1': row1['Date'],
                        'Date2': row2['Date'],
                        'Description': row1['Description'],
                        'Amount': row1['Amount'],
                        'Days_Apart': date_diff
                    })

        self.analysis_results['duplicates'] = pd.DataFrame(duplicates)
        return self.analysis_results['duplicates']

    def identify_recurring_transactions(self, min_occurrences=3):
        """
        Identify recurring transactions based on description and approximate amount
        """
        recurring = {}

        for desc in self.df['Description'].unique():
            desc_df = self.df[self.df['Description'] == desc].copy()
            if len(desc_df) >= min_occurrences:
                amounts = desc_df['Amount'].values
                if np.std(amounts) < 0.1 * np.mean(amounts):  # Standard deviation < 10%
                    dates = sorted(desc_df['Date'].values)
                    intervals = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]

                    recurring[desc] = {
                        'count': len(desc_df),
                        'amount': np.mean(amounts),
                        'interval_days': np.mean(intervals) if intervals else 0,
                        'total': np.sum(amounts)
                    }

        self.analysis_results['recurring'] = recurring
        return recurring

    def calculate_monthly_totals(self):
        """Calculate total spending and income by month"""
        self.df['YearMonth'] = self.df['Date'].dt.to_period('M')

        monthly_totals = {}
        for period in sorted(self.df['YearMonth'].unique()):
            period_df = self.df[self.df['YearMonth'] == period]
            month_str = str(period)

            income = period_df[period_df['Type'] == 'Credit']['Amount'].sum()
            expense = period_df[period_df['Type'] == 'Debit']['Amount'].sum()
            net = income - expense

            monthly_totals[month_str] = {
                'income': income,
                'expense': expense,
                'net': net,
                'transaction_count': len(period_df)
            }

        self.analysis_results['monthly_totals'] = monthly_totals
        return monthly_totals

    def spending_by_category(self):
        """Analyze spending by category"""
        expense_df = self.df[self.df['Type'] == 'Debit'].copy()
        category_totals = expense_df.groupby('Category').agg({
            'Amount': ['sum', 'mean', 'count']
        }).round(2)

        category_totals.columns = ['Total', 'Average', 'Count']
        category_totals = category_totals.sort_values('Total', ascending=False)

        self.analysis_results['category_spending'] = category_totals
        return category_totals

    def spending_patterns(self):
        """Identify spending patterns"""
        self.df['DayOfWeek'] = self.df['Date'].dt.day_name()
        self.df['Month'] = self.df['Date'].dt.strftime('%B')

        expense_df = self.df[self.df['Type'] == 'Debit']

        patterns = {
            'by_day_of_week': expense_df.groupby('DayOfWeek')['Amount'].agg(['sum', 'count', 'mean']).round(2),
            'by_month': expense_df.groupby('Month')['Amount'].agg(['sum', 'count', 'mean']).round(2),
            'average_daily_expense': expense_df['Amount'].sum() / len(expense_df['Date'].unique()),
            'daily_statistics': {
                'min': expense_df['Amount'].min(),
                'max': expense_df['Amount'].max(),
                'mean': expense_df['Amount'].mean(),
                'median': expense_df['Amount'].median()
            }
        }

        self.analysis_results['patterns'] = patterns
        return patterns

    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "="*70)
        print("TRANSACTION ANALYSIS REPORT")
        print("="*70)

        print("\n1. DUPLICATE TRANSACTIONS")
        print("-"*70)
        duplicates = self.find_duplicate_transactions()
        if len(duplicates) > 0:
            print(f"Found {len(duplicates)} potential duplicate transaction(s):")
            print(duplicates.to_string(index=False))
        else:
            print("No duplicate transactions found.")

        print("\n2. RECURRING TRANSACTIONS (3+ occurrences)")
        print("-"*70)
        recurring = self.identify_recurring_transactions()
        if recurring:
            for desc, data in recurring.items():
                print(f"  • {desc}")
                print(f"    - Frequency: Every {data['interval_days']:.1f} days (~{data['count']} times)")
                print(f"    - Amount: ₹{data['amount']:.2f}")
                print(f"    - Total: ₹{data['total']:.2f}")
        else:
            print("No recurring transactions found.")

        print("\n3. MONTHLY SUMMARY")
        print("-"*70)
        monthly = self.calculate_monthly_totals()
        for month, data in monthly.items():
            print(f"  {month}:")
            print(f"    - Income:       ₹{data['income']:>10,.2f}")
            print(f"    - Expense:      ₹{data['expense']:>10,.2f}")
            print(f"    - Net:          ₹{data['net']:>10,.2f}")
            print(f"    - Transactions: {data['transaction_count']}")

        print("\n4. SPENDING BY CATEGORY")
        print("-"*70)
        category = self.spending_by_category()
        print(category.to_string())

        print("\n5. SPENDING PATTERNS")
        print("-"*70)
        patterns = self.spending_patterns()
        print("\n  Daily Spending Statistics:")
        for stat, value in patterns['daily_statistics'].items():
            print(f"    - {stat.capitalize()}: ₹{value:.2f}")

        avg_daily = patterns['average_daily_expense']
        print(f"    - Average Daily: ₹{avg_daily:.2f}")

        print("\n  Spending by Day of Week:")
        print(patterns['by_day_of_week'].to_string())

        print("\n" + "="*70)

    def export_analysis_to_excel(self, output_file='transaction_analysis.xlsx'):
        """Export analysis results to Excel file"""
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            self.df.to_excel(writer, sheet_name='Transactions', index=False)

            if 'duplicates' in self.analysis_results:
                duplicates = self.analysis_results['duplicates']
                if len(duplicates) > 0:
                    duplicates.to_excel(writer, sheet_name='Duplicates', index=False)

            if 'category_spending' in self.analysis_results:
                category = self.analysis_results['category_spending']
                category.to_excel(writer, sheet_name='By Category')

            if 'monthly_totals' in self.analysis_results:
                monthly_df = pd.DataFrame(self.analysis_results['monthly_totals']).T
                monthly_df.to_excel(writer, sheet_name='Monthly Summary')

        print(f"✓ Analysis exported to {output_file}")

    def get_summary(self):
        """Get quick summary of all analyses"""
        summary = {
            'total_transactions': len(self.df),
            'date_range': f"{self.df['Date'].min().date()} to {self.df['Date'].max().date()}",
            'total_income': self.df[self.df['Type'] == 'Credit']['Amount'].sum(),
            'total_expense': self.df[self.df['Type'] == 'Debit']['Amount'].sum(),
            'duplicate_count': len(self.analysis_results.get('duplicates', [])),
            'recurring_count': len(self.analysis_results.get('recurring', {}))
        }
        return summary


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
    else:
        excel_file = 'sample_transactions.xlsx'

    try:
        analyzer = TransactionAnalyzer(excel_file)
        analyzer.generate_report()
        analyzer.export_analysis_to_excel()

        print("\n" + "="*70)
        print("QUICK SUMMARY")
        print("="*70)
        summary = analyzer.get_summary()
        for key, value in summary.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

    except Exception as e:
        print(f"Error: {str(e)}")
