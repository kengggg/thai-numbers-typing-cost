"""
Unit tests for keyboard layout classes.

Tests Thai keyboard layouts including Kedmanee and Pattajoti layouts,
key information, cost calculations, and layout comparisons.
"""

import pytest
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from models.keyboard_layouts import (
    KeyboardType, KeyInfo, ThaiKeyboardLayout,
    explain_keyboard_rows, compare_layouts
)


class TestKeyboardType:
    """Test suite for KeyboardType enum."""

    def test_keyboard_type_values(self):
        """Test that KeyboardType enum has correct values."""
        assert KeyboardType.KEDMANEE.value == "kedmanee"
        assert KeyboardType.PATTAJOTI.value == "pattajoti"

    def test_keyboard_type_membership(self):
        """Test that all expected keyboard types are defined."""
        all_types = [item.value for item in KeyboardType]
        assert "kedmanee" in all_types
        assert "pattajoti" in all_types
        assert len(all_types) == 2


class TestKeyInfo:
    """Test suite for KeyInfo class."""

    def test_keyinfo_initialization_minimal(self):
        """Test KeyInfo initialization with minimal parameters."""
        key = KeyInfo('a')

        assert key.char == 'a'
        assert key.requires_shift  is False
        assert key.hand == "unknown"
        assert key.finger == "unknown"
        assert key.row == 0

    def test_keyinfo_initialization_complete(self):
        """Test KeyInfo initialization with all parameters."""
        key = KeyInfo('A', requires_shift=True, hand="left", finger="pinky", row=2)

        assert key.char == 'A'
        assert key.requires_shift  is True
        assert key.hand == "left"
        assert key.finger == "pinky"
        assert key.row == 2

    def test_keyinfo_with_thai_character(self):
        """Test KeyInfo with Thai character."""
        key = KeyInfo('ก', requires_shift=False, hand="left", finger="middle", row=1)

        assert key.char == 'ก'
        assert key.requires_shift  is False
        assert key.hand == "left"
        assert key.finger == "middle"
        assert key.row == 1

    def test_keyinfo_with_thai_digit(self):
        """Test KeyInfo with Thai digit."""
        key = KeyInfo('๑', requires_shift=True, hand="left", finger="pinky", row=3)

        assert key.char == '๑'
        assert key.requires_shift  is True
        assert key.hand == "left"
        assert key.finger == "pinky"
        assert key.row == 3


class TestThaiKeyboardLayout:
    """Test suite for ThaiKeyboardLayout base class."""

    def test_base_class_cannot_be_instantiated_directly(self):
        """Test that base class raises NotImplementedError when initialized."""
        with pytest.raises(NotImplementedError):
            layout = ThaiKeyboardLayout(KeyboardType.KEDMANEE)

    def test_abstract_methods_must_be_implemented(self):
        """Test that subclasses must implement abstract methods."""
        class IncompleteLayout(ThaiKeyboardLayout):
            pass  # Missing _initialize_layout implementation

        with pytest.raises(NotImplementedError):
            IncompleteLayout(KeyboardType.KEDMANEE)


class TestKedmaneeLayout:
    """Test suite for KedmaneeLayout class."""

    def test_kedmanee_initialization(self, kedmanee_layout):
        """Test KedmaneeLayout initialization."""
        assert kedmanee_layout.layout_type == KeyboardType.KEDMANEE
        assert len(kedmanee_layout.key_map) > 0
        assert isinstance(kedmanee_layout.key_map, dict)

    def test_kedmanee_thai_digits_require_shift(self, kedmanee_layout, thai_digits):
        """Test that all Thai digits require SHIFT on Kedmanee."""
        for digit in thai_digits:
            key_info = kedmanee_layout.get_key_info(digit)
            assert key_info is not None, f"Thai digit {digit} not found in layout"
            assert key_info.requires_shift  is True, f"Thai digit {digit} should require SHIFT"
            assert key_info.row == 3, f"Thai digit {digit} should be on row 3"

    def test_kedmanee_international_digits_no_shift(self, kedmanee_layout, international_digits):
        """Test that international digits don't require SHIFT on Kedmanee."""
        for digit in international_digits:
            key_info = kedmanee_layout.get_key_info(digit)
            assert key_info is not None, f"International digit {digit} not found in layout"
            assert key_info.requires_shift  is False, f"International digit {digit} should not require SHIFT"
            assert key_info.row == 3, f"International digit {digit} should be on row 3"

    def test_kedmanee_digit_finger_assignments(self, kedmanee_layout):
        """Test Thai digit finger assignments match standard typing."""
        expected_assignments = {
            '๑': ('left', 'pinky'), '๒': ('left', 'ring'), '๓': ('left', 'middle'),
            '๔': ('left', 'index'), '๕': ('left', 'index'), '๖': ('right', 'index'),
            '๗': ('right', 'index'), '๘': ('right', 'middle'), '๙': ('right', 'ring'),
            '๐': ('right', 'pinky')
        }

        for digit, (expected_hand, expected_finger) in expected_assignments.items():
            key_info = kedmanee_layout.get_key_info(digit)
            assert key_info.hand == expected_hand, f"Digit {digit} hand assignment incorrect"
            assert key_info.finger == expected_finger, f"Digit {digit} finger assignment incorrect"

    def test_kedmanee_international_digit_finger_assignments(self, kedmanee_layout):
        """Test international digit finger assignments match standard typing."""
        expected_assignments = {
            '1': ('left', 'pinky'), '2': ('left', 'ring'), '3': ('left', 'middle'),
            '4': ('left', 'index'), '5': ('left', 'index'), '6': ('right', 'index'),
            '7': ('right', 'index'), '8': ('right', 'middle'), '9': ('right', 'ring'),
            '0': ('right', 'pinky')
        }

        for digit, (expected_hand, expected_finger) in expected_assignments.items():
            key_info = kedmanee_layout.get_key_info(digit)
            assert key_info.hand == expected_hand, f"Digit {digit} hand assignment incorrect"
            assert key_info.finger == expected_finger, f"Digit {digit} finger assignment incorrect"

    def test_kedmanee_common_thai_characters(self, kedmanee_layout):
        """Test that common Thai characters are included."""
        common_chars = ['ก', 'า', 'น', 'ร', 'ส', 'ห', 'ม', 'ล', 'ว', 'ด']

        for char in common_chars:
            key_info = kedmanee_layout.get_key_info(char)
            assert key_info is not None, f"Common Thai character {char} not found"
            assert key_info.char == char

    def test_kedmanee_punctuation_and_space(self, kedmanee_layout):
        """Test that common punctuation and space are included."""
        punctuation = [' ', '.', ',', '?', '!', '"', '(', ')']

        for char in punctuation:
            key_info = kedmanee_layout.get_key_info(char)
            assert key_info is not None, f"Punctuation {char} not found"

    def test_kedmanee_layout_completeness(self, kedmanee_layout):
        """Test that Kedmanee layout has comprehensive character coverage."""
        layout_info = kedmanee_layout.get_layout_info()

        assert layout_info['layout_type'] == 'kedmanee'
        assert layout_info['total_mapped_keys'] >= 60  # Should have at least 60 keys
        assert layout_info['shifted_keys'] >= 20  # Should have at least 20 shifted keys
        assert layout_info['non_shifted_keys'] >= 40  # Should have at least 40 non-shifted keys


class TestPattajotiLayout:
    """Test suite for PattajotiLayout class."""

    def test_pattajoti_initialization(self, pattajoti_layout):
        """Test PattajotiLayout initialization."""
        assert pattajoti_layout.layout_type == KeyboardType.PATTAJOTI
        assert len(pattajoti_layout.key_map) > 0
        assert isinstance(pattajoti_layout.key_map, dict)

    def test_pattajoti_thai_digits_no_shift(self, pattajoti_layout, thai_digits):
        """Test that Thai digits don't require SHIFT on Pattajoti."""
        for digit in thai_digits:
            key_info = pattajoti_layout.get_key_info(digit)
            assert key_info is not None, f"Thai digit {digit} not found in layout"
            assert key_info.requires_shift  is False, f"Thai digit {digit} should not require SHIFT"
            assert key_info.row == 3, f"Thai digit {digit} should be on row 3"

    def test_pattajoti_international_digits_no_shift(self, pattajoti_layout, international_digits):
        """Test that international digits don't require SHIFT on Pattajoti."""
        for digit in international_digits:
            key_info = pattajoti_layout.get_key_info(digit)
            assert key_info is not None, f"International digit {digit} not found in layout"
            assert key_info.requires_shift  is False, f"International digit {digit} should not require SHIFT"
            assert key_info.row == 3, f"International digit {digit} should be on row 3"

    def test_pattajoti_thai_digit_order(self, pattajoti_layout):
        """Test that Pattajoti Thai digits follow the correct left-to-right order."""
        expected_order = ['๒', '๓', '๔', '๕', '๗', '๘', '๙', '๐', '๑', '๖']
        expected_fingers = ['pinky', 'ring', 'middle', 'index', 'index',
                            'index', 'index', 'middle', 'ring', 'pinky']
        expected_hands = ['left', 'left', 'left', 'left', 'left',
                          'right', 'right', 'right', 'right', 'right']

        for i, digit in enumerate(expected_order):
            key_info = pattajoti_layout.get_key_info(digit)
            assert key_info is not None, f"Thai digit {digit} not found"
            assert key_info.finger == expected_fingers[i], f"Digit {digit} finger assignment incorrect"
            assert key_info.hand == expected_hands[i], f"Digit {digit} hand assignment incorrect"

    def test_pattajoti_layout_completeness(self, pattajoti_layout):
        """Test that Pattajoti layout has comprehensive character coverage."""
        layout_info = pattajoti_layout.get_layout_info()

        assert layout_info['layout_type'] == 'pattajoti'
        assert layout_info['total_mapped_keys'] >= 70  # Should have at least 70 keys
        assert layout_info['shifted_keys'] >= 5  # Should have some shifted keys for punctuation
        assert layout_info['non_shifted_keys'] >= 65  # Most keys should be non-shifted

    def test_pattajoti_vowel_and_tone_marks(self, pattajoti_layout):
        """Test that Pattajoti includes comprehensive vowel and tone mark coverage."""
        vowels_and_tones = ['า', 'ิ', 'ี', 'ึ', 'ื', 'ุ', 'ู', 'เ', 'แ', 'โ', 'ใ', 'ไ', 'ำ', 'ะ', 'ั']
        tone_marks = ['่', '้', '๊', '๋', '์']

        for char in vowels_and_tones + tone_marks:
            key_info = pattajoti_layout.get_key_info(char)
            assert key_info is not None, f"Vowel/tone mark {char} not found in Pattajoti layout"

    def test_pattajoti_thai_consonants(self, pattajoti_layout):
        """Test that Pattajoti includes comprehensive Thai consonant coverage."""
        consonants = ['ก', 'ข', 'ค', 'ง', 'จ', 'ช', 'ซ', 'ท', 'ร', 'น', 'ย', 'บ', 'ล', 'ว', 'ส', 'ห', 'อ']

        for char in consonants:
            key_info = pattajoti_layout.get_key_info(char)
            assert key_info is not None, f"Consonant {char} not found in Pattajoti layout"


class TestTypingCostCalculation:
    """Test suite for typing cost calculations."""

    def test_base_cost_calculation(self, kedmanee_layout):
        """Test basic cost calculation without modifiers."""
        base_time = 0.28

        # Test with non-shifted character
        cost = kedmanee_layout.calculate_typing_cost('1', base_time)
        assert cost == base_time

    def test_shift_penalty_calculation(self, kedmanee_layout):
        """Test SHIFT penalty calculation."""
        base_time = 0.5

        # Thai digit requires SHIFT on Kedmanee
        cost = kedmanee_layout.calculate_typing_cost('๑', base_time)
        assert cost == base_time * 2.0  # Double cost for SHIFT

    def test_unknown_character_handling(self, kedmanee_layout):
        """Test handling of unknown characters."""
        base_time = 0.28

        # Use a character not in the layout
        unknown_char = '🎉'  # Emoji not in keyboard layout
        cost = kedmanee_layout.calculate_typing_cost(unknown_char, base_time)
        assert cost == base_time  # Should return base cost for unknown chars

    def test_cost_calculation_different_base_times(self, kedmanee_layout, pattajoti_layout):
        """Test cost calculation with different base keystroke times."""
        base_times = [0.12, 0.20, 0.28, 1.2]  # Different typist skill levels

        for base_time in base_times:
            # Test non-shifted character
            ked_cost = kedmanee_layout.calculate_typing_cost('1', base_time)
            pat_cost = pattajoti_layout.calculate_typing_cost('1', base_time)
            assert ked_cost == base_time
            assert pat_cost == base_time

            # Test shifted character
            ked_thai_cost = kedmanee_layout.calculate_typing_cost('๑', base_time)
            pat_thai_cost = pattajoti_layout.calculate_typing_cost('๑', base_time)
            assert ked_thai_cost == base_time * 2.0  # Kedmanee has SHIFT penalty
            assert pat_thai_cost == base_time  # Pattajoti has no SHIFT penalty

    @pytest.mark.parametrize("digit,expected_kedmanee_shift,expected_pattajoti_shift", [
        ('๐', True, False), ('๑', True, False), ('๒', True, False), ('๓', True, False), ('๔', True, False),
        ('๕', True, False), ('๖', True, False), ('๗', True, False), ('๘', True, False), ('๙', True, False),
        ('0', False, False), ('1', False, False), ('2', False, False), ('3', False, False), ('4', False, False),
        ('5', False, False), ('6', False, False), ('7', False, False), ('8', False, False), ('9', False, False),
    ])
    def test_digit_shift_requirements_parametrized(self, kedmanee_layout, pattajoti_layout,
                                                   digit, expected_kedmanee_shift, expected_pattajoti_shift):
        """Parametrized test for digit SHIFT requirements across layouts."""
        base_time = 0.28

        ked_cost = kedmanee_layout.calculate_typing_cost(digit, base_time)
        pat_cost = pattajoti_layout.calculate_typing_cost(digit, base_time)

        expected_ked_cost = base_time * (2.0 if expected_kedmanee_shift else 1.0)
        expected_pat_cost = base_time * (2.0 if expected_pattajoti_shift else 1.0)

        assert ked_cost == expected_ked_cost, f"Kedmanee cost for {digit} incorrect"
        assert pat_cost == expected_pat_cost, f"Pattajoti cost for {digit} incorrect"


class TestLayoutComparison:
    """Test suite for layout comparison functionality."""

    def test_layout_info_structure(self, kedmanee_layout, pattajoti_layout):
        """Test that layout info returns expected structure."""
        ked_info = kedmanee_layout.get_layout_info()
        pat_info = pattajoti_layout.get_layout_info()

        required_keys = ['layout_type', 'total_mapped_keys', 'shifted_keys', 'non_shifted_keys']

        for info in [ked_info, pat_info]:
            for key in required_keys:
                assert key in info, f"Layout info missing key: {key}"

            # Verify math
            assert info['total_mapped_keys'] == info['shifted_keys'] + info['non_shifted_keys']

    def test_kedmanee_vs_pattajoti_digit_costs(self, kedmanee_layout, pattajoti_layout):
        """Test cost comparison between layouts for digits."""
        base_time = 0.28
        thai_digits = ['๐', '๑', '๒', '๓', '๔', '๕', '๖', '๗', '๘', '๙']

        for digit in thai_digits:
            ked_cost = kedmanee_layout.calculate_typing_cost(digit, base_time)
            pat_cost = pattajoti_layout.calculate_typing_cost(digit, base_time)

            # Kedmanee should always cost more for Thai digits (due to SHIFT)
            assert ked_cost > pat_cost, f"Kedmanee should cost more than Pattajoti for Thai digit {digit}"
            assert ked_cost == base_time * 2.0, f"Kedmanee cost for {digit} should be 2x base time"
            assert pat_cost == base_time, f"Pattajoti cost for {digit} should be base time"

    def test_international_digits_equal_cost(self, kedmanee_layout, pattajoti_layout):
        """Test that international digits cost the same on both layouts."""
        base_time = 0.28
        intl_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        for digit in intl_digits:
            ked_cost = kedmanee_layout.calculate_typing_cost(digit, base_time)
            pat_cost = pattajoti_layout.calculate_typing_cost(digit, base_time)

            # International digits should cost the same on both layouts
            assert ked_cost == pat_cost, f"International digit {digit} should cost same on both layouts"
            assert ked_cost == base_time, f"International digit {digit} should cost base time"


class TestModuleFunctions:
    """Test suite for module-level functions."""

    def test_explain_keyboard_rows_execution(self, capsys):
        """Test that explain_keyboard_rows executes without errors."""
        explain_keyboard_rows()

        captured = capsys.readouterr()
        assert "KEYBOARD ROW SYSTEM EXPLANATION" in captured.out
        assert "Row 3:" in captured.out
        assert "Row 2:" in captured.out
        assert "Row 1:" in captured.out
        assert "Row 0:" in captured.out
        assert "KEDMANEE" in captured.out
        assert "PATTAJOTI" in captured.out

    def test_compare_layouts_execution(self, capsys):
        """Test that compare_layouts executes without errors."""
        compare_layouts(base_keystroke_time=0.28)

        captured = capsys.readouterr()
        assert "KEYBOARD LAYOUT COMPARISON" in captured.out
        assert "Kedmanee Layout Info:" in captured.out
        assert "Pattajoti Layout Info:" in captured.out
        assert "DIGIT TYPING COSTS" in captured.out

    def test_compare_layouts_with_different_base_times(self, capsys):
        """Test compare_layouts with different base keystroke times."""
        base_times = [0.12, 0.28, 1.2]

        for base_time in base_times:
            capsys.readouterr()  # Clear previous output
            compare_layouts(base_keystroke_time=base_time)

            captured = capsys.readouterr()
            assert f"base time: {base_time}s" in captured.out


class TestEdgeCases:
    """Test suite for edge cases and error conditions."""

    def test_empty_character_handling(self, kedmanee_layout):
        """Test handling of empty character."""
        cost = kedmanee_layout.calculate_typing_cost('', 0.28)
        assert cost == 0.28  # Should return base cost

    def test_zero_base_time(self, kedmanee_layout):
        """Test handling of zero base time."""
        cost = kedmanee_layout.calculate_typing_cost('๑', 0.0)
        assert cost == 0.0  # Should handle zero gracefully

    def test_negative_base_time(self, kedmanee_layout):
        """Test handling of negative base time."""
        base_time = -0.1

        # Should still apply SHIFT multiplier
        cost = kedmanee_layout.calculate_typing_cost('๑', base_time)
        assert cost == base_time * 2.0

    def test_very_large_base_time(self, kedmanee_layout):
        """Test handling of very large base time."""
        base_time = 1000.0

        cost = kedmanee_layout.calculate_typing_cost('๑', base_time)
        assert cost == base_time * 2.0  # Should still apply SHIFT multiplier

    def test_unicode_edge_cases(self, kedmanee_layout, pattajoti_layout):
        """Test handling of various Unicode edge cases."""
        edge_cases = [
            '\u0000',  # Null character
            '\u200B',  # Zero-width space
            '﷽',       # Basmala (very wide character)
            '𝒽𝑒𝓁𝓁𝑜',   # Mathematical script characters
        ]

        for char in edge_cases:
            ked_cost = kedmanee_layout.calculate_typing_cost(char, 0.28)
            pat_cost = pattajoti_layout.calculate_typing_cost(char, 0.28)

            # Should handle gracefully and return base cost
            assert ked_cost == 0.28
            assert pat_cost == 0.28


class TestPerformance:
    """Test suite for performance-related tests."""

    def test_large_scale_cost_calculation(self, kedmanee_layout, pattajoti_layout):
        """Test performance with large number of cost calculations."""
        base_time = 0.28
        text = "๑๒๓๔๕๖๗๘๙๐" * 1000  # 10,000 characters

        # Should complete without performance issues
        total_ked_cost = sum(kedmanee_layout.calculate_typing_cost(char, base_time) for char in text)
        total_pat_cost = sum(pattajoti_layout.calculate_typing_cost(char, base_time) for char in text)

        # Verify calculations are correct
        expected_ked_cost = len(text) * base_time * 2.0  # All Thai digits with SHIFT
        expected_pat_cost = len(text) * base_time  # All Thai digits without SHIFT

        assert abs(total_ked_cost - expected_ked_cost) < 0.01
        assert abs(total_pat_cost - expected_pat_cost) < 0.01

    def test_key_lookup_performance(self, kedmanee_layout):
        """Test key lookup performance."""
        # Should be able to perform many lookups quickly
        for _ in range(10000):
            key_info = kedmanee_layout.get_key_info('๑')
            assert key_info is not None


# Pytest markers
pytestmark = [pytest.mark.unit]
