"""Pytest-compatible data validation for all CSV data files.

Validates every row and numeric column across the four research CSV
datasets. Mirrors the checks from validate_data.py but integrates
with pytest for consistent CI reporting.
"""

import csv
import os
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "termite-projects" / "biofuel-research" / "data"

FILES = [
    "cellulase_assay_data.csv",
    "fermentation_results.csv",
    "agricultural_waste_test.csv",
    "glucose_calibration.csv",
]

NUMERIC_COLS = {
    "cellulase_assay_data.csv": [
        "Absorbance_540nm", "Glucose_mM", "Protein_mg_mL",
        "Activity_U_mL", "Specific_Activity_U_mg", "Temperature_C", "pH",
    ],
    "fermentation_results.csv": [
        "Time_h", "Substrate_g_L", "Ethanol_g_L", "Biomass_g_L", "pH", "Temperature_C",
    ],
    "agricultural_waste_test.csv": [
        "Glucose_g_L", "Conversion_Percent", "Yield_g_g", "Enzyme_FPU_g",
    ],
    "glucose_calibration.csv": [
        "Glucose_mM", "Absorbance_540nm",
    ],
}


def is_valid_number(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False


def test_all_csv_files_exist():
    for fname in FILES:
        path = DATA_DIR / fname
        assert path.exists(), f"Missing CSV file: {path}"
        assert path.stat().st_size > 0, f"Empty CSV file: {path}"


def test_all_files_have_headers():
    for fname in FILES:
        path = DATA_DIR / fname
        with open(str(path), "r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            assert reader.fieldnames is not None, f"No headers in {fname}"
            assert len(reader.fieldnames) > 0, f"Empty headers in {fname}"


def test_cellulase_assay_data():
    errors = validate_file("cellulase_assay_data.csv")
    assert not errors, f"Validation errors:\n" + "\n".join(errors)


def test_fermentation_results():
    errors = validate_file("fermentation_results.csv")
    assert not errors, f"Validation errors:\n" + "\n".join(errors)


def test_agricultural_waste_test():
    errors = validate_file("agricultural_waste_test.csv")
    assert not errors, f"Validation errors:\n" + "\n".join(errors)


def test_glucose_calibration():
    errors = validate_file("glucose_calibration.csv")
    assert not errors, f"Validation errors:\n" + "\n".join(errors)


def validate_file(filename):
    path = DATA_DIR / filename
    if not path.exists():
        return [f"File not found: {path}"]

    errors = []
    row_count = 0
    expected_numeric = NUMERIC_COLS.get(filename, [])

    with open(str(path), "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return ["No headers found"]

        headers = reader.fieldnames
        for row_num, row in enumerate(reader, start=2):
            row_count += 1
            for h in headers:
                val = row.get(h, "").strip()
                if val == "":
                    errors.append(f"Row {row_num}, column '{h}': empty value")

            for col in expected_numeric:
                if col not in row:
                    continue
                val = row[col].strip()
                if val == "":
                    continue
                if not is_valid_number(val):
                    errors.append(f"Row {row_num}, column '{col}': invalid number '{val}'")

    if row_count == 0:
        errors.append("Zero data rows")

    return errors
