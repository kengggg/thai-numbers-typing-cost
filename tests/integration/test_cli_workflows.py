import json

"""
Integration tests for CLI workflows and JSON-first architecture.

Tests end-to-end functionality including command-line interface,
file operations, and complete analysis pipelines.
"""

import os
import sys
from pathlib import Path

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from main import TypistProfile, main


class TestBasicCLIWorkflows:
    """Test suite for basic CLI workflows."""

    def test_cli_basic_analysis(
        self, sample_thai_text_file, tmp_path, monkeypatch, capsys
    ):
        """Test basic CLI analysis workflow."""
        # Use --output to direct output to tmp directory
        output_dir = tmp_path / "output"
        test_args = ["main.py", sample_thai_text_file, "--output", str(output_dir)]
        monkeypatch.setattr("sys.argv", test_args)

        # Run main function
        main()

        # Check console output
        captured = capsys.readouterr()
        assert (
            "AUTOMATIC COMPARISON: ALL SCENARIOS & TYPIST PROFILES" in captured.out
        )
        assert "📦 JSON ANALYSIS SAVED" in captured.out
        assert "📄 COMPARISON REPORT GENERATED" in captured.out

        # Check that both JSON and markdown are always created
        json_file = output_dir / "analysis.json"
        assert json_file.exists()

        # Check for markdown report (with timestamp)
        markdown_files = list(output_dir.glob("comparison_report_*.md"))
        assert len(markdown_files) >= 1

    def test_cli_analyzes_all_typist_profiles(
        self, sample_thai_text_file, tmp_path, monkeypatch, capsys
    ):
        """Test CLI automatically analyzes all typist profiles."""
        # Use --output to direct output to tmp directory
        output_dir = tmp_path / "output"
        test_args = ["main.py", sample_thai_text_file, "--output", str(output_dir)]
        monkeypatch.setattr("sys.argv", test_args)

        main()

        # Check that JSON contains all typist profiles
        json_file = output_dir / "analysis.json"
        assert json_file.exists()

        with open(json_file, "r", encoding="utf-8") as f:
            analysis_data = json.load(f)

        # Should have all 4 typist profiles
        typist_profiles = analysis_data["typist_profiles"]
        analysis_results = analysis_data["analysis_results"]

        assert len(typist_profiles) == 4
        assert len(analysis_results) == 4

        for profile_key in ["expert", "skilled", "average", "worst"]:
            assert profile_key in typist_profiles
            assert profile_key in analysis_results

    def test_cli_list_typists(self, monkeypatch, capsys):
        """Test CLI --list-typists functionality."""
        test_args = ["main.py", "--list-typists"]
        monkeypatch.setattr("sys.argv", test_args)

        main()

        captured = capsys.readouterr()
        assert "Available Typist Profiles:" in captured.out

        # Should list all profiles
        for profile_key, profile in TypistProfile.PROFILES.items():
            assert profile_key in captured.out
            assert profile["name"] in captured.out
            assert str(profile["keystroke_time"]) in captured.out

    def test_cli_invalid_document_path(self, monkeypatch, capsys):
        """Test CLI with invalid document path."""
        test_args = ["main.py", "/nonexistent/path.txt"]
        monkeypatch.setattr("sys.argv", test_args)

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Error: Document not found" in captured.out


class TestFileOperations:
    """Test suite for file operations and I/O."""

    def test_cli_creates_output_directories(
        self, sample_thai_text_file, tmp_path, monkeypatch
    ):
        """Test that CLI creates necessary output directories."""
        # Use --output to direct output to tmp directory
        output_dir = tmp_path / "output"
        test_args = ["main.py", sample_thai_text_file, "--output", str(output_dir)]
        monkeypatch.setattr("sys.argv", test_args)

        main()

        # Check that output directory was created and JSON file exists
        assert output_dir.exists()
        json_file = output_dir / "analysis.json"
        assert json_file.exists()

    def test_cli_handles_unicode_paths(self, tmp_path, monkeypatch):
        """Test CLI with Unicode file paths."""
        # Create Thai text file with Unicode name
        unicode_file = tmp_path / "ไฟล์ไทย.txt"
        unicode_file.write_text("ปี ๒๕๖๐ มีความสำคัญ", encoding="utf-8")

        # Use --output to direct output to tmp directory
        output_dir = tmp_path / "output"
        test_args = ["main.py", str(unicode_file), "--output", str(output_dir)]
        monkeypatch.setattr("sys.argv", test_args)

        main()

        # Should handle Unicode paths without issues and create JSON file
        assert output_dir.exists()
        json_file = output_dir / "analysis.json"
        assert json_file.exists()

    def test_cli_handles_spaces_in_paths(self, tmp_path, monkeypatch):
        """Test CLI with spaces in file paths."""
        # Create file with spaces in name
        spaced_file = tmp_path / "file with spaces.txt"
        spaced_file.write_text("ปี ๒๕๖๐ test", encoding="utf-8")

        # Use --output to direct output to tmp directory
        output_dir = tmp_path / "output"
        test_args = ["main.py", str(spaced_file), "--output", str(output_dir)]
        monkeypatch.setattr("sys.argv", test_args)

        main()

        # Should handle spaced paths without issues and create JSON file
        assert output_dir.exists()
        json_file = output_dir / "analysis.json"
        assert json_file.exists()

    def test_cli_preserves_file_encoding(self, tmp_path, monkeypatch, capsys):
        """Test that CLI preserves UTF-8 encoding in analysis."""
        # Create Thai text file
        thai_file = tmp_path / "thai_content.txt"
        thai_content = "วิเคราะห์ตัวเลขไทย ๑๒๓๔๕ และตัวเลขสากล 67890"
        thai_file.write_text(thai_content, encoding="utf-8")

        # Use --output to direct output to tmp directory
        output_dir = tmp_path / "output"
        test_args = ["main.py", str(thai_file), "--output", str(output_dir)]
        monkeypatch.setattr("sys.argv", test_args)

        main()

        # Check that analysis ran successfully with Thai characters
        captured = capsys.readouterr()
        assert "THAI NUMBERS TYPING COST COMPARISON" in captured.out
        assert "📦 JSON ANALYSIS SAVED" in captured.out
        # Analysis should handle Thai characters without errors


class TestErrorHandling:
    """Test suite for error handling and edge cases."""

    def test_cli_handles_empty_document(self, tmp_path, monkeypatch, capsys):
        """Test CLI with empty document."""
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("", encoding="utf-8")

        # Use --output to direct output to tmp directory
        output_dir = tmp_path / "output"
        test_args = ["main.py", str(empty_file), "--output", str(output_dir)]
        monkeypatch.setattr("sys.argv", test_args)

        main()

        # Should handle empty document gracefully
        captured = capsys.readouterr()
        assert "📦 JSON ANALYSIS SAVED" in captured.out
        assert "THAI NUMBERS TYPING COST COMPARISON" in captured.out

    def test_cli_handles_document_without_digits(self, tmp_path, monkeypatch, capsys):
        """Test CLI with document containing no digits."""
        no_digits_file = tmp_path / "no_digits.txt"
        no_digits_file.write_text("สวัสดี Hello World ไม่มีตัวเลข", encoding="utf-8")

        # Use --output to direct output to tmp directory
        output_dir = tmp_path / "output"
        test_args = ["main.py", str(no_digits_file), "--output", str(output_dir)]
        monkeypatch.setattr("sys.argv", test_args)

        main()

        # Should handle no digits gracefully
        captured = capsys.readouterr()
        assert "📦 JSON ANALYSIS SAVED" in captured.out

    def test_cli_invalid_arguments_show_help(self, monkeypatch, capsys):
        """Test that invalid arguments show help message."""
        test_args = ["main.py", "--invalid-argument"]
        monkeypatch.setattr("sys.argv", test_args)

        with pytest.raises(SystemExit):
            main()

        captured = capsys.readouterr()
        # Should show help or error message
        assert len(captured.err) > 0 or len(captured.out) > 0


class TestEndToEndWorkflows:
    """Test suite for complete end-to-end workflows."""

    def test_complete_analysis_workflow(
        self, sample_thai_text_file, tmp_path, monkeypatch, capsys
    ):
        """Test complete analysis workflow from start to finish."""
        # Use --output to direct output to tmp directory
        output_dir = tmp_path / "output"
        test_args = ["main.py", sample_thai_text_file, "--output", str(output_dir)]
        monkeypatch.setattr("sys.argv", test_args)
        main()

        # Verify complete workflow outputs
        json_file = output_dir / "analysis.json"
        assert json_file.exists()

        # Check JSON content
        with open(json_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        assert len(json_data["typist_profiles"]) == 4  # All typists
        assert len(json_data["analysis_results"]) == 4

        # Check markdown files were created
        markdown_files = list(output_dir.glob("comparison_report_*.md"))
        assert len(markdown_files) > 0

        # Verify simplified markdown content
        markdown_content = markdown_files[0].read_text(encoding="utf-8")
        assert "# Thai Numbers Typing Analysis Comparison" in markdown_content
        assert "## Typing Time Comparison (minutes)" in markdown_content
        assert "## Detailed Breakdown by Typist Profile" in markdown_content

    def test_json_and_markdown_data_consistency(
        self, sample_thai_text_file, tmp_path, monkeypatch, capsys
    ):
        """Test that JSON and markdown contain consistent data."""
        # Use --output to direct output to tmp directory
        output_dir = tmp_path / "output"
        test_args = ["main.py", sample_thai_text_file, "--output", str(output_dir)]
        monkeypatch.setattr("sys.argv", test_args)
        main()

        # Load JSON data
        json_file = output_dir / "analysis.json"
        with open(json_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        # Load markdown data
        markdown_files = list(output_dir.glob("comparison_report_*.md"))
        assert len(markdown_files) > 0
        markdown_content = markdown_files[0].read_text(encoding="utf-8")

        # Verify key data points are consistent between JSON and markdown
        # Check that all 4 typist profiles are represented
        for profile_key in ["expert", "skilled", "average", "worst"]:
            assert profile_key in json_data["typist_profiles"]
            assert profile_key in json_data["analysis_results"]

            # Profile name should appear in markdown
            profile_name = json_data["typist_profiles"][profile_key]["name"]
            assert profile_name in markdown_content

        # Check that typing times from JSON appear in markdown
        for profile_key in ["expert", "skilled", "average", "worst"]:
            scenarios = json_data["analysis_results"][profile_key]["scenarios"]
            for scenario_key in [
                "thai_kedmanee",
                "intl_kedmanee",
                "thai_pattajoti",
                "intl_pattajoti",
            ]:
                time_minutes = scenarios[scenario_key]["total_cost_minutes"]
                # Time should appear in markdown (formatted to 1 decimal place)
                assert f"{time_minutes:.1f}" in markdown_content


# Pytest markers
pytestmark = [pytest.mark.integration]
