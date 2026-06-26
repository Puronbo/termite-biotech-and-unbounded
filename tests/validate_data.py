"""Validate all CSV data files in the biofuel-research data directory.

Usage: python validate_data.py

Reads each CSV file, validates row parsing and numeric columns,
and prints a PASS/FAIL report. Exit code 0 on success, 1 on failure.
"""

import csv
import os
import sys

DATA_DIR = os.path.join(
    os.path.dirname(__file__),
    '..',
    'termite-projects',
    'biofuel-research',
    'data'
)

FILES = [
    'cellulase_assay_data.csv',
    'fermentation_results.csv',
    'agricultural_waste_test.csv',
    'glucose_calibration.csv',
]

# Numeric columns expected per file (subset to validate)
NUMERIC_COLS = {
    'cellulase_assay_data.csv': [
        'Absorbance_540nm', 'Glucose_mM', 'Protein_mg_mL',
        'Activity_U_mL', 'Specific_Activity_U_mg', 'Temperature_C', 'pH'
    ],
    'fermentation_results.csv': [
        'Time_h', 'Substrate_g_L', 'Ethanol_g_L', 'Biomass_g_L', 'pH', 'Temperature_C'
    ],
    'agricultural_waste_test.csv': [
        'Glucose_g_L', 'Conversion_Percent', 'Yield_g_g', 'Enzyme_FPU_g'
    ],
    'glucose_calibration.csv': [
        'Glucose_mM', 'Absorbance_540nm'
    ],
}


def is_valid_number(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False


def validate_file(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.isfile(path):
        return False, f"File not found: {path}"

    errors = []
    row_count = 0
    expected_numeric = NUMERIC_COLS.get(filename, [])

    with open(path, 'r', newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return False, "No headers found"

        headers = reader.fieldnames
        for row_num, row in enumerate(reader, start=2):
            row_count += 1

            # Check all columns present
            for h in headers:
                val = row.get(h, '').strip()
                if val == '':
                    errors.append(f"Row {row_num}, column '{h}': empty value")

            # Validate numeric columns
            for col in expected_numeric:
                if col not in row:
                    continue
                val = row[col].strip()
                if val == '':
                    continue
                if not is_valid_number(val):
                    errors.append(
                        f"Row {row_num}, column '{col}': "
                        f"invalid number '{val}'"
                    )

    if row_count == 0:
        return False, f"Zero data rows"

    return True, (row_count, errors)


def main():
    total_files = 0
    total_rows = 0
    all_errors = []

    for fname in FILES:
        ok, result = validate_file(fname)
        total_files += 1
        if not ok:
            all_errors.append(f"[{fname}] {result}")
        else:
            rows, errs = result
            total_rows += rows
            if errs:
                all_errors.append(f"[{fname}] {len(errs)} validation issue(s)")
                for e in errs:
                    all_errors.append(f"  {e}")

    if all_errors:
        print("FAIL: errors found")
        for err in all_errors:
            print(err)
        sys.exit(1)
    else:
        print(f"PASS: {total_files} files, {total_rows} rows — all valid")
        sys.exit(0)


if __name__ == '__main__':
    main()
