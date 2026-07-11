#!/usr/bin/env python3
"""
Transaction Analysis Application - Main Entry Point

This script provides a menu-driven interface for transaction analysis.
"""

import os
import sys
from transaction_analyzer import TransactionAnalyzer


def print_banner():
    """Print application banner"""
    print("\n" + "="*70)
    print(" "*15 + "TRANSACTION ANALYSIS APPLICATION")
    print("="*70)


def print_menu():
    """Print main menu"""
    print("\nSelect an option:")
    print("  1. Generate sample transaction data")
    print("  2. Analyze existing transactions")
    print("  3. Create visualizations")
    print("  4. Run complete analysis (1+2+3)")
    print("  5. Exit")
    print("-"*70)


def check_dependencies():
    """Check if required packages are installed"""
    required = ['pandas', 'openpyxl', 'matplotlib', 'seaborn', 'numpy']
    missing = []

    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        print("\n⚠ Missing required packages:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\nInstall with:")
        print(f"  pip install {' '.join(missing)}")
        return False

    return True


def generate_sample_data():
    """Generate sample transaction data"""
    print("\n📊 Generating sample transaction data...")
    try:
        from sample_transactions import generate_sample_transactions

        df = generate_sample_transactions()
        output_file = 'sample_transactions.xlsx'
        df.to_excel(output_file, index=False, sheet_name='Transactions')
        print(f"✓ Sample data created: {output_file}")
        print(f"  - Total transactions: {len(df)}")
        print(f"  - Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
        print(f"  - Total income: ₹{df[df['Type']=='Credit']['Amount'].sum():,.2f}")
        print(f"  - Total expense: ₹{df[df['Type']=='Debit']['Amount'].sum():,.2f}")
        return True
    except Exception as e:
        print(f"✗ Error generating sample data: {str(e)}")
        return False


def analyze_transactions(excel_file='sample_transactions.xlsx'):
    """Analyze transactions from Excel file"""
    if not os.path.exists(excel_file):
        print(f"\n✗ File not found: {excel_file}")
        excel_file = input("Enter Excel file path: ").strip()

        if not os.path.exists(excel_file):
            print(f"✗ File still not found: {excel_file}")
            return False

    print(f"\n📈 Analyzing transactions from {excel_file}...")

    try:
        analyzer = TransactionAnalyzer(excel_file)
        analyzer.generate_report()
        analyzer.export_analysis_to_excel()
        return True
    except Exception as e:
        print(f"✗ Error during analysis: {str(e)}")
        return False


def create_visualizations(excel_file='sample_transactions.xlsx'):
    """Create visualization charts"""
    if not os.path.exists(excel_file):
        print(f"\n✗ File not found: {excel_file}")
        return False

    print(f"\n📊 Creating visualizations...")

    try:
        from visualize_transactions import TransactionVisualizer

        visualizer = TransactionVisualizer(excel_file)
        visualizer.create_all_visualizations('transaction_analysis.png')
        visualizer.create_category_breakdown('category_breakdown.png')
        print("✓ Visualizations created successfully")
        return True
    except Exception as e:
        print(f"✗ Error creating visualizations: {str(e)}")
        return False


def run_complete_analysis():
    """Run complete analysis pipeline"""
    print("\n🚀 Running complete analysis pipeline...")

    # Step 1: Generate sample data
    if not generate_sample_data():
        return False

    # Step 2: Analyze
    if not analyze_transactions():
        return False

    # Step 3: Visualize
    if not create_visualizations():
        return False

    print("\n" + "="*70)
    print("✓ COMPLETE ANALYSIS FINISHED SUCCESSFULLY!")
    print("="*70)
    print("\nGenerated files:")
    print("  • sample_transactions.xlsx - Original transaction data")
    print("  • transaction_analysis.xlsx - Analysis results")
    print("  • transaction_analysis.png - Visual dashboard")
    print("  • category_breakdown.png - Category analysis")

    return True


def main():
    """Main application flow"""
    print_banner()

    # Check dependencies
    if not check_dependencies():
        print("\nPlease install missing packages and try again.")
        sys.exit(1)

    print("✓ All dependencies installed")

    while True:
        print_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            generate_sample_data()

        elif choice == '2':
            excel_file = input("\nEnter Excel file path (default: sample_transactions.xlsx): ").strip()
            if not excel_file:
                excel_file = 'sample_transactions.xlsx'
            analyze_transactions(excel_file)

        elif choice == '3':
            excel_file = input("\nEnter Excel file path (default: sample_transactions.xlsx): ").strip()
            if not excel_file:
                excel_file = 'sample_transactions.xlsx'
            create_visualizations(excel_file)

        elif choice == '4':
            run_complete_analysis()

        elif choice == '5':
            print("\n👋 Goodbye!")
            break

        else:
            print("✗ Invalid choice. Please enter 1-5.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        sys.exit(1)
