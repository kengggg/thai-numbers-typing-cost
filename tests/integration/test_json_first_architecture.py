import json
"""
Integration tests for JSON-first architecture.

Tests the complete data flow from analysis generation through JSON
to various output renderers, ensuring data integrity and portability.
"""

import pytest
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from generators.json_analysis_generator import JSONAnalysisGenerator
from renderers.markdown_renderer import render_json_to_markdown
from renderers.console_renderer import render_json_to_console


class TestJSONDataIntegrity:
    """Test suite for JSON data integrity across the pipeline."""

    def test_json_generation_to_markdown_pipeline(self, sample_thai_text_file, tmp_path):
        """Test complete pipeline from JSON generation to markdown rendering."""
        # Step 1: Generate JSON
        generator = JSONAnalysisGenerator(sample_thai_text_file)
        json_data = generator.generate_comprehensive_analysis(include_all_typists=True)

        # Step 2: Save JSON
        json_file = tmp_path / "pipeline_test.json"
        generator.save_to_file(json_data, str(json_file))

        # Step 3: Load JSON and render markdown
        loaded_data = generator.load_from_file(str(json_file))
        markdown_content = render_json_to_markdown(loaded_data)

        # Step 4: Save markdown
        markdown_file = tmp_path / "pipeline_test.md"
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        # Verify data integrity throughout pipeline
        assert json_data == loaded_data  # JSON round-trip integrity

        # Verify key data appears in markdown
        key_findings = json_data['key_findings']
        assert str(key_findings['improvement']['time_saved_minutes']) in markdown_content
        assert str(key_findings['improvement']['efficiency_gain_percentage']) in markdown_content
        assert key_findings['improvement']['root_cause'] in markdown_content

        # Verify markdown structure
        assert "# Thai Numbers Typing Cost Analysis - Research Report" in markdown_content
        assert "## Executive Summary" in markdown_content
        assert "## Research Questions Answered" in markdown_content
        assert "## Impact Analysis: Government Scale Projections" in markdown_content
        assert "## Conclusion & Recommendations" in markdown_content

    def test_json_generation_to_console_pipeline(self, sample_thai_text_file):
        """Test complete pipeline from JSON generation to console rendering."""
        # Step 1: Generate JSON
        generator = JSONAnalysisGenerator(sample_thai_text_file)
        json_data = generator.generate_comprehensive_analysis()

        # Step 2: Render to different console formats
        formats = ['summary', 'quick', 'scenarios', 'json', 'comprehensive']

        for format_type in formats:
            console_output = render_json_to_console(json_data, format_type)

            # Verify format-specific content
            if format_type == 'summary':
                assert "THAI NUMBERS TYPING COST ANALYSIS - SUMMARY" in console_output
            elif format_type == 'quick':
                assert "⚡ Quick result:" in console_output
            elif format_type == 'scenarios':
                assert "TYPING COST BY SCENARIO:" in console_output
            elif format_type == 'json':
                # Should be valid JSON
                parsed = json.loads(console_output)
                assert isinstance(parsed, dict)
            elif format_type == 'comprehensive':
                assert "THAI NUMBERS TYPING COST ANALYSIS - SUMMARY" in console_output
                assert "RECOMMENDATIONS:" in console_output

            # Verify key data appears in all formats
            key_findings = json_data['key_findings']
            time_saved = str(key_findings['improvement']['time_saved_minutes'])
            efficiency_gain = str(key_findings['improvement']['efficiency_gain_percentage'])

            assert time_saved in console_output
            assert efficiency_gain in console_output

    def test_json_schema_consistency(self, sample_thai_text_file):
        """Test that JSON schema is consistent across different configurations."""
        generator = JSONAnalysisGenerator(sample_thai_text_file)

        # Test different configurations
        configs = [
            {'include_all_typists': False},
            {'include_all_typists': True}
        ]

        schemas = []
        for config in configs:
            json_data = generator.generate_comprehensive_analysis(**config)

            # Extract schema (structure and keys)
            schema = extract_json_schema(json_data)
            schemas.append(schema)

        # All schemas should have the same top-level structure
        base_schema = schemas[0]
        for schema in schemas[1:]:
            assert schema['top_level_keys'] == base_schema['top_level_keys']
            assert schema['metadata_keys'] == base_schema['metadata_keys']
            assert schema['key_findings_keys'] == base_schema['key_findings_keys']

        # But typist profiles should differ based on include_all_typists
        single_typist_data = generator.generate_comprehensive_analysis(include_all_typists=False)
        all_typists_data = generator.generate_comprehensive_analysis(include_all_typists=True)

        assert len(single_typist_data['typist_profiles']) == 1
        assert len(all_typists_data['typist_profiles']) == 4
        assert len(single_typist_data['analysis_results']) == 1
        assert len(all_typists_data['analysis_results']) == 4

    def test_unicode_preservation_through_pipeline(self, tmp_path):
        """Test that Unicode content is preserved throughout the JSON-first pipeline."""
        # Create Thai text file with comprehensive Unicode content
        thai_file = tmp_path / "unicode_test.txt"
        unicode_content = """พระราชบัญญัติรัฐธรรมนูญแห่งราชอาณาจักรไทย พุทธศักราช ๒๕๖๐

รัชกาลที่ ๑๐ ทรงครองราชย์ในปี ๒๕๖๐
มีตัวเลขไทย: ๑๒๓๔๕๖๗๘๙๐
มีตัวเลขสากล: 1234567890
ข้อความภาษาไทย: การวิเคราะห์ประสิทธิภาพการพิมพ์
ตัวอักษรพิเศษ: ก่ ข่ ค่ ง่ จ๊ ฉ๋ ช์ ซํ ฏ๎ ฐ๏"""

        thai_file.write_text(unicode_content, encoding='utf-8')

        # Generate JSON
        generator = JSONAnalysisGenerator(str(thai_file))
        json_data = generator.generate_comprehensive_analysis()

        # Save and reload JSON
        json_file = tmp_path / "unicode_test.json"
        generator.save_to_file(json_data, str(json_file))
        loaded_data = generator.load_from_file(str(json_file))

        # Verify Unicode preservation in JSON
        assert json_data == loaded_data

        # Check that Thai content appears in various sections
        assert '๒๕๖๐' in str(loaded_data)  # Thai year
        assert 'พระราชบัญญัติ' in str(loaded_data)  # Thai text
        assert 'การวิเคราะห์' in str(loaded_data)  # Thai text

        # Render to markdown and verify Unicode preservation
        markdown_content = render_json_to_markdown(loaded_data)
        markdown_file = tmp_path / "unicode_test.md"
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        # Reload markdown and verify Unicode
        saved_markdown = markdown_file.read_text(encoding='utf-8')
        assert '๐-๙' in saved_markdown  # Thai digits range that appears in executive summary
        assert 'Thai' in saved_markdown  # Thai text should be present

        # Render to console and verify Unicode preservation
        console_output = render_json_to_console(loaded_data, 'comprehensive')
        assert 'THAI NUMBERS TYPING COST ANALYSIS' in console_output  # Should have Thai text

    def test_data_precision_preservation(self, sample_thai_text_file):
        """Test that numerical precision is preserved through JSON serialization."""
        generator = JSONAnalysisGenerator(sample_thai_text_file)
        original_data = generator.generate_comprehensive_analysis()

        # Serialize to JSON string and back
        json_string = json.dumps(original_data, ensure_ascii=False, indent=2)
        reconstructed_data = json.loads(json_string)

        # Check that numerical values are precisely preserved
        def compare_numerical_values(original, reconstructed, path=""):
            if isinstance(original, dict):
                for key, value in original.items():
                    compare_numerical_values(value, reconstructed[key], f"{path}.{key}")
            elif isinstance(original, list):
                for i, value in enumerate(original):
                    compare_numerical_values(value, reconstructed[i], f"{path}[{i}]")
            elif isinstance(original, (int, float)):
                assert original == reconstructed, f"Precision lost at {path}: {original} != {reconstructed}"
                if isinstance(original, float):
                    # Check precision to reasonable decimal places
                    assert abs(original - reconstructed) < 1e-10, f"Float precision lost at {path}"

        compare_numerical_values(original_data, reconstructed_data)


class TestCrossFormatConsistency:
    """Test suite for consistency across different output formats."""

    def test_key_metrics_consistency(self, sample_thai_text_file):
        """Test that key metrics are consistent across all output formats."""
        generator = JSONAnalysisGenerator(sample_thai_text_file)
        json_data = generator.generate_comprehensive_analysis()

        # Extract key metrics from JSON
        key_findings = json_data['key_findings']
        expected_metrics = {
            'time_saved_minutes': key_findings['improvement']['time_saved_minutes'],
            'efficiency_gain_percentage': key_findings['improvement']['efficiency_gain_percentage'],
            'current_time_minutes': key_findings['current_state']['time_minutes'],
            'optimal_time_minutes': key_findings['optimal_state']['time_minutes']
        }

        # Test markdown renderer
        markdown_content = render_json_to_markdown(json_data)
        for metric_name, metric_value in expected_metrics.items():
            assert str(metric_value) in markdown_content, f"Missing {metric_name} in markdown"

        # Test console renderer (different formats)
        console_formats = ['summary', 'quick', 'comprehensive', 'json']
        for format_type in console_formats:
            console_output = render_json_to_console(json_data, format_type)

            # At least time_saved_minutes and efficiency_gain should appear in all formats
            assert str(expected_metrics['time_saved_minutes']) in console_output
            assert str(expected_metrics['efficiency_gain_percentage']) in console_output

    def test_research_questions_consistency(self, sample_thai_text_file):
        """Test that research questions are consistently represented across formats."""
        generator = JSONAnalysisGenerator(sample_thai_text_file)
        json_data = generator.generate_comprehensive_analysis()

        research_questions = json_data['research_questions']

        # Test markdown renderer
        markdown_content = render_json_to_markdown(json_data)

        for q_id, question_data in research_questions.items():
            question_text = question_data['question']
            answer_text = question_data['answer']

            # Question and answer should appear in markdown
            assert question_text in markdown_content
            assert answer_text in markdown_content

        # Test console renderer
        console_output = render_json_to_console(json_data, 'comprehensive')

        # At least some research question content should appear
        assert "Research Questions" in console_output or "RESEARCH" in console_output

    def test_recommendations_consistency(self, sample_thai_text_file):
        """Test that recommendations are consistently represented across formats."""
        generator = JSONAnalysisGenerator(sample_thai_text_file)
        json_data = generator.generate_comprehensive_analysis()

        recommendations = json_data['recommendations']
        primary_action = recommendations['primary_recommendation']['action']

        # Test markdown renderer
        markdown_content = render_json_to_markdown(json_data)
        assert primary_action in markdown_content

        # Implementation steps should appear
        for step in recommendations['implementation_steps']:
            assert step in markdown_content

        # Benefits should appear (check for key content, accounting for markdown formatting)
        for benefit in recommendations['benefits']:
            # Extract the core content (after the colon if present)
            if ':' in benefit:
                core_content = benefit.split(':', 1)[1].strip()
            else:
                core_content = benefit
            assert core_content in markdown_content

        # Test console renderer
        console_output = render_json_to_console(json_data, 'comprehensive')
        assert primary_action in console_output

        # At least some implementation steps should appear
        for step in recommendations['implementation_steps'][:3]:  # First 3 steps
            assert step in console_output


class TestScalabilityAndPerformance:
    """Test suite for scalability and performance of JSON-first architecture."""

    def test_large_document_json_generation(self, tmp_path):
        """Test JSON generation performance with larger documents."""
        # Create a larger test document
        large_content = """พระราชบัญญัติรัฐธรรมนูญแห่งราชอาณาจักรไทย พุทธศักราช ๒๕๖๐

ปี ๒๕๖๐ เป็นปีสำคัญในประวัติศาสตร์ไทย มีการใช้ตัวเลขไทย ๑๒๓๔๕๖๗๘๙๐
และตัวเลขสากล 1234567890 ในเอกสารราชการต่างๆ

""" * 100  # Repeat 100 times to create larger document

        large_file = tmp_path / "large_document.txt"
        large_file.write_text(large_content, encoding='utf-8')

        # Test JSON generation performance
        generator = JSONAnalysisGenerator(str(large_file))

        # Should complete without performance issues
        json_data = generator.generate_comprehensive_analysis(include_all_typists=True)

        # Verify data quality
        assert json_data['metadata']['document_stats']['total_characters'] > 10000
        assert json_data['metadata']['document_stats']['total_digits'] > 100

        # Test JSON serialization performance
        json_file = tmp_path / "large_analysis.json"
        saved_path = generator.save_to_file(json_data, str(json_file))

        assert Path(saved_path).exists()
        assert Path(saved_path).stat().st_size > 1000  # Should be substantial

        # Test loading performance
        loaded_data = generator.load_from_file(saved_path)
        assert loaded_data == json_data

    def test_multiple_format_rendering_performance(self, sample_thai_text_file):
        """Test performance of rendering to multiple formats from same JSON."""
        generator = JSONAnalysisGenerator(sample_thai_text_file)
        json_data = generator.generate_comprehensive_analysis(include_all_typists=True)

        # Test rendering to multiple formats quickly
        formats = ['markdown', 'summary', 'quick', 'scenarios', 'json', 'comprehensive']

        results = {}
        for format_type in formats:
            if format_type == 'markdown':
                results[format_type] = render_json_to_markdown(json_data)
            else:
                results[format_type] = render_json_to_console(json_data, format_type)

        # Verify all formats produced output
        for format_type, output in results.items():
            assert isinstance(output, str)
            assert len(output) > 100  # Should have substantial content

        # Verify markdown is significantly longer than other formats
        assert len(results['markdown']) > len(results['summary'])
        assert len(results['comprehensive']) > len(results['quick'])

    def test_json_file_size_efficiency(self, sample_thai_text_file, tmp_path):
        """Test that JSON files are reasonably sized and efficient."""
        generator = JSONAnalysisGenerator(sample_thai_text_file)

        # Test different configurations
        single_typist_data = generator.generate_comprehensive_analysis(include_all_typists=False)
        all_typists_data = generator.generate_comprehensive_analysis(include_all_typists=True)

        # Save both configurations
        single_file = tmp_path / "single_typist.json"
        all_file = tmp_path / "all_typists.json"

        generator.save_to_file(single_typist_data, str(single_file))
        generator.save_to_file(all_typists_data, str(all_file))

        # Check file sizes
        single_size = single_file.stat().st_size
        all_size = all_file.stat().st_size

        # All typists file should be larger but not excessively so
        assert all_size > single_size
        assert all_size < single_size * 10  # Should not be more than 10x larger

        # Both files should be reasonably sized (not too small or too large)
        assert single_size > 1000  # At least 1KB
        assert single_size < 1000000  # Less than 1MB
        assert all_size > 2000  # At least 2KB
        assert all_size < 2000000  # Less than 2MB


# Helper functions
def extract_json_schema(json_data):
    """Extract schema information from JSON data for comparison."""
    schema = {
        'top_level_keys': set(json_data.keys()),
        'metadata_keys': set(json_data.get('metadata', {}).keys()),
        'key_findings_keys': set(json_data.get('key_findings', {}).keys()),
    }

    if 'key_findings' in json_data and 'improvement' in json_data['key_findings']:
        schema['improvement_keys'] = set(json_data['key_findings']['improvement'].keys())

    return schema


# Pytest markers
pytestmark = [pytest.mark.integration]
