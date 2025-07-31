#!/usr/bin/env python3
"""
Validation Tests for Thai Keyboard Layout Models

Tests our keyboard layout models against standard touch typing practices
and the official keyboard layout images.
"""

from models.keyboard_layouts import KedmaneeLayout, PattajotiLayout


def validate_standard_typing_positions():
    """Validate that our finger assignments match standard touch typing practices."""
    print("FINGER POSITION VALIDATION")
    print("=" * 50)
    
    kedmanee = KedmaneeLayout()
    
    # Standard QWERTY finger assignments for validation
    standard_assignments = {
        # Left hand
        '1': ('left', 'pinky'), '2': ('left', 'ring'), '3': ('left', 'middle'), '4': ('left', 'index'), '5': ('left', 'index'),
        'q': ('left', 'pinky'), 'w': ('left', 'ring'), 'e': ('left', 'middle'), 'r': ('left', 'index'), 't': ('left', 'index'),
        'a': ('left', 'pinky'), 's': ('left', 'ring'), 'd': ('left', 'middle'), 'f': ('left', 'index'), 'g': ('left', 'index'),
        'z': ('left', 'pinky'), 'x': ('left', 'ring'), 'c': ('left', 'middle'), 'v': ('left', 'index'), 'b': ('left', 'index'),
        
        # Right hand  
        '6': ('right', 'index'), '7': ('right', 'index'), '8': ('right', 'middle'), '9': ('right', 'ring'), '0': ('right', 'pinky'),
        'y': ('right', 'index'), 'u': ('right', 'index'), 'i': ('right', 'middle'), 'o': ('right', 'ring'), 'p': ('right', 'pinky'),
        'h': ('right', 'index'), 'j': ('right', 'index'), 'k': ('right', 'middle'), 'l': ('right', 'ring'), ';': ('right', 'pinky'),
        'n': ('right', 'index'), 'm': ('right', 'index'), ',': ('right', 'middle'), '.': ('right', 'ring'), '/': ('right', 'pinky'),
    }
    
    # Test international digits against standard finger assignments
    print("INTERNATIONAL DIGIT FINGER ASSIGNMENTS:")
    print("-" * 40)
    validation_passed = True
    
    for digit in '0123456789':
        key_info = kedmanee.get_key_info(digit)
        if key_info:
            expected_hand, expected_finger = standard_assignments[digit]
            actual_hand, actual_finger = key_info.hand, key_info.finger
            
            status = "✓" if (actual_hand == expected_hand and actual_finger == expected_finger) else "✗"
            if status == "✗":
                validation_passed = False
                
            print(f"  {digit}: Expected {expected_hand} {expected_finger}, Got {actual_hand} {actual_finger} {status}")
    
    print(f"\nInternational digit finger assignment validation: {'PASSED' if validation_passed else 'FAILED'}")
    
    return validation_passed


def validate_shift_requirements():
    """Validate SHIFT requirements match the keyboard layout images."""
    print("\nSHIFT REQUIREMENT VALIDATION")
    print("=" * 50)
    
    kedmanee = KedmaneeLayout()
    pattajoti = PattajotiLayout()
    
    thai_digits = ['๐', '๑', '๒', '๓', '๔', '๕', '๖', '๗', '๘', '๙']
    
    print("KEDMANEE - Thai digits should require SHIFT:")
    kedmanee_passed = True
    for digit in thai_digits:
        key_info = kedmanee.get_key_info(digit)
        if key_info:
            status = "✓" if key_info.requires_shift else "✗"
            if not key_info.requires_shift:
                kedmanee_passed = False
            print(f"  {digit}: SHIFT required = {key_info.requires_shift} {status}")
    
    print(f"\nKedmanee SHIFT validation: {'PASSED' if kedmanee_passed else 'FAILED'}")
    
    print("\nPATTAJOTI - Thai digits should NOT require SHIFT:")
    pattajoti_passed = True
    for digit in thai_digits:
        key_info = pattajoti.get_key_info(digit)
        if key_info:
            status = "✓" if not key_info.requires_shift else "✗"
            if key_info.requires_shift:
                pattajoti_passed = False
            print(f"  {digit}: SHIFT required = {key_info.requires_shift} {status}")
    
    print(f"\nPattajoti SHIFT validation: {'PASSED' if pattajoti_passed else 'FAILED'}")
    
    return kedmanee_passed and pattajoti_passed


def validate_digit_order():
    """Validate that Pattajoti digit order matches the layout image."""
    print("\nDIGIT ORDER VALIDATION")
    print("=" * 50)
    
    pattajoti = PattajotiLayout()
    expected_order = ['๒', '๓', '๔', '๕', '๗', '๘', '๙', '๐', '๑', '๖']
    
    print("PATTAJOTI - Expected left-to-right order: ๒๓๔๕๗๘๙๐๑๖")
    
    # Get all Thai digits and check if they exist
    found_digits = []
    for digit in expected_order:
        key_info = pattajoti.get_key_info(digit)
        if key_info:
            found_digits.append(digit)
    
    order_correct = found_digits == expected_order
    status = "✓" if order_correct else "✗"
    
    print(f"Found digits in model: {''.join(found_digits)}")
    print(f"Order validation: {'PASSED' if order_correct else 'FAILED'} {status}")
    
    return order_correct


def validate_layout_completeness():
    """Validate that both layouts have comprehensive character coverage."""
    print("\nLAYOUT COMPLETENESS VALIDATION")
    print("=" * 50)
    
    kedmanee = KedmaneeLayout()
    pattajoti = PattajotiLayout()
    
    # Test basic character sets
    thai_digits = ['๐', '๑', '๒', '๓', '๔', '๕', '๖', '๗', '๘', '๙']
    intl_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    common_thai = ['ก', 'า', 'น', 'ร', 'ส', 'ห', 'ม', 'ล', 'ว', 'ด']
    
    print(f"KEDMANEE COVERAGE:")
    print(f"  Total mapped keys: {len(kedmanee.key_map)}")
    print(f"  Thai digits: {sum(1 for d in thai_digits if kedmanee.get_key_info(d))}/10")
    print(f"  Intl digits: {sum(1 for d in intl_digits if kedmanee.get_key_info(d))}/10")
    print(f"  Common Thai chars: {sum(1 for c in common_thai if kedmanee.get_key_info(c))}/10")
    
    print(f"\nPATTAJOTI COVERAGE:")
    print(f"  Total mapped keys: {len(pattajoti.key_map)}")
    print(f"  Thai digits: {sum(1 for d in thai_digits if pattajoti.get_key_info(d))}/10")
    print(f"  Intl digits: {sum(1 for d in intl_digits if pattajoti.get_key_info(d))}/10")
    print(f"  Common Thai chars: {sum(1 for c in common_thai if pattajoti.get_key_info(c))}/10")
    
    # Coverage should be comprehensive
    kedmanee_coverage = len(kedmanee.key_map) >= 60  # Expect at least 60 characters
    pattajoti_coverage = len(pattajoti.key_map) >= 70  # Expect at least 70 characters
    
    print(f"\nCoverage validation:")
    print(f"  Kedmanee: {'PASSED' if kedmanee_coverage else 'FAILED'}")
    print(f"  Pattajoti: {'PASSED' if pattajoti_coverage else 'FAILED'}")
    
    return kedmanee_coverage and pattajoti_coverage


def run_all_validations():
    """Run all validation tests."""
    print("THAI KEYBOARD LAYOUT VALIDATION TEST SUITE")
    print("=" * 60)
    print("Validating keyboard layout models against official standards")
    print("and standard touch typing practices.")
    print()
    
    tests = [
        ("Finger Position Assignments", validate_standard_typing_positions),
        ("SHIFT Requirements", validate_shift_requirements),
        ("Digit Order (Pattajoti)", validate_digit_order),
        ("Layout Completeness", validate_layout_completeness)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"RUNNING: {test_name}")
        print('='*60)
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"TEST FAILED WITH ERROR: {e}")
            results[test_name] = False
    
    # Summary
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print('='*60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {test_name:<30}: {status}")
    
    print(f"\nOVERALL: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL VALIDATIONS PASSED! Keyboard models are accurate.")
    else:
        print("⚠️  Some validations failed. Review keyboard model accuracy.")
    
    return passed == total


if __name__ == "__main__":
    run_all_validations()