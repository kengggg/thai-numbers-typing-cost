import json
from datetime import datetime
from unittest.mock import patch
"""
Unit tests for JSONAnalysisGenerator class.

Tests JSON generation functionality including comprehensive analysis,
data structure validation, and file I/O operations.
"""

import pytest
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from generators.json_analysis_generator import JSONAnalysisGenerator


class TestJSONAnalysisGeneratorInitialization:
    """Test suite for JSONAnalysisGenerator initialization."""

    def test_initialization_basic(self, sample_thai_text_file):
        """Test basic initialization."""
        generator = JSONAnalysisGenerator(sample_thai_text_file)

        assert generator.document_path == sample_thai_text_file
        assert generator.analyzer is not None
        assert isinstance(generator.generated_at, datetime)

    def test_initialization_with_nonexistent_file(self, tmp_path):
        """Test initialization with nonexistent file."""
        nonexistent_file = tmp_path / "nonexistent.txt"

        with pytest.raises(FileNotFoundError):
            JSONAnalysisGenerator(str(nonexistent_file))

    def test_generated_at_timestamp(self, sample_thai_text_file):
        """Test that generated_at timestamp is properly set."""
        before_creation = datetime.now()
        generator = JSONAnalysisGenerator(sample_thai_text_file)
        after_creation = datetime.now()

        assert before_creation <= generator.generated_at <= after_creation


class TestMetadataGeneration:
    """Test suite for metadata generation."""

    def test_generate_metadata_structure(self, json_analysis_generator):
        """Test metadata section structure."""
        stats = json_analysis_generator.analyzer.get_statistics()
        metadata = json_analysis_generator._generate_metadata(stats)

        required_keys = [
            'generated_at', 'tool_version', 'document_path',
            'document_stats', 'analysis_focus'
        ]

        for key in required_keys:
            assert key in metadata, f"Missing metadata key: {key}"

    def test_generate_metadata_document_stats(self, json_analysis_generator):
        """Test document statistics in metadata."""
        stats = json_analysis_generator.analyzer.get_statistics()
        metadata = json_analysis_generator._generate_metadata(stats)

        doc_stats = metadata['document_stats']
        required_stats = [
            'total_characters', 'total_digits', 'digit_percentage',
            'thai_digits', 'international_digits'
        ]

        for key in required_stats:
            assert key in doc_stats, f"Missing document stat: {key}"

        # Verify data consistency
        assert doc_stats['total_digits'] == doc_stats['thai_digits'] + doc_stats['international_digits']

    def test_generate_metadata_iso_timestamp(self, json_analysis_generator):
        """Test that timestamp is in ISO format."""
        stats = json_analysis_generator.analyzer.get_statistics()
        metadata = json_analysis_generator._generate_metadata(stats)

        timestamp_str = metadata['generated_at']

        # Should be able to parse back to datetime
        parsed_dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        assert isinstance(parsed_dt, datetime)

    def test_generate_metadata_document_name_only(self, tmp_path):
        """Test that only filename (not full path) is included in metadata."""
        test_file = tmp_path / "subdir" / "test_document.txt"
        test_file.parent.mkdir()
        test_file.write_text("ปี ๒๕๖๐", encoding='utf-8')

        generator = JSONAnalysisGenerator(str(test_file))
        stats = generator.analyzer.get_statistics()
        metadata = generator._generate_metadata(stats)

        assert metadata['document_path'] == "test_document.txt"


class TestDocumentAnalysisGeneration:
    """Test suite for document analysis generation."""

    def test_generate_document_analysis_structure(self, json_analysis_generator):
        """Test document analysis section structure."""
        stats = json_analysis_generator.analyzer.get_statistics()
        doc_analysis = json_analysis_generator._generate_document_analysis(stats)

        required_keys = ['digit_distribution', 'number_sequences', 'sample_contexts']

        for key in required_keys:
            assert key in doc_analysis, f"Missing document analysis key: {key}"

    def test_generate_document_analysis_digit_distribution(self, json_analysis_generator):
        """Test digit distribution analysis."""
        stats = json_analysis_generator.analyzer.get_statistics()
        doc_analysis = json_analysis_generator._generate_document_analysis(stats)

        digit_dist = doc_analysis['digit_distribution']

        assert 'thai_digits' in digit_dist
        assert isinstance(digit_dist['thai_digits'], dict)

        # Should have most/least frequent digits if Thai digits exist
        if digit_dist['thai_digits']:
            assert 'most_frequent_digit' in digit_dist
            assert 'least_frequent_digit' in digit_dist
            assert digit_dist['most_frequent_digit'] is not None
            assert digit_dist['least_frequent_digit'] is not None

    def test_generate_document_analysis_number_sequences(self, json_analysis_generator):
        """Test number sequences analysis."""
        stats = json_analysis_generator.analyzer.get_statistics()
        doc_analysis = json_analysis_generator._generate_document_analysis(stats)

        num_seq = doc_analysis['number_sequences']
        required_keys = ['total_sequences', 'thai_sequences', 'average_thai_length']

        for key in required_keys:
            assert key in num_seq, f"Missing number sequence key: {key}"
            assert isinstance(num_seq[key], (int, float))

    def test_generate_document_analysis_sample_contexts(self, json_analysis_generator):
        """Test sample contexts generation."""
        stats = json_analysis_generator.analyzer.get_statistics()
        doc_analysis = json_analysis_generator._generate_document_analysis(stats)

        contexts = doc_analysis['sample_contexts']
        assert isinstance(contexts, list)
        assert len(contexts) <= 5  # Should limit to 5 contexts

        for context in contexts:
            required_keys = ['number', 'type', 'context']
            for key in required_keys:
                assert key in context, f"Missing context key: {key}"


class TestTypistProfilesGeneration:
    """Test suite for typist profiles generation."""

    def test_generate_typist_profiles_single(self, json_analysis_generator):
        """Test generation of single typist profile."""
        profiles = {'average': {
            'name': 'Average Non-secretarial',
            'keystroke_time': 0.28,
            'description': 'Average office worker'
        }}

        result = json_analysis_generator._generate_typist_profiles(profiles)

        assert 'average' in result
        profile = result['average']

        required_keys = ['name', 'keystroke_time', 'description']
        for key in required_keys:
            assert key in profile, f"Missing profile key: {key}"

        assert profile['name'] == 'Average Non-secretarial'
        assert profile['keystroke_time'] == 0.28

    def test_generate_typist_profiles_multiple(self, json_analysis_generator, typist_profiles):
        """Test generation of multiple typist profiles."""
        result = json_analysis_generator._generate_typist_profiles(typist_profiles)

        assert len(result) == len(typist_profiles)

        for profile_key in typist_profiles.keys():
            assert profile_key in result

            profile = result[profile_key]
            original = typist_profiles[profile_key]

            assert profile['name'] == original['name']
            assert profile['keystroke_time'] == original['keystroke_time']
            assert profile['description'] == original['description']


class TestAnalysisResultsGeneration:
    """Test suite for analysis results generation."""

    def test_generate_analysis_results_structure(self, json_analysis_generator, typist_profiles):
        """Test analysis results structure."""
        # Use single profile for faster testing
        single_profile = {'average': typist_profiles['average']}

        results = json_analysis_generator._generate_analysis_results(single_profile)

        assert 'average' in results
        profile_result = results['average']

        required_keys = ['scenarios', 'savings_analysis', 'optimal_scenario']
        for key in required_keys:
            assert key in profile_result, f"Missing result key: {key}"

    def test_generate_analysis_results_scenarios(self, json_analysis_generator, typist_profiles):
        """Test scenarios in analysis results."""
        single_profile = {'average': typist_profiles['average']}
        results = json_analysis_generator._generate_analysis_results(single_profile)

        scenarios = results['average']['scenarios']

        expected_scenarios = ['thai_kedmanee', 'intl_kedmanee', 'thai_pattajoti', 'intl_pattajoti']
        for scenario_name in expected_scenarios:
            assert scenario_name in scenarios, f"Missing scenario: {scenario_name}"

            scenario = scenarios[scenario_name]
            required_keys = [
                'description', 'total_cost_seconds', 'total_cost_minutes',
                'total_cost_hours', 'average_cost_per_char_ms',
                'keyboard_layout', 'conversion_applied'
            ]

            for key in required_keys:
                assert key in scenario, f"Missing scenario key: {key}"

    def test_generate_analysis_results_savings_analysis(self, json_analysis_generator, typist_profiles):
        """Test savings analysis in results."""
        single_profile = {'average': typist_profiles['average']}
        results = json_analysis_generator._generate_analysis_results(single_profile)

        savings = results['average']['savings_analysis']

        # Should have savings for all scenarios except baseline
        expected_savings = ['intl_kedmanee', 'thai_pattajoti', 'intl_pattajoti']
        for scenario_name in expected_savings:
            assert scenario_name in savings, f"Missing savings for: {scenario_name}"

            saving = savings[scenario_name]
            required_keys = [
                'time_saved_minutes', 'time_saved_hours',
                'percentage_saved', 'description'
            ]

            for key in required_keys:
                assert key in saving, f"Missing savings key: {key}"

    def test_get_scenario_description(self, json_analysis_generator):
        """Test scenario description generation."""
        descriptions = {
            'thai_kedmanee': 'Thai digits on Kedmanee keyboard (current state)',
            'intl_kedmanee': 'International digits on Kedmanee keyboard',
            'thai_pattajoti': 'Thai digits on Pattajoti keyboard',
            'intl_pattajoti': 'International digits on Pattajoti keyboard (optimal)'
        }

        for scenario_key, expected_desc in descriptions.items():
            result = json_analysis_generator._get_scenario_description(scenario_key)
            assert result == expected_desc

        # Test unknown scenario
        unknown_result = json_analysis_generator._get_scenario_description('unknown')
        assert unknown_result == 'unknown'


class TestResearchQuestionsGeneration:
    """Test suite for research questions generation."""

    def test_generate_research_questions_structure(self, json_analysis_generator):
        """Test research questions structure."""
        research_q = json_analysis_generator._generate_research_questions()

        expected_questions = ['q1', 'q2', 'q3', 'q4', 'q5']

        for q_key in expected_questions:
            assert q_key in research_q, f"Missing research question: {q_key}"

            question = research_q[q_key]
            required_keys = ['question', 'answer', 'details']

            for key in required_keys:
                assert key in question, f"Missing question key: {key}"

    def test_generate_research_questions_content(self, json_analysis_generator):
        """Test research questions content quality."""
        research_q = json_analysis_generator._generate_research_questions()

        # Q1 should be about Thai digits on Kedmanee
        q1 = research_q['q1']
        assert 'Thai digits' in q1['question']
        assert 'Kedmanee' in q1['question']
        assert 'SHIFT' in q1['details']['why_higher_cost']

        # Q5 should be about productivity loss
        q5 = research_q['q5']
        assert 'LOST' in q5['question'] or 'productivity' in q5['question']
        assert 'efficiency_loss_percentage' in q5['details']


class TestImpactProjectionsGeneration:
    """Test suite for impact projections generation."""

    def test_generate_impact_projections_structure(self, json_analysis_generator):
        """Test impact projections structure."""
        impact = json_analysis_generator._generate_impact_projections()

        required_keys = [
            'per_document_savings_minutes', 'per_document_savings_hours',
            'government_scale_projections', 'assumptions'
        ]

        for key in required_keys:
            assert key in impact, f"Missing impact key: {key}"

    def test_generate_impact_projections_scales(self, json_analysis_generator):
        """Test government scale projections."""
        impact = json_analysis_generator._generate_impact_projections()

        projections = impact['government_scale_projections']
        assert isinstance(projections, list)
        assert len(projections) == 4  # Should have 4 scales

        for projection in projections:
            required_keys = [
                'scale', 'docs_per_day', 'annual_hours_saved', 'annual_cost_savings'
            ]

            for key in required_keys:
                assert key in projection, f"Missing projection key: {key}"

            # Verify calculations are reasonable
            assert projection['docs_per_day'] > 0
            assert projection['annual_hours_saved'] >= 0
            assert projection['annual_cost_savings'] >= 0

    def test_generate_impact_projections_assumptions(self, json_analysis_generator):
        """Test impact projections assumptions."""
        impact = json_analysis_generator._generate_impact_projections()

        assumptions = impact['assumptions']
        assert 'working_days_per_year' in assumptions
        assert 'hourly_labor_cost' in assumptions

        assert assumptions['working_days_per_year'] == 250
        assert assumptions['hourly_labor_cost'] == 15


class TestKeyFindingsGeneration:
    """Test suite for key findings generation."""

    def test_generate_key_findings_structure(self, json_analysis_generator):
        """Test key findings structure."""
        findings = json_analysis_generator._generate_key_findings()

        required_keys = ['current_state', 'optimal_state', 'improvement']

        for key in required_keys:
            assert key in findings, f"Missing findings key: {key}"

    def test_generate_key_findings_states(self, json_analysis_generator):
        """Test current and optimal state descriptions."""
        findings = json_analysis_generator._generate_key_findings()

        current = findings['current_state']
        optimal = findings['optimal_state']

        # Current state should mention Thai digits and Kedmanee
        assert 'Thai digits' in current['description']
        assert 'Kedmanee' in current['description']

        # Optimal state should mention international digits and Pattajoti
        assert 'International digits' in optimal['description']
        assert 'Pattajoti' in optimal['description']

        # Both should have time measurements
        for state in [current, optimal]:
            assert 'time_minutes' in state
            assert 'time_hours' in state
            assert isinstance(state['time_minutes'], (int, float))
            assert isinstance(state['time_hours'], (int, float))

    def test_generate_key_findings_improvement(self, json_analysis_generator):
        """Test improvement calculations."""
        findings = json_analysis_generator._generate_key_findings()

        improvement = findings['improvement']
        required_keys = [
            'time_saved_minutes', 'efficiency_gain_percentage', 'root_cause'
        ]

        for key in required_keys:
            assert key in improvement, f"Missing improvement key: {key}"

        # Verify calculations are reasonable
        assert improvement['time_saved_minutes'] >= 0
        assert improvement['efficiency_gain_percentage'] >= 0
        assert 'SHIFT' in improvement['root_cause']


class TestRecommendationsGeneration:
    """Test suite for recommendations generation."""

    def test_generate_recommendations_structure(self, json_analysis_generator):
        """Test recommendations structure."""
        recommendations = json_analysis_generator._generate_recommendations()

        required_keys = [
            'primary_recommendation', 'implementation_steps',
            'benefits', 'risk_assessment'
        ]

        for key in required_keys:
            assert key in recommendations, f"Missing recommendation key: {key}"

    def test_generate_recommendations_primary(self, json_analysis_generator):
        """Test primary recommendation."""
        recommendations = json_analysis_generator._generate_recommendations()

        primary = recommendations['primary_recommendation']
        assert 'action' in primary
        assert 'rationale' in primary

        # Should recommend international digits
        assert 'international digits' in primary['action']

    def test_generate_recommendations_implementation(self, json_analysis_generator):
        """Test implementation steps."""
        recommendations = json_analysis_generator._generate_recommendations()

        steps = recommendations['implementation_steps']
        assert isinstance(steps, list)
        assert len(steps) > 0

        # Should be actionable steps
        for step in steps:
            assert isinstance(step, str)
            assert len(step) > 10  # Should be meaningful descriptions

    def test_generate_recommendations_benefits(self, json_analysis_generator):
        """Test benefits list."""
        recommendations = json_analysis_generator._generate_recommendations()

        benefits = recommendations['benefits']
        assert isinstance(benefits, list)
        assert len(benefits) > 0

        # Should mention cost and time savings
        benefits_text = ' '.join(benefits)
        assert 'cost' in benefits_text.lower() or 'minutes' in benefits_text.lower()

    def test_generate_recommendations_risk_assessment(self, json_analysis_generator):
        """Test risk assessment."""
        recommendations = json_analysis_generator._generate_recommendations()

        risks = recommendations['risk_assessment']
        risk_types = ['implementation_risk', 'technical_risk', 'user_adoption_risk']

        for risk_type in risk_types:
            assert risk_type in risks, f"Missing risk type: {risk_type}"


class TestComprehensiveAnalysis:
    """Test suite for comprehensive analysis generation."""

    def test_generate_comprehensive_analysis_single_typist(self, json_analysis_generator):
        """Test comprehensive analysis with single typist."""
        analysis = json_analysis_generator.generate_comprehensive_analysis(include_all_typists=False)

        required_sections = [
            'metadata', 'document_analysis', 'typist_profiles',
            'analysis_results', 'research_questions', 'impact_projections',
            'key_findings', 'recommendations'
        ]

        for section in required_sections:
            assert section in analysis, f"Missing analysis section: {section}"

        # Should only have average typist
        assert len(analysis['typist_profiles']) == 1
        assert 'average' in analysis['typist_profiles']

    @patch('generators.json_analysis_generator.TypistProfile')
    def test_generate_comprehensive_analysis_all_typists(self, mock_typist_profile, json_analysis_generator):
        """Test comprehensive analysis with all typists."""
        # Mock the TypistProfile class to avoid importing main
        mock_profiles = {
            'expert': {'name': 'Expert', 'keystroke_time': 0.12, 'description': 'Expert'},
            'average': {'name': 'Average', 'keystroke_time': 0.28, 'description': 'Average'},
            'worst': {'name': 'Worst', 'keystroke_time': 1.2, 'description': 'Worst'}
        }
        mock_typist_profile.PROFILES = mock_profiles

        analysis = json_analysis_generator.generate_comprehensive_analysis(include_all_typists=True)

        # Should have all typist profiles
        assert len(analysis['typist_profiles']) == 3
        for profile_key in mock_profiles.keys():
            assert profile_key in analysis['typist_profiles']
            assert profile_key in analysis['analysis_results']

    def test_generate_comprehensive_analysis_json_serializable(self, json_analysis_generator):
        """Test that comprehensive analysis is JSON serializable."""
        analysis = json_analysis_generator.generate_comprehensive_analysis()

        # Should be able to serialize to JSON without errors
        json_str = json.dumps(analysis, ensure_ascii=False, indent=2)
        assert isinstance(json_str, str)
        assert len(json_str) > 1000  # Should be substantial content

        # Should be able to deserialize back
        parsed = json.loads(json_str)
        assert parsed == analysis


class TestFileOperations:
    """Test suite for file operations."""

    def test_save_to_file_basic(self, json_analysis_generator, tmp_path):
        """Test basic file saving."""
        analysis_data = {"test": "data", "number": 123}
        output_file = tmp_path / "test_output.json"

        json_analysis_generator.save_to_file(analysis_data, str(output_file))

        # File path should match
        assert output_file.exists()

        # Verify content
        with open(output_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)

        assert loaded_data == analysis_data

    def test_save_to_file_creates_directories(self, json_analysis_generator, tmp_path):
        """Test that save_to_file creates necessary directories."""
        analysis_data = {"test": "data"}
        output_file = tmp_path / "nested" / "subdir" / "output.json"

        json_analysis_generator.save_to_file(analysis_data, str(output_file))

        # File path should match
        assert output_file.exists()
        assert output_file.parent.exists()

    def test_save_to_file_unicode_content(self, json_analysis_generator, tmp_path):
        """Test saving file with Unicode content."""
        analysis_data = {
            "thai_text": "ปี ๒๕๖๐",
            "chinese_text": "中文",
            "emoji": "🎉📊"
        }
        output_file = tmp_path / "unicode_output.json"

        json_analysis_generator.save_to_file(analysis_data, str(output_file))

        # Verify Unicode content is preserved
        with open(output_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)

        assert loaded_data == analysis_data
        assert loaded_data["thai_text"] == "ปี ๒๕๖๐"

    def test_load_from_file_basic(self, json_analysis_generator, tmp_path):
        """Test basic file loading."""
        test_data = {"test": "data", "number": 456}
        json_file = tmp_path / "test_input.json"

        # Create test file
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False)

        loaded_data = json_analysis_generator.load_from_file(str(json_file))

        assert loaded_data == test_data

    def test_load_from_file_nonexistent(self, json_analysis_generator, tmp_path):
        """Test loading from nonexistent file."""
        nonexistent_file = tmp_path / "nonexistent.json"

        with pytest.raises(FileNotFoundError):
            json_analysis_generator.load_from_file(str(nonexistent_file))

    def test_load_from_file_invalid_json(self, json_analysis_generator, tmp_path):
        """Test loading from file with invalid JSON."""
        invalid_file = tmp_path / "invalid.json"
        invalid_file.write_text("invalid json content", encoding='utf-8')

        with pytest.raises(json.JSONDecodeError):
            json_analysis_generator.load_from_file(str(invalid_file))

    def test_round_trip_file_operations(self, json_analysis_generator, tmp_path):
        """Test save and load round trip."""
        # Generate comprehensive analysis
        original_data = json_analysis_generator.generate_comprehensive_analysis()

        # Save to file
        output_file = tmp_path / "round_trip.json"
        saved_path = json_analysis_generator.save_to_file(original_data, str(output_file))

        # Load back from file
        loaded_data = json_analysis_generator.load_from_file(saved_path)

        # Should be identical
        assert loaded_data == original_data


class TestMainFunction:
    """Test suite for main function when run as script."""

    def test_main_function_with_valid_args(self, sample_thai_text_file, tmp_path, monkeypatch, capsys):
        """Test main function with valid command line arguments."""
        output_file = tmp_path / "main_output.json"
        test_args = ['json_analysis_generator.py', sample_thai_text_file, str(output_file)]
        monkeypatch.setattr('sys.argv', test_args)

        # Import and run main (this executes the if __name__ == "__main__" block)
        from generators.json_analysis_generator import main
        main()

        # Check output
        captured = capsys.readouterr()
        assert "Analysis completed and saved to:" in captured.out
        assert str(output_file) in captured.out

        # Verify file was created
        assert output_file.exists()

    def test_main_function_default_output(self, sample_thai_text_file, monkeypatch, capsys):
        """Test main function with default output filename."""
        test_args = ['json_analysis_generator.py', sample_thai_text_file]
        monkeypatch.setattr('sys.argv', test_args)

        # Import and run main
        from generators.json_analysis_generator import main
        main()

        captured = capsys.readouterr()
        assert "analysis_results.json" in captured.out

    def test_main_function_insufficient_args(self, monkeypatch, capsys):
        """Test main function with insufficient arguments."""
        test_args = ['json_analysis_generator.py']
        monkeypatch.setattr('sys.argv', test_args)

        with pytest.raises(SystemExit) as exc_info:
            from generators.json_analysis_generator import main
            main()

        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Usage:" in captured.out


class TestEdgeCases:
    """Test suite for edge cases and error conditions."""

    def test_empty_document_analysis(self, tmp_path):
        """Test analysis with empty document."""
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("", encoding='utf-8')

        generator = JSONAnalysisGenerator(str(empty_file))
        analysis = generator.generate_comprehensive_analysis()

        # Should handle empty document gracefully
        assert analysis['metadata']['document_stats']['total_characters'] == 0
        assert analysis['metadata']['document_stats']['total_digits'] == 0
        assert len(analysis['document_analysis']['sample_contexts']) == 0

    def test_document_without_digits(self, tmp_path):
        """Test analysis with document containing no digits."""
        no_digits_file = tmp_path / "no_digits.txt"
        no_digits_file.write_text("สวัสดี Hello World ไม่มีตัวเลข", encoding='utf-8')

        generator = JSONAnalysisGenerator(str(no_digits_file))
        analysis = generator.generate_comprehensive_analysis()

        # Should handle no digits gracefully
        assert analysis['metadata']['document_stats']['total_digits'] == 0
        assert analysis['metadata']['document_stats']['thai_digits'] == 0
        assert analysis['metadata']['document_stats']['international_digits'] == 0

    def test_very_large_numbers_precision(self, tmp_path):
        """Test analysis with calculations that might have precision issues."""
        # Create a document that would result in very small or large numbers
        tiny_file = tmp_path / "tiny.txt"
        tiny_file.write_text("๑", encoding='utf-8')  # Single character

        # Use very small keystroke time
        generator = JSONAnalysisGenerator(str(tiny_file))
        analysis = generator.generate_comprehensive_analysis()

        # Should handle precision gracefully (no NaN or Inf values)
        def check_no_invalid_numbers(obj):
            if isinstance(obj, dict):
                for value in obj.values():
                    check_no_invalid_numbers(value)
            elif isinstance(obj, list):
                for item in obj:
                    check_no_invalid_numbers(item)
            elif isinstance(obj, float):
                assert not (obj != obj)  # Check for NaN
                assert obj != float('inf')  # Check for infinity
                assert obj != float('-inf')  # Check for negative infinity

        check_no_invalid_numbers(analysis)


# Pytest markers
pytestmark = [pytest.mark.unit]
