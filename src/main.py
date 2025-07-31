#!/usr/bin/env python3
"""
Thai Numbers Typing Cost Analysis - Main CLI Application

Analyzes the typing cost difference between Thai and international digits
across different keyboard layouts and typist skill levels.
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Dict

# Add the src directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from models.text_analyzer import TextAnalyzer
from models.keyboard_layouts import KedmaneeLayout, PattajotiLayout, explain_keyboard_rows, compare_layouts
from calculators.typing_cost_calculator import TypingCostCalculator
from reporters.markdown_reporter import MarkdownReporter


class TypistProfile:
    """Represents different typist skill levels with associated keystroke times."""
    
    PROFILES = {
        'expert': {
            'name': 'Expert Typist (90 WPM)',
            'keystroke_time': 0.12,
            'description': 'Professional typist, ~90 WPM, touch typing mastery'
        },
        'skilled': {
            'name': 'Skilled Typist',
            'keystroke_time': 0.20,
            'description': 'Experienced office worker, good typing skills'
        },
        'average': {
            'name': 'Average Non-secretarial',
            'keystroke_time': 0.28,
            'description': 'Average office worker, moderate typing skills (default)'
        },
        'worst': {
            'name': 'Worst Typist',
            'keystroke_time': 1.2,
            'description': 'Hunt-and-peck typist, very slow typing'
        }
    }
    
    @classmethod
    def get_profile(cls, profile_name: str) -> Dict:
        """Get typist profile by name."""
        return cls.PROFILES.get(profile_name.lower())
    
    @classmethod
    def list_profiles(cls):
        """Print all available typist profiles."""
        print("Available Typist Profiles:")
        print("-" * 50)
        for key, profile in cls.PROFILES.items():
            print(f"  {key:<8}: {profile['name']} ({profile['keystroke_time']}s per keystroke)")
            print(f"           {profile['description']}")
            print()


def create_output_directories(base_output_dir: str):
    """Create output directories if they don't exist."""
    Path(base_output_dir).mkdir(parents=True, exist_ok=True)
    Path(f"{base_output_dir}/reports").mkdir(parents=True, exist_ok=True)
    Path(f"{base_output_dir}/analysis").mkdir(parents=True, exist_ok=True)


def run_text_analysis(document_path: str, output_dir: str):
    """Run text analysis and save results."""
    print("Running text analysis...")
    analyzer = TextAnalyzer(document_path)
    
    # Print analysis to console
    analyzer.print_report()
    
    # Save detailed results
    stats = analyzer.get_statistics()
    output_file = f"{output_dir}/analysis/text_analysis.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("DETAILED TEXT ANALYSIS RESULTS\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Document Statistics: {stats['document_stats']}\n")
        f.write(f"Digit Counts: {stats['digit_counts']}\n")
        f.write(f"Number Sequences: {stats['number_sequences']}\n\n")
        
        f.write("ALL NUMBER CONTEXTS:\n")
        for i, ctx in enumerate(stats['contexts'], 1):
            f.write(f"{i}. {ctx['number']} ({ctx['type']}) at pos {ctx['position']}\n")
            f.write(f"   Context: {ctx['context']}\n\n")
    
    print(f"Text analysis saved to: {output_file}")
    return analyzer


def run_keyboard_comparison(typist_profile: Dict, output_dir: str, use_weights: bool = True):
    """Run keyboard layout comparison."""
    weight_mode = "weighted" if use_weights else "unweighted"
    print(f"\nRunning keyboard comparison for {typist_profile['name']} ({weight_mode})...")
    
    # Show explanation and comparison
    explain_keyboard_rows()
    print()
    compare_layouts(typist_profile['keystroke_time'], use_weights)
    
    # Save results to file
    profile_name_safe = typist_profile['name'].lower().replace(' ', '_').replace('(', '').replace(')', '')
    output_file = f"{output_dir}/analysis/keyboard_comparison_{profile_name_safe}_{weight_mode}.txt"
    
    # Capture the keyboard comparison output
    kedmanee = KedmaneeLayout()
    pattajoti = PattajotiLayout()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"KEYBOARD LAYOUT COMPARISON - {typist_profile['name']} ({weight_mode})\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Base keystroke time: {typist_profile['keystroke_time']}s\n")
        f.write(f"Weight mode: {weight_mode}\n\n")
        
        # Layout info
        kedmanee_info = kedmanee.get_layout_info()
        pattajoti_info = pattajoti.get_layout_info()
        
        f.write("LAYOUT INFORMATION:\n")
        f.write("-" * 40 + "\n")
        f.write(f"Kedmanee Layout:\n")
        for key, value in kedmanee_info.items():
            f.write(f"  {key}: {value}\n")
        f.write(f"\nPattajoti Layout:\n")
        for key, value in pattajoti_info.items():
            f.write(f"  {key}: {value}\n")
        
        # Digit typing costs
        f.write(f"\nDIGIT TYPING COSTS ({weight_mode}):\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Digit':<8} {'Kedmanee':<12} {'Pattajoti':<12} {'Difference':<12}\n")
        f.write("-" * 50 + "\n")
        
        # Thai digits
        f.write("Thai Digits:\n")
        thai_digits = ['๐', '๑', '๒', '๓', '๔', '๕', '๖', '๗', '๘', '๙']
        for digit in thai_digits:
            ked_cost = kedmanee.calculate_typing_cost(digit, typist_profile['keystroke_time'], use_weights)
            pat_cost = pattajoti.calculate_typing_cost(digit, typist_profile['keystroke_time'], use_weights)
            diff = ked_cost - pat_cost
            f.write(f"  {digit:<8} {ked_cost:<12.3f} {pat_cost:<12.3f} {diff:+.3f}\n")
        
        # International digits
        f.write("\nInternational Digits:\n")
        intl_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for digit in intl_digits:
            ked_cost = kedmanee.calculate_typing_cost(digit, typist_profile['keystroke_time'], use_weights)
            pat_cost = pattajoti.calculate_typing_cost(digit, typist_profile['keystroke_time'], use_weights)
            diff = ked_cost - pat_cost
            f.write(f"  {digit:<8} {ked_cost:<12.3f} {pat_cost:<12.3f} {diff:+.3f}\n")
        
        f.write(f"\nKEY FINDINGS:\n")
        f.write("- Thai digits on Kedmanee require SHIFT (2x cost penalty)\n")
        f.write("- Pattajoti eliminates SHIFT penalty for Thai digits\n")
        f.write("- International digits perform similarly on both layouts\n")
    
    print(f"Keyboard comparison saved to: {output_file}")


def run_typing_cost_analysis(document_path: str, typist_profile: Dict, output_dir: str, use_weights: bool = True):
    """Run comprehensive typing cost analysis."""
    weight_mode = "weighted" if use_weights else "unweighted"
    print(f"\nRunning typing cost analysis for {typist_profile['name']} ({weight_mode})...")
    
    calculator = TypingCostCalculator(document_path, typist_profile['keystroke_time'], use_weights)
    scenarios, savings = calculator.print_comprehensive_report()
    
    # Save detailed results
    profile_name_safe = typist_profile['name'].lower().replace(' ', '_').replace('(', '').replace(')', '')
    weight_suffix = "weighted" if use_weights else "unweighted"
    
    # Save typing cost analysis
    analysis_file = f"{output_dir}/analysis/typing_cost_{profile_name_safe}_{weight_suffix}.txt"
    with open(analysis_file, 'w', encoding='utf-8') as f:
        f.write(f"TYPING COST ANALYSIS - {typist_profile['name']}\n")
        f.write(f"Base keystroke time: {typist_profile['keystroke_time']}s\n")
        f.write("=" * 60 + "\n\n")
        
        for scenario_name, scenario_data in scenarios.items():
            f.write(f"SCENARIO: {scenario_name}\n")
            f.write(f"  Total cost: {scenario_data['total_cost_seconds']:.2f} seconds\n")
            f.write(f"  Total cost: {scenario_data['total_cost_minutes']:.2f} minutes\n")
            f.write(f"  Total cost: {scenario_data['total_cost_hours']:.4f} hours\n")
            f.write(f"  Average per character: {scenario_data['average_cost_per_char']*1000:.2f} ms\n")
            f.write(f"  Keyboard: {scenario_data['keyboard_layout']}\n")
            f.write(f"  Conversion: {scenario_data['conversion_applied']}\n\n")
        
        f.write("SAVINGS ANALYSIS:\n")
        for scenario_name, saving_data in savings.items():
            f.write(f"  {scenario_name}:\n")
            f.write(f"    Time saved: {saving_data['time_saved_minutes']:.2f} minutes\n")
            f.write(f"    Percentage saved: {saving_data['percentage_saved']:.2f}%\n")
            f.write(f"    Cost per digit: {saving_data['cost_per_digit']*1000:.2f} ms\n\n")
    
    print(f"Typing cost analysis saved to: {analysis_file}")
    return scenarios, savings


def run_comparative_analysis(document_path: str, output_dir: str, use_weights: bool = True):
    """Run analysis across all typist profiles for comparison."""
    weight_mode = "weighted" if use_weights else "unweighted"
    print(f"\nRunning comparative analysis across all typist skill levels ({weight_mode})...")
    
    all_results = {}
    
    for profile_key, profile in TypistProfile.PROFILES.items():
        print(f"\n{'='*60}")
        print(f"ANALYZING: {profile['name']} ({weight_mode})")
        print(f"{'='*60}")
        
        calculator = TypingCostCalculator(document_path, profile['keystroke_time'], use_weights)
        scenarios, savings = calculator.print_comprehensive_report()
        
        all_results[profile_key] = {
            'profile': profile,
            'scenarios': scenarios,
            'savings': savings
        }
    
    # Generate comparative report
    weight_suffix = "weighted" if use_weights else "unweighted"
    report_file = f"{output_dir}/reports/comparative_analysis_{weight_suffix}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("COMPARATIVE ANALYSIS ACROSS TYPIST SKILL LEVELS\n")
        f.write("=" * 80 + "\n\n")
        
        # Summary table
        f.write("SUMMARY BY TYPIST SKILL LEVEL:\n")
        f.write(f"{'Typist Level':<20} {'Current (min)':<15} {'Optimal (min)':<15} {'Savings (min)':<15} {'Savings (%)':<12}\n")
        f.write("-" * 85 + "\n")
        
        for profile_key, results in all_results.items():
            profile = results['profile']
            scenarios = results['scenarios']
            savings = results['savings']
            
            current_time = scenarios['thai_kedmanee']['total_cost_minutes']
            optimal_key = min(scenarios.keys(), key=lambda k: scenarios[k]['total_cost_minutes'])
            optimal_time = scenarios[optimal_key]['total_cost_minutes']
            time_saved = current_time - optimal_time
            percent_saved = (time_saved / current_time) * 100
            
            f.write(f"{profile['name']:<20} {current_time:<15.1f} {optimal_time:<15.1f} {time_saved:<15.1f} {percent_saved:<12.1f}\n")
        
        f.write("\nDETAILED RESULTS BY PROFILE:\n")
        f.write("-" * 40 + "\n")
        
        for profile_key, results in all_results.items():
            profile = results['profile']
            scenarios = results['scenarios']
            savings = results['savings']
            
            f.write(f"\n{profile['name']} ({profile['keystroke_time']}s per keystroke):\n")
            f.write("  Scenarios:\n")
            for scenario_name, scenario_data in scenarios.items():
                f.write(f"    {scenario_name}: {scenario_data['total_cost_minutes']:.1f} minutes\n")
            
            f.write("  Savings vs current:\n")
            for scenario_name, saving_data in savings.items():
                f.write(f"    {scenario_name}: {saving_data['time_saved_minutes']:.1f} min ({saving_data['percentage_saved']:.1f}%)\n")
    
    print(f"\nComparative analysis saved to: {report_file}")
    return all_results


def main():
    """Main CLI application."""
    parser = argparse.ArgumentParser(
        description="Thai Numbers Typing Cost Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis with average typist (weighted by default)
  python main.py ../data/thai-con.txt
  
  # Analysis with expert typist, no ergonomic weights
  python main.py ../data/thai-con.txt --typist expert --no-weights
  
  # Compare weighted vs unweighted for average typist
  python main.py ../data/thai-con.txt --compare-weights
  
  # Compare all typist levels with unweighted calculation
  python main.py ../data/thai-con.txt --compare-all --no-weights
  
  # Generate comprehensive markdown report
  python main.py ../data/thai-con.txt --compare-all --markdown-report
  
  # Custom output directory
  python main.py ../data/thai-con.txt --output ../custom_output/
  
  # Show available typist profiles
  python main.py --list-typists
        """
    )
    
    parser.add_argument('document', nargs='?', help='Path to Thai document to analyze')
    
    parser.add_argument('--typist', choices=['expert', 'skilled', 'average', 'worst'], 
                       default='average', help='Typist skill level (default: average)')
    
    parser.add_argument('--output', '-o', default='../output', 
                       help='Output directory for generated files (default: ../output/)')
    
    parser.add_argument('--compare-all', action='store_true',
                       help='Run analysis for all typist skill levels')
    
    parser.add_argument('--list-typists', action='store_true',
                       help='List available typist profiles and exit')
    
    parser.add_argument('--keyboard-only', action='store_true',
                       help='Only run keyboard layout comparison')
    
    parser.add_argument('--text-only', action='store_true',
                       help='Only run text analysis')
    
    # Weight-related arguments
    weight_group = parser.add_mutually_exclusive_group()
    weight_group.add_argument('--use-weights', dest='use_weights', action='store_true',
                             help='Use ergonomic difficulty multipliers (default)')
    weight_group.add_argument('--no-weights', dest='use_weights', action='store_false', 
                             help='Ignore ergonomic weights, use only base times and SHIFT penalty')
    parser.set_defaults(use_weights=True)
    
    parser.add_argument('--compare-weights', action='store_true',
                       help='Run analysis with both weighted and unweighted calculations')
    
    parser.add_argument('--markdown-report', action='store_true',
                       help='Generate comprehensive markdown report with date/time naming')
    
    parser.add_argument('--no-markdown', action='store_true',
                       help='Skip automatic markdown report generation')
    
    args = parser.parse_args()
    
    # Handle special commands
    if args.list_typists:
        TypistProfile.list_profiles()
        return
    
    if not args.document:
        parser.error("Document path is required unless using --list-typists")
    
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
    
    weight_mode = "weighted" if args.use_weights else "unweighted"
    print("=" * 80)
    print("THAI NUMBERS TYPING COST ANALYSIS")
    print("=" * 80)
    print(f"Document: {args.document}")
    print(f"Typist Profile: {typist_profile['name']}")
    print(f"Base Keystroke Time: {typist_profile['keystroke_time']}s")
    print(f"Weight Mode: {weight_mode}")
    print(f"Output Directory: {args.output}")
    print("=" * 80)
    
    # Run requested analyses
    if args.text_only:
        run_text_analysis(args.document, args.output)
    elif args.keyboard_only:
        if args.compare_weights:
            print("Running keyboard comparison with both weighted and unweighted modes...")
            run_keyboard_comparison(typist_profile, args.output, use_weights=True)
            run_keyboard_comparison(typist_profile, args.output, use_weights=False)
        else:
            run_keyboard_comparison(typist_profile, args.output, args.use_weights)
    elif args.compare_all:
        run_text_analysis(args.document, args.output)
        if args.compare_weights:
            print("Running comparative analysis with both weighted and unweighted modes...")
            run_comparative_analysis(args.document, args.output, use_weights=True)
            run_comparative_analysis(args.document, args.output, use_weights=False)
        else:
            run_comparative_analysis(args.document, args.output, args.use_weights)
    elif args.compare_weights:
        # Special case: compare weighted vs unweighted for selected typist
        run_text_analysis(args.document, args.output)
        print("Running analysis with both weighted and unweighted modes...")
        run_keyboard_comparison(typist_profile, args.output, use_weights=True)
        run_keyboard_comparison(typist_profile, args.output, use_weights=False)
        run_typing_cost_analysis(args.document, typist_profile, args.output, use_weights=True)
        run_typing_cost_analysis(args.document, typist_profile, args.output, use_weights=False)
    else:
        # Full analysis for selected typist with chosen weight mode
        run_text_analysis(args.document, args.output)
        run_keyboard_comparison(typist_profile, args.output, args.use_weights)
        run_typing_cost_analysis(args.document, typist_profile, args.output, args.use_weights)
    
    print(f"\nAnalysis complete! Results saved to: {args.output}/")
    
    # Generate markdown report if requested or for comprehensive analyses
    should_generate_markdown = (
        args.markdown_report or 
        (args.compare_all and not args.no_markdown) or
        (args.compare_weights and not args.no_markdown)
    )
    
    if should_generate_markdown:
        print("\n" + "="*80)
        print("GENERATING COMPREHENSIVE MARKDOWN REPORT")
        print("="*80)
        
        try:
            reporter = MarkdownReporter(args.document, args.output)
            report_path = reporter.generate_comprehensive_report(
                include_all_typists=args.compare_all,
                include_weight_comparison=args.compare_weights
            )
            
            print(f"\n📊 MARKDOWN REPORT GENERATED SUCCESSFULLY!")
            print(f"📄 Location: {report_path}")
            print(f"🎯 Features: Enhanced keyboard models, validation results, official standards")
            
        except Exception as e:
            print(f"\n⚠️  Markdown report generation failed: {e}")
            print("Regular analysis results are still available in the output directory.")


if __name__ == "__main__":
    main()