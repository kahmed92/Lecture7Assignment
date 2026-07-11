# How to Create Your Sample Transaction History

Complete guide to generate your personal transaction Excel file.

## 📋 What You'll Get

A realistic 3-month transaction history including:
- **Income**: Monthly salary (₹65,000)
- **Personal Expenses**: Groceries, pharmacy, clothing, haircut, personal care
- **Social Expenses**: Coffee, lunch, restaurants, movies, cafes
- **Official Expenses**: Rent, utilities, internet, phone, insurance, fuel

## 🚀 Quick Start (2 minutes)

### Step 1: Run the Script
```bash
python create_sample_excel.py
```

### Step 2: Check Your File
Look for `my_transaction_history.xlsx` in your project folder

### Step 3: Open in Excel
- Double-click the file to open
- View your colorful transaction data
- Analyze with the transaction analyzer!

## 📊 What's Inside the Excel File

### Columns in Your Transaction History

| Column | Description | Example |
|--------|-------------|---------|
| **Date** | Transaction date | 2024-04-01 |
| **Day** | Day of week | Monday |
| **Description** | What you bought | Coffee Shop |
| **Category** | Type of expense | Social |
| **Type** | Credit or Debit | Debit |
| **Amount** | How much (₹) | 250.00 |
| **Balance** | Running balance | 50,000.00 |

### Color Coding

Different colors for different categories:
- 🟢 **Green** = Income (Salary)
- 🟡 **Yellow** = Personal (Groceries, clothing, pharmacy)
- 🔵 **Blue** = Social (Coffee, movies, restaurants)
- 🟦 **Light Green** = Official (Rent, utilities, bills)

## 💰 Sample Data Breakdown

### Monthly Income
```
Salary (Monthly):  ₹65,000
Total (3 months):  ₹195,000
```

### Monthly Expenses
```
Personal:   ₹8,000-10,000  (Groceries, clothes, pharmacy)
Social:     ₹6,000-8,000   (Coffee, food, movies)
Official:  ₹22,000-25,000  (Rent, utilities, bills, insurance)
           ─────────────────
Total:     ₹36,000-43,000  per month
```

### Expense Breakdown
```
Personal:   ~20% (Groceries, household)
Social:     ~18% (Entertainment, dining)
Official:   ~62% (Fixed costs - rent, bills)
```

## 📅 Transaction Patterns (Realistic)

### Weekly Patterns
- **Monday-Friday**: Office supplies, transport, coffee
- **Wednesday**: Lunch with friends
- **Saturday**: Groceries shopping, restaurant dinner
- **Sunday**: Fuel for car

### Monthly Patterns
- **1st**: Salary deposit, rent payment, software subscription
- **5th**: Internet bill
- **10th**: Electricity bill
- **15th**: Mobile phone bill, haircut
- **20th**: Insurance premium
- **Various**: Coffee (2-3 times/week), occasional shopping

## 🎯 Total Transactions

```
Over 3 months:
• Total transactions: 180+
• Average daily: 2-3 transactions
• Recurring payments: 6
• One-time purchases: 80+
```

## 📈 Monthly Summary

### Month 1 (April)
```
Income:      ₹65,000
Expenses:    ₹42,500
Savings:     ₹22,500
```

### Month 2 (May)
```
Income:      ₹65,000
Expenses:    ₹39,800
Savings:     ₹25,200
```

### Month 3 (June)
```
Income:      ₹65,000
Expenses:    ₹38,200
Savings:     ₹26,800
```

## ✨ Excel Features

### Formatting
- ✓ Color-coded by category
- ✓ Professional fonts and borders
- ✓ Currency formatting (₹)
- ✓ Frozen header row (scroll while seeing headers)
- ✓ Optimized column widths

### Easy to Use
- ✓ Sorted by date
- ✓ Running balance column
- ✓ Clear descriptions
- ✓ Consistent categorization

## 🔄 How to Use the Data

### Option 1: Analyze with Built-in Tool
```bash
# After creating the file, analyze it
python transaction_analyzer.py my_transaction_history.xlsx
```

### Option 2: Manual Analysis
1. Open file in Excel
2. Use Excel functions to:
   - Sum by category
   - Create pivot tables
   - Generate charts
   - Filter by date range

### Option 3: Customize
1. Edit the Excel file directly
2. Add your own transactions
3. Change amounts to match your spending
4. Adjust categories as needed

## 🎨 Sample Entries

Here are some realistic transactions you'll find:

```
Date       | Description           | Category | Type   | Amount
-----------|----------------------|----------|--------|--------
2024-04-01 | Salary - Monthly      | Income   | Credit | 65,000
2024-04-01 | Rent - Monthly        | Official | Debit  | 15,000
2024-04-05 | Groceries Shopping    | Personal | Debit  | 2,500
2024-04-06 | Coffee Shop           | Social   | Debit  | 250
2024-04-10 | Electricity Bill       | Official | Debit  | 2,000
2024-04-12 | Restaurant Dinner     | Social   | Debit  | 1,500
2024-04-15 | Mobile Phone Bill     | Official | Debit  | 1,200
2024-04-20 | Insurance - Health    | Official | Debit  | 3,500
2024-04-25 | Clothing - Jeans      | Personal | Debit  | 2,500
```

## 📊 What You Can Do Next

### Analyze
```bash
python transaction_analyzer.py my_transaction_history.xlsx
```
Generates:
- Duplicate detection report
- Recurring payment analysis
- Monthly summary
- Category breakdown
- Spending patterns
- Visual dashboard

### Visualize
```bash
python visualize_transactions.py my_transaction_history.xlsx
```
Creates:
- 6-panel dashboard
- Category breakdown charts
- Spending trends

### Export
- Excel report (multi-sheet)
- PNG visualizations
- Console summary

## 🎓 Learning Opportunities

This sample data is great for:
- Learning Excel formulas
- Understanding data analysis
- Creating pivot tables
- Building charts
- Tracking personal finances
- Practicing SQL queries
- Learning Python data analysis

## 🔧 Customization Options

### Edit in Excel
1. Open `my_transaction_history.xlsx`
2. Change amounts to match your actual spending
3. Add or remove transactions
4. Adjust dates
5. Save the file

### Edit the Python Script
Edit `create_sample_excel.py` to:
- Change salary amount
- Adjust expense amounts
- Change date ranges
- Add new categories
- Modify frequencies

### Modify Both
1. Create initial file with script
2. Open in Excel
3. Make manual adjustments
4. Use for analysis

## ❓ FAQ

### Q: Can I modify the generated file?
**A**: Yes! The Excel file is fully editable. Change any values you want.

### Q: How do I add my own transactions?
**A**: Open the file in Excel and add new rows with your data.

### Q: Can I change the date range?
**A**: Edit `create_sample_excel.py` and change the start_date variable.

### Q: Can I use this as a template?
**A**: Yes! Delete all rows and add your own transaction history.

### Q: How do I analyze the file?
**A**: Run: `python transaction_analyzer.py my_transaction_history.xlsx`

### Q: Can I create multiple files?
**A**: Yes! Just rename the file each time before running the script again.

## 📋 File Details

**File Name**: `my_transaction_history.xlsx`
**Sheet Name**: `Transactions`
**Date Range**: Last 90 days
**Total Rows**: 180+ transactions
**Columns**: 7 (Date, Day, Description, Category, Type, Amount, Balance)
**Format**: Excel 2007+ (.xlsx)
**Size**: ~100-150 KB

## ✅ Verification Checklist

After running the script:
- [ ] File `my_transaction_history.xlsx` exists
- [ ] File opens in Excel without errors
- [ ] Data is properly formatted with colors
- [ ] Dates are in sequence
- [ ] Amounts look reasonable
- [ ] Categories are consistent
- [ ] Balance column calculates correctly

## 🎁 Bonus: Pre-built Duplicates

The script includes one realistic duplicate transaction for testing:
- Repeated Coffee Shop entry (simulating accidental duplicate charge)
- Perfect for testing the duplicate detection feature!

## 📞 Support

**Script not working?**
1. Ensure Python 3.7+ is installed
2. Run: `pip install -r requirements.txt`
3. Try again: `python create_sample_excel.py`

**Excel file issues?**
1. Close the file if it's open
2. Delete the file
3. Run the script again to recreate

**Want to see what the analyzer finds?**
```bash
python transaction_analyzer.py my_transaction_history.xlsx
```

## 🚀 Next Steps

1. **Create the file**
   ```bash
   python create_sample_excel.py
   ```

2. **View the file**
   - Open `my_transaction_history.xlsx` in Excel

3. **Analyze the data**
   ```bash
   python transaction_analyzer.py my_transaction_history.xlsx
   ```

4. **Explore the visualizations**
   ```bash
   python visualize_transactions.py my_transaction_history.xlsx
   ```

5. **Read the results**
   - Check `transaction_analysis.xlsx`
   - View `transaction_analysis.png`
   - Review console report

---

**Ready? Run this command now:**
```bash
python create_sample_excel.py
```

**Happy analyzing!** 🎉

---

*Last Updated: July 12, 2024*
