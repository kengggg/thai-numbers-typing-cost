from unittest.mock import patch
"""
Unit tests for TypingCostCalculator class.

Tests typing cost calculations, scenario analysis, digit conversions,
and comprehensive reporting functionality.
"""

import pytest
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from calculators.typing_cost_calculator import TypingCostCalculator
from models.keyboard_layouts import KedmaneeLayout, PattajotiLayout


class TestTypingCostCalculatorInitialization:
    """Test suite for TypingCostCalculator initialization."""

    def test_initialization_with_default_params(self, sample_thai_text_file):
        """Test initialization with default parameters."""
        calculator = TypingCostCalculator(sample_thai_text_file)

        assert calculator.document_path == sample_thai_text_file
        assert calculator.base_keystroke_time == 0.28  # Default value
        assert calculator.analyzer is not None
        assert isinstance(calculator.kedmanee, KedmaneeLayout)
        assert isinstance(calculator.pattajoti, PattajotiLayout)

    def test_initialization_with_custom_params(self, sample_thai_text_file):
        """Test initialization with custom parameters."""
        custom_time = 0.15
        calculator = TypingCostCalculator(sample_thai_text_file, custom_time)

        assert calculator.base_keystroke_time == custom_time

    def test_digit_mapping_initialization(self, sample_thai_text_file):
        """Test that digit mappings are correctly initialized."""
        calculator = TypingCostCalculator(sample_thai_text_file)

        expected_thai_to_intl = {
            '๐': '0', '๑': '1', '๒': '2', '๓': '3', '๔': '4',
            '๕': '5', '๖': '6', '๗': '7', '๘': '8', '๙': '9'
        }
        expected_intl_to_thai = {v: k for k, v in expected_thai_to_intl.items()}

        assert calculator.thai_to_intl_map == expected_thai_to_intl
        assert calculator.intl_to_thai_map == expected_intl_to_thai

    def test_initialization_with_nonexistent_file(self, tmp_path):
        """Test initialization with nonexistent file."""
        nonexistent_file = tmp_path / "nonexistent.txt"

        with pytest.raises(FileNotFoundError):
            TypingCostCalculator(str(nonexistent_file))


class TestDigitConversion:
    """Test suite for digit conversion functionality."""

    def test_convert_digits_to_international(self, typing_cost_calculator):
        """Test conversion of Thai digits to international."""
        text = "ปี ๒๕๖๐ มีความสำคัญ"
        converted = typing_cost_calculator.convert_digits(text, "international")

        expected = "ปี 2560 มีความสำคัญ"
        assert converted == expected

    def test_convert_digits_to_thai(self, typing_cost_calculator):
        """Test conversion of international digits to Thai."""
        text = "Year 2017 is important"
        converted = typing_cost_calculator.convert_digits(text, "thai")

        expected = "Year ๒๐๑๗ is important"
        assert converted == expected

    def test_convert_digits_mixed_content(self, typing_cost_calculator):
        """Test conversion with mixed Thai and international digits."""
        text = "ปี ๒๕๖๐ คือ 2017 AD"

        # Convert to international
        to_intl = typing_cost_calculator.convert_digits(text, "international")
        assert to_intl == "ปี 2560 คือ 2017 AD"

        # Convert to Thai
        to_thai = typing_cost_calculator.convert_digits(text, "thai")
        assert to_thai == "ปี ๒๕๖๐ คือ ๒๐๑๗ AD"

    def test_convert_digits_no_conversion(self, typing_cost_calculator):
        """Test that 'none' conversion leaves text unchanged."""
        original_text = "ปี ๒๕๖๐ คือ 2017 AD"
        converted = typing_cost_calculator.convert_digits(original_text, "none")

        assert converted == original_text

    def test_convert_digits_invalid_target(self, typing_cost_calculator):
        """Test conversion with invalid target type."""
        text = "ปี ๒๕๖๐"
        converted = typing_cost_calculator.convert_digits(text, "invalid")

        # Should return original text unchanged
        assert converted == text

    def test_convert_digits_empty_text(self, typing_cost_calculator):
        """Test conversion with empty text."""
        converted = typing_cost_calculator.convert_digits("", "international")
        assert converted == ""

    def test_convert_digits_text_without_digits(self, typing_cost_calculator):
        """Test conversion with text containing no digits."""
        text = "สวัสดีครับ Hello World"

        converted_intl = typing_cost_calculator.convert_digits(text, "international")
        converted_thai = typing_cost_calculator.convert_digits(text, "thai")

        assert converted_intl == text
        assert converted_thai == text

    def test_convert_digits_all_thai_digits(self, typing_cost_calculator):
        """Test conversion of all Thai digits."""
        thai_text = "๐๑๒๓๔๕๖๗๘๙"
        converted = typing_cost_calculator.convert_digits(thai_text, "international")

        assert converted == "0123456789"

    def test_convert_digits_all_international_digits(self, typing_cost_calculator):
        """Test conversion of all international digits."""
        intl_text = "0123456789"
        converted = typing_cost_calculator.convert_digits(intl_text, "thai")

        assert converted == "๐๑๒๓๔๕๖๗๘๙"


class TestDocumentCostCalculation:
    """Test suite for document cost calculation."""

    def test_calculate_document_cost_basic(self, typing_cost_calculator):
        """Test basic document cost calculation."""
        result = typing_cost_calculator.calculate_document_cost(
            typing_cost_calculator.kedmanee, "none"
        )

        # Check result structure
        required_keys = [
            'total_cost_seconds', 'total_cost_minutes', 'total_cost_hours',
            'total_characters', 'average_cost_per_char', 'character_costs',
            'digit_costs', 'keyboard_layout', 'conversion_applied',
            'base_keystroke_time'
        ]

        for key in required_keys:
            assert key in result, f"Missing key: {key}"

        # Check data types and basic constraints
        assert isinstance(result['total_cost_seconds'], float)
        assert result['total_cost_seconds'] > 0
        assert result['total_cost_minutes'] == result['total_cost_seconds'] / 60
        assert result['total_cost_hours'] == result['total_cost_seconds'] / 3600
        assert result['total_characters'] > 0
        assert result['keyboard_layout'] == 'kedmanee'
        assert result['conversion_applied'] == 'none'

    def test_calculate_document_cost_with_conversion(self, typing_cost_calculator):
        """Test document cost calculation with digit conversion."""
        kedmanee_result = typing_cost_calculator.calculate_document_cost(
            typing_cost_calculator.kedmanee, "to_international"
        )

        assert kedmanee_result['conversion_applied'] == 'to_international'

        # Should have some digit costs tracked
        assert len(kedmanee_result['digit_costs']) > 0

    def test_calculate_document_cost_different_layouts(self, typing_cost_calculator):
        """Test cost calculation with different keyboard layouts."""
        kedmanee_result = typing_cost_calculator.calculate_document_cost(
            typing_cost_calculator.kedmanee, "none"
        )
        pattajoti_result = typing_cost_calculator.calculate_document_cost(
            typing_cost_calculator.pattajoti, "none"
        )

        # Same document, so character count should be identical
        assert kedmanee_result['total_characters'] == pattajoti_result['total_characters']

        # But costs should differ (Kedmanee has SHIFT penalty for Thai digits)
        if typing_cost_calculator.analyzer.count_numeric_characters()['thai_digits'] > 0:
            assert kedmanee_result['total_cost_seconds'] > pattajoti_result['total_cost_seconds']

    def test_calculate_document_cost_empty_document(self, tmp_path):
        """Test cost calculation with empty document."""
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("", encoding='utf-8')

        calculator = TypingCostCalculator(str(empty_file))
        result = calculator.calculate_document_cost(calculator.kedmanee, "none")

        assert result['total_cost_seconds'] == 0
        assert result['total_characters'] == 0
        assert result['average_cost_per_char'] == 0
        assert len(result['character_costs']) == 0
        assert len(result['digit_costs']) == 0

    def test_calculate_document_cost_single_character(self, tmp_path):
        """Test cost calculation with single character document."""
        single_file = tmp_path / "single.txt"
        single_file.write_text("๑", encoding='utf-8')

        calculator = TypingCostCalculator(str(single_file), 0.5)
        result = calculator.calculate_document_cost(calculator.kedmanee, "none")

        assert result['total_characters'] == 1
        assert result['total_cost_seconds'] == 1.0  # 0.5 * 2 (SHIFT penalty)
        assert result['average_cost_per_char'] == 1.0
        assert '๑' in result['character_costs']
        assert '๑' in result['digit_costs']

    def test_character_cost_tracking(self, typing_cost_calculator):
        """Test that character costs are properly tracked."""
        result = typing_cost_calculator.calculate_document_cost(
            typing_cost_calculator.kedmanee, "none"
        )

        # Check character cost structure
        for char, data in result['character_costs'].items():
            assert 'count' in data
            assert 'total_cost' in data
            assert isinstance(data['count'], int)
            assert isinstance(data['total_cost'], float)
            assert data['count'] > 0
            assert data['total_cost'] > 0

    def test_digit_cost_tracking(self, typing_cost_calculator):
        """Test that digit costs are specifically tracked."""
        result = typing_cost_calculator.calculate_document_cost(
            typing_cost_calculator.kedmanee, "none"
        )

        # Check that only digits are in digit_costs
        for char in result['digit_costs'].keys():
            assert char.isdigit() or char in typing_cost_calculator.thai_to_intl_map


class TestScenarioAnalysis:
    """Test suite for scenario analysis functionality."""

    def test_analyze_all_scenarios_structure(self, typing_cost_calculator):
        """Test that analyze_all_scenarios returns proper structure."""
        scenarios = typing_cost_calculator.analyze_all_scenarios()

        expected_scenarios = ['thai_kedmanee', 'intl_kedmanee', 'thai_pattajoti', 'intl_pattajoti']

        for scenario_name in expected_scenarios:
            assert scenario_name in scenarios, f"Missing scenario: {scenario_name}"

            scenario_data = scenarios[scenario_name]
            assert 'total_cost_seconds' in scenario_data
            assert 'keyboard_layout' in scenario_data
            assert 'conversion_applied' in scenario_data

    def test_analyze_all_scenarios_layout_assignments(self, typing_cost_calculator):
        """Test that scenarios use correct keyboard layouts."""
        scenarios = typing_cost_calculator.analyze_all_scenarios()

        assert scenarios['thai_kedmanee']['keyboard_layout'] == 'kedmanee'
        assert scenarios['intl_kedmanee']['keyboard_layout'] == 'kedmanee'
        assert scenarios['thai_pattajoti']['keyboard_layout'] == 'pattajoti'
        assert scenarios['intl_pattajoti']['keyboard_layout'] == 'pattajoti'

    def test_analyze_all_scenarios_conversion_assignments(self, typing_cost_calculator):
        """Test that scenarios use correct digit conversions."""
        scenarios = typing_cost_calculator.analyze_all_scenarios()

        assert scenarios['thai_kedmanee']['conversion_applied'] == 'none'
        assert scenarios['intl_kedmanee']['conversion_applied'] == 'to_international'
        assert scenarios['thai_pattajoti']['conversion_applied'] == 'none'
        assert scenarios['intl_pattajoti']['conversion_applied'] == 'to_international'

    def test_analyze_all_scenarios_cost_relationships(self, typing_cost_calculator):
        """Test expected cost relationships between scenarios."""
        scenarios = typing_cost_calculator.analyze_all_scenarios()

        # If document has Thai digits, these relationships should hold:
        if typing_cost_calculator.analyzer.count_numeric_characters()['thai_digits'] > 0:
            # Kedmanee with Thai digits should be most expensive (SHIFT penalty)
            thai_ked_cost = scenarios['thai_kedmanee']['total_cost_seconds']

            # Other scenarios should be cheaper
            for scenario_name, scenario_data in scenarios.items():
                if scenario_name != 'thai_kedmanee':
                    assert scenario_data['total_cost_seconds'] <= thai_ked_cost

    @patch('builtins.print')
    def test_analyze_all_scenarios_output(self, mock_print, typing_cost_calculator):
        """Test that analyze_all_scenarios produces expected output."""
        typing_cost_calculator.analyze_all_scenarios()

        # Check that progress messages were printed
        mock_print.assert_any_call("Calculating typing costs for all scenarios...")
        mock_print.assert_any_call("  Scenario 1: Thai digits on Kedmanee...")
        mock_print.assert_any_call("  Scenario 2: International digits on Kedmanee...")
        mock_print.assert_any_call("  Scenario 3: Thai digits on Pattajoti...")
        mock_print.assert_any_call("  Scenario 4: International digits on Pattajoti...")


class TestSavingsAnalysis:
    """Test suite for savings analysis functionality."""

    def test_calculate_savings_analysis_structure(self, typing_cost_calculator):
        """Test savings analysis result structure."""
        scenarios = typing_cost_calculator.analyze_all_scenarios()
        savings = typing_cost_calculator.calculate_savings_analysis(scenarios)

        # Should have savings for all scenarios except the baseline
        expected_scenarios = ['intl_kedmanee', 'thai_pattajoti', 'intl_pattajoti']

        for scenario_name in expected_scenarios:
            assert scenario_name in savings, f"Missing savings for: {scenario_name}"

            saving_data = savings[scenario_name]
            required_keys = [
                'time_saved_seconds', 'time_saved_minutes', 'time_saved_hours',
                'percentage_saved', 'cost_per_digit'
            ]

            for key in required_keys:
                assert key in saving_data, f"Missing key in savings: {key}"

    def test_calculate_savings_analysis_baseline(self, typing_cost_calculator):
        """Test that baseline scenario (thai_kedmanee) is not in savings."""
        scenarios = typing_cost_calculator.analyze_all_scenarios()
        savings = typing_cost_calculator.calculate_savings_analysis(scenarios)

        assert 'thai_kedmanee' not in savings

    def test_calculate_savings_analysis_calculations(self, typing_cost_calculator):
        """Test that savings calculations are mathematically correct."""
        scenarios = typing_cost_calculator.analyze_all_scenarios()
        savings = typing_cost_calculator.calculate_savings_analysis(scenarios)

        baseline_cost = scenarios['thai_kedmanee']['total_cost_seconds']

        for scenario_name, saving_data in savings.items():
            scenario_cost = scenarios[scenario_name]['total_cost_seconds']

            expected_saved_seconds = baseline_cost - scenario_cost
            expected_saved_minutes = expected_saved_seconds / 60
            expected_saved_hours = expected_saved_seconds / 3600
            expected_percentage = (expected_saved_seconds / baseline_cost) * 100

            assert abs(saving_data['time_saved_seconds'] - expected_saved_seconds) < 0.001
            assert abs(saving_data['time_saved_minutes'] - expected_saved_minutes) < 0.001
            assert abs(saving_data['time_saved_hours'] - expected_saved_hours) < 0.001
            assert abs(saving_data['percentage_saved'] - expected_percentage) < 0.001

    def test_calculate_savings_analysis_cost_per_digit(self, typing_cost_calculator):
        """Test cost per digit calculation in savings analysis."""
        scenarios = typing_cost_calculator.analyze_all_scenarios()
        savings = typing_cost_calculator.calculate_savings_analysis(scenarios)

        for scenario_name, saving_data in savings.items():
            scenario_data = scenarios[scenario_name]

            if scenario_data['digit_costs']:
                total_digits = sum(data['count'] for data in scenario_data['digit_costs'].values())
                expected_cost_per_digit = scenario_data['total_cost_seconds'] / total_digits

                assert abs(saving_data['cost_per_digit'] - expected_cost_per_digit) < 0.001
            else:
                assert saving_data['cost_per_digit'] == 0


class TestComprehensiveReport:
    """Test suite for comprehensive report functionality."""

    @patch('builtins.print')
    def test_print_comprehensive_report_execution(self, mock_print, typing_cost_calculator):
        """Test that comprehensive report executes without errors."""
        scenarios, savings = typing_cost_calculator.print_comprehensive_report()

        # Check that report sections were printed
        assert any("THAI CONSTITUTION TYPING COST ANALYSIS" in str(call) for call in mock_print.call_args_list)
        assert any("DOCUMENT STATISTICS:" in str(call) for call in mock_print.call_args_list)
        assert any("TYPING COST BY SCENARIO:" in str(call) for call in mock_print.call_args_list)
        assert any("TIME SAVINGS COMPARED TO CURRENT STATE" in str(call) for call in mock_print.call_args_list)
        assert any("OPTIMAL SCENARIO ANALYSIS:" in str(call) for call in mock_print.call_args_list)

    def test_print_comprehensive_report_return_values(self, typing_cost_calculator):
        """Test that comprehensive report returns expected values."""
        scenarios, savings = typing_cost_calculator.print_comprehensive_report()

        # Should return the same data as individual methods
        expected_scenarios = typing_cost_calculator.analyze_all_scenarios()
        expected_savings = typing_cost_calculator.calculate_savings_analysis(expected_scenarios)

        assert scenarios == expected_scenarios
        assert savings == expected_savings


class TestEdgeCases:
    """Test suite for edge cases and error conditions."""

    def test_calculator_with_zero_base_time(self, sample_thai_text_file):
        """Test calculator with zero base keystroke time."""
        calculator = TypingCostCalculator(sample_thai_text_file, 0.0)
        result = calculator.calculate_document_cost(calculator.kedmanee, "none")

        assert result['total_cost_seconds'] == 0.0
        assert result['base_keystroke_time'] == 0.0

    def test_calculator_with_negative_base_time(self, sample_thai_text_file):
        """Test calculator with negative base keystroke time."""
        calculator = TypingCostCalculator(sample_thai_text_file, -0.1)
        result = calculator.calculate_document_cost(calculator.kedmanee, "none")

        # Should still apply multipliers correctly
        assert result['base_keystroke_time'] == -0.1

    def test_calculator_with_very_large_base_time(self, sample_thai_text_file):
        """Test calculator with very large base keystroke time."""
        calculator = TypingCostCalculator(sample_thai_text_file, 1000.0)
        result = calculator.calculate_document_cost(calculator.kedmanee, "none")

        assert result['base_keystroke_time'] == 1000.0
        assert result['total_cost_seconds'] > 0

    def test_document_with_only_spaces(self, tmp_path):
        """Test calculator with document containing only spaces."""
        spaces_file = tmp_path / "spaces.txt"
        spaces_file.write_text("     ", encoding='utf-8')

        calculator = TypingCostCalculator(str(spaces_file))
        result = calculator.calculate_document_cost(calculator.kedmanee, "none")

        assert result['total_characters'] == 5
        assert result['total_cost_seconds'] > 0  # Spaces have cost
        assert len(result['digit_costs']) == 0  # No digits

    def test_document_with_only_unknown_characters(self, tmp_path):
        """Test calculator with document containing only unknown characters."""
        unknown_file = tmp_path / "unknown.txt"
        unknown_file.write_text("🎉🌟💫", encoding='utf-8')

        calculator = TypingCostCalculator(str(unknown_file))
        result = calculator.calculate_document_cost(calculator.kedmanee, "none")

        assert result['total_characters'] == 3
        # Should assign default cost to unknown characters
        expected_cost = 3 * calculator.base_keystroke_time
        assert abs(result['total_cost_seconds'] - expected_cost) < 0.001

    def test_document_with_mixed_line_endings(self, tmp_path):
        """Test calculator with document having mixed line endings."""
        mixed_file = tmp_path / "mixed.txt"
        content = "line1\nline2\r\nline3\rline4"
        mixed_file.write_text(content, encoding='utf-8')

        calculator = TypingCostCalculator(str(mixed_file))
        result = calculator.calculate_document_cost(calculator.kedmanee, "none")

        # Read the actual content as the calculator would to account for line ending normalization
        with open(mixed_file, 'r', encoding='utf-8') as f:
            actual_content = f.read()

        assert result['total_characters'] == len(actual_content)
        assert result['total_cost_seconds'] > 0


class TestPerformance:
    """Test suite for performance-related tests."""

    def test_performance_with_large_document(self, tmp_path):
        """Test calculator performance with large document."""
        large_file = tmp_path / "large.txt"
        # Create a reasonably large document
        content = "ปี ๒๕๖๐ เป็นปีสำคัญ และมี 123 numbers\n" * 100
        large_file.write_text(content, encoding='utf-8')

        calculator = TypingCostCalculator(str(large_file))

        # Should complete without performance issues
        scenarios = calculator.analyze_all_scenarios()
        savings = calculator.calculate_savings_analysis(scenarios)

        assert len(scenarios) == 4
        assert len(savings) == 3

    def test_multiple_calculations_consistency(self, typing_cost_calculator):
        """Test that multiple calculations return consistent results."""
        # Run the same calculation multiple times
        results = []
        for _ in range(5):
            result = typing_cost_calculator.calculate_document_cost(
                typing_cost_calculator.kedmanee, "none"
            )
            results.append(result['total_cost_seconds'])

        # All results should be identical
        assert all(abs(result - results[0]) < 0.001 for result in results)


class TestMainFunction:
    """Test suite for main function when run as script."""

    def test_main_function_with_valid_args(self, sample_thai_text_file, monkeypatch):
        """Test main function with valid command line arguments."""
        # Mock sys.argv
        test_args = ['typing_cost_calculator.py', sample_thai_text_file, '0.5']
        monkeypatch.setattr('sys.argv', test_args)

        # Mock the report function to avoid output
        with patch.object(TypingCostCalculator, 'print_comprehensive_report') as mock_report:
            # Import and run main
            from calculators.typing_cost_calculator import main
            main()

            # Should create calculator with correct parameters
            mock_report.assert_called_once()

    def test_main_function_with_invalid_file(self, monkeypatch, capsys):
        """Test main function with invalid file path."""
        test_args = ['typing_cost_calculator.py', 'nonexistent.txt']
        monkeypatch.setattr('sys.argv', test_args)

        with pytest.raises(SystemExit) as exc_info:
            from calculators.typing_cost_calculator import main
            main()

        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Error: Document not found" in captured.out

    def test_main_function_insufficient_args(self, monkeypatch, capsys):
        """Test main function with insufficient arguments."""
        test_args = ['typing_cost_calculator.py']
        monkeypatch.setattr('sys.argv', test_args)

        with pytest.raises(SystemExit) as exc_info:
            from calculators.typing_cost_calculator import main
            main()

        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Usage:" in captured.out


# Pytest markers
pytestmark = [pytest.mark.unit]
