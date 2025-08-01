#!/usr/bin/env python3
"""
Thai Numbers Typing Cost Analysis - Main CLI Application

Analyzes the typing cost difference between Thai and international digits
across different keyboard layouts and typist skill levels.
"""

import argparse
import os
import sys
from pathlib import Path

# Add the src directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from generators.json_analysis_generator import JSONAnalysisGenerator
from models.typist_profiles import TypistProfile


def render_simple_comparison_markdown(analysis_data: dict, output_path: str) -> None:
    """Render simple comparison table markdown report."""
    metadata = analysis_data.get("metadata", {})
    document_stats = metadata.get("document_stats", {})
    typist_profiles = analysis_data.get("typist_profiles", {})
    analysis_results = analysis_data.get("analysis_results", {})

    # Build simple markdown content
    content = []
    content.append("# Thai Numbers Typing Analysis Comparison")
    content.append("")
    content.append(f"## Document: {metadata.get('document_path', 'Unknown')}")
    content.append(
        f"Characters: {document_stats.get('total_characters', 'N/A'):,} | "
        f"Digits: {document_stats.get('total_digits', 'N/A'):,}"
    )
    content.append("")

    # Main comparison table
    content.append("## Typing Time Comparison (minutes)")
    content.append("")
    content.append(
        "| Typist Profile | Thai + Kedmanee | Intl + Kedmanee | Thai + Pattajoti | Intl + Pattajoti |"
    )
    content.append(
        "|----------------|-----------------|-----------------|------------------|------------------|"
    )

    # Sort profiles for consistent ordering
    profile_order = ["expert", "skilled", "average", "worst"]
    for profile_key in profile_order:
        if profile_key in analysis_results:
            profile_name = typist_profiles.get(profile_key, {}).get(
                "name", profile_key.title()
            )
            scenarios = analysis_results[profile_key].get("scenarios", {})

            thai_kedmanee = scenarios.get("thai_kedmanee", {}).get(
                "total_cost_minutes", 0
            )
            intl_kedmanee = scenarios.get("intl_kedmanee", {}).get(
                "total_cost_minutes", 0
            )
            thai_pattajoti = scenarios.get("thai_pattajoti", {}).get(
                "total_cost_minutes", 0
            )
            intl_pattajoti = scenarios.get("intl_pattajoti", {}).get(
                "total_cost_minutes", 0
            )

            content.append(
                f"| {profile_name:<14} | {thai_kedmanee:>13.1f} | "
                f"{intl_kedmanee:>13.1f} | {thai_pattajoti:>14.1f} | {intl_pattajoti:>14.1f} |"
            )

    content.append("")
    content.append("## Detailed Breakdown by Typist Profile")
    content.append("")

    # Detailed sections for each profile
    for profile_key in profile_order:
        if profile_key in analysis_results:
            profile_info = typist_profiles.get(profile_key, {})
            profile_name = profile_info.get("name", profile_key.title())
            keystroke_time = profile_info.get("keystroke_time", 0)
            scenarios = analysis_results[profile_key].get("scenarios", {})

            content.append(f"### {profile_name} ({keystroke_time}s keystroke)")
            content.append(
                f"- Thai + Kedmanee: {scenarios.get('thai_kedmanee', {}).get('total_cost_minutes', 0):.1f} minutes"
            )
            content.append(
                f"- Intl + Kedmanee: {scenarios.get('intl_kedmanee', {}).get('total_cost_minutes', 0):.1f} minutes"
            )
            content.append(
                f"- Thai + Pattajoti: {scenarios.get('thai_pattajoti', {}).get('total_cost_minutes', 0):.1f} minutes"
            )
            content.append(
                f"- Intl + Pattajoti: {scenarios.get('intl_pattajoti', {}).get('total_cost_minutes', 0):.1f} minutes"
            )
            content.append("")

    # Write to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))


def create_output_directories(base_output_dir: str) -> None:
    """Create output directory if it doesn't exist."""
    Path(base_output_dir).mkdir(parents=True, exist_ok=True)


def generate_analysis(document_path: str, output_dir: str) -> None:
    """Generate comprehensive JSON and markdown analysis for all scenarios."""
    print("\n" + "=" * 80)
    print("THAI NUMBERS TYPING COST COMPARISON")
    print("=" * 80)

    try:
        # Generate comprehensive JSON analysis for ALL typist profiles
        generator = JSONAnalysisGenerator(document_path)
        analysis_data = generator.generate_comprehensive_analysis(
            include_all_typists=True
        )

        # Always save JSON analysis
        json_path = os.path.join(output_dir, "analysis.json")
        generator.save_to_file(analysis_data, json_path)
        print(f"\n📦 JSON ANALYSIS SAVED: {json_path}")

        # Always generate simplified markdown comparison report
        timestamp = (
            analysis_data["metadata"]["generated_at"]
            .replace(":", "")
            .replace("-", "")
            .replace("T", "_")
            .split(".")[0]
        )
        markdown_path = f"{output_dir}/comparison_report_{timestamp}.md"

        render_simple_comparison_markdown(analysis_data, markdown_path)
        print(f"\n📄 COMPARISON REPORT GENERATED: {markdown_path}")

    except Exception as e:
        print(f"\n⚠️  Analysis failed: {e}")
        sys.exit(1)


def main() -> None:
    """Simplified Thai Numbers Typing Cost Comparison."""
    parser = argparse.ArgumentParser(
        description="Thai Numbers Typing Cost Comparison - Automatically analyzes all scenarios",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze document and generate all comparisons
  python main.py ../data/thai-con.txt

  # Show available typist profiles
  python main.py --list-typists
        """,
    )

    parser.add_argument("document", nargs="?", help="Path to Thai document to analyze")
    parser.add_argument(
        "--list-typists",
        action="store_true",
        help="List available typist profiles and exit",
    )

    args = parser.parse_args()

    # Handle list-typists command
    if args.list_typists:
        TypistProfile.list_profiles()
        return

    # Document path is required for analysis
    if not args.document:
        parser.error("Document path is required unless using --list-typists")

    # Validate document path
    if not os.path.exists(args.document):
        print(f"Error: Document not found at {args.document}")
        sys.exit(1)

    # Create output directory
    output_dir = "output"
    create_output_directories(output_dir)

    print("=" * 80)
    print("AUTOMATIC COMPARISON: ALL SCENARIOS & TYPIST PROFILES")
    print("=" * 80)
    print(f"Document: {args.document}")
    print(f"Output Directory: {output_dir}")
    print("Analyzing: Thai/Intl digits × Kedmanee/Pattajoti × All typist profiles")
    print("=" * 80)

    # Generate comprehensive analysis
    generate_analysis(args.document, output_dir)


if __name__ == "__main__":
    main()
