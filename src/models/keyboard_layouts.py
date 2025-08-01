#!/usr/bin/env python3
"""
Thai Keyboard Layout Models
Defines Thai Kedmanee and Pattajoti keyboard layouts with typing cost calculations.
"""

from enum import Enum
from typing import Dict, Optional


class KeyboardType(Enum):
    """Keyboard layout types."""

    KEDMANEE = "kedmanee"
    PATTAJOTI = "pattajoti"


class KeyInfo:
    """Information about a key's typing characteristics."""

    def __init__(
        self,
        char: str,
        requires_shift: bool = False,
        hand: str = "unknown",
        finger: str = "unknown",
        row: int = 0,
    ):
        self.char = char
        self.requires_shift = requires_shift
        self.hand = hand  # "left" or "right"
        self.finger = finger  # "thumb", "index", "middle", "ring", "pinky"
        self.row = (
            row  # Keyboard rows: 0=bottom, 1=home (easiest), 2=top, 3=numbers (hardest)
        )


class ThaiKeyboardLayout:
    """Base class for Thai keyboard layouts."""

    def __init__(self, layout_type: KeyboardType):
        self.layout_type = layout_type
        self.key_map: Dict[str, KeyInfo] = {}
        self._initialize_layout()

    def _initialize_layout(self) -> None:
        """Initialize the keyboard layout. Override in subclasses."""
        raise NotImplementedError

    def get_key_info(self, char: str) -> Optional[KeyInfo]:
        """Get key information for a character."""
        return self.key_map.get(char)

    def calculate_typing_cost(
        self, char: str, base_keystroke_time: float = 0.28
    ) -> float:
        """Calculate typing cost for a character in seconds.

        Args:
            char: Character to calculate cost for
            base_keystroke_time: Base time per keystroke in seconds
        """
        key_info = self.get_key_info(char)
        if not key_info:
            return base_keystroke_time  # Default cost for unknown characters

        cost = base_keystroke_time

        # Double cost for shifted characters (core research question)
        if key_info.requires_shift:
            cost *= 2.0

        return cost

    def get_layout_info(self) -> Dict:
        """Get information about the keyboard layout."""
        total_keys = len(self.key_map)
        shifted_keys = sum(1 for key in self.key_map.values() if key.requires_shift)

        return {
            "layout_type": self.layout_type.value,
            "total_mapped_keys": total_keys,
            "shifted_keys": shifted_keys,
            "non_shifted_keys": total_keys - shifted_keys,
        }


class KedmaneeLayout(ThaiKeyboardLayout):
    """Thai Kedmanee keyboard layout."""

    def __init__(self) -> None:
        super().__init__(KeyboardType.KEDMANEE)

    def _initialize_layout(self) -> None:
        """Initialize Kedmanee layout with key positions and characteristics.
        Based on TIS 820-2535 Thai Keyboard Layout Standard.
        """

        # Thai digits on Kedmanee require SHIFT key (located on number row)
        thai_digits = {
            "๐": KeyInfo("๐", requires_shift=True, hand="right", finger="pinky", row=3),
            "๑": KeyInfo("๑", requires_shift=True, hand="left", finger="pinky", row=3),
            "๒": KeyInfo("๒", requires_shift=True, hand="left", finger="ring", row=3),
            "๓": KeyInfo("๓", requires_shift=True, hand="left", finger="middle", row=3),
            "๔": KeyInfo("๔", requires_shift=True, hand="left", finger="index", row=3),
            "๕": KeyInfo("๕", requires_shift=True, hand="left", finger="index", row=3),
            "๖": KeyInfo("๖", requires_shift=True, hand="right", finger="index", row=3),
            "๗": KeyInfo("๗", requires_shift=True, hand="right", finger="index", row=3),
            "๘": KeyInfo(
                "๘", requires_shift=True, hand="right", finger="middle", row=3
            ),
            "๙": KeyInfo("๙", requires_shift=True, hand="right", finger="ring", row=3),
        }

        # International digits on Kedmanee (no shift required, on number row)
        intl_digits = {
            "0": KeyInfo(
                "0", requires_shift=False, hand="right", finger="pinky", row=3
            ),
            "1": KeyInfo("1", requires_shift=False, hand="left", finger="pinky", row=3),
            "2": KeyInfo("2", requires_shift=False, hand="left", finger="ring", row=3),
            "3": KeyInfo(
                "3", requires_shift=False, hand="left", finger="middle", row=3
            ),
            "4": KeyInfo("4", requires_shift=False, hand="left", finger="index", row=3),
            "5": KeyInfo("5", requires_shift=False, hand="left", finger="index", row=3),
            "6": KeyInfo(
                "6", requires_shift=False, hand="right", finger="index", row=3
            ),
            "7": KeyInfo(
                "7", requires_shift=False, hand="right", finger="index", row=3
            ),
            "8": KeyInfo(
                "8", requires_shift=False, hand="right", finger="middle", row=3
            ),
            "9": KeyInfo("9", requires_shift=False, hand="right", finger="ring", row=3),
        }

        # Thai consonants and vowels based on TIS 820-2535 standard
        thai_characters = {
            # Row 2 (Top row) - Based on QWERTYUIOP positions
            "ไ": KeyInfo("ไ", requires_shift=False, hand="left", finger="pinky", row=2),
            "ำ": KeyInfo("ำ", requires_shift=False, hand="left", finger="ring", row=2),
            "พ": KeyInfo(
                "พ", requires_shift=False, hand="left", finger="middle", row=2
            ),
            "ะ": KeyInfo("ะ", requires_shift=False, hand="left", finger="index", row=2),
            "ั": KeyInfo("ั", requires_shift=False, hand="left", finger="index", row=2),
            "ี": KeyInfo("ี", requires_shift=False, hand="right", finger="index", row=2),
            "ร": KeyInfo(
                "ร", requires_shift=False, hand="right", finger="index", row=2
            ),
            "น": KeyInfo(
                "น", requires_shift=False, hand="right", finger="middle", row=2
            ),
            "ย": KeyInfo("ย", requires_shift=False, hand="right", finger="ring", row=2),
            "บ": KeyInfo(
                "บ", requires_shift=False, hand="right", finger="pinky", row=2
            ),
            # Row 1 (Home row) - Based on ASDFGHJKL; positions
            "ฟ": KeyInfo("ฟ", requires_shift=False, hand="left", finger="pinky", row=1),
            "ห": KeyInfo("ห", requires_shift=False, hand="left", finger="ring", row=1),
            "ก": KeyInfo(
                "ก", requires_shift=False, hand="left", finger="middle", row=1
            ),
            "ด": KeyInfo("ด", requires_shift=False, hand="left", finger="index", row=1),
            "เ": KeyInfo("เ", requires_shift=False, hand="left", finger="index", row=1),
            "้": KeyInfo("้", requires_shift=False, hand="right", finger="index", row=1),
            "่": KeyInfo("่", requires_shift=False, hand="right", finger="index", row=1),
            "า": KeyInfo(
                "า", requires_shift=False, hand="right", finger="middle", row=1
            ),
            "ส": KeyInfo("ส", requires_shift=False, hand="right", finger="ring", row=1),
            "ว": KeyInfo(
                "ว", requires_shift=False, hand="right", finger="pinky", row=1
            ),
            # Row 0 (Bottom row) - Based on ZXCVBNM,./ positions
            "ผ": KeyInfo("ผ", requires_shift=False, hand="left", finger="pinky", row=0),
            "ป": KeyInfo("ป", requires_shift=False, hand="left", finger="ring", row=0),
            "แ": KeyInfo(
                "แ", requires_shift=False, hand="left", finger="middle", row=0
            ),
            "อ": KeyInfo("อ", requires_shift=False, hand="left", finger="index", row=0),
            "ิ": KeyInfo("ิ", requires_shift=False, hand="left", finger="index", row=0),
            "ื": KeyInfo("ื", requires_shift=False, hand="right", finger="index", row=0),
            "ท": KeyInfo(
                "ท", requires_shift=False, hand="right", finger="index", row=0
            ),
            "ม": KeyInfo(
                "ม", requires_shift=False, hand="right", finger="middle", row=0
            ),
            "ใ": KeyInfo("ใ", requires_shift=False, hand="right", finger="ring", row=0),
            "ฝ": KeyInfo(
                "ฝ", requires_shift=False, hand="right", finger="pinky", row=0
            ),
            # Common Thai characters likely to appear in government documents
            "ช": KeyInfo(
                "ช", requires_shift=True, hand="left", finger="middle", row=1
            ),  # Shifted ก
            "ซ": KeyInfo(
                "ซ", requires_shift=True, hand="right", finger="ring", row=1
            ),  # Shifted ส
            "ญ": KeyInfo(
                "ญ", requires_shift=True, hand="right", finger="middle", row=2
            ),  # Shifted น
            "ณ": KeyInfo(
                "ณ", requires_shift=True, hand="right", finger="index", row=2
            ),  # Shifted ร
            "ค": KeyInfo(
                "ค", requires_shift=True, hand="left", finger="index", row=1
            ),  # Shifted ด
            "ต": KeyInfo(
                "ต", requires_shift=True, hand="left", finger="index", row=0
            ),  # Shifted อ
            "จ": KeyInfo(
                "จ", requires_shift=True, hand="left", finger="index", row=1
            ),  # Shifted เ
            "ข": KeyInfo(
                "ข", requires_shift=True, hand="left", finger="ring", row=1
            ),  # Shifted ห
            "ล": KeyInfo(
                "ล", requires_shift=True, hand="right", finger="ring", row=1
            ),  # Shifted ส (alt)
            "ง": KeyInfo(
                "ง", requires_shift=True, hand="left", finger="ring", row=0
            ),  # Shifted ป
            # Additional Thai vowels and characters for complete coverage
            "ุ": KeyInfo(
                "ุ", requires_shift=True, hand="right", finger="index", row=0
            ),  # Sara u
            "ู": KeyInfo(
                "ู", requires_shift=True, hand="right", finger="middle", row=0
            ),  # Sara uu
            "ึ": KeyInfo(
                "ึ", requires_shift=True, hand="left", finger="middle", row=0
            ),  # Sara ue
            "ฎ": KeyInfo(
                "ฎ", requires_shift=True, hand="left", finger="middle", row=2
            ),  # Do chada
            "ธ": KeyInfo(
                "ธ", requires_shift=True, hand="right", finger="index", row=1
            ),  # Tho thung
            "ศ": KeyInfo(
                "ศ", requires_shift=True, hand="right", finger="ring", row=0
            ),  # So sala
            "โ": KeyInfo(
                "โ", requires_shift=True, hand="right", finger="pinky", row=2
            ),  # Sara o
            # Common punctuation and symbols
            " ": KeyInfo(" ", requires_shift=False, hand="both", finger="thumb", row=0),
            ".": KeyInfo(".", requires_shift=False, hand="right", finger="ring", row=0),
            ",": KeyInfo(
                ",", requires_shift=False, hand="right", finger="middle", row=0
            ),
            "?": KeyInfo("?", requires_shift=True, hand="right", finger="pinky", row=0),
            "!": KeyInfo("!", requires_shift=True, hand="left", finger="pinky", row=3),
            '"': KeyInfo('"', requires_shift=True, hand="left", finger="ring", row=3),
            "(": KeyInfo("(", requires_shift=True, hand="right", finger="ring", row=3),
            ")": KeyInfo(")", requires_shift=True, hand="right", finger="pinky", row=3),
        }

        self.key_map.update(thai_digits)
        self.key_map.update(intl_digits)
        self.key_map.update(thai_characters)


class PattajotiLayout(ThaiKeyboardLayout):
    """Thai Pattajoti keyboard layout."""

    def __init__(self) -> None:
        super().__init__(KeyboardType.PATTAJOTI)

    def _initialize_layout(self) -> None:
        """Initialize Pattajoti layout with key positions and characteristics.
        Based on observed Pattajoti keyboard layout with Thai-optimized character placement.
        """

        # Thai digits on Pattajoti: NO SHIFT required!
        # Correct order from left to right: ๒๓๔๕๗๘๙๐๑๖
        thai_digits = {
            "๒": KeyInfo("๒", requires_shift=False, hand="left", finger="pinky", row=3),
            "๓": KeyInfo("๓", requires_shift=False, hand="left", finger="ring", row=3),
            "๔": KeyInfo(
                "๔", requires_shift=False, hand="left", finger="middle", row=3
            ),
            "๕": KeyInfo("๕", requires_shift=False, hand="left", finger="index", row=3),
            "๗": KeyInfo(
                "๗", requires_shift=False, hand="left", finger="index", row=3
            ),  # stretch
            "๘": KeyInfo(
                "๘", requires_shift=False, hand="right", finger="index", row=3
            ),
            "๙": KeyInfo(
                "๙", requires_shift=False, hand="right", finger="index", row=3
            ),  # stretch
            "๐": KeyInfo(
                "๐", requires_shift=False, hand="right", finger="middle", row=3
            ),
            "๑": KeyInfo("๑", requires_shift=False, hand="right", finger="ring", row=3),
            "๖": KeyInfo(
                "๖", requires_shift=False, hand="right", finger="pinky", row=3
            ),
        }

        # International digits on Pattajoti (generally easier access than Kedmanee)
        intl_digits = {
            "0": KeyInfo(
                "0", requires_shift=False, hand="right", finger="pinky", row=3
            ),
            "1": KeyInfo("1", requires_shift=False, hand="left", finger="pinky", row=3),
            "2": KeyInfo("2", requires_shift=False, hand="left", finger="ring", row=3),
            "3": KeyInfo(
                "3", requires_shift=False, hand="left", finger="middle", row=3
            ),
            "4": KeyInfo("4", requires_shift=False, hand="left", finger="index", row=3),
            "5": KeyInfo("5", requires_shift=False, hand="left", finger="index", row=3),
            "6": KeyInfo(
                "6", requires_shift=False, hand="right", finger="index", row=3
            ),
            "7": KeyInfo(
                "7", requires_shift=False, hand="right", finger="index", row=3
            ),
            "8": KeyInfo(
                "8", requires_shift=False, hand="right", finger="middle", row=3
            ),
            "9": KeyInfo("9", requires_shift=False, hand="right", finger="ring", row=3),
        }

        # Thai characters based on Pattajoti layout - optimized for Thai text
        thai_characters = {
            # Row 2 (Top row) - Thai-optimized placement
            "ข": KeyInfo("ข", requires_shift=False, hand="left", finger="pinky", row=2),
            "ฃ": KeyInfo("ฃ", requires_shift=False, hand="left", finger="ring", row=2),
            "ค": KeyInfo(
                "ค", requires_shift=False, hand="left", finger="middle", row=2
            ),
            "ฅ": KeyInfo("ฅ", requires_shift=False, hand="left", finger="index", row=2),
            "ฆ": KeyInfo("ฆ", requires_shift=False, hand="left", finger="index", row=2),
            "ง": KeyInfo(
                "ง", requires_shift=False, hand="right", finger="index", row=2
            ),
            "จ": KeyInfo(
                "จ", requires_shift=False, hand="right", finger="index", row=2
            ),
            "ฉ": KeyInfo(
                "ฉ", requires_shift=False, hand="right", finger="middle", row=2
            ),
            "ช": KeyInfo("ช", requires_shift=False, hand="right", finger="ring", row=2),
            "ซ": KeyInfo(
                "ซ", requires_shift=False, hand="right", finger="pinky", row=2
            ),
            # Row 1 (Home row) - Most frequently used Thai characters
            "ท": KeyInfo("ท", requires_shift=False, hand="left", finger="pinky", row=1),
            "ร": KeyInfo("ร", requires_shift=False, hand="left", finger="ring", row=1),
            "น": KeyInfo(
                "น", requires_shift=False, hand="left", finger="middle", row=1
            ),
            "ย": KeyInfo("ย", requires_shift=False, hand="left", finger="index", row=1),
            "บ": KeyInfo("บ", requires_shift=False, hand="left", finger="index", row=1),
            "ล": KeyInfo(
                "ล", requires_shift=False, hand="right", finger="index", row=1
            ),
            "ว": KeyInfo(
                "ว", requires_shift=False, hand="right", finger="index", row=1
            ),
            "ส": KeyInfo(
                "ส", requires_shift=False, hand="right", finger="middle", row=1
            ),
            "ห": KeyInfo("ห", requires_shift=False, hand="right", finger="ring", row=1),
            "อ": KeyInfo(
                "อ", requires_shift=False, hand="right", finger="pinky", row=1
            ),
            # Row 0 (Bottom row)
            "ผ": KeyInfo("ผ", requires_shift=False, hand="left", finger="pinky", row=0),
            "ฝ": KeyInfo("ฝ", requires_shift=False, hand="left", finger="ring", row=0),
            "พ": KeyInfo(
                "พ", requires_shift=False, hand="left", finger="middle", row=0
            ),
            "ฟ": KeyInfo("ฟ", requires_shift=False, hand="left", finger="index", row=0),
            "ภ": KeyInfo("ภ", requires_shift=False, hand="left", finger="index", row=0),
            "ม": KeyInfo(
                "ม", requires_shift=False, hand="right", finger="index", row=0
            ),
            "ด": KeyInfo(
                "ด", requires_shift=False, hand="right", finger="index", row=0
            ),
            "ต": KeyInfo(
                "ต", requires_shift=False, hand="right", finger="middle", row=0
            ),
            "ถ": KeyInfo("ถ", requires_shift=False, hand="right", finger="ring", row=0),
            "ก": KeyInfo(
                "ก", requires_shift=False, hand="right", finger="pinky", row=0
            ),
            # Common vowels and tone marks (frequently used in Thai text)
            "า": KeyInfo(
                "า", requires_shift=False, hand="right", finger="middle", row=1
            ),  # Most common vowel
            "ิ": KeyInfo("ิ", requires_shift=False, hand="left", finger="index", row=0),
            "ี": KeyInfo("ี", requires_shift=False, hand="right", finger="index", row=2),
            "ึ": KeyInfo("ึ", requires_shift=False, hand="left", finger="middle", row=0),
            "ื": KeyInfo("ื", requires_shift=False, hand="right", finger="index", row=0),
            "ุ": KeyInfo("ุ", requires_shift=False, hand="right", finger="ring", row=0),
            "ู": KeyInfo("ู", requires_shift=False, hand="right", finger="pinky", row=0),
            "เ": KeyInfo("เ", requires_shift=False, hand="left", finger="index", row=1),
            "แ": KeyInfo(
                "แ", requires_shift=False, hand="left", finger="middle", row=0
            ),
            "โ": KeyInfo("โ", requires_shift=False, hand="left", finger="ring", row=2),
            "ใ": KeyInfo("ใ", requires_shift=False, hand="right", finger="ring", row=0),
            "ไ": KeyInfo("ไ", requires_shift=False, hand="left", finger="pinky", row=2),
            "ำ": KeyInfo("ำ", requires_shift=False, hand="left", finger="ring", row=2),
            "ะ": KeyInfo("ะ", requires_shift=False, hand="left", finger="index", row=2),
            "ั": KeyInfo("ั", requires_shift=False, hand="left", finger="index", row=2),
            "่": KeyInfo(
                "่", requires_shift=False, hand="right", finger="index", row=1
            ),  # Mai ek
            "้": KeyInfo(
                "้", requires_shift=False, hand="right", finger="index", row=1
            ),  # Mai tho
            "๊": KeyInfo(
                "๊", requires_shift=False, hand="right", finger="middle", row=1
            ),  # Mai tri
            "๋": KeyInfo(
                "๋", requires_shift=False, hand="right", finger="ring", row=1
            ),  # Mai chattawa
            "์": KeyInfo(
                "์", requires_shift=False, hand="right", finger="pinky", row=1
            ),  # Thanthakhat
            # Additional Thai characters for complete coverage
            "ธ": KeyInfo(
                "ธ", requires_shift=False, hand="left", finger="middle", row=1
            ),  # Tho thung
            "ศ": KeyInfo(
                "ศ", requires_shift=False, hand="left", finger="ring", row=1
            ),  # So sala
            "ฎ": KeyInfo(
                "ฎ", requires_shift=False, hand="left", finger="index", row=1
            ),  # Do chada
            "ป": KeyInfo(
                "ป", requires_shift=False, hand="left", finger="ring", row=0
            ),  # Po pla
            # Common punctuation and symbols
            " ": KeyInfo(" ", requires_shift=False, hand="both", finger="thumb", row=0),
            ".": KeyInfo(".", requires_shift=False, hand="right", finger="ring", row=0),
            ",": KeyInfo(
                ",", requires_shift=False, hand="right", finger="middle", row=0
            ),
            "?": KeyInfo("?", requires_shift=True, hand="right", finger="pinky", row=0),
            "!": KeyInfo("!", requires_shift=True, hand="left", finger="pinky", row=3),
            '"': KeyInfo('"', requires_shift=True, hand="left", finger="ring", row=3),
            "(": KeyInfo("(", requires_shift=True, hand="right", finger="ring", row=3),
            ")": KeyInfo(")", requires_shift=True, hand="right", finger="pinky", row=3),
        }

        self.key_map.update(thai_digits)
        self.key_map.update(intl_digits)
        self.key_map.update(thai_characters)


def explain_keyboard_rows() -> None:
    """Explain the keyboard row system used in cost calculations.

    References:
    - TIS 820-2535: Thai Keyboard Layout Standard (Kedmanee)
    - Pattajoti keyboard layout specification
    """
    print("KEYBOARD ROW SYSTEM EXPLANATION")
    print("=" * 50)
    print("Based on TIS 820-2535 Thai Keyboard Layout Standard")
    print()
    print("Physical keyboard layout (side view):")
    print()
    print("Row 3: [1][2][3][4][5][6][7][8][9][0]  ← Numbers (hardest)")
    print("Row 2: [Q][W][E][R][T][Y][U][I][O][P]  ← Top row")
    print("Row 1: [A][S][D][F][G][H][J][K][L][;]  ← HOME ROW (easiest)")
    print("Row 0: [Z][X][C][V][B][N][M][,][.][/]  ← Bottom row")
    print("       [    SPACE BAR    ]              ← Thumbs")
    print()
    print("Typing difficulty by row:")
    print("  Row 1 (Home): Fingers naturally rest here - FASTEST")
    print("  Row 2 (Top):  Short upward movement - moderate")
    print("  Row 0 (Bottom): Short downward movement - moderate")
    print("  Row 3 (Numbers): Long upward stretch - SLOWEST")
    print()
    print("LAYOUT COMPARISON:")
    print("=" * 50)
    print("KEDMANEE (TIS 820-2535 Standard):")
    print("  - Thai digits (๐-๙): Row 3 + SHIFT required = 2x penalty")
    print("  - International (0-9): Row 3 only = 1x penalty")
    print("  - Standard QWERTY-based layout with Thai character overlay")
    print()
    print("PATTAJOTI (Thai-optimized layout):")
    print("  - Thai digits (๒๓๔๕๗๘๙๐๑๖): Row 3, NO SHIFT = 1x penalty")
    print("  - International (1234567890): Row 3 only = 1x penalty")
    print("  - Optimized character placement for Thai text efficiency")
    print()
    print("KEY INSIGHT: Kedmanee's SHIFT requirement for Thai digits")
    print("             creates significant typing cost penalty!")
    print()


def compare_layouts(
    base_keystroke_time: float = 0.28, use_weights: bool = True
) -> None:
    """Compare keyboard layouts for digit typing costs."""
    kedmanee = KedmaneeLayout()
    pattajoti = PattajotiLayout()

    weight_mode = "weighted" if use_weights else "unweighted"
    print(f"KEYBOARD LAYOUT COMPARISON ({weight_mode})")
    print("=" * 60)

    print("\nKedmanee Layout Info:")
    kedmanee_info = kedmanee.get_layout_info()
    for key, value in kedmanee_info.items():
        print(f"  {key}: {value}")

    print("\nPattajoti Layout Info:")
    pattajoti_info = pattajoti.get_layout_info()
    for key, value in pattajoti_info.items():
        print(f"  {key}: {value}")

    print(f"\nDIGIT TYPING COSTS ({weight_mode}, base time: {base_keystroke_time}s):")
    print(f"{'Digit':<8} {'Kedmanee':<12} {'Pattajoti':<12} {'Difference':<12}")
    print("-" * 50)

    # Compare Thai digits
    thai_digits = ["๐", "๑", "๒", "๓", "๔", "๕", "๖", "๗", "๘", "๙"]
    for digit in thai_digits:
        ked_cost = kedmanee.calculate_typing_cost(digit, base_keystroke_time)
        pat_cost = pattajoti.calculate_typing_cost(digit, base_keystroke_time)
        diff = ked_cost - pat_cost
        print(f"{digit:<8} {ked_cost:<12.3f} {pat_cost:<12.3f} {diff:+.3f}")

    print()

    # Compare international digits
    intl_digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for digit in intl_digits:
        ked_cost = kedmanee.calculate_typing_cost(digit, base_keystroke_time)
        pat_cost = pattajoti.calculate_typing_cost(digit, base_keystroke_time)
        diff = ked_cost - pat_cost
        print(f"{digit:<8} {ked_cost:<12.3f} {pat_cost:<12.3f} {diff:+.3f}")


if __name__ == "__main__":
    explain_keyboard_rows()
    print()
    compare_layouts()
