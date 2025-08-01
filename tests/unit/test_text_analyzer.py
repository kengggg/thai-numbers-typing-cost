"""
Unit tests for TextAnalyzer class.

Tests text analysis functionality including digit counting, context extraction,
and statistical analysis of Thai documents.
"""

import sys
from pathlib import Path

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from models.text_analyzer import TextAnalyzer


class TestTextAnalyzer:
    """Test suite for TextAnalyzer class."""

    def test_initialization_with_valid_file(self, sample_thai_text_file):
        """Test TextAnalyzer initialization with a valid file."""
        analyzer = TextAnalyzer(sample_thai_text_file)

        assert analyzer.file_path == sample_thai_text_file
        assert len(analyzer.text) > 0
        assert analyzer.thai_digit_chars == {
            "๐",
            "๑",
            "๒",
            "๓",
            "๔",
            "๕",
            "๖",
            "๗",
            "๘",
            "๙",
        }
        assert analyzer.intl_digit_chars == {
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
        }

    def test_initialization_with_nonexistent_file(self, tmp_path):
        """Test TextAnalyzer initialization with nonexistent file raises error."""
        nonexistent_file = tmp_path / "nonexistent.txt"

        with pytest.raises(FileNotFoundError):
            TextAnalyzer(str(nonexistent_file))

    def test_unicode_ranges_constants(self):
        """Test that Unicode ranges are correctly defined."""
        # Thai digits: U+0E50 to U+0E59
        assert TextAnalyzer.THAI_DIGITS == range(0x0E50, 0x0E5A)

        # International digits: U+0030 to U+0039
        assert TextAnalyzer.INTERNATIONAL_DIGITS == range(0x0030, 0x003A)

    def test_load_text_with_utf8_encoding(self, tmp_path):
        """Test loading text with UTF-8 encoding."""
        text_content = "สวัสดี ๑๒๓ hello 456"
        test_file = tmp_path / "utf8_test.txt"
        test_file.write_text(text_content, encoding="utf-8")

        analyzer = TextAnalyzer(str(test_file))
        assert analyzer.text == text_content

    def test_count_numeric_characters_thai_only(self, tmp_path):
        """Test counting Thai digits only."""
        text_content = "ปี ๒๕๖๐ มีความสำคัญ ตัวเลข ๑๒๓"
        test_file = tmp_path / "thai_only.txt"
        test_file.write_text(text_content, encoding="utf-8")

        analyzer = TextAnalyzer(str(test_file))
        counts = analyzer.count_numeric_characters()

        assert counts["thai_digits"] == 7  # ๒๕๖๐๑๒๓
        assert counts["international_digits"] == 0
        assert counts["total_digits"] == 7

    def test_count_numeric_characters_international_only(self, tmp_path):
        """Test counting international digits only."""
        text_content = "Year 2017 is important, numbers 123"
        test_file = tmp_path / "intl_only.txt"
        test_file.write_text(text_content, encoding="utf-8")

        analyzer = TextAnalyzer(str(test_file))
        counts = analyzer.count_numeric_characters()

        assert counts["thai_digits"] == 0
        assert counts["international_digits"] == 7  # 2017123
        assert counts["total_digits"] == 7

    def test_count_numeric_characters_mixed(self, tmp_path):
        """Test counting mixed Thai and international digits."""
        text_content = "ปี ๒๕๖๐ คือ 2017 AD"
        test_file = tmp_path / "mixed.txt"
        test_file.write_text(text_content, encoding="utf-8")

        analyzer = TextAnalyzer(str(test_file))
        counts = analyzer.count_numeric_characters()

        assert counts["thai_digits"] == 4  # ๒๕๖๐
        assert counts["international_digits"] == 4  # 2017
        assert counts["total_digits"] == 8

    def test_count_numeric_characters_empty_text(self, empty_text_file):
        """Test counting digits in empty text."""
        analyzer = TextAnalyzer(empty_text_file)
        counts = analyzer.count_numeric_characters()

        assert counts["thai_digits"] == 0
        assert counts["international_digits"] == 0
        assert counts["total_digits"] == 0

    def test_analyze_digit_usage_comprehensive(self, tmp_path):
        """Test detailed digit usage analysis."""
        text_content = "๑๒๑ และ 123 มีการใช้ ๐๐๙"
        test_file = tmp_path / "usage_test.txt"
        test_file.write_text(text_content, encoding="utf-8")

        analyzer = TextAnalyzer(str(test_file))
        analysis = analyzer.analyze_digit_usage()

        # Thai digit breakdown
        assert analysis["thai_digit_breakdown"]["๑"] == 2
        assert analysis["thai_digit_breakdown"]["๒"] == 1
        assert analysis["thai_digit_breakdown"]["๐"] == 2
        assert analysis["thai_digit_breakdown"]["๙"] == 1

        # International digit breakdown
        assert analysis["intl_digit_breakdown"]["1"] == 1
        assert analysis["intl_digit_breakdown"]["2"] == 1
        assert analysis["intl_digit_breakdown"]["3"] == 1

        # Unicode codes
        assert analysis["thai_digit_unicode"]["๑"] == "U+0E51"
        assert analysis["intl_digit_unicode"]["1"] == "U+0031"

    def test_find_number_contexts_basic(self, tmp_path):
        """Test finding number contexts in text."""
        text_content = "เริ่มต้นปี ๒๕๖๐ และสิ้นสุดปี 2017 AD"
        test_file = tmp_path / "context_test.txt"
        test_file.write_text(text_content, encoding="utf-8")

        analyzer = TextAnalyzer(str(test_file))
        contexts = analyzer.find_number_contexts()

        assert len(contexts) == 2

        # First context (Thai number)
        thai_ctx = contexts[0]
        assert thai_ctx["number"] == "๒๕๖๐"
        assert thai_ctx["type"] == "thai"
        assert thai_ctx["length"] == 4
        assert "เริ่มต้นปี" in thai_ctx["context"]

        # Second context (International number)
        intl_ctx = contexts[1]
        assert intl_ctx["number"] == "2017"
        assert intl_ctx["type"] == "international"
        assert intl_ctx["length"] == 4
        assert "สิ้นสุดปี" in intl_ctx["context"]

    def test_find_number_contexts_long_sequences(self, tmp_path):
        """Test finding contexts for long number sequences."""
        text_content = "เลขไทย ๑๒๓๔๕๖๗๘๙๐ และเลขสากล 1234567890"
        test_file = tmp_path / "long_seq.txt"
        test_file.write_text(text_content, encoding="utf-8")

        analyzer = TextAnalyzer(str(test_file))
        contexts = analyzer.find_number_contexts()

        assert len(contexts) == 2
        assert contexts[0]["number"] == "๑๒๓๔๕๖๗๘๙๐"
        assert contexts[0]["length"] == 10
        assert contexts[1]["number"] == "1234567890"
        assert contexts[1]["length"] == 10

    def test_find_number_contexts_edge_of_text(self, tmp_path):
        """Test finding contexts at the beginning and end of text."""
        text_content = "๑๒๓ เป็นตัวเลขเริ่มต้น และ 456"
        test_file = tmp_path / "edge_test.txt"
        test_file.write_text(text_content, encoding="utf-8")

        analyzer = TextAnalyzer(str(test_file))
        contexts = analyzer.find_number_contexts()

        assert len(contexts) == 2

        # First context should start from beginning
        first_ctx = contexts[0]
        assert first_ctx["position"][0] == 0
        assert first_ctx["context"].startswith("๑๒๓")

        # Last context should go to end
        last_ctx = contexts[1]
        assert last_ctx["context"].endswith("456")

    def test_find_number_contexts_no_numbers(self, tmp_path):
        """Test finding contexts when no numbers exist."""
        text_content = "ไม่มีตัวเลขในข้อความนี้เลย"
        test_file = tmp_path / "no_numbers.txt"
        test_file.write_text(text_content, encoding="utf-8")

        analyzer = TextAnalyzer(str(test_file))
        contexts = analyzer.find_number_contexts()

        assert len(contexts) == 0

    def test_get_statistics_comprehensive(self, tmp_path):
        """Test comprehensive statistics generation."""
        text_content = "ปี ๒๕๖๐\nมีความสำคัญ\nเลข 123 ด้วย"
        test_file = tmp_path / "stats_test.txt"
        test_file.write_text(text_content, encoding="utf-8")

        analyzer = TextAnalyzer(str(test_file))
        stats = analyzer.get_statistics()

        # Document stats
        assert stats["document_stats"]["total_characters"] == len(text_content)
        assert stats["document_stats"]["total_lines"] == 3
        assert stats["document_stats"]["total_digits"] == 7

        # Calculate expected digit percentage
        expected_percentage = (7 / len(text_content)) * 100
        assert (
            abs(stats["document_stats"]["digit_percentage"] - expected_percentage)
            < 0.01
        )

        # Digit counts
        assert stats["digit_counts"]["thai_digits"] == 4
        assert stats["digit_counts"]["international_digits"] == 3

        # Number sequences
        assert stats["number_sequences"]["total_sequences"] == 2
        assert stats["number_sequences"]["thai_sequences"] == 1
        assert stats["number_sequences"]["intl_sequences"] == 1

    def test_get_statistics_sequence_averages(self, tmp_path):
        """Test calculation of average sequence lengths."""
        text_content = "๑ ๒๓ ๔๕๖ และ 1 23 456"  # Thai: 1,2,3 digits; Intl: 1,2,3 digits
        test_file = tmp_path / "avg_test.txt"
        test_file.write_text(text_content, encoding="utf-8")

        analyzer = TextAnalyzer(str(test_file))
        stats = analyzer.get_statistics()

        # Average Thai length: (1+2+3)/3 = 2.0
        assert abs(stats["number_sequences"]["avg_thai_length"] - 2.0) < 0.01

        # Average International length: (1+2+3)/3 = 2.0
        assert abs(stats["number_sequences"]["avg_intl_length"] - 2.0) < 0.01

    def test_get_statistics_no_sequences(self, tmp_path):
        """Test statistics when no number sequences exist."""
        text_content = "ไม่มีตัวเลข"
        test_file = tmp_path / "no_seq.txt"
        test_file.write_text(text_content, encoding="utf-8")

        analyzer = TextAnalyzer(str(test_file))
        stats = analyzer.get_statistics()

        assert stats["number_sequences"]["avg_thai_length"] == 0
        assert stats["number_sequences"]["avg_intl_length"] == 0
        assert stats["number_sequences"]["total_sequences"] == 0

    def test_get_statistics_contexts_limit(self, tmp_path):
        """Test that contexts are limited to first 10 entries."""
        # Create text with more than 10 number sequences
        numbers = " ".join([f"๑{i}" for i in range(15)])  # 15 sequences
        test_file = tmp_path / "many_contexts.txt"
        test_file.write_text(numbers, encoding="utf-8")

        analyzer = TextAnalyzer(str(test_file))
        stats = analyzer.get_statistics()

        assert len(stats["contexts"]) == 10
        assert stats["number_sequences"]["total_sequences"] == 15

    def test_print_report_execution(self, sample_thai_text_file, capsys):
        """Test that print_report executes without errors."""
        analyzer = TextAnalyzer(sample_thai_text_file)

        # Should not raise any exceptions
        analyzer.print_report()

        # Check that something was printed
        captured = capsys.readouterr()
        assert "THAI CONSTITUTION NUMERIC CHARACTER ANALYSIS" in captured.out
        assert "DOCUMENT OVERVIEW:" in captured.out
        assert "DIGIT TYPE BREAKDOWN:" in captured.out

    def test_edge_case_single_character_file(self, tmp_path):
        """Test analyzer with single character file."""
        test_file = tmp_path / "single.txt"
        test_file.write_text("๑", encoding="utf-8")

        analyzer = TextAnalyzer(str(test_file))
        counts = analyzer.count_numeric_characters()

        assert counts["thai_digits"] == 1
        assert counts["international_digits"] == 0
        assert counts["total_digits"] == 1

    def test_edge_case_only_whitespace(self, tmp_path):
        """Test analyzer with only whitespace."""
        test_file = tmp_path / "whitespace.txt"
        test_file.write_text("   \n\t  \n  ", encoding="utf-8")

        analyzer = TextAnalyzer(str(test_file))
        counts = analyzer.count_numeric_characters()

        assert counts["thai_digits"] == 0
        assert counts["international_digits"] == 0
        assert counts["total_digits"] == 0

    def test_unicode_handling_various_scripts(self, tmp_path):
        """Test that analyzer correctly handles various Unicode scripts."""
        # Include various scripts but only count Thai and international digits
        text_content = "English ๑๒๓ العربية 456 中文 ๗๘๙ русский 789"
        test_file = tmp_path / "unicode_test.txt"
        test_file.write_text(text_content, encoding="utf-8")

        analyzer = TextAnalyzer(str(test_file))
        counts = analyzer.count_numeric_characters()

        assert counts["thai_digits"] == 6  # ๑๒๓๗๘๙
        assert counts["international_digits"] == 6  # 456789
        assert counts["total_digits"] == 12


class TestTextAnalyzerIntegration:
    """Integration tests for TextAnalyzer with real-world scenarios."""

    def test_with_real_thai_constitution_format(self, tmp_path):
        """Test with text formatted like real Thai constitution."""
        text_content = """พระราชบัญญัติรัฐธรรมนูญแห่งราชอาณาจักรไทย พุทธศักราช ๒๕๖๐

มาตรา ๑ ราชอาณาจักรไทยเป็นราชอาณาจักรอันหนึ่งอันเดียวและมิอาจแบ่งแยกได้

มาตรา ๒ ไทยเป็นประชาธิปไตยอันมีพระมหากษัตริย์ทรงเป็นประมุข

บทเฉพาะกาล
มาตรา ๒๗๙ รัฐธรรมนูญนี้ให้ใช้บังคับตั้งแต่วันที่ ๖ เมษายน พุทธศักราช ๒๕๖๐ เป็นต้นไป"""

        test_file = tmp_path / "constitution.txt"
        test_file.write_text(text_content, encoding="utf-8")

        analyzer = TextAnalyzer(str(test_file))
        stats = analyzer.get_statistics()

        # Should find Thai year and article numbers
        assert stats["digit_counts"]["thai_digits"] > 0
        assert "๒๕๖๐" in [ctx["number"] for ctx in stats["contexts"]]
        assert any("มาตรา" in ctx["context"] for ctx in stats["contexts"])

    def test_performance_with_large_text(self, tmp_path):
        """Test performance with relatively large text."""
        # Create a larger text file (repeated content)
        base_content = "ปี ๒๕๖๐ เป็นปีสำคัญ และมี numbers 123 ด้วย\n"
        large_content = base_content * 1000  # 1000 lines

        test_file = tmp_path / "large.txt"
        test_file.write_text(large_content, encoding="utf-8")

        analyzer = TextAnalyzer(str(test_file))

        # Should complete without issues
        stats = analyzer.get_statistics()

        # Verify scaling
        assert (
            stats["digit_counts"]["thai_digits"] == 4000
        )  # 4 Thai digits per line * 1000
        assert (
            stats["digit_counts"]["international_digits"] == 3000
        )  # 3 intl digits per line * 1000


# Pytest markers for organization
pytestmark = [pytest.mark.unit]
