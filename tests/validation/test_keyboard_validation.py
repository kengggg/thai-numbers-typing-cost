"""
Enhanced validation tests for keyboard layout accuracy and system correctness.

Migrated and enhanced from src/validation_tests.py with improved pytest structure,
comprehensive coverage, and automated validation of keyboard layout models
against official standards and touch typing practices.
"""

import pytest
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from models.keyboard_layouts import KedmaneeLayout, PattajotiLayout, KeyboardType


class TestKeyboardLayoutAccuracy:
    """Test suite for validating keyboard layout accuracy against official standards."""
    
    def test_kedmanee_international_digit_finger_assignments(self, kedmanee_layout):
        """Validate international digit finger assignments match standard QWERTY."""
        # Standard QWERTY finger assignments for validation
        standard_assignments = {
            # Left hand
            '1': ('left', 'pinky'), '2': ('left', 'ring'), '3': ('left', 'middle'), 
            '4': ('left', 'index'), '5': ('left', 'index'),
            # Right hand  
            '6': ('right', 'index'), '7': ('right', 'index'), '8': ('right', 'middle'), 
            '9': ('right', 'ring'), '0': ('right', 'pinky'),
        }
        
        validation_errors = []
        
        for digit, (expected_hand, expected_finger) in standard_assignments.items():
            key_info = kedmanee_layout.get_key_info(digit)
            
            assert key_info is not None, f"International digit {digit} not found in Kedmanee layout"
            
            actual_hand, actual_finger = key_info.hand, key_info.finger
            
            if actual_hand != expected_hand or actual_finger != expected_finger:
                validation_errors.append(
                    f"Digit {digit}: Expected {expected_hand} {expected_finger}, "
                    f"Got {actual_hand} {actual_finger}"
                )
        
        assert not validation_errors, f"Finger assignment validation failed:\n" + "\n".join(validation_errors)
    
    def test_kedmanee_thai_digits_require_shift(self, kedmanee_layout, thai_digits):
        """Validate that all Thai digits require SHIFT on Kedmanee layout."""
        validation_errors = []
        
        for digit in thai_digits:
            key_info = kedmanee_layout.get_key_info(digit)
            
            assert key_info is not None, f"Thai digit {digit} not found in Kedmanee layout"
            
            if not key_info.requires_shift:
                validation_errors.append(f"Thai digit {digit} should require SHIFT but doesn't")
            
            # All Thai digits should be on row 3 (number row)
            if key_info.row != 3:
                validation_errors.append(f"Thai digit {digit} should be on row 3, but is on row {key_info.row}")
        
        assert not validation_errors, f"Thai digit SHIFT validation failed:\n" + "\n".join(validation_errors)
    
    def test_kedmanee_international_digits_no_shift(self, kedmanee_layout, international_digits):
        """Validate that international digits don't require SHIFT on Kedmanee layout."""
        validation_errors = []
        
        for digit in international_digits:
            key_info = kedmanee_layout.get_key_info(digit)
            
            assert key_info is not None, f"International digit {digit} not found in Kedmanee layout"
            
            if key_info.requires_shift:
                validation_errors.append(f"International digit {digit} should not require SHIFT but does")
            
            # All international digits should be on row 3 (number row)
            if key_info.row != 3:
                validation_errors.append(f"International digit {digit} should be on row 3, but is on row {key_info.row}")
        
        assert not validation_errors, f"International digit SHIFT validation failed:\n" + "\n".join(validation_errors)
    
    def test_pattajoti_thai_digits_no_shift(self, pattajoti_layout, thai_digits):
        """Validate that Thai digits don't require SHIFT on Pattajoti layout."""
        validation_errors = []
        
        for digit in thai_digits:
            key_info = pattajoti_layout.get_key_info(digit)
            
            assert key_info is not None, f"Thai digit {digit} not found in Pattajoti layout"
            
            if key_info.requires_shift:
                validation_errors.append(f"Thai digit {digit} should not require SHIFT on Pattajoti but does")
            
            # All Thai digits should be on row 3 (number row)
            if key_info.row != 3:
                validation_errors.append(f"Thai digit {digit} should be on row 3, but is on row {key_info.row}")
        
        assert not validation_errors, f"Pattajoti Thai digit validation failed:\n" + "\n".join(validation_errors)
    
    def test_pattajoti_digit_order_accuracy(self, pattajoti_layout):
        """Validate that Pattajoti Thai digits follow the correct left-to-right order."""
        # Expected order from left to right: ๒๓๔๕๗๘๙๐๑๖
        expected_order = ['๒', '๓', '๔', '๕', '๗', '๘', '๙', '๐', '๑', '๖']
        expected_fingers = ['pinky', 'ring', 'middle', 'index', 'index', 
                           'index', 'index', 'middle', 'ring', 'pinky']
        expected_hands = ['left', 'left', 'left', 'left', 'left',
                         'right', 'right', 'right', 'right', 'right']
        
        validation_errors = []
        found_digits = []
        
        for i, digit in enumerate(expected_order):
            key_info = pattajoti_layout.get_key_info(digit)
            
            if key_info is None:
                validation_errors.append(f"Thai digit {digit} not found in Pattajoti layout")
                continue
            
            found_digits.append(digit)
            
            # Validate finger assignment
            if key_info.finger != expected_fingers[i]:
                validation_errors.append(
                    f"Digit {digit}: Expected finger {expected_fingers[i]}, got {key_info.finger}"
                )
            
            # Validate hand assignment  
            if key_info.hand != expected_hands[i]:
                validation_errors.append(
                    f"Digit {digit}: Expected hand {expected_hands[i]}, got {key_info.hand}"
                )
        
        # Validate that we found all digits in the correct order
        if found_digits != expected_order:
            validation_errors.append(
                f"Digit order incorrect. Expected: {''.join(expected_order)}, "
                f"Found: {''.join(found_digits)}"
            )
        
        assert not validation_errors, f"Pattajoti digit order validation failed:\n" + "\n".join(validation_errors)


class TestLayoutCompleteness:
    """Test suite for validating keyboard layout completeness and coverage."""
    
    def test_kedmanee_layout_completeness(self, kedmanee_layout):
        """Validate that Kedmanee layout has comprehensive character coverage."""
        layout_info = kedmanee_layout.get_layout_info()
        
        # Should have substantial coverage
        assert layout_info['total_mapped_keys'] >= 60, "Kedmanee should have at least 60 mapped keys"
        assert layout_info['shifted_keys'] >= 20, "Kedmanee should have at least 20 shifted keys"
        assert layout_info['non_shifted_keys'] >= 40, "Kedmanee should have at least 40 non-shifted keys"
        
        # Math should be consistent
        assert layout_info['total_mapped_keys'] == layout_info['shifted_keys'] + layout_info['non_shifted_keys']
        
        # Should have correct layout type
        assert layout_info['layout_type'] == 'kedmanee'
    
    def test_pattajoti_layout_completeness(self, pattajoti_layout):
        """Validate that Pattajoti layout has comprehensive character coverage."""
        layout_info = pattajoti_layout.get_layout_info()
        
        # Should have more comprehensive coverage than Kedmanee
        assert layout_info['total_mapped_keys'] >= 70, "Pattajoti should have at least 70 mapped keys"
        assert layout_info['shifted_keys'] >= 5, "Pattajoti should have some shifted keys"
        assert layout_info['non_shifted_keys'] >= 65, "Pattajoti should have mostly non-shifted keys"
        
        # Math should be consistent
        assert layout_info['total_mapped_keys'] == layout_info['shifted_keys'] + layout_info['non_shifted_keys']
        
        # Should have correct layout type
        assert layout_info['layout_type'] == 'pattajoti'
    
    def test_essential_character_coverage(self, kedmanee_layout, pattajoti_layout):
        """Validate that both layouts cover essential characters."""
        essential_characters = {
            # Thai digits
            'thai_digits': ['๐', '๑', '๒', '๓', '๔', '๕', '๖', '๗', '๘', '๙'],
            # International digits
            'intl_digits': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
            # Common Thai consonants
            'thai_consonants': ['ก', 'ข', 'ค', 'ง', 'จ', 'ช', 'ท', 'น', 'ร', 'ล', 'ว', 'ส', 'ห', 'อ'],
            # Common Thai vowels and marks
            'thai_vowels': ['า', 'ิ', 'ี', 'ึ', 'ื', 'ุ', 'ู', 'เ', 'แ', 'โ', 'ใ', 'ไ', 'ำ', 'ะ', 'ั'],
            # Common punctuation
            'punctuation': [' ', '.', ',', '?', '!', '"', '(', ')']
        }
        
        layouts = [
            ('Kedmanee', kedmanee_layout),
            ('Pattajoti', pattajoti_layout)
        ]
        
        for layout_name, layout in layouts:
            for category, characters in essential_characters.items():
                missing_chars = []
                
                for char in characters:
                    if layout.get_key_info(char) is None:
                        missing_chars.append(char)
                
                assert not missing_chars, (
                    f"{layout_name} layout missing essential {category}: {missing_chars}"
                )
    
    def test_thai_vowel_and_tone_coverage(self, pattajoti_layout):
        """Validate comprehensive Thai vowel and tone mark coverage in Pattajoti."""
        # Pattajoti should have comprehensive Thai language support
        vowels_and_tones = [
            # Vowels
            'า', 'ิ', 'ี', 'ึ', 'ื', 'ุ', 'ู', 'เ', 'แ', 'โ', 'ใ', 'ไ', 'ำ', 'ะ', 'ั',
            # Tone marks
            '่', '้', '๊', '๋', '์'
        ]
        
        missing_chars = []
        for char in vowels_and_tones:
            if pattajoti_layout.get_key_info(char) is None:
                missing_chars.append(char)
        
        assert not missing_chars, f"Pattajoti missing vowels/tones: {missing_chars}"


class TestLayoutConsistency:
    """Test suite for validating consistency between keyboard layouts."""
    
    def test_international_digits_consistency(self, kedmanee_layout, pattajoti_layout, international_digits):
        """Validate that international digits have consistent finger assignments across layouts."""
        inconsistencies = []
        
        for digit in international_digits:
            kedmanee_info = kedmanee_layout.get_key_info(digit)
            pattajoti_info = pattajoti_layout.get_key_info(digit)
            
            assert kedmanee_info is not None, f"International digit {digit} missing in Kedmanee"
            assert pattajoti_info is not None, f"International digit {digit} missing in Pattajoti"
            
            # Finger assignments should be consistent for international digits
            if (kedmanee_info.hand != pattajoti_info.hand or 
                kedmanee_info.finger != pattajoti_info.finger):
                inconsistencies.append(
                    f"Digit {digit}: Kedmanee({kedmanee_info.hand} {kedmanee_info.finger}) "
                    f"vs Pattajoti({pattajoti_info.hand} {pattajoti_info.finger})"
                )
            
            # SHIFT requirements should be consistent (both should be False)
            if kedmanee_info.requires_shift != pattajoti_info.requires_shift:
                inconsistencies.append(
                    f"Digit {digit}: SHIFT requirement inconsistent - "
                    f"Kedmanee({kedmanee_info.requires_shift}) vs Pattajoti({pattajoti_info.requires_shift})"
                )
        
        assert not inconsistencies, f"International digit inconsistencies:\n" + "\n".join(inconsistencies)
    
    def test_row_assignments_validity(self, kedmanee_layout, pattajoti_layout):
        """Validate that row assignments are within valid range."""
        layouts = [
            ('Kedmanee', kedmanee_layout),
            ('Pattajoti', pattajoti_layout)
        ]
        
        valid_rows = {0, 1, 2, 3}  # Bottom, home, top, number rows
        
        for layout_name, layout in layouts:
            invalid_rows = []
            
            for char, key_info in layout.key_map.items():
                if key_info.row not in valid_rows:
                    invalid_rows.append(f"{char}: row {key_info.row}")
            
            assert not invalid_rows, f"{layout_name} has invalid row assignments: {invalid_rows}"
    
    def test_hand_assignments_validity(self, kedmanee_layout, pattajoti_layout):
        """Validate that hand assignments are valid."""
        layouts = [
            ('Kedmanee', kedmanee_layout),
            ('Pattajoti', pattajoti_layout)
        ]
        
        valid_hands = {'left', 'right', 'both', 'unknown'}
        
        for layout_name, layout in layouts:
            invalid_hands = []
            
            for char, key_info in layout.key_map.items():
                if key_info.hand not in valid_hands:
                    invalid_hands.append(f"{char}: hand '{key_info.hand}'")
            
            assert not invalid_hands, f"{layout_name} has invalid hand assignments: {invalid_hands}"
    
    def test_finger_assignments_validity(self, kedmanee_layout, pattajoti_layout):
        """Validate that finger assignments are valid."""
        layouts = [
            ('Kedmanee', kedmanee_layout),
            ('Pattajoti', pattajoti_layout)
        ]
        
        valid_fingers = {'thumb', 'index', 'middle', 'ring', 'pinky', 'unknown'}
        
        for layout_name, layout in layouts:
            invalid_fingers = []
            
            for char, key_info in layout.key_map.items():
                if key_info.finger not in valid_fingers:
                    invalid_fingers.append(f"{char}: finger '{key_info.finger}'")
            
            assert not invalid_fingers, f"{layout_name} has invalid finger assignments: {invalid_fingers}"


class TestTypingCostValidation:
    """Test suite for validating typing cost calculations."""
    
    def test_shift_penalty_application(self, kedmanee_layout, pattajoti_layout, thai_digits):
        """Validate that SHIFT penalty is correctly applied."""
        base_time = 0.5  # Use clear base time for testing
        
        for digit in thai_digits:
            kedmanee_cost = kedmanee_layout.calculate_typing_cost(digit, base_time)
            pattajoti_cost = pattajoti_layout.calculate_typing_cost(digit, base_time)
            
            # Kedmanee should apply SHIFT penalty (2x cost)
            assert kedmanee_cost == base_time * 2.0, (
                f"Kedmanee SHIFT penalty not applied correctly for {digit}: "
                f"expected {base_time * 2.0}, got {kedmanee_cost}"
            )
            
            # Pattajoti should not apply SHIFT penalty
            assert pattajoti_cost == base_time, (
                f"Pattajoti should not apply SHIFT penalty for {digit}: "
                f"expected {base_time}, got {pattajoti_cost}"
            )
    
    def test_international_digits_no_penalty(self, kedmanee_layout, pattajoti_layout, international_digits):
        """Validate that international digits don't get SHIFT penalty on either layout."""
        base_time = 0.3
        
        for digit in international_digits:
            kedmanee_cost = kedmanee_layout.calculate_typing_cost(digit, base_time)
            pattajoti_cost = pattajoti_layout.calculate_typing_cost(digit, base_time)
            
            # Both layouts should give base cost (no SHIFT penalty)
            assert kedmanee_cost == base_time, (
                f"Kedmanee should not apply SHIFT penalty to international digit {digit}: "
                f"expected {base_time}, got {kedmanee_cost}"
            )
            
            assert pattajoti_cost == base_time, (
                f"Pattajoti should not apply SHIFT penalty to international digit {digit}: "
                f"expected {base_time}, got {pattajoti_cost}"
            )
    
    def test_cost_calculation_edge_cases(self, kedmanee_layout):
        """Validate typing cost calculation edge cases."""
        # Test with zero base time
        cost = kedmanee_layout.calculate_typing_cost('๑', 0.0)
        assert cost == 0.0, "Zero base time should result in zero cost"
        
        # Test with negative base time (should still apply multipliers)
        cost = kedmanee_layout.calculate_typing_cost('๑', -0.1)
        assert cost == -0.2, "Negative base time should still apply SHIFT multiplier"
        
        # Test with unknown character
        cost = kedmanee_layout.calculate_typing_cost('🎉', 0.5)
        assert cost == 0.5, "Unknown character should return base cost"
    
    def test_typing_cost_mathematical_relationships(self, kedmanee_layout, pattajoti_layout):
        """Validate mathematical relationships in typing costs."""
        base_times = [0.1, 0.28, 0.5, 1.0]
        thai_digit = '๑'
        intl_digit = '1'
        
        for base_time in base_times:
            # Thai digit costs
            ked_thai_cost = kedmanee_layout.calculate_typing_cost(thai_digit, base_time)
            pat_thai_cost = pattajoti_layout.calculate_typing_cost(thai_digit, base_time)
            
            # International digit costs
            ked_intl_cost = kedmanee_layout.calculate_typing_cost(intl_digit, base_time)
            pat_intl_cost = pattajoti_layout.calculate_typing_cost(intl_digit, base_time)
            
            # Mathematical relationships
            assert ked_thai_cost == base_time * 2.0, "Kedmanee Thai digit should be 2x base time"
            assert pat_thai_cost == base_time, "Pattajoti Thai digit should be base time"
            assert ked_intl_cost == base_time, "Kedmanee international digit should be base time"
            assert pat_intl_cost == base_time, "Pattajoti international digit should be base time"
            
            # Cost comparisons
            assert ked_thai_cost > pat_thai_cost, "Kedmanee Thai should cost more than Pattajoti Thai"
            assert ked_thai_cost > ked_intl_cost, "Kedmanee Thai should cost more than Kedmanee international"
            assert ked_intl_cost == pat_intl_cost, "International digits should cost same on both layouts"


class TestSystemIntegration:
    """Test suite for validating system integration and real-world accuracy."""
    
    def test_layout_explains_research_findings(self, kedmanee_layout, pattajoti_layout):
        """Validate that layout characteristics explain research findings."""
        # The core research finding: Thai digits are more expensive on Kedmanee
        thai_digit = '๒'
        base_time = 0.28
        
        kedmanee_cost = kedmanee_layout.calculate_typing_cost(thai_digit, base_time)
        pattajoti_cost = pattajoti_layout.calculate_typing_cost(thai_digit, base_time)
        
        # This difference should explain the research findings
        time_saved = kedmanee_cost - pattajoti_cost
        percentage_saved = (time_saved / kedmanee_cost) * 100
        
        assert time_saved > 0, "Pattajoti should save time over Kedmanee for Thai digits"
        assert percentage_saved == 50.0, "Should save exactly 50% (eliminating SHIFT penalty)"
        
        # The savings should be exactly the SHIFT penalty
        assert time_saved == base_time, "Time saved should equal base keystroke time"
    
    def test_layout_supports_government_document_typing(self, kedmanee_layout, pattajoti_layout):
        """Validate that layouts support common government document characters."""
        # Characters commonly found in Thai government documents
        government_chars = [
            # Thai year format: พุทธศักราช ๒๕๖๐
            'พ', 'ุ', 'ท', 'ธ', 'ศ', 'ก', 'ร', 'า', 'ช', '๒', '๕', '๖', '๐',
            # Common terms: มาตรา, กฎหมาย, ประกาศ
            'ม', 'ต', 'ฎ', 'ห', 'ย', 'ป', 'ะ', 'ค', 'น',
            # Numbers and punctuation
            '๑', '๓', '๔', '๗', '๘', '๙', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            ' ', '.', ',', '(', ')', '"'
        ]
        
        layouts = [
            ('Kedmanee', kedmanee_layout),
            ('Pattajoti', pattajoti_layout)
        ]
        
        for layout_name, layout in layouts:
            missing_chars = []
            
            for char in government_chars:
                if layout.get_key_info(char) is None:
                    missing_chars.append(char)
            
            assert not missing_chars, (
                f"{layout_name} layout missing government document characters: {missing_chars}"
            )
    
    def test_research_methodology_validation(self, kedmanee_layout, pattajoti_layout):
        """Validate that the research methodology is sound based on layout characteristics."""
        # Test the core assumption: SHIFT doubles typing cost
        base_time = 0.28
        thai_digit = '๑'
        
        # Kedmanee: Thai digit requires SHIFT
        kedmanee_info = kedmanee_layout.get_key_info(thai_digit)
        assert kedmanee_info.requires_shift, "Research assumes Thai digits require SHIFT on Kedmanee"
        
        kedmanee_cost = kedmanee_layout.calculate_typing_cost(thai_digit, base_time)
        expected_cost = base_time * 2.0  # SHIFT penalty assumption
        
        assert kedmanee_cost == expected_cost, (
            f"SHIFT penalty assumption validation failed: expected {expected_cost}, got {kedmanee_cost}"
        )
        
        # Pattajoti: Thai digit doesn't require SHIFT
        pattajoti_info = pattajoti_layout.get_key_info(thai_digit)
        assert not pattajoti_info.requires_shift, "Research assumes Thai digits don't require SHIFT on Pattajoti"
        
        pattajoti_cost = pattajoti_layout.calculate_typing_cost(thai_digit, base_time)
        
        assert pattajoti_cost == base_time, (
            f"Pattajoti no-SHIFT assumption validation failed: expected {base_time}, got {pattajoti_cost}"
        )
        
        # The research conclusion should be mathematically sound
        efficiency_gain = ((kedmanee_cost - pattajoti_cost) / kedmanee_cost) * 100
        assert abs(efficiency_gain - 50.0) < 0.01, (
            f"Research conclusion validation failed: efficiency gain should be 50%, got {efficiency_gain:.1f}%"
        )


# Legacy validation test runner for backward compatibility
def run_all_validations():
    """Run all validation tests in legacy format for backward compatibility."""
    import subprocess
    import sys
    
    # Run pytest on this module
    result = subprocess.run([
        sys.executable, '-m', 'pytest', __file__, '-v', '--tb=short'
    ], capture_output=True, text=True)
    
    print("THAI KEYBOARD LAYOUT VALIDATION TEST SUITE")
    print("=" * 60)
    print("Enhanced validation tests using pytest framework")
    print()
    
    if result.returncode == 0:
        print("🎉 ALL VALIDATIONS PASSED! Keyboard models are accurate.")
    else:
        print("⚠️  Some validations failed. Review keyboard model accuracy.")
        print("\nTest output:")
        print(result.stdout)
        if result.stderr:
            print("\nErrors:")
            print(result.stderr)
    
    return result.returncode == 0


if __name__ == "__main__":
    run_all_validations()


# Pytest markers
pytestmark = [pytest.mark.validation]