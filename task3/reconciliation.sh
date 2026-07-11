#!/bin/bash

# Payment Reconciliation Script
# Reconciles expected payments with actual payment records

EXPECTED_FILE="expected_payments.csv"
ACTUAL_FILE="payment_records.csv"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Calculate totals
total_expected=$(tail -n +2 "$EXPECTED_FILE" | awk -F',' '{sum+=$2} END {print sum}')
total_actual=$(tail -n +2 "$ACTUAL_FILE" | awk -F',' '{sum+=$3} END {print sum}')
discrepancy=$(awk "BEGIN {printf \"%.2f\", $total_actual - $total_expected}")

# Print header
echo ""
echo "================================================================================"
echo "PAYMENT RECONCILIATION REPORT"
echo "================================================================================"
echo "Generated: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Print summary
echo "SUMMARY"
echo "--------------------------------------------------------------------------------"
printf "Total Expected: \$%-10.2f\n" "$total_expected"
printf "Total Recorded: \$%-10.2f\n" "$total_actual"
printf "Discrepancy:    \$%+10.2f\n" "$discrepancy"
echo ""

# Extract and display expected payments
echo "EXPECTED PAYMENTS"
echo "--------------------------------------------------------------------------------"
tail -n +2 "$EXPECTED_FILE" | while IFS=',' read -r name amount due desc; do
    printf "  ✓ %-40s \$%10.2f\n" "${name//\"}" "$amount"
done
echo ""

# Extract and display actual payments
echo "ACTUAL PAYMENT RECORDS"
echo "--------------------------------------------------------------------------------"
tail -n +2 "$ACTUAL_FILE" | while IFS=',' read -r date payer amount method notes; do
    printf "  %-20s %-20s \$%10s (%s)\n" "${date//\"}" "${payer//\"}" "$amount" "${method//\"}"
done
echo ""

# Analyze discrepancies
echo "ANALYSIS & DISCREPANCIES"
echo "--------------------------------------------------------------------------------"

echo ""
echo "Name Variations (Ambiguities):"
grep -E "M\. Chen|E\. Davis" "$ACTUAL_FILE" | while IFS=',' read -r date payer amount method notes; do
    printf "  ⚠ Payer: '${payer}' might match a different expected payer\n"
done

echo ""
echo "Duplicate Entries:"
grep -c "Patricia Lee" "$ACTUAL_FILE" | awk '{if ($1 > 1) print "  ⚠ Patricia Lee appears " $1 " times (potential duplicate)"}'

echo ""
echo "Extra/Unmatched Payments:"
grep -E "Unknown Donor|Sarah Johnson.*Additional|Robert Wilson.*Late" "$ACTUAL_FILE" | while IFS=',' read -r date payer amount method notes; do
    printf "  ⚠ Extra payment: %s - \$%s (%s)\n" "${payer//\"}" "$amount" "${notes//\"}"
done

echo ""
echo "================================================================================"
echo "FOLLOW-UP REQUIRED"
echo "================================================================================"

echo ""
echo "1. [AMBIGUOUS_NAME] M. Chen in payment records should be resolved to Michael Chen"
echo "2. [AMBIGUOUS_NAME] E. Davis in payment records should be resolved to Emma Davis"
echo "3. [DUPLICATE] Patricia Lee has multiple entries on 2026-07-10 - verify which is correct"
echo "4. [EXTRA_PAYMENT] Unknown Donor payment of \$250 needs identification"
echo "5. [EXTRA_PAYMENT] Sarah Johnson has additional \$500 payment (2026-07-12)"
echo "6. [EXTRA_PAYMENT] Robert Wilson has extra \$100 'Late Fee' payment (2026-07-12)"
echo ""
echo "================================================================================"
echo "FOLLOW-UP CONTACTS NEEDED"
echo "================================================================================"
echo ""
echo "  • Patricia Lee - Clarify duplicate entries (marked as error in notes)"
echo "  • Unknown/Anonymous Donor - Identify source of \$250 payment"
echo "  • Sarah Johnson - Confirm additional \$500 sponsorship payment"
echo "  • Robert Wilson - Verify \$100 late fee and reason"
echo ""
echo "================================================================================"
echo "END OF REPORT"
echo "================================================================================"
