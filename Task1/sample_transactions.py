import pandas as pd
from datetime import datetime, timedelta
import random

def generate_sample_transactions():
    """Generate 3 months of sample transaction data"""

    categories = {
        'Personal': ['Groceries', 'Pharmacy', 'Haircut', 'Clothing', 'Electronics'],
        'Social': ['Restaurant', 'Movie', 'Coffee', 'Games', 'Entertainment'],
        'Official': ['Internet', 'Phone Bill', 'Rent', 'Office Supplies', 'Software']
    }

    transactions = []
    start_date = datetime.now() - timedelta(days=90)

    # Generate recurring transactions
    recurring_transactions = {
        'Rent': (5000, 'Official', 1),  # (amount, category, day of month)
        'Internet': (1500, 'Official', 15),
        'Phone Bill': (800, 'Official', 20),
        'Coffee': (300, 'Social', random.randint(1, 28)),
    }

    # Generate all transactions for 3 months
    current_date = start_date
    while current_date <= datetime.now():
        # Day of month
        day = current_date.day

        # Add recurring transactions
        for desc, (amount, cat, recur_day) in recurring_transactions.items():
            if day == recur_day:
                transactions.append({
                    'Date': current_date.strftime('%Y-%m-%d'),
                    'Description': desc,
                    'Amount': amount,
                    'Category': cat,
                    'Type': 'Debit'
                })

        # Add random transactions
        if random.random() > 0.6:  # 40% chance of additional transaction
            cat_type = random.choice(['Personal', 'Social', 'Official'])
            desc = random.choice(categories[cat_type])
            amount = random.randint(100, 2000)

            transactions.append({
                'Date': current_date.strftime('%Y-%m-%d'),
                'Description': desc,
                'Amount': amount,
                'Category': cat_type,
                'Type': 'Debit'
            })

        current_date += timedelta(days=1)

    # Add some income (credit transactions)
    salary_dates = [
        (start_date.replace(day=1), 50000),
        ((start_date + timedelta(days=30)).replace(day=1), 50000),
        ((start_date + timedelta(days=60)).replace(day=1), 50000),
    ]

    for date, amount in salary_dates:
        transactions.append({
            'Date': date.strftime('%Y-%m-%d'),
            'Description': 'Salary',
            'Amount': amount,
            'Category': 'Income',
            'Type': 'Credit'
        })

    # Add some duplicate transactions for testing
    if transactions:
        dup = transactions[10].copy()
        transactions.insert(11, dup)

    df = pd.DataFrame(transactions)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)

    return df

if __name__ == "__main__":
    df = generate_sample_transactions()
    df.to_excel('sample_transactions.xlsx', index=False, sheet_name='Transactions')
    print("Sample transactions file created: sample_transactions.xlsx")
    print(f"Total records: {len(df)}")
    print("\nFirst 10 records:")
    print(df.head(10))
