"""
Simple Transaction Excel Generator
Creates 3 months of realistic transaction data
"""

import pandas as pd
from datetime import datetime, timedelta

def create_transactions():
    """Generate 90 days of realistic transaction data"""

    data = []
    start = datetime(2024, 4, 1)

    # Add transactions manually for clarity
    transactions = [
        # April 1st
        ("2024-04-01", "Monday", "Salary - Monthly", "Income", "Credit", 65000),
        ("2024-04-01", "Monday", "Rent - Monthly", "Official", "Debit", 15000),
        ("2024-04-01", "Monday", "Software Subscription", "Official", "Debit", 500),

        # April 3rd
        ("2024-04-03", "Wednesday", "Coffee Shop", "Social", "Debit", 250),

        # April 5th
        ("2024-04-05", "Friday", "Internet Bill", "Official", "Debit", 1500),

        # April 6th
        ("2024-04-06", "Saturday", "Groceries - Weekly", "Personal", "Debit", 2500),
        ("2024-04-06", "Saturday", "Vegetables & Fruits", "Personal", "Debit", 600),
        ("2024-04-06", "Saturday", "Restaurant Dinner", "Social", "Debit", 1500),

        # April 8th
        ("2024-04-08", "Monday", "Coffee Shop", "Social", "Debit", 250),

        # April 10th
        ("2024-04-10", "Wednesday", "Electricity Bill", "Official", "Debit", 2000),
        ("2024-04-10", "Wednesday", "Lunch with Friends", "Social", "Debit", 600),

        # April 12th
        ("2024-04-12", "Friday", "Movie Tickets", "Social", "Debit", 400),

        # April 15th
        ("2024-04-15", "Monday", "Mobile Phone Bill", "Official", "Debit", 1200),
        ("2024-04-15", "Monday", "Haircut", "Personal", "Debit", 300),

        # April 17th
        ("2024-04-17", "Wednesday", "Coffee Shop", "Social", "Debit", 250),

        # April 20th
        ("2024-04-20", "Saturday", "Insurance - Health", "Official", "Debit", 3500),
        ("2024-04-20", "Saturday", "Clothing - Jeans", "Personal", "Debit", 2500),

        # April 21st
        ("2024-04-21", "Sunday", "Transport - Fuel", "Official", "Debit", 2000),

        # April 24th
        ("2024-04-24", "Wednesday", "Coffee Shop", "Social", "Debit", 250),
        ("2024-04-24", "Wednesday", "Lunch with Friends", "Social", "Debit", 600),

        # April 27th
        ("2024-04-27", "Saturday", "Groceries - Weekly", "Personal", "Debit", 2500),
        ("2024-04-27", "Saturday", "Vegetables & Fruits", "Personal", "Debit", 600),

        # April 28th
        ("2024-04-28", "Sunday", "Transport - Fuel", "Official", "Debit", 2000),

        # May 1st
        ("2024-05-01", "Wednesday", "Salary - Monthly", "Income", "Credit", 65000),
        ("2024-05-01", "Wednesday", "Rent - Monthly", "Official", "Debit", 15000),
        ("2024-05-01", "Wednesday", "Software Subscription", "Official", "Debit", 500),

        # May 3rd
        ("2024-05-03", "Friday", "Internet Bill", "Official", "Debit", 1500),
        ("2024-05-03", "Friday", "Coffee Shop", "Social", "Debit", 250),

        # May 4th
        ("2024-05-04", "Saturday", "Groceries - Weekly", "Personal", "Debit", 2500),
        ("2024-05-04", "Saturday", "Vegetables & Fruits", "Personal", "Debit", 600),

        # May 5th
        ("2024-05-05", "Sunday", "Transport - Fuel", "Official", "Debit", 2000),

        # May 8th
        ("2024-05-08", "Wednesday", "Electricity Bill", "Official", "Debit", 2000),
        ("2024-05-08", "Wednesday", "Lunch with Friends", "Social", "Debit", 600),
        ("2024-05-08", "Wednesday", "Coffee Shop", "Social", "Debit", 250),

        # May 11th
        ("2024-05-11", "Saturday", "Restaurant Dinner", "Social", "Debit", 1500),
        ("2024-05-11", "Saturday", "Movie Tickets", "Social", "Debit", 400),

        # May 12th
        ("2024-05-12", "Sunday", "Transport - Fuel", "Official", "Debit", 2000),

        # May 15th
        ("2024-05-15", "Wednesday", "Mobile Phone Bill", "Official", "Debit", 1200),
        ("2024-05-15", "Wednesday", "Lunch with Friends", "Social", "Debit", 600),
        ("2024-05-15", "Wednesday", "Coffee Shop", "Social", "Debit", 250),

        # May 18th
        ("2024-05-18", "Saturday", "Groceries - Weekly", "Personal", "Debit", 2500),
        ("2024-05-18", "Saturday", "Vegetables & Fruits", "Personal", "Debit", 600),
        ("2024-05-18", "Saturday", "Pharmacy - Medicine", "Personal", "Debit", 450),

        # May 19th
        ("2024-05-19", "Sunday", "Transport - Fuel", "Official", "Debit", 2000),

        # May 20th
        ("2024-05-20", "Monday", "Insurance - Health", "Official", "Debit", 3500),

        # May 22nd
        ("2024-05-22", "Wednesday", "Coffee Shop", "Social", "Debit", 250),

        # May 25th
        ("2024-05-25", "Saturday", "Clothing - T-Shirt", "Personal", "Debit", 1200),
        ("2024-05-25", "Saturday", "Restaurant Dinner", "Social", "Debit", 1500),

        # May 26th
        ("2024-05-26", "Sunday", "Transport - Fuel", "Official", "Debit", 2000),

        # June 1st
        ("2024-06-01", "Saturday", "Salary - Monthly", "Income", "Credit", 65000),
        ("2024-06-01", "Saturday", "Rent - Monthly", "Official", "Debit", 15000),
        ("2024-06-01", "Saturday", "Software Subscription", "Official", "Debit", 500),

        # June 3rd
        ("2024-06-03", "Monday", "Internet Bill", "Official", "Debit", 1500),
        ("2024-06-03", "Monday", "Coffee Shop", "Social", "Debit", 250),

        # June 5th
        ("2024-06-05", "Wednesday", "Groceries - Weekly", "Personal", "Debit", 2500),
        ("2024-06-05", "Wednesday", "Vegetables & Fruits", "Personal", "Debit", 600),
        ("2024-06-05", "Wednesday", "Lunch with Friends", "Social", "Debit", 600),

        # June 8th
        ("2024-06-08", "Saturday", "Electricity Bill", "Official", "Debit", 2000),
        ("2024-06-08", "Saturday", "Restaurant Dinner", "Social", "Debit", 1500),

        # June 9th
        ("2024-06-09", "Sunday", "Transport - Fuel", "Official", "Debit", 2000),

        # June 12th
        ("2024-06-12", "Wednesday", "Movie Tickets", "Social", "Debit", 400),
        ("2024-06-12", "Wednesday", "Coffee Shop", "Social", "Debit", 250),

        # June 15th
        ("2024-06-15", "Saturday", "Mobile Phone Bill", "Official", "Debit", 1200),
        ("2024-06-15", "Saturday", "Haircut", "Personal", "Debit", 300),
        ("2024-06-15", "Saturday", "Groceries - Weekly", "Personal", "Debit", 2500),
        ("2024-06-15", "Saturday", "Vegetables & Fruits", "Personal", "Debit", 600),

        # June 16th
        ("2024-06-16", "Sunday", "Transport - Fuel", "Official", "Debit", 2000),

        # June 19th
        ("2024-06-19", "Wednesday", "Lunch with Friends", "Social", "Debit", 600),
        ("2024-06-19", "Wednesday", "Coffee Shop", "Social", "Debit", 250),

        # June 20th
        ("2024-06-20", "Thursday", "Insurance - Health", "Official", "Debit", 3500),

        # June 22nd
        ("2024-06-22", "Saturday", "Restaurant Dinner", "Social", "Debit", 1500),
        ("2024-06-22", "Saturday", "Personal Care Products", "Personal", "Debit", 800),

        # June 23rd
        ("2024-06-23", "Sunday", "Transport - Fuel", "Official", "Debit", 2000),

        # June 26th
        ("2024-06-26", "Wednesday", "Coffee Shop", "Social", "Debit", 250),

        # June 29th
        ("2024-06-29", "Saturday", "Groceries - Weekly", "Personal", "Debit", 2500),
        ("2024-06-29", "Saturday", "Vegetables & Fruits", "Personal", "Debit", 600),

        # June 30th
        ("2024-06-30", "Sunday", "Transport - Fuel", "Official", "Debit", 2000),
    ]

    # Create DataFrame
    df = pd.DataFrame(transactions, columns=['Date', 'Day', 'Description', 'Category', 'Type', 'Amount'])
    df['Date'] = pd.to_datetime(df['Date'])

    # Calculate balance
    balance = 0
    balances = []
    for idx, row in df.iterrows():
        if row['Type'] == 'Credit':
            balance += row['Amount']
        else:
            balance -= row['Amount']
        balances.append(balance)

    df['Balance'] = balances

    return df


def main():
    print("\n" + "="*70)
    print("📊 Creating Sample Transaction History")
    print("="*70 + "\n")

    print("1. Generating transactions...")
    df = create_transactions()
    print(f"   ✓ Generated {len(df)} transactions")
    print(f"   ✓ Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")

    # Save to Excel
    output_file = 'my_transaction_history.xlsx'
    print(f"\n2. Saving to Excel...")
    df.to_excel(output_file, index=False, sheet_name='Transactions')
    print(f"   ✓ File created: {output_file}")

    # Calculate statistics
    print(f"\n3. Summary Statistics:")
    print(f"   {'='*70}")

    credit = df[df['Type'] == 'Credit']['Amount'].sum()
    debit = df[df['Type'] == 'Debit']['Amount'].sum()

    print(f"   Total Income:              ₹{credit:>12,.2f}")
    print(f"   Total Expenses:            ₹{debit:>12,.2f}")
    print(f"   Net Income:                ₹{credit - debit:>12,.2f}")
    print(f"   {'='*70}")

    print(f"\n   Expenses by Category:")
    for category in ['Personal', 'Social', 'Official']:
        cat_df = df[(df['Category'] == category) & (df['Type'] == 'Debit')]
        amount = cat_df['Amount'].sum()
        count = len(cat_df)
        pct = (amount / debit * 100) if debit > 0 else 0
        print(f"   • {category:<15} ₹{amount:>10,.2f} ({count:>2} trans, {pct:>5.1f}%)")

    print(f"\n   Transactions by Day:")
    day_counts = df['Day'].value_counts().sort_values(ascending=False)
    for day, count in day_counts.items():
        print(f"   • {day:<12} {count:>3} transactions")

    print(f"\n{'='*70}")
    print("✅ SUCCESS! Your transaction history is ready!")
    print(f"   File: {output_file}")
    print(f"   Transactions: {len(df)}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
        print("Troubleshooting:")
        print("1. Install pandas: pip install pandas openpyxl")
        print("2. Make sure you're in the correct directory")
        print("3. Check that Python 3.7+ is installed")
