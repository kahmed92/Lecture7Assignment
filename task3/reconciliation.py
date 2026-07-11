#!/usr/bin/env python3
"""
Payment Reconciliation Script
Reconciles expected payments with actual payment records to identify discrepancies.
"""

import csv
from difflib import SequenceMatcher
from datetime import datetime
from collections import defaultdict

class PaymentReconciler:
    def __init__(self, expected_file, actual_file, fuzzy_threshold=0.7):
        self.expected_file = expected_file
        self.actual_file = actual_file
        self.fuzzy_threshold = fuzzy_threshold
        self.expected_payments = []
        self.actual_payments = []
        self.ambiguity_rules = {
            "M. Chen": "Michael Chen",
            "E. Davis": "Emma Davis",
            "Unknown Donor": "UNMATCHED",
        }

    def load_files(self):
        """Load expected and actual payment records from CSV files."""
        with open(self.expected_file, 'r') as f:
            reader = csv.DictReader(f)
            self.expected_payments = list(reader)

        with open(self.actual_file, 'r') as f:
            reader = csv.DictReader(f)
            self.actual_payments = list(reader)

    def fuzzy_match(self, name1, name2):
        """Calculate similarity between two names."""
        name1_lower = name1.lower().strip()
        name2_lower = name2.lower().strip()
        return SequenceMatcher(None, name1_lower, name2_lower).ratio()

    def resolve_name(self, payer_name):
        """Resolve ambiguous payer names using predefined rules."""
        if payer_name in self.ambiguity_rules:
            return self.ambiguity_rules[payer_name]

        # Fuzzy match against expected names
        for expected_payment in self.expected_payments:
            expected_name = expected_payment['Name']
            similarity = self.fuzzy_match(payer_name, expected_name)
            if similarity >= self.fuzzy_threshold:
                return expected_name

        return payer_name

    def reconcile(self):
        """Perform reconciliation and identify discrepancies."""
        self.load_files()

        results = {
            'matched': [],
            'unmatched_expected': [],
            'unmatched_actual': [],
            'duplicates': [],
            'amount_mismatches': [],
            'extra_payments': [],
            'follow_up_list': []
        }

        # Create dictionaries for tracking
        expected_dict = {}
        for exp in self.expected_payments:
            name = exp['Name']
            amount = float(exp['Amount'])
            if name not in expected_dict:
                expected_dict[name] = {'count': 0, 'total': 0, 'entries': []}
            expected_dict[name]['total'] += amount
            expected_dict[name]['count'] += 1
            expected_dict[name]['entries'].append(exp)

        actual_dict = defaultdict(list)
        for act in self.actual_payments:
            resolved_name = self.resolve_name(act['Payer Name'])
            actual_dict[resolved_name].append(act)

        # Match payments
        matched_actual = set()

        for name in expected_dict:
            expected_amount = expected_dict[name]['total']

            if name in actual_dict:
                actual_records = actual_dict[name]
                actual_total = sum(float(r['Amount']) for r in actual_records)

                # Check for duplicates
                if len(actual_records) > 1 and actual_total > expected_amount:
                    for i, record in enumerate(actual_records):
                        results['duplicates'].append({
                            'name': name,
                            'amount': record['Amount'],
                            'date': record['Date'],
                            'notes': record['Reference/Notes'],
                            'index': i
                        })

                # Check amount mismatch
                if abs(actual_total - expected_amount) > 0.01:  # Account for rounding
                    results['amount_mismatches'].append({
                        'name': name,
                        'expected': expected_amount,
                        'actual': actual_total,
                        'difference': actual_total - expected_amount
                    })
                else:
                    results['matched'].append({
                        'name': name,
                        'amount': expected_amount,
                        'records': len(actual_records)
                    })

                # Mark as matched
                for record in actual_records:
                    matched_actual.add(tuple(record.items()))
            else:
                results['unmatched_expected'].append({
                    'name': name,
                    'amount': expected_amount
                })

        # Find unmatched actual payments
        for name, records in actual_dict.items():
            for record in records:
                if tuple(record.items()) not in matched_actual:
                    # Check if it's an unmatched expected payment that was found
                    found = False
                    for exp_name in expected_dict:
                        if self.fuzzy_match(name, exp_name) >= self.fuzzy_threshold:
                            found = True
                            break

                    if not found or name not in expected_dict:
                        results['extra_payments'].append({
                            'name': name,
                            'amount': record['Amount'],
                            'date': record['Date'],
                            'method': record['Payment Method'],
                            'notes': record['Reference/Notes']
                        })

        # Generate follow-up list
        for item in results['unmatched_expected']:
            results['follow_up_list'].append({
                'type': 'MISSING_PAYMENT',
                'name': item['name'],
                'amount': item['amount'],
                'action': f"Contact {item['name']} for payment of ${item['amount']}"
            })

        for item in results['amount_mismatches']:
            results['follow_up_list'].append({
                'type': 'AMOUNT_MISMATCH',
                'name': item['name'],
                'amount': item['expected'],
                'action': f"Verify payment for {item['name']}: Expected ${item['expected']}, Received ${item['actual']} (Diff: ${item['difference']:.2f})"
            })

        for item in results['duplicates']:
            results['follow_up_list'].append({
                'type': 'DUPLICATE',
                'name': item['name'],
                'amount': item['amount'],
                'action': f"Review duplicate entry for {item['name']} on {item['date']} (${item['amount']}) - {item['notes']}"
            })

        return results

    def calculate_totals(self):
        """Calculate total expected and actual amounts."""
        total_expected = sum(float(p['Amount']) for p in self.expected_payments)
        total_actual = sum(float(p['Amount']) for p in self.actual_payments)
        return total_expected, total_actual

    def print_report(self, results):
        """Print a formatted reconciliation report."""
        total_expected, total_actual = self.calculate_totals()

        print("\n" + "="*80)
        print("PAYMENT RECONCILIATION REPORT")
        print("="*80)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Summary
        print("SUMMARY")
        print("-" * 80)
        print(f"Total Expected: ${total_expected:,.2f}")
        print(f"Total Recorded: ${total_actual:,.2f}")
        print(f"Discrepancy:    ${total_actual - total_expected:+,.2f}")
        print()

        # Matched Payments
        print("MATCHED PAYMENTS ({})".format(len(results['matched'])))
        print("-" * 80)
        for item in results['matched']:
            print(f"  ✓ {item['name']:.<40} ${item['amount']:>10,.2f}")
        print()

        # Unmatched Expected
        if results['unmatched_expected']:
            print("MISSING PAYMENTS ({})".format(len(results['unmatched_expected'])))
            print("-" * 80)
            for item in results['unmatched_expected']:
                print(f"  ✗ {item['name']:.<40} ${item['amount']:>10,.2f}")
            print()

        # Duplicates
        if results['duplicates']:
            print("DUPLICATE ENTRIES ({})".format(len(results['duplicates'])))
            print("-" * 80)
            for item in results['duplicates']:
                print(f"  ⚠ {item['name']:.<30} ${item['amount']:>10} on {item['date']}")
                print(f"     Notes: {item['notes']}")
            print()

        # Amount Mismatches
        if results['amount_mismatches']:
            print("AMOUNT MISMATCHES ({})".format(len(results['amount_mismatches'])))
            print("-" * 80)
            for item in results['amount_mismatches']:
                print(f"  {item['name']:.<30}")
                print(f"    Expected: ${item['expected']:>10,.2f}  |  Received: ${item['actual']:>10,.2f}  |  Diff: ${item['difference']:+10,.2f}")
            print()

        # Extra/Unmatched Actual
        if results['extra_payments']:
            print("EXTRA/UNIDENTIFIED PAYMENTS ({})".format(len(results['extra_payments'])))
            print("-" * 80)
            for item in results['extra_payments']:
                print(f"  {item['name']:.<30} ${item['amount']:>10} ({item['method']})")
                print(f"    Date: {item['date']}  |  Notes: {item['notes']}")
            print()

        # Follow-up List
        print("FOLLOW-UP REQUIRED ({})".format(len(results['follow_up_list'])))
        print("-" * 80)
        for i, item in enumerate(results['follow_up_list'], 1):
            print(f"  {i}. [{item['type']:.<15}] {item['action']}")
        print()

        print("="*80)
        print("END OF REPORT")
        print("="*80)


if __name__ == "__main__":
    reconciler = PaymentReconciler(
        expected_file="expected_payments.csv",
        actual_file="payment_records.csv",
        fuzzy_threshold=0.7
    )

    results = reconciler.reconcile()
    reconciler.print_report(results)
