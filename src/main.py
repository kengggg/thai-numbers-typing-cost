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
from typing import Dict

# Add the src directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from calculators.typing_cost_calculator import TypingCostCalculator
from generators.json_analysis_generator import JSONAnalysisGenerator
from models.keyboard_layouts import (
    KedmaneeLayout,
    PattajotiLayout,
    compare_layouts,
    explain_keyboard_rows,
)
from models.text_analyzer import TextAnalyzer
from models.typist_profiles import TypistProfile
from renderers.console_renderer import render_json_to_console
from renderers.markdown_renderer import render_json_to_markdown


def create_output_directories(base_output_dir: str) -> None:
    """Create output directories if they don't exist."""
    Path(base_output_dir).mkdir(parents=True, exist_ok=True)
    Path(f"{base_output_dir}/reports").mkdir(parents=True, exist_ok=True)
    Path(f"{base_output_dir}/analysis").mkdir(parents=True, exist_ok=True)


def run_text_analysis(document_path: str, output_dir: str) -> None:
    """Run text analysis and save results."""
    print("Running text analysis...")
    analyzer = TextAnalyzer(document_path)

    # Print analysis to console
    analyzer.print_report()

    # Save detailed results
    stats = analyzer.get_statistics()
    output_file = f"{output_dir}/analysis/text_analysis.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("DETAILED TEXT ANALYSIS RESULTS\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Document Statistics: {stats['document_stats']}\n")
        f.write(f"Digit Counts: {stats['digit_counts']}\n")
        f.write(f"Number Sequences: {stats['number_sequences']}\n\n")

        f.write("ALL NUMBER CONTEXTS:\n")
        for i, ctx in enumerate(stats["contexts"], 1):
            f.write(f"{i}. {ctx['number']} ({ctx['type']}) at pos {ctx['position']}\n")
            f.write(f"   Context: {ctx['context']}\n\n")

    print(f"Text analysis saved to: {output_file}")
    return analyzer


def run_keyboard_comparison(typist_profile: Dict, output_dir: str) -> None:
    """Run keyboard layout comparison."""
    print(f"\nRunning keyboard comparison for {typist_profile['name']}...")

    # Show explanation and comparison
    explain_keyboard_rows()
    print()
    compare_layouts(typist_profile["keystroke_time"])

    # Save results to file
    profile_name_safe = (
        typist_profile["name"]
        .lower()
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
    )
    output_file = f"{output_dir}/analysis/keyboard_comparison_{profile_name_safe}.txt"

    # Capture the keyboard comparison output
    kedmanee = KedmaneeLayout()
    pattajoti = PattajotiLayout()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"KEYBOARD LAYOUT COMPARISON - {typist_profile['name']}\n")
        f.write("=" * 80 + "\n\n")
        f.write(
            f"Base keystroke time: {typist_profile['keystroke_time']}s + SHIFT penalty\n\n"
        )

        # Layout info
        kedmanee_info = kedmanee.get_layout_info()
        pattajoti_info = pattajoti.get_layout_info()

        f.write("LAYOUT INFORMATION:\n")
        f.write("-" * 40 + "\n")
        f.write("Kedmanee Layout:\n")
        for key, value in kedmanee_info.items():
            f.write(f"  {key}: {value}\n")
        f.write("\nPattajoti Layout:\n")
        for key, value in pattajoti_info.items():
            f.write(f"  {key}: {value}\n")

        # Digit typing costs
        f.write("\nDIGIT TYPING COSTS (base time + SHIFT penalty):\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Digit':<8} {'Kedmanee':<12} {'Pattajoti':<12} {'Difference':<12}\n")
        f.write("-" * 50 + "\n")

        # Thai digits
        f.write("Thai Digits:\n")
        thai_digits = ["๐", "๑", "๒", "๓", "๔", "๕", "๖", "๗", "๘", "๙"]
        for digit in thai_digits:
            ked_cost = kedmanee.calculate_typing_cost(
                digit, typist_profile["keystroke_time"]
            )
            pat_cost = pattajoti.calculate_typing_cost(
                digit, typist_profile["keystroke_time"]
            )
            diff = ked_cost - pat_cost
            f.write(f"  {digit:<8} {ked_cost:<12.3f} {pat_cost:<12.3f} {diff:+.3f}\n")

        # International digits
        f.write("\nInternational Digits:\n")
        intl_digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for digit in intl_digits:
            ked_cost = kedmanee.calculate_typing_cost(
                digit, typist_profile["keystroke_time"]
            )
            pat_cost = pattajoti.calculate_typing_cost(
                digit, typist_profile["keystroke_time"]
            )
            diff = ked_cost - pat_cost
            f.write(f"  {digit:<8} {ked_cost:<12.3f} {pat_cost:<12.3f} {diff:+.3f}\n")

        f.write("\nKEY FINDINGS:\n")
        f.write("- Thai digits on Kedmanee require SHIFT (2x cost penalty)\n")
        f.write("- Pattajoti eliminates SHIFT penalty for Thai digits\n")
        f.write("- International digits perform similarly on both layouts\n")

    print(f"Keyboard comparison saved to: {output_file}")


def run_typing_cost_analysis(
    document_path: str, typist_profile: Dict, output_dir: str
) -> None:
    """Run comprehensive typing cost analysis."""
    print(f"\nRunning typing cost analysis for {typist_profile['name']}...")

    calculator = TypingCostCalculator(document_path, typist_profile["keystroke_time"])
    calculator.print_comprehensive_report()
    scenarios = calculator.analyze_all_scenarios()
    savings = calculator.calculate_savings_analysis(scenarios)

    # Save detailed results
    profile_name_safe = (
        typist_profile["name"]
        .lower()
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
    )

    # Save typing cost analysis
    analysis_file = f"{output_dir}/analysis/typing_cost_{profile_name_safe}.txt"
    with open(analysis_file, "w", encoding="utf-8") as f:
        f.write(f"TYPING COST ANALYSIS - {typist_profile['name']}\n")
        f.write(f"Base keystroke time: {typist_profile['keystroke_time']}s\n")
        f.write("=" * 60 + "\n\n")

        for scenario_name, scenario_data in scenarios.items():
            f.write(f"SCENARIO: {scenario_name}\n")
            f.write(
                f"  Total cost: {scenario_data['total_cost_seconds']:.2f} seconds\n"
            )
            f.write(
                f"  Total cost: {scenario_data['total_cost_minutes']:.2f} minutes\n"
            )
            f.write(f"  Total cost: {scenario_data['total_cost_hours']:.4f} hours\n")
            f.write(
                f"  Average per character: {scenario_data['average_cost_per_char']*1000:.2f} ms\n"
            )
            f.write(f"  Keyboard: {scenario_data['keyboard_layout']}\n")
            f.write(f"  Conversion: {scenario_data['conversion_applied']}\n\n")

        f.write("SAVINGS ANALYSIS:\n")
        for scenario_name, saving_data in savings.items():
            f.write(f"  {scenario_name}:\n")
            f.write(
                f"    Time saved: {saving_data['time_saved_minutes']:.2f} minutes\n"
            )
            f.write(f"    Percentage saved: {saving_data['percentage_saved']:.2f}%\n")
            f.write(
                f"    Cost per digit: {saving_data['cost_per_digit']*1000:.2f} ms\n\n"
            )

    print(f"Typing cost analysis saved to: {analysis_file}")


def run_comparative_analysis(document_path: str, output_dir: str) -> None:
    """Run analysis across all typist profiles for comparison."""
    print("\nRunning comparative analysis across all typist skill levels...")

    all_results = {}

    for profile_key, profile in TypistProfile.PROFILES.items():
        print(f"\n{'='*60}")
        print(f"ANALYZING: {profile['name']}")
        print(f"{'='*60}")

        calculator = TypingCostCalculator(document_path, profile["keystroke_time"])
        calculator.print_comprehensive_report()
        scenarios = calculator.analyze_all_scenarios()
        savings = calculator.calculate_savings_analysis(scenarios)

        all_results[profile_key] = {
            "profile": profile,
            "scenarios": scenarios,
            "savings": savings,
        }

    # Generate comparative report
    report_file = f"{output_dir}/reports/comparative_analysis.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("COMPARATIVE ANALYSIS ACROSS TYPIST SKILL LEVELS\n")
        f.write("=" * 80 + "\n\n")

        # Summary table
        f.write("SUMMARY BY TYPIST SKILL LEVEL:\n")
        f.write(
            f"{'Typist Level':<20} {'Current (min)':<15} {'Optimal (min)':<15} {'Savings (min)':<15} {'Savings (%)':<12}\n"
        )
        f.write("-" * 85 + "\n")

        for profile_key, results in all_results.items():
            profile = results["profile"]
            scenarios = results["scenarios"]
            savings = results["savings"]

            current_time = scenarios["thai_kedmanee"]["total_cost_minutes"]

            def get_cost(key: str) -> float:
                return scenarios[key]["total_cost_minutes"]

            optimal_key = min(scenarios.keys(), key=get_cost)
            optimal_time = scenarios[optimal_key]["total_cost_minutes"]
            time_saved = current_time - optimal_time
            percent_saved = (time_saved / current_time) * 100

            f.write(
                f"{profile['name']:<20} {current_time:<15.1f} {optimal_time:<15.1f} {time_saved:<15.1f} {percent_saved:<12.1f}\n"
            )

        f.write("\nDETAILED RESULTS BY PROFILE:\n")
        f.write("-" * 40 + "\n")

        for profile_key, results in all_results.items():
            profile = results["profile"]
            scenarios = results["scenarios"]
            savings = results["savings"]

            f.write(
                f"\n{profile['name']} ({profile['keystroke_time']}s per keystroke):\n"
            )
            f.write("  Scenarios:\n")
            for scenario_name, scenario_data in scenarios.items():
                f.write(
                    f"    {scenario_name}: {scenario_data['total_cost_minutes']:.1f} minutes\n"
                )

            f.write("  Savings vs current:\n")
            for scenario_name, saving_data in savings.items():
                f.write(
                    f"    {scenario_name}: {saving_data['time_saved_minutes']:.1f} min ({saving_data['percentage_saved']:.1f}%)\n"
                )

    print(f"\nComparative analysis saved to: {report_file}")


def generate_json_and_render(args: argparse.Namespace) -> None:
    """Generate JSON analysis and render to requested format."""
    print("\n" + "=" * 80)
    print("GENERATING JSON-FIRST ANALYSIS")
    print("=" * 80)

    try:
        # Generate JSON analysis
        generator = JSONAnalysisGenerator(args.document)
        analysis_data = generator.generate_comprehensive_analysis(
            include_all_typists=args.compare_all
        )

        # Save JSON if requested
        if args.output_json:
            json_path = args.output_json
            if not json_path.endswith(".json"):
                json_path += ".json"

            # Handle both absolute and relative paths correctly
            if os.path.isabs(json_path):
                json_full_path = json_path
            else:
                json_full_path = os.path.join(args.output, json_path)

            generator.save_to_file(analysis_data, json_full_path)
            print(f"\n📦 JSON ANALYSIS SAVED: {json_full_path}")

        # Render to requested format
        if args.format == "markdown":
            timestamp = (
                analysis_data["metadata"]["generated_at"]
                .replace(":", "")
                .replace("-", "")
                .replace("T", "_")
                .split(".")[0]
            )
            markdown_path = f"{args.output}/Thai_Numbers_Analysis_Report_{timestamp}.md"

            render_json_to_markdown(analysis_data, markdown_path)
            print(f"\n📄 MARKDOWN REPORT GENERATED: {markdown_path}")

        elif args.format == "console":
            console_output = render_json_to_console(analysis_data, "comprehensive")
            print("\n" + console_output)

        elif args.format == "json":
            # JSON already saved above, just show summary
            console_output = render_json_to_console(analysis_data, "quick")
            print(f"\n{console_output}")

        print(
            f"\n🎯 Key Finding: {analysis_data['key_findings']['improvement']['time_saved_minutes']} minutes saved per document"
        )

    except Exception as e:
        print(f"\n⚠️  JSON analysis failed: {e}")
        print("Falling back to legacy analysis mode...")
        # Could fall back to legacy mode here if needed


def render_from_existing_json(args: argparse.Namespace) -> None:
    """Render reports from existing JSON file."""
    json_file = args.render_from_json

    if not os.path.exists(json_file):
        print(f"Error: JSON file not found at {json_file}")
        sys.exit(1)

    print(f"Loading analysis data from: {json_file}")

    try:
        # Load JSON directly without needing generator
        import json

        with open(json_file, "r", encoding="utf-8") as f:
            analysis_data = json.load(f)

        if args.format == "markdown":
            timestamp = (
                analysis_data["metadata"]["generated_at"]
                .replace(":", "")
                .replace("-", "")
                .replace("T", "_")
                .split(".")[0]
            )
            output_name = Path(json_file).stem + f"_report_{timestamp}.md"
            output_path = os.path.join(args.output, output_name)

            render_json_to_markdown(analysis_data, output_path)
            print(f"\n📄 MARKDOWN REPORT GENERATED: {output_path}")

        elif args.format == "console":
            console_output = render_json_to_console(analysis_data, "comprehensive")
            print("\n" + console_output)

        elif args.format == "json":
            # Pretty print the JSON
            import json

            print(json.dumps(analysis_data, indent=2, ensure_ascii=False))

        print(
            f"\n🎯 Key Finding: {analysis_data['key_findings']['improvement']['time_saved_minutes']} minutes saved per document"
        )

    except Exception as e:
        print(f"\n⚠️  Failed to render from JSON: {e}")
        sys.exit(1)


def generate_legacy_markdown_report(args: argparse.Namespace) -> None:
    """Generate report using JSON-first approach (legacy CLI compatibility)."""
    print("\n" + "=" * 80)
    print("GENERATING FOCUSED RESEARCH REPORT (Legacy Compatibility)")
    print("=" * 80)

    try:
        # Use JSON-first approach for backward compatibility
        generator = JSONAnalysisGenerator(args.document)
        analysis_data = generator.generate_comprehensive_analysis(
            include_all_typists=args.compare_all
        )

        # Generate markdown report with timestamp naming
        timestamp = (
            analysis_data["metadata"]["generated_at"]
            .replace(":", "")
            .replace("-", "")
            .replace("T", "_")
            .split(".")[0]
        )
        report_path = (
            f"{args.output}/Thai_Numbers_Typing_Cost_Analysis_Report_{timestamp}.md"
        )

        render_json_to_markdown(analysis_data, report_path)

        print("\n📊 RESEARCH REPORT GENERATED SUCCESSFULLY!")
        print(f"📄 Location: {report_path}")
        print(
            "🎯 Focus: Direct comparison of Thai vs International digits typing costs"
        )

    except Exception as e:
        print(f"\n⚠️  Research report generation failed: {e}")
        print("Regular analysis results are still available in the output directory.")


def main() -> None:
    """Main CLI application."""
    parser = argparse.ArgumentParser(
        description="Thai Numbers Typing Cost Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis with console output
  python main.py ../data/thai-con.txt

  # Save analysis as JSON
  python main.py ../data/thai-con.txt --output-json analysis.json

  # Generate markdown from JSON
  python main.py --render-from-json analysis.json --format markdown

  # Compare all typist levels and save as JSON + markdown
  python main.py ../data/thai-con.txt --compare-all --output-json results.json --format markdown

  # Legacy: Generate focused research report
  python main.py ../data/thai-con.txt --compare-all --markdown-report

  # Show available typist profiles
  python main.py --list-typists
        """,
    )

    parser.add_argument("document", nargs="?", help="Path to Thai document to analyze")

    parser.add_argument(
        "--typist",
        choices=["expert", "skilled", "average", "worst"],
        default="average",
        help="Typist skill level (default: average)",
    )

    parser.add_argument(
        "--output",
        "-o",
        default="../output",
        help="Output directory for generated files (default: ../output/)",
    )

    parser.add_argument(
        "--compare-all",
        action="store_true",
        help="Run analysis for all typist skill levels",
    )

    parser.add_argument(
        "--list-typists",
        action="store_true",
        help="List available typist profiles and exit",
    )

    parser.add_argument(
        "--keyboard-only",
        action="store_true",
        help="Only run keyboard layout comparison",
    )

    parser.add_argument(
        "--text-only", action="store_true", help="Only run text analysis"
    )

    # JSON-first output options
    parser.add_argument(
        "--output-json", metavar="JSON_FILE", help="Save analysis results as JSON file"
    )

    parser.add_argument(
        "--render-from-json",
        metavar="JSON_FILE",
        help="Generate reports from existing JSON file",
    )

    parser.add_argument(
        "--format",
        choices=["json", "markdown", "console"],
        default="console",
        help="Output format (default: console)",
    )

    # Legacy markdown support
    parser.add_argument(
        "--markdown-report",
        action="store_true",
        help="Generate focused research report with date/time naming (legacy)",
    )

    parser.add_argument(
        "--no-markdown",
        action="store_true",
        help="Skip automatic markdown report generation (legacy)",
    )

    args = parser.parse_args()

    # Handle special commands
    if args.list_typists:
        TypistProfile.list_profiles()
        return

    # Handle render-from-json mode
    if args.render_from_json:
        render_from_existing_json(args)
        return

    if not args.document:
        parser.error(
            "Document path is required unless using --list-typists or --render-from-json"
        )

    # Validate document path
    if not os.path.exists(args.document):
        print(f"Error: Document not found at {args.document}")
        sys.exit(1)

    # Get typist profile
    typist_profile = TypistProfile.get_profile(args.typist)
    if not typist_profile:
        print(f"Error: Invalid typist profile '{args.typist}'")
        TypistProfile.list_profiles()
        sys.exit(1)

    # Create output directories
    create_output_directories(args.output)

    print("=" * 80)
    print("THAI NUMBERS TYPING COST ANALYSIS")
    print("=" * 80)
    print(f"Document: {args.document}")
    print(f"Typist Profile: {typist_profile['name']}")
    print(f"Base Keystroke Time: {typist_profile['keystroke_time']}s + SHIFT penalty")
    print(f"Output Directory: {args.output}")
    print("=" * 80)

    # Run requested analyses
    if args.text_only:
        run_text_analysis(args.document, args.output)
    elif args.keyboard_only:
        run_keyboard_comparison(typist_profile, args.output)
    elif args.compare_all:
        run_text_analysis(args.document, args.output)
        run_comparative_analysis(args.document, args.output)
    else:
        # Full analysis for selected typist
        run_text_analysis(args.document, args.output)
        run_keyboard_comparison(typist_profile, args.output)
        run_typing_cost_analysis(args.document, typist_profile, args.output)

    print(f"\nAnalysis complete! Results saved to: {args.output}/")

    # New JSON-first workflow (check first for explicit JSON requests, but not legacy)
    if args.output_json or (
        args.format in ["json", "markdown", "console"]
        and not args.markdown_report
        and not (args.compare_all and not args.no_markdown)
    ):
        generate_json_and_render(args)

    # Legacy markdown report support
    elif args.markdown_report or (
        args.compare_all and not args.no_markdown and not args.output_json
    ):
        generate_legacy_markdown_report(args)


if __name__ == "__main__":
    main()
