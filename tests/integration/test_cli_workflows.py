"""
Integration tests for CLI workflows and JSON-first architecture.

Tests end-to-end functionality including command-line interface,
file operations, and complete analysis pipelines.
"""

import pytest
import subprocess
import json
import tempfile
from pathlib import Path
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from main import main, TypistProfile


class TestBasicCLIWorkflows:
    """Test suite for basic CLI workflows."""
    
    def test_cli_basic_analysis(self, sample_thai_text_file, tmp_path, monkeypatch, capsys):
        """Test basic CLI analysis workflow."""
        # Mock sys.argv for basic analysis
        test_args = ['main.py', sample_thai_text_file, '--output', str(tmp_path)]
        monkeypatch.setattr('sys.argv', test_args)
        
        # Run main function
        main()
        
        # Check console output
        captured = capsys.readouterr()
        assert "THAI NUMBERS TYPING COST ANALYSIS" in captured.out
        assert "Analysis complete!" in captured.out
        
        # Check that output files were created
        analysis_dir = tmp_path / "analysis"
        assert analysis_dir.exists()
        
        # Should have text analysis file
        text_analysis_file = analysis_dir / "text_analysis.txt"
        assert text_analysis_file.exists()
        
        # Should have keyboard comparison file
        keyboard_files = list(analysis_dir.glob("keyboard_comparison_*.txt"))
        assert len(keyboard_files) > 0
        
        # Should have typing cost analysis file
        cost_files = list(analysis_dir.glob("typing_cost_*.txt"))
        assert len(cost_files) > 0
    
    def test_cli_with_different_typist_profiles(self, sample_thai_text_file, tmp_path, monkeypatch, capsys):
        """Test CLI with different typist profiles."""
        for profile in ['expert', 'skilled', 'average', 'worst']:
            capsys.readouterr()  # Clear previous output
            
            test_args = ['main.py', sample_thai_text_file, '--typist', profile, '--output', str(tmp_path)]
            monkeypatch.setattr('sys.argv', test_args)
            
            main()
            
            captured = capsys.readouterr()
            profile_info = TypistProfile.get_profile(profile)
            assert profile_info['name'] in captured.out
            assert str(profile_info['keystroke_time']) in captured.out
    
    def test_cli_text_only_mode(self, sample_thai_text_file, tmp_path, monkeypatch, capsys):
        """Test CLI text-only analysis mode."""
        test_args = ['main.py', sample_thai_text_file, '--text-only', '--output', str(tmp_path)]
        monkeypatch.setattr('sys.argv', test_args)
        
        main()
        
        captured = capsys.readouterr()
        assert "Running text analysis..." in captured.out
        
        # Should only have text analysis file
        analysis_dir = tmp_path / "analysis"
        text_analysis_file = analysis_dir / "text_analysis.txt"
        assert text_analysis_file.exists()
        
        # Should not have other analysis files in this run
        # (Note: other files might exist from previous tests)
    
    def test_cli_keyboard_only_mode(self, sample_thai_text_file, tmp_path, monkeypatch, capsys):
        """Test CLI keyboard-only comparison mode."""
        test_args = ['main.py', sample_thai_text_file, '--keyboard-only', '--output', str(tmp_path)]
        monkeypatch.setattr('sys.argv', test_args)
        
        main()
        
        captured = capsys.readouterr()
        assert "Running keyboard comparison" in captured.out
        assert "KEYBOARD ROW SYSTEM EXPLANATION" in captured.out
        assert "KEYBOARD LAYOUT COMPARISON" in captured.out
    
    def test_cli_compare_all_typists(self, sample_thai_text_file, tmp_path, monkeypatch, capsys):
        """Test CLI with --compare-all flag."""
        test_args = ['main.py', sample_thai_text_file, '--compare-all', '--output', str(tmp_path)]
        monkeypatch.setattr('sys.argv', test_args)
        
        main()
        
        captured = capsys.readouterr()
        assert "Running comparative analysis across all typist skill levels..." in captured.out
        
        # Should analyze all typist profiles
        for profile_name in TypistProfile.PROFILES.keys():
            profile = TypistProfile.PROFILES[profile_name]
            assert profile['name'] in captured.out
        
        # Should create comparative report
        reports_dir = tmp_path / "reports"
        comparative_file = reports_dir / "comparative_analysis.txt"
        assert comparative_file.exists()
    
    def test_cli_list_typists(self, monkeypatch, capsys):
        """Test CLI --list-typists functionality."""
        test_args = ['main.py', '--list-typists']
        monkeypatch.setattr('sys.argv', test_args)
        
        main()
        
        captured = capsys.readouterr()
        assert "Available Typist Profiles:" in captured.out
        
        # Should list all profiles
        for profile_key, profile in TypistProfile.PROFILES.items():
            assert profile_key in captured.out
            assert profile['name'] in captured.out
            assert str(profile['keystroke_time']) in captured.out
    
    def test_cli_invalid_document_path(self, monkeypatch, capsys):
        """Test CLI with invalid document path."""
        test_args = ['main.py', '/nonexistent/path.txt']
        monkeypatch.setattr('sys.argv', test_args)
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "Error: Document not found" in captured.out
    
    def test_cli_invalid_typist_profile(self, sample_thai_text_file, monkeypatch, capsys):
        """Test CLI with invalid typist profile."""
        test_args = ['main.py', sample_thai_text_file, '--typist', 'invalid_profile']
        monkeypatch.setattr('sys.argv', test_args)
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 2  # argparse exits with code 2 for invalid choices
        
        captured = capsys.readouterr()
        # argparse handles the error and shows usage info, not our custom error messages
        assert "invalid choice" in captured.err or "invalid choice" in captured.out


class TestJSONFirstArchitecture:
    """Test suite for JSON-first architecture workflows."""
    
    def test_cli_output_json_basic(self, sample_thai_text_file, tmp_path, monkeypatch, capsys):
        """Test basic JSON output functionality."""
        json_file = tmp_path / "analysis_results.json"
        test_args = ['main.py', sample_thai_text_file, '--output-json', str(json_file)]
        monkeypatch.setattr('sys.argv', test_args)
        
        main()
        
        captured = capsys.readouterr()
        assert "JSON ANALYSIS SAVED" in captured.out
        assert str(json_file) in captured.out
        
        # Verify JSON file was created and is valid
        assert json_file.exists()
        
        with open(json_file, 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        
        # Check JSON structure
        required_sections = [
            'metadata', 'document_analysis', 'typist_profiles',
            'analysis_results', 'research_questions', 'impact_projections',
            'key_findings', 'recommendations'
        ]
        
        for section in required_sections:
            assert section in analysis_data, f"Missing JSON section: {section}"
    
    def test_cli_output_json_with_all_typists(self, sample_thai_text_file, tmp_path, monkeypatch, capsys):
        """Test JSON output with all typist profiles."""
        json_file = tmp_path / "all_typists.json"
        test_args = ['main.py', sample_thai_text_file, '--compare-all', '--output-json', str(json_file)]
        monkeypatch.setattr('sys.argv', test_args)
        
        main()
        
        # Verify JSON includes all typist profiles
        with open(json_file, 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        
        typist_profiles = analysis_data['typist_profiles']
        analysis_results = analysis_data['analysis_results']
        
        # Should have all 4 typist profiles
        assert len(typist_profiles) == 4
        assert len(analysis_results) == 4
        
        for profile_key in TypistProfile.PROFILES.keys():
            assert profile_key in typist_profiles
            assert profile_key in analysis_results
    
    def test_cli_render_from_json_markdown(self, sample_thai_text_file, tmp_path, monkeypatch, capsys):
        """Test rendering markdown from existing JSON."""
        # First, create JSON file
        json_file = tmp_path / "source.json"
        test_args = ['main.py', sample_thai_text_file, '--output-json', str(json_file)]
        monkeypatch.setattr('sys.argv', test_args)
        main()
        
        capsys.readouterr()  # Clear output
        
        # Then, render markdown from JSON
        test_args = ['main.py', '--render-from-json', str(json_file), '--format', 'markdown', '--output', str(tmp_path)]
        monkeypatch.setattr('sys.argv', test_args)
        main()
        
        captured = capsys.readouterr()
        assert "MARKDOWN REPORT GENERATED" in captured.out
        
        # Check that markdown file was created
        markdown_files = list(tmp_path.glob("*.md"))
        assert len(markdown_files) > 0
        
        # Verify markdown content
        markdown_file = markdown_files[0]
        content = markdown_file.read_text(encoding='utf-8')
        assert "# Thai Numbers Typing Cost Analysis - Research Report" in content
        assert "## Executive Summary" in content
        assert "## Research Questions Answered" in content
    
    def test_cli_render_from_json_console(self, sample_thai_text_file, tmp_path, monkeypatch, capsys):
        """Test rendering console output from existing JSON."""
        # First, create JSON file
        json_file = tmp_path / "source.json"
        test_args = ['main.py', sample_thai_text_file, '--output-json', str(json_file)]
        monkeypatch.setattr('sys.argv', test_args)
        main()
        
        capsys.readouterr()  # Clear output
        
        # Then, render console from JSON
        test_args = ['main.py', '--render-from-json', str(json_file), '--format', 'console']
        monkeypatch.setattr('sys.argv', test_args)
        main()
        
        captured = capsys.readouterr()
        assert "THAI NUMBERS TYPING COST ANALYSIS - SUMMARY" in captured.out
        assert "TYPING COST BY SCENARIO:" in captured.out
        assert "RECOMMENDATIONS:" in captured.out
    
    def test_cli_json_first_with_format_options(self, sample_thai_text_file, tmp_path, monkeypatch, capsys):
        """Test JSON-first workflow with different format options."""
        formats = ['json', 'markdown', 'console']
        
        for format_type in formats:
            capsys.readouterr()  # Clear output
            
            if format_type == 'json':
                json_file = tmp_path / f"test_{format_type}.json"
                test_args = ['main.py', sample_thai_text_file, '--output-json', str(json_file), '--format', format_type]
            else:
                test_args = ['main.py', sample_thai_text_file, '--format', format_type, '--output', str(tmp_path)]
            
            monkeypatch.setattr('sys.argv', test_args)
            main()
            
            captured = capsys.readouterr()
            
            if format_type == 'json':
                assert "JSON ANALYSIS SAVED" in captured.out
            elif format_type == 'markdown':
                assert "MARKDOWN REPORT GENERATED" in captured.out
            elif format_type == 'console':
                assert "THAI NUMBERS TYPING COST ANALYSIS - SUMMARY" in captured.out
    
    def test_cli_render_from_nonexistent_json(self, monkeypatch, capsys):
        """Test rendering from nonexistent JSON file."""
        test_args = ['main.py', '--render-from-json', '/nonexistent/file.json', '--format', 'markdown']
        monkeypatch.setattr('sys.argv', test_args)
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "Error: JSON file not found" in captured.out


class TestLegacyCompatibility:
    """Test suite for legacy compatibility features."""
    
    def test_cli_legacy_markdown_report(self, sample_thai_text_file, tmp_path, monkeypatch, capsys):
        """Test legacy --markdown-report functionality."""
        test_args = ['main.py', sample_thai_text_file, '--markdown-report', '--output', str(tmp_path)]
        monkeypatch.setattr('sys.argv', test_args)
        
        main()
        
        captured = capsys.readouterr()
        assert "GENERATING FOCUSED RESEARCH REPORT (Legacy Compatibility)" in captured.out
        assert "RESEARCH REPORT GENERATED SUCCESSFULLY!" in captured.out
        
        # Check that markdown report was created
        markdown_files = list(tmp_path.glob("Thai_Numbers_Typing_Cost_Analysis_Report_*.md"))
        assert len(markdown_files) > 0
        
        # Verify report content
        report_file = markdown_files[0]
        content = report_file.read_text(encoding='utf-8')
        assert "# Thai Numbers Typing Cost Analysis - Research Report" in content
    
    def test_cli_legacy_with_compare_all(self, sample_thai_text_file, tmp_path, monkeypatch, capsys):
        """Test legacy compatibility with --compare-all."""
        test_args = ['main.py', sample_thai_text_file, '--compare-all', '--output', str(tmp_path)]
        monkeypatch.setattr('sys.argv', test_args)
        
        main()
        
        captured = capsys.readouterr()
        # Should automatically generate markdown report with --compare-all
        assert "GENERATING FOCUSED RESEARCH REPORT (Legacy Compatibility)" in captured.out
    
    def test_cli_legacy_no_markdown_flag(self, sample_thai_text_file, tmp_path, monkeypatch, capsys):
        """Test --no-markdown flag to skip automatic report generation."""
        test_args = ['main.py', sample_thai_text_file, '--compare-all', '--no-markdown', '--output', str(tmp_path)]
        monkeypatch.setattr('sys.argv', test_args)
        
        main()
        
        captured = capsys.readouterr()
        # Should NOT generate automatic markdown report with --no-markdown
        assert "GENERATING FOCUSED RESEARCH REPORT (Legacy Compatibility)" not in captured.out


class TestFileOperations:
    """Test suite for file operations and I/O."""
    
    def test_cli_creates_output_directories(self, sample_thai_text_file, tmp_path, monkeypatch):
        """Test that CLI creates necessary output directories."""
        output_dir = tmp_path / "custom_output"
        test_args = ['main.py', sample_thai_text_file, '--output', str(output_dir)]
        monkeypatch.setattr('sys.argv', test_args)
        
        main()
        
        # Check that directories were created
        assert output_dir.exists()
        assert (output_dir / "reports").exists()
        assert (output_dir / "analysis").exists()
    
    def test_cli_handles_unicode_paths(self, tmp_path, monkeypatch):
        """Test CLI with Unicode file paths."""
        # Create Thai text file with Unicode name
        unicode_file = tmp_path / "ไฟล์ไทย.txt"
        unicode_file.write_text("ปี ๒๕๖๐ มีความสำคัญ", encoding='utf-8')
        
        unicode_output = tmp_path / "ผลลัพธ์"
        
        test_args = ['main.py', str(unicode_file), '--output', str(unicode_output)]
        monkeypatch.setattr('sys.argv', test_args)
        
        main()
        
        # Should handle Unicode paths without issues
        assert unicode_output.exists()
        assert (unicode_output / "analysis").exists()
    
    def test_cli_handles_spaces_in_paths(self, tmp_path, monkeypatch):
        """Test CLI with spaces in file paths."""
        # Create file with spaces in name
        spaced_file = tmp_path / "file with spaces.txt"
        spaced_file.write_text("ปี ๒๕๖๐ test", encoding='utf-8')
        
        spaced_output = tmp_path / "output with spaces"
        
        test_args = ['main.py', str(spaced_file), '--output', str(spaced_output)]
        monkeypatch.setattr('sys.argv', test_args)
        
        main()
        
        # Should handle spaced paths without issues
        assert spaced_output.exists()
        assert (spaced_output / "analysis").exists()
    
    def test_cli_preserves_file_encoding(self, tmp_path, monkeypatch):
        """Test that CLI preserves UTF-8 encoding in output files."""
        # Create Thai text file
        thai_file = tmp_path / "thai_content.txt"
        thai_content = "วิเคราะห์ตัวเลขไทย ๑๒๓๔๕ และตัวเลขสากล 67890"
        thai_file.write_text(thai_content, encoding='utf-8')
        
        test_args = ['main.py', str(thai_file), '--output', str(tmp_path)]
        monkeypatch.setattr('sys.argv', test_args)
        
        main()
        
        # Check that output files preserve Thai characters
        text_analysis_file = tmp_path / "analysis" / "text_analysis.txt"
        assert text_analysis_file.exists()
        
        content = text_analysis_file.read_text(encoding='utf-8')
        assert "๑๒๓๔๕" in content  # Thai digits should be preserved


class TestErrorHandling:
    """Test suite for error handling and edge cases."""
    
    def test_cli_handles_empty_document(self, tmp_path, monkeypatch, capsys):
        """Test CLI with empty document."""
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("", encoding='utf-8')
        
        test_args = ['main.py', str(empty_file), '--output', str(tmp_path)]
        monkeypatch.setattr('sys.argv', test_args)
        
        main()
        
        # Should handle empty document gracefully
        captured = capsys.readouterr()
        assert "Analysis complete!" in captured.out
        
        # Files should still be created
        assert (tmp_path / "analysis" / "text_analysis.txt").exists()
    
    def test_cli_handles_document_without_digits(self, tmp_path, monkeypatch, capsys):
        """Test CLI with document containing no digits."""
        no_digits_file = tmp_path / "no_digits.txt"
        no_digits_file.write_text("สวัสดี Hello World ไม่มีตัวเลข", encoding='utf-8')
        
        test_args = ['main.py', str(no_digits_file), '--output', str(tmp_path)]
        monkeypatch.setattr('sys.argv', test_args)
        
        main()
        
        # Should handle no digits gracefully
        captured = capsys.readouterr()
        assert "Analysis complete!" in captured.out
    
    def test_cli_handles_read_only_output_directory(self, sample_thai_text_file, tmp_path, monkeypatch):
        """Test CLI with read-only output directory."""
        readonly_dir = tmp_path / "readonly"
        readonly_dir.mkdir()
        readonly_dir.chmod(0o444)  # Read-only
        
        test_args = ['main.py', sample_thai_text_file, '--output', str(readonly_dir)]
        monkeypatch.setattr('sys.argv', test_args)
        
        try:
            # Should handle permission errors gracefully
            with pytest.raises((PermissionError, OSError)):
                main()
        finally:
            # Restore permissions for cleanup
            readonly_dir.chmod(0o755)
    
    def test_cli_invalid_arguments_show_help(self, monkeypatch, capsys):
        """Test that invalid arguments show help message."""
        test_args = ['main.py', '--invalid-argument']
        monkeypatch.setattr('sys.argv', test_args)
        
        with pytest.raises(SystemExit):
            main()
        
        captured = capsys.readouterr()
        # Should show help or error message
        assert len(captured.err) > 0 or len(captured.out) > 0


class TestEndToEndWorkflows:
    """Test suite for complete end-to-end workflows."""
    
    def test_complete_analysis_workflow(self, sample_thai_text_file, tmp_path, monkeypatch, capsys):
        """Test complete analysis workflow from start to finish."""
        json_file = tmp_path / "complete_analysis.json"
        markdown_file = tmp_path / "complete_report.md"
        
        # Step 1: Generate JSON analysis
        test_args = ['main.py', sample_thai_text_file, '--compare-all', '--output-json', str(json_file)]
        monkeypatch.setattr('sys.argv', test_args)
        main()
        
        capsys.readouterr()  # Clear output
        
        # Step 2: Render markdown from JSON
        test_args = ['main.py', '--render-from-json', str(json_file), '--format', 'markdown', '--output', str(tmp_path)]
        monkeypatch.setattr('sys.argv', test_args)
        main()
        
        # Verify complete workflow
        assert json_file.exists()
        
        # Check JSON content
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        assert len(json_data['typist_profiles']) == 4  # All typists
        assert len(json_data['analysis_results']) == 4
        
        # Check markdown files were created
        markdown_files = list(tmp_path.glob("*.md"))
        assert len(markdown_files) > 0
        
        # Verify markdown content quality
        markdown_content = markdown_files[0].read_text(encoding='utf-8')
        assert len(markdown_content) > 5000  # Substantial report
        assert "# Thai Numbers Typing Cost Analysis" in markdown_content
        assert "## Executive Summary" in markdown_content
        assert "## Conclusion & Recommendations" in markdown_content
    
    def test_data_consistency_across_formats(self, sample_thai_text_file, tmp_path, monkeypatch, capsys):
        """Test that data is consistent across different output formats."""
        json_file = tmp_path / "consistency_test.json"
        
        # Generate JSON
        test_args = ['main.py', sample_thai_text_file, '--output-json', str(json_file)]
        monkeypatch.setattr('sys.argv', test_args)
        main()
        
        # Load JSON data
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        capsys.readouterr()  # Clear output
        
        # Render console format and capture output
        test_args = ['main.py', '--render-from-json', str(json_file), '--format', 'console']
        monkeypatch.setattr('sys.argv', test_args)
        main()
        
        captured = capsys.readouterr()
        console_output = captured.out
        
        # Verify key data points are consistent
        key_findings = json_data['key_findings']
        time_saved = str(key_findings['improvement']['time_saved_minutes'])
        efficiency_gain = str(key_findings['improvement']['efficiency_gain_percentage'])
        
        assert time_saved in console_output
        assert efficiency_gain in console_output
        
        # Render markdown and check consistency
        test_args = ['main.py', '--render-from-json', str(json_file), '--format', 'markdown', '--output', str(tmp_path)]
        monkeypatch.setattr('sys.argv', test_args)
        main()
        
        markdown_files = list(tmp_path.glob("*.md"))
        markdown_content = markdown_files[0].read_text(encoding='utf-8')
        
        assert time_saved in markdown_content
        assert efficiency_gain in markdown_content


# Pytest markers
pytestmark = [pytest.mark.integration]