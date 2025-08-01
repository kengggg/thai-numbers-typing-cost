#!/usr/bin/env python3
"""
Thai Numbers Typing Cost Analysis - Text Analyzer
Analyzes Thai constitution text for numeric character usage patterns.
"""

import re
from collections import Counter
from typing import Dict, List


class TextAnalyzer:
    """Analyzes Thai text for numeric character patterns and usage."""

    # Unicode ranges
    THAI_DIGITS = range(0x0E50, 0x0E5A)  # U+0E50 to U+0E59
    INTERNATIONAL_DIGITS = range(0x0030, 0x003A)  # U+0030 to U+0039

    def __init__(self, file_path: str):
        """Initialize analyzer with text file."""
        self.file_path = file_path
        self.text = self._load_text()
        self.thai_digit_chars = set(chr(i) for i in self.THAI_DIGITS)
        self.intl_digit_chars = set(chr(i) for i in self.INTERNATIONAL_DIGITS)

    def _load_text(self) -> str:
        """Load text from file."""
        with open(self.file_path, "r", encoding="utf-8") as f:
            return f.read()

    def count_numeric_characters(self) -> Dict[str, int]:
        """Count all numeric characters by type."""
        thai_count = sum(1 for char in self.text if char in self.thai_digit_chars)
        intl_count = sum(1 for char in self.text if char in self.intl_digit_chars)

        return {
            "thai_digits": thai_count,
            "international_digits": intl_count,
            "total_digits": thai_count + intl_count,
        }

    def analyze_digit_usage(self) -> Dict:
        """Detailed analysis of digit usage patterns."""
        thai_digits: Counter[str] = Counter()
        intl_digits: Counter[str] = Counter()

        for char in self.text:
            if char in self.thai_digit_chars:
                thai_digits[char] += 1
            elif char in self.intl_digit_chars:
                intl_digits[char] += 1

        return {
            "thai_digit_breakdown": dict(thai_digits),
            "intl_digit_breakdown": dict(intl_digits),
            "thai_digit_unicode": {char: f"U+{ord(char):04X}" for char in thai_digits},
            "intl_digit_unicode": {char: f"U+{ord(char):04X}" for char in intl_digits},
        }

    def find_number_contexts(self) -> List[Dict]:
        """Find contexts where numbers appear in the text."""
        # Pattern to match sequences of digits (Thai or international)
        digit_pattern = r"[๐-๙0-9]+"
        contexts = []

        for match in re.finditer(digit_pattern, self.text):
            start, end = match.span()
            number = match.group()

            # Get surrounding context (80 chars before and after)
            context_start = max(0, start - 80)
            context_end = min(len(self.text), end + 80)
            context = self.text[context_start:context_end]

            # Determine number type
            has_thai = any(char in self.thai_digit_chars for char in number)
            has_intl = any(char in self.intl_digit_chars for char in number)

            contexts.append(
                {
                    "number": number,
                    "position": (start, end),
                    "context": context.strip(),
                    "type": (
                        "thai" if has_thai else "international" if has_intl else "mixed"
                    ),
                    "length": len(number),
                }
            )

        return contexts

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics about the text."""
        counts = self.count_numeric_characters()
        analysis = self.analyze_digit_usage()
        contexts = self.find_number_contexts()

        # Character statistics
        total_chars = len(self.text)
        total_lines = self.text.count("\n") + 1

        # Number sequence statistics
        thai_sequences = [ctx for ctx in contexts if ctx["type"] == "thai"]
        intl_sequences = [ctx for ctx in contexts if ctx["type"] == "international"]

        return {
            "document_stats": {
                "total_characters": total_chars,
                "total_lines": total_lines,
                "total_digits": counts["total_digits"],
                "digit_percentage": (
                    (counts["total_digits"] / total_chars) * 100
                    if total_chars > 0
                    else 0.0
                ),
            },
            "digit_counts": counts,
            "digit_analysis": analysis,
            "number_sequences": {
                "total_sequences": len(contexts),
                "thai_sequences": len(thai_sequences),
                "intl_sequences": len(intl_sequences),
                "avg_thai_length": (
                    sum(ctx["length"] for ctx in thai_sequences) / len(thai_sequences)
                    if thai_sequences
                    else 0
                ),
                "avg_intl_length": (
                    sum(ctx["length"] for ctx in intl_sequences) / len(intl_sequences)
                    if intl_sequences
                    else 0
                ),
            },
            "contexts": contexts[:10],  # First 10 contexts for preview
        }

    def print_report(self) -> None:
        """Print a detailed analysis report."""
        stats = self.get_statistics()

        print("=" * 60)
        print("THAI CONSTITUTION NUMERIC CHARACTER ANALYSIS")
        print("=" * 60)

        print("\nDOCUMENT OVERVIEW:")
        print(f"  Total characters: {stats['document_stats']['total_characters']:,}")
        print(f"  Total lines: {stats['document_stats']['total_lines']:,}")
        print(f"  Total digits: {stats['document_stats']['total_digits']:,}")
        print(f"  Digit percentage: {stats['document_stats']['digit_percentage']:.2f}%")

        print("\nDIGIT TYPE BREAKDOWN:")
        print(f"  Thai digits (๐-๙): {stats['digit_counts']['thai_digits']:,}")
        print(
            f"  International digits (0-9): {stats['digit_counts']['international_digits']:,}"
        )

        if stats["digit_analysis"]["thai_digit_breakdown"]:
            print("\n  Thai digit frequency:")
            for char, count in sorted(
                stats["digit_analysis"]["thai_digit_breakdown"].items()
            ):
                unicode_code = stats["digit_analysis"]["thai_digit_unicode"][char]
                print(f"    {char} ({unicode_code}): {count:,}")

        if stats["digit_analysis"]["intl_digit_breakdown"]:
            print("\n  International digit frequency:")
            for char, count in sorted(
                stats["digit_analysis"]["intl_digit_breakdown"].items()
            ):
                unicode_code = stats["digit_analysis"]["intl_digit_unicode"][char]
                print(f"    {char} ({unicode_code}): {count:,}")

        print("\nNUMBER SEQUENCES:")
        print(
            f"  Total number sequences: {stats['number_sequences']['total_sequences']:,}"
        )
        print(
            f"  Thai number sequences: {stats['number_sequences']['thai_sequences']:,}"
        )
        print(
            f"  International sequences: {stats['number_sequences']['intl_sequences']:,}"
        )
        print(
            f"  Average Thai sequence length: {stats['number_sequences']['avg_thai_length']:.1f}"
        )
        print(
            f"  Average International sequence length: {stats['number_sequences']['avg_intl_length']:.1f}"
        )

        if stats["contexts"]:
            print("\nSAMPLE CONTEXTS:")
            for i, ctx in enumerate(stats["contexts"][:5], 1):
                print(f"  {i}. Number: '{ctx['number']}' (Type: {ctx['type']})")
                print(f"     Context: ...{ctx['context'][:100]}...")
                print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python text_analyzer.py <path_to_text_file>")
        sys.exit(1)

    analyzer = TextAnalyzer(sys.argv[1])
    analyzer.print_report()
