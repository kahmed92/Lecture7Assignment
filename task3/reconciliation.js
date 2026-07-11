#!/usr/bin/env node

/**
 * Payment Reconciliation Script
 * Reconciles expected payments with actual payment records to identify discrepancies.
 */

const fs = require('fs');
const path = require('path');

class PaymentReconciler {
    constructor(expectedFile, actualFile, fuzzyThreshold = 0.7) {
        this.expectedFile = expectedFile;
        this.actualFile = actualFile;
        this.fuzzyThreshold = fuzzyThreshold;
        this.expectedPayments = [];
        this.actualPayments = [];
        this.ambiguityRules = {
            'M. Chen': 'Michael Chen',
            'E. Davis': 'Emma Davis',
            'Unknown Donor': 'UNMATCHED',
        };
    }

    // Parse CSV content
    parseCSV(content) {
        const lines = content.trim().split('\n');
        const headers = lines[0].split(',').map(h => h.trim());
        const records = [];

        for (let i = 1; i < lines.length; i++) {
            const values = lines[i].split(',').map(v => v.trim());
            const record = {};
            headers.forEach((header, idx) => {
                record[header] = values[idx];
            });
            records.push(record);
        }
        return records;
    }

    // Load CSV files
    loadFiles() {
        const expectedContent = fs.readFileSync(this.expectedFile, 'utf-8');
        const actualContent = fs.readFileSync(this.actualFile, 'utf-8');

        this.expectedPayments = this.parseCSV(expectedContent);
        this.actualPayments = this.parseCSV(actualContent);
    }

    // Calculate string similarity
    fuzzyMatch(name1, name2) {
        const n1 = name1.toLowerCase().trim();
        const n2 = name2.toLowerCase().trim();

        if (n1 === n2) return 1;

        let matches = 0;
        const minLen = Math.min(n1.length, n2.length);

        for (let i = 0; i < minLen; i++) {
            if (n1[i] === n2[i]) matches++;
        }

        return matches / Math.max(n1.length, n2.length);
    }

    // Resolve ambiguous names
    resolveName(payerName) {
        if (this.ambiguityRules[payerName]) {
            return this.ambiguityRules[payerName];
        }

        // Fuzzy match against expected names
        for (const expected of this.expectedPayments) {
            const expectedName = expected.Name;
            const similarity = this.fuzzyMatch(payerName, expectedName);
            if (similarity >= this.fuzzyThreshold) {
                return expectedName;
            }
        }

        return payerName;
    }

    // Perform reconciliation
    reconcile() {
        this.loadFiles();

        const results = {
            matched: [],
            unmatchedExpected: [],
            unmatchedActual: [],
            duplicates: [],
            amountMismatches: [],
            extraPayments: [],
            followUpList: []
        };

        // Create dictionaries for tracking
        const expectedDict = {};
        for (const exp of this.expectedPayments) {
            const name = exp.Name;
            const amount = parseFloat(exp.Amount);
            if (!expectedDict[name]) {
                expectedDict[name] = { count: 0, total: 0, entries: [] };
            }
            expectedDict[name].total += amount;
            expectedDict[name].count += 1;
            expectedDict[name].entries.push(exp);
        }

        const actualDict = {};
        for (const act of this.actualPayments) {
            const resolvedName = this.resolveName(act['Payer Name']);
            if (!actualDict[resolvedName]) {
                actualDict[resolvedName] = [];
            }
            actualDict[resolvedName].push(act);
        }

        // Match payments
        const matchedActual = new Set();

        for (const name in expectedDict) {
            const expectedAmount = expectedDict[name].total;

            if (actualDict[name]) {
                const actualRecords = actualDict[name];
                const actualTotal = actualRecords.reduce((sum, r) => sum + parseFloat(r.Amount), 0);

                // Check for duplicates
                if (actualRecords.length > 1 && actualTotal > expectedAmount) {
                    for (let i = 0; i < actualRecords.length; i++) {
                        const record = actualRecords[i];
                        results.duplicates.push({
                            name: name,
                            amount: record.Amount,
                            date: record.Date,
                            notes: record['Reference/Notes'],
                            index: i
                        });
                    }
                }

                // Check amount mismatch
                if (Math.abs(actualTotal - expectedAmount) > 0.01) {
                    results.amountMismatches.push({
                        name: name,
                        expected: expectedAmount,
                        actual: actualTotal,
                        difference: actualTotal - expectedAmount
                    });
                } else {
                    results.matched.push({
                        name: name,
                        amount: expectedAmount,
                        records: actualRecords.length
                    });
                }

                // Mark as matched
                for (const record of actualRecords) {
                    matchedActual.add(JSON.stringify(record));
                }
            } else {
                results.unmatchedExpected.push({
                    name: name,
                    amount: expectedAmount
                });
            }
        }

        // Find unmatched actual payments
        for (const name in actualDict) {
            const records = actualDict[name];
            for (const record of records) {
                if (!matchedActual.has(JSON.stringify(record))) {
                    let found = false;
                    for (const expName in expectedDict) {
                        if (this.fuzzyMatch(name, expName) >= this.fuzzyThreshold) {
                            found = true;
                            break;
                        }
                    }

                    if (!found || !expectedDict[name]) {
                        results.extraPayments.push({
                            name: name,
                            amount: record.Amount,
                            date: record.Date,
                            method: record['Payment Method'],
                            notes: record['Reference/Notes']
                        });
                    }
                }
            }
        }

        // Generate follow-up list
        for (const item of results.unmatchedExpected) {
            results.followUpList.push({
                type: 'MISSING_PAYMENT',
                name: item.name,
                amount: item.amount,
                action: `Contact ${item.name} for payment of $${parseFloat(item.amount).toFixed(2)}`
            });
        }

        for (const item of results.amountMismatches) {
            results.followUpList.push({
                type: 'AMOUNT_MISMATCH',
                name: item.name,
                amount: item.expected,
                action: `Verify payment for ${item.name}: Expected $${item.expected.toFixed(2)}, Received $${item.actual.toFixed(2)} (Diff: $${item.difference.toFixed(2)})`
            });
        }

        for (const item of results.duplicates) {
            results.followUpList.push({
                type: 'DUPLICATE',
                name: item.name,
                amount: item.amount,
                action: `Review duplicate entry for ${item.name} on ${item.date} ($${item.amount}) - ${item.notes}`
            });
        }

        return results;
    }

    // Calculate totals
    calculateTotals() {
        const totalExpected = this.expectedPayments.reduce((sum, p) => sum + parseFloat(p.Amount), 0);
        const totalActual = this.actualPayments.reduce((sum, p) => sum + parseFloat(p.Amount), 0);
        return [totalExpected, totalActual];
    }

    // Print formatted report
    printReport(results) {
        const [totalExpected, totalActual] = this.calculateTotals();
        const now = new Date().toISOString().replace('T', ' ').substring(0, 19);

        console.log('\n' + '='.repeat(80));
        console.log('PAYMENT RECONCILIATION REPORT');
        console.log('='.repeat(80));
        console.log(`Generated: ${now}`);
        console.log();

        // Summary
        console.log('SUMMARY');
        console.log('-'.repeat(80));
        console.log(`Total Expected: $${totalExpected.toFixed(2).padStart(12)}`);
        console.log(`Total Recorded: $${totalActual.toFixed(2).padStart(12)}`);
        const diff = totalActual - totalExpected;
        const sign = diff >= 0 ? '+' : '';
        console.log(`Discrepancy:    $${sign}${diff.toFixed(2).padStart(11)}`);
        console.log();

        // Matched Payments
        console.log(`MATCHED PAYMENTS (${results.matched.length})`);
        console.log('-'.repeat(80));
        for (const item of results.matched) {
            const name = item.name.padEnd(40, '.');
            const amount = `$${parseFloat(item.amount).toFixed(2)}`.padStart(10);
            console.log(`  ✓ ${name} ${amount}`);
        }
        console.log();

        // Unmatched Expected
        if (results.unmatchedExpected.length > 0) {
            console.log(`MISSING PAYMENTS (${results.unmatchedExpected.length})`);
            console.log('-'.repeat(80));
            for (const item of results.unmatchedExpected) {
                const name = item.name.padEnd(40, '.');
                const amount = `$${parseFloat(item.amount).toFixed(2)}`.padStart(10);
                console.log(`  ✗ ${name} ${amount}`);
            }
            console.log();
        }

        // Duplicates
        if (results.duplicates.length > 0) {
            console.log(`DUPLICATE ENTRIES (${results.duplicates.length})`);
            console.log('-'.repeat(80));
            for (const item of results.duplicates) {
                const name = item.name.padEnd(30, '.');
                console.log(`  ⚠ ${name} $${item.amount} on ${item.date}`);
                console.log(`     Notes: ${item.notes}`);
            }
            console.log();
        }

        // Amount Mismatches
        if (results.amountMismatches.length > 0) {
            console.log(`AMOUNT MISMATCHES (${results.amountMismatches.length})`);
            console.log('-'.repeat(80));
            for (const item of results.amountMismatches) {
                console.log(`  ${item.name.padEnd(30)}`);
                const expected = `$${item.expected.toFixed(2)}`.padStart(12);
                const actual = `$${item.actual.toFixed(2)}`.padStart(12);
                const diff = `$${item.difference.toFixed(2)}`.padStart(12);
                console.log(`    Expected: ${expected}  |  Received: ${actual}  |  Diff: ${diff}`);
            }
            console.log();
        }

        // Extra/Unmatched Actual
        if (results.extraPayments.length > 0) {
            console.log(`EXTRA/UNIDENTIFIED PAYMENTS (${results.extraPayments.length})`);
            console.log('-'.repeat(80));
            for (const item of results.extraPayments) {
                const name = item.name.padEnd(30, '.');
                console.log(`  ${name} $${item.amount} (${item.method})`);
                console.log(`    Date: ${item.date}  |  Notes: ${item.notes}`);
            }
            console.log();
        }

        // Follow-up List
        console.log(`FOLLOW-UP REQUIRED (${results.followUpList.length})`);
        console.log('-'.repeat(80));
        for (let i = 0; i < results.followUpList.length; i++) {
            const item = results.followUpList[i];
            const typeStr = item.type.padEnd(15, '.');
            console.log(`  ${i + 1}. [${typeStr}] ${item.action}`);
        }
        console.log();

        console.log('='.repeat(80));
        console.log('END OF REPORT');
        console.log('='.repeat(80));
    }
}

// Main execution
if (require.main === module) {
    const reconciler = new PaymentReconciler(
        'expected_payments.csv',
        'payment_records.csv',
        0.7
    );

    try {
        const results = reconciler.reconcile();
        reconciler.printReport(results);
    } catch (error) {
        console.error('Error during reconciliation:', error.message);
        process.exit(1);
    }
}

module.exports = PaymentReconciler;
