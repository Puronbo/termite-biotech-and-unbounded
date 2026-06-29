"""Tests for the Termite Research Project Tracker."""

import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "termite-projects" / "src" / "project-manager"))

from project_tracker import ProjectTracker, ProjectStatus, Priority, Task


def test_tracker_creates_default_projects():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "test_data.json")
        tracker = ProjectTracker(data_file=data_file)
        assert len(tracker.projects) == 3
        assert "BIOFUEL-001" in tracker.projects
        assert "PEST-001" in tracker.projects
        assert "FARM-001" in tracker.projects


def test_project_names():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "test_data.json")
        tracker = ProjectTracker(data_file=data_file)
        assert tracker.projects["BIOFUEL-001"].name == "Biofuel Research Project"
        assert tracker.projects["PEST-001"].name == "Natural Pest Control Project"
        assert tracker.projects["FARM-001"].name == "Termite Farming Project"


def test_project_status_types():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "test_data.json")
        tracker = ProjectTracker(data_file=data_file)
        for pid, proj in tracker.projects.items():
            assert isinstance(proj.status, ProjectStatus)
            assert proj.budget > 0


def test_get_project_summary():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "test_data.json")
        tracker = ProjectTracker(data_file=data_file)
        summary = tracker.get_project_summary("BIOFUEL-001")
        assert "error" not in summary
        assert summary["project_name"] == "Biofuel Research Project"
        assert summary["tasks"]["total"] > 0
        assert summary["budget"]["total"] == 23000000
        assert summary["budget"]["spent"] == 8200000


def test_get_project_summary_invalid():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "test_data.json")
        tracker = ProjectTracker(data_file=data_file)
        result = tracker.get_project_summary("INVALID")
        assert "error" in result


def test_all_projects_summary():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "test_data.json")
        tracker = ProjectTracker(data_file=data_file)
        summaries = tracker.get_all_projects_summary()
        assert len(summaries) == 3
        for s in summaries:
            assert "project_id" in s
            assert "tasks" in s
            assert "budget" in s
            assert "timeline" in s


def test_update_task_status():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "test_data.json")
        tracker = ProjectTracker(data_file=data_file)
        result = tracker.update_task_status("BIOFUEL-001", "BIO-010", ProjectStatus.IN_PROGRESS)
        assert result == True
        task = next(t for t in tracker.projects["BIOFUEL-001"].tasks if t.id == "BIO-010")
        assert task.status == ProjectStatus.IN_PROGRESS


def test_update_task_status_invalid_project():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "test_data.json")
        tracker = ProjectTracker(data_file=data_file)
        result = tracker.update_task_status("INVALID", "BIO-001", ProjectStatus.COMPLETED)
        assert result == False


def test_update_task_status_invalid_task():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "test_data.json")
        tracker = ProjectTracker(data_file=data_file)
        result = tracker.update_task_status("BIOFUEL-001", "INVALID", ProjectStatus.COMPLETED)
        assert result == False


def test_add_task():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "test_data.json")
        tracker = ProjectTracker(data_file=data_file)
        new_task = Task(
            id="BIO-013",
            name="Test Task",
            description="A test task",
            status=ProjectStatus.IN_PROGRESS,
            priority=Priority.HIGH,
            start_date="2026-07-01",
            end_date="2026-07-15",
            assigned_to="Test",
            dependencies=[],
        )
        result = tracker.add_task("BIOFUEL-001", new_task)
        assert result == True
        assert len(tracker.projects["BIOFUEL-001"].tasks) > 0
        task_ids = [t.id for t in tracker.projects["BIOFUEL-001"].tasks]
        assert "BIO-013" in task_ids


def test_add_task_invalid_project():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "test_data.json")
        tracker = ProjectTracker(data_file=data_file)
        new_task = Task(
            id="TEST-001", name="Test", description="", status=ProjectStatus.NOT_STARTED,
            priority=Priority.LOW, start_date="2026-01-01", end_date="2026-01-02",
            assigned_to="Tester", dependencies=[],
        )
        result = tracker.add_task("INVALID", new_task)
        assert result == False


def test_generate_report():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "test_data.json")
        tracker = ProjectTracker(data_file=data_file)
        report = tracker.generate_report()
        assert "TERMITE RESEARCH PROJECTS" in report
        assert "Biofuel Research Project" in report
        assert "Natural Pest Control Project" in report
        assert "Termite Farming Project" in report
        assert "END OF REPORT" in report


def test_export_to_markdown():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "test_data.json")
        md_path = os.path.join(tmpdir, "test_report.md")
        tracker = ProjectTracker(data_file=data_file)
        tracker.export_to_markdown(md_path)
        assert os.path.exists(md_path)
        with open(md_path) as f:
            content = f.read()
        assert "# Termite Research Projects Report" in content
        assert "Biofuel Research Project" in content


def test_save_and_load_persistence():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "persist_test.json")
        # Create and modify
        tracker1 = ProjectTracker(data_file=data_file)
        tracker1.update_task_status("BIOFUEL-001", "BIO-010", ProjectStatus.IN_PROGRESS)
        # Load fresh instance
        tracker2 = ProjectTracker(data_file=data_file)
        task = next(t for t in tracker2.projects["BIOFUEL-001"].tasks if t.id == "BIO-010")
        assert task.status == ProjectStatus.IN_PROGRESS


def test_biofuel_tasks_count():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "test_data.json")
        tracker = ProjectTracker(data_file=data_file)
        assert len(tracker.projects["BIOFUEL-001"].tasks) == 12


def test_pest_tasks_count():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "test_data.json")
        tracker = ProjectTracker(data_file=data_file)
        assert len(tracker.projects["PEST-001"].tasks) == 7


def test_farm_tasks_count():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "test_data.json")
        tracker = ProjectTracker(data_file=data_file)
        assert len(tracker.projects["FARM-001"].tasks) == 4


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
