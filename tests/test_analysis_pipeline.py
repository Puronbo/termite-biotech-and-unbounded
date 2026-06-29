"""Integration tests for the termite analysis pipeline.

Verifies that the analysis pipeline produces consistent, expected
outputs when run against the example CSV data files.
"""

import importlib.util
import json
import sys
from pathlib import Path

_SCRIPT = str(Path(__file__).resolve().parent.parent / "chronosend" / "termite-analysis.py")
_spec = importlib.util.spec_from_file_location("termite_analysis", _SCRIPT)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

DATA_DIR = Path(__file__).resolve().parent.parent / "chronosend" / "examples" / "termite"
CSV_FILES = [
    "cellulase_assay_data.csv",
    "fermentation_results.csv",
    "agricultural_waste_test.csv",
    "glucose_calibration.csv",
]


def load_csv(filename):
    return mod.parse_csv(str(DATA_DIR / filename))


def test_all_csv_files_exist():
    for fname in CSV_FILES:
        path = DATA_DIR / fname
        assert path.exists(), f"Missing CSV file: {path}"
        assert path.stat().st_size > 0, f"Empty CSV file: {path}"


def test_cellulase_analysis():
    rows = load_csv("cellulase_assay_data.csv")
    assert rows is not None and not isinstance(rows, str)
    result = mod.analyze_cellulase(rows)
    assert "error" not in result
    assert result["total_rows"] == 15
    assert result["isolates_tested"] == 5
    assert result["top_strain"] is not None
    assert result["top_activity"] > 0
    assert len(result["rankings"]) == 5
    for i in range(len(result["rankings"]) - 1):
        assert result["rankings"][i][1]["mean_activity"] >= result["rankings"][i + 1][1]["mean_activity"]


def test_fermentation_analysis():
    rows = load_csv("fermentation_results.csv")
    assert rows is not None and not isinstance(rows, str)
    result = mod.analyze_fermentation(rows)
    assert "error" not in result
    assert result["total_rows"] == 21
    assert result["strains_tested"] == 3
    for strain_data in result["results"].values():
        traj = strain_data["ethanol_trajectory"]
        for i in range(len(traj) - 1):
            assert traj[i]["time"] < traj[i + 1]["time"]


def test_waste_test_analysis():
    rows = load_csv("agricultural_waste_test.csv")
    assert rows is not None and not isinstance(rows, str)
    result = mod.analyze_waste_test(rows)
    assert "error" not in result
    assert result["total_rows"] == 24
    assert result["combinations_tested"] >= 1
    assert result["best_combination"] is not None
    for i in range(len(result["rankings"]) - 1):
        assert result["rankings"][i]["mean_glucose_g_L"] >= result["rankings"][i + 1]["mean_glucose_g_L"]


def test_calibration_analysis():
    rows = load_csv("glucose_calibration.csv")
    assert rows is not None and not isinstance(rows, str)
    result = mod.analyze_calibration(rows)
    assert "error" not in result
    assert result["n"] == 10
    assert result["r_squared"] > 0.99
    assert result["slope"] > 0
    assert result["detection_limit_mM"] >= 0
    assert len(result["data_points"]) == 10


def test_calibration_curve_quality():
    rows = load_csv("glucose_calibration.csv")
    result = mod.analyze_calibration(rows)
    assert result["r_squared"] >= 0.9999, f"Calibration R² {result['r_squared']} below 0.9999"


def test_all_strains_have_positive_activity():
    rows = load_csv("cellulase_assay_data.csv")
    result = mod.analyze_cellulase(rows)
    for iso, data in result["summary"].items():
        assert data["mean_activity"] > 0
        assert data["max_activity"] > 0


def test_ethanol_monotonic():
    rows = load_csv("fermentation_results.csv")
    result = mod.analyze_fermentation(rows)
    for strain, data in result["results"].items():
        traj = data["ethanol_trajectory"]
        for i in range(len(traj) - 1):
            assert traj[i]["ethanol"] <= traj[i + 1]["ethanol"] + 0.01


def test_analysis_json_integrity():
    json_path = DATA_DIR / "analysis_results.json"
    assert json_path.exists()
    with open(json_path) as f:
        saved = json.load(f)
    assert "cellulase" in saved
    assert "fermentation" in saved
    assert "waste_test" in saved
    assert "calibration" in saved
    r = mod.analyze_cellulase(load_csv("cellulase_assay_data.csv"))
    assert r["top_strain"] == saved["cellulase"]["top_strain"]
    c = mod.analyze_calibration(load_csv("glucose_calibration.csv"))
    assert abs(c["slope"] - saved["calibration"]["slope"]) < 0.001


def test_empty_data_handling():
    assert "error" in mod.analyze_cellulase([])
    assert "error" in mod.analyze_fermentation([])
    assert "error" in mod.analyze_waste_test([])
    assert "error" in mod.analyze_calibration([])


def test_missing_file_handling():
    assert mod.parse_csv(str(DATA_DIR / "nonexistent.csv")) is None


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
