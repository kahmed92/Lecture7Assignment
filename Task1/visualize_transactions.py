import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class TransactionVisualizer:
    """Create visualizations for transaction analysis"""

    def __init__(self, excel_file):
        self.df = pd.read_excel(excel_file, sheet_name='Transactions')
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (15, 12)

    def create_all_visualizations(self, output_file='transaction_analysis.png'):
        """Create a comprehensive visualization dashboard"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle('Transaction Analysis Dashboard', fontsize=16, fontweight='bold')

        # 1. Spending by Category
        expense_df = self.df[self.df['Type'] == 'Debit']
        category_totals = expense_df.groupby('Category')['Amount'].sum().sort_values(ascending=True)
        axes[0, 0].barh(category_totals.index, category_totals.values, color='steelblue')
        axes[0, 0].set_title('Total Spending by Category', fontweight='bold')
        axes[0, 0].set_xlabel('Amount (₹)')
        for i, v in enumerate(category_totals.values):
            axes[0, 0].text(v + 100, i, f'₹{v:.0f}', va='center')

        # 2. Monthly Income vs Expense
        self.df['YearMonth'] = self.df['Date'].dt.to_period('M')
        monthly_data = self.df.groupby('YearMonth').apply(
            lambda x: pd.Series({
                'Income': x[x['Type'] == 'Credit']['Amount'].sum(),
                'Expense': x[x['Type'] == 'Debit']['Amount'].sum()
            })
        )
        monthly_data.plot(kind='bar', ax=axes[0, 1], color=['green', 'red'])
        axes[0, 1].set_title('Monthly Income vs Expense', fontweight='bold')
        axes[0, 1].set_ylabel('Amount (₹)')
        axes[0, 1].set_xlabel('Month')
        axes[0, 1].legend(['Income', 'Expense'])
        axes[0, 1].tick_params(axis='x', rotation=45)

        # 3. Daily Spending Trend
        daily_expense = expense_df.groupby(expense_df['Date'].dt.date)['Amount'].sum()
        axes[0, 2].plot(daily_expense.index, daily_expense.values, marker='o', linestyle='-', color='coral')
        axes[0, 2].fill_between(range(len(daily_expense)), daily_expense.values, alpha=0.3, color='coral')
        axes[0, 2].set_title('Daily Spending Trend', fontweight='bold')
        axes[0, 2].set_ylabel('Amount (₹)')
        axes[0, 2].set_xlabel('Date')
        axes[0, 2].tick_params(axis='x', rotation=45)
        axes[0, 2].grid(True, alpha=0.3)

        # 4. Spending Distribution (Box Plot)
        expense_df.boxplot(column='Amount', by='Category', ax=axes[1, 0])
        axes[1, 0].set_title('Spending Distribution by Category', fontweight='bold')
        axes[1, 0].set_xlabel('Category')
        axes[1, 0].set_ylabel('Amount (₹)')
        plt.sca(axes[1, 0])
        plt.xticks(rotation=45)

        # 5. Top 10 Transactions
        top_transactions = self.df.nlargest(10, 'Amount')[['Date', 'Description', 'Amount']].copy()
        top_transactions['Date'] = top_transactions['Date'].dt.strftime('%Y-%m-%d')
        colors = ['green' if self.df.iloc[idx]['Type'] == 'Credit' else 'red'
                  for idx in self.df.nlargest(10, 'Amount').index]
        axes[1, 1].barh(range(len(top_transactions)), top_transactions['Amount'].values, color=colors)
        axes[1, 1].set_yticks(range(len(top_transactions)))
        axes[1, 1].set_yticklabels([f"{row['Description'][:15]}" for _, row in top_transactions.iterrows()], fontsize=8)
        axes[1, 1].set_title('Top 10 Transactions', fontweight='bold')
        axes[1, 1].set_xlabel('Amount (₹)')
        axes[1, 1].invert_yaxis()

        # 6. Category Pie Chart
        category_totals = expense_df.groupby('Category')['Amount'].sum()
        colors_pie = plt.cm.Set3(range(len(category_totals)))
        wedges, texts, autotexts = axes[1, 2].pie(category_totals.values, labels=category_totals.index,
                                                    autopct='%1.1f%%', colors=colors_pie, startangle=90)
        axes[1, 2].set_title('Expense Distribution', fontweight='bold')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Visualization saved to {output_file}")
        plt.show()

    def create_category_breakdown(self, output_file='category_breakdown.png'):
        """Create detailed category breakdown"""
        expense_df = self.df[self.df['Type'] == 'Debit']
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Count of transactions by category
        category_counts = expense_df.groupby('Category').size()
        axes[0].bar(category_counts.index, category_counts.values, color='skyblue')
        axes[0].set_title('Number of Transactions by Category', fontweight='bold')
        axes[0].set_ylabel('Count')
        axes[0].tick_params(axis='x', rotation=45)

        # Average transaction amount by category
        category_avg = expense_df.groupby('Category')['Amount'].mean()
        axes[1].bar(category_avg.index, category_avg.values, color='lightcoral')
        axes[1].set_title('Average Transaction Amount by Category', fontweight='bold')
        axes[1].set_ylabel('Amount (₹)')
        axes[1].tick_params(axis='x', rotation=45)

        for ax in axes:
            for i, (idx, val) in enumerate(zip(ax.get_xticklabels(), ax.patches)):
                height = val.get_height()
                ax.text(val.get_x() + val.get_width()/2., height,
                       f'{height:.0f}', ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Category breakdown saved to {output_file}")
        plt.show()


if __name__ == "__main__":
    import sys

    excel_file = sys.argv[1] if len(sys.argv) > 1 else 'sample_transactions.xlsx'

    try:
        visualizer = TransactionVisualizer(excel_file)
        visualizer.create_all_visualizations()
        visualizer.create_category_breakdown()
    except Exception as e:
        print(f"Error: {str(e)}")
