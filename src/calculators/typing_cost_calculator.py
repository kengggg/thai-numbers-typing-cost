#!/usr/bin/env python3
"""
Typing Cost Calculator
Calculates the actual typing cost for the Thai constitution under different scenarios.
"""

import re
from typing import Dict, List, Tuple
from models.text_analyzer import TextAnalyzer
from models.keyboard_layouts import KedmaneeLayout, PattajotiLayout, KeyboardType


class TypingCostCalculator:
    """Calculates typing costs for documents under different keyboard scenarios."""
    
    def __init__(self, document_path: str, base_keystroke_time: float = 0.28):
        self.document_path = document_path
        self.base_keystroke_time = base_keystroke_time
        self.analyzer = TextAnalyzer(document_path)
        self.kedmanee = KedmaneeLayout()
        self.pattajoti = PattajotiLayout()
        
        # Create digit mapping for conversion scenarios
        self.thai_to_intl_map = {
            '๐': '0', '๑': '1', '๒': '2', '๓': '3', '๔': '4',
            '๕': '5', '๖': '6', '๗': '7', '๘': '8', '๙': '9'
        }
        self.intl_to_thai_map = {v: k for k, v in self.thai_to_intl_map.items()}
    
    def convert_digits(self, text: str, target_type: str) -> str:
        """Convert digits in text to target type (thai/international)."""
        if target_type == "thai":
            # Convert international to Thai digits
            for intl, thai in self.intl_to_thai_map.items():
                text = text.replace(intl, thai)
        elif target_type == "international":
            # Convert Thai to international digits
            for thai, intl in self.thai_to_intl_map.items():
                text = text.replace(thai, intl)
        return text
    
    def calculate_document_cost(self, keyboard_layout, digit_conversion: str = "none") -> Dict:
        """Calculate typing cost for the entire document."""
        text = self.analyzer.text
        
        # Apply digit conversion if specified
        if digit_conversion == "to_international":
            text = self.convert_digits(text, "international")
        elif digit_conversion == "to_thai":
            text = self.convert_digits(text, "thai")
        
        total_cost = 0.0
        character_costs = {}
        digit_costs = {}
        
        # Calculate cost for each character
        for char in text:
            cost = keyboard_layout.calculate_typing_cost(char, self.base_keystroke_time)
            total_cost += cost
            
            # Track character-specific costs
            if char not in character_costs:
                character_costs[char] = {'count': 0, 'total_cost': 0.0}
            character_costs[char]['count'] += 1
            character_costs[char]['total_cost'] += cost
            
            # Track digit costs specifically
            if char.isdigit() or char in self.thai_to_intl_map:
                if char not in digit_costs:
                    digit_costs[char] = {'count': 0, 'total_cost': 0.0}
                digit_costs[char]['count'] += 1
                digit_costs[char]['total_cost'] += cost
        
        return {
            'total_cost_seconds': total_cost,
            'total_cost_minutes': total_cost / 60,
            'total_cost_hours': total_cost / 3600,
            'total_characters': len(text),
            'average_cost_per_char': total_cost / len(text) if len(text) > 0 else 0,
            'character_costs': character_costs,
            'digit_costs': digit_costs,
            'keyboard_layout': keyboard_layout.layout_type.value,
            'conversion_applied': digit_conversion,
            'base_keystroke_time': self.base_keystroke_time
        }
    
    def analyze_all_scenarios(self) -> Dict:
        """Analyze all research question scenarios."""
        scenarios = {}
        
        print("Calculating typing costs for all scenarios...")
        
        # Scenario 1: Thai digits on Kedmanee (current state)
        print("  Scenario 1: Thai digits on Kedmanee...")
        scenarios['thai_kedmanee'] = self.calculate_document_cost(
            self.kedmanee, "none"  # Text already has Thai digits
        )
        
        # Scenario 2: International digits on Kedmanee
        print("  Scenario 2: International digits on Kedmanee...")
        scenarios['intl_kedmanee'] = self.calculate_document_cost(
            self.kedmanee, "to_international"
        )
        
        # Scenario 3: Thai digits on Pattajoti
        print("  Scenario 3: Thai digits on Pattajoti...")
        scenarios['thai_pattajoti'] = self.calculate_document_cost(
            self.pattajoti, "none"  # Text already has Thai digits
        )
        
        # Scenario 4: International digits on Pattajoti
        print("  Scenario 4: International digits on Pattajoti...")
        scenarios['intl_pattajoti'] = self.calculate_document_cost(
            self.pattajoti, "to_international"
        )
        
        return scenarios
    
    def calculate_savings_analysis(self, scenarios: Dict) -> Dict:
        """Calculate time savings between different scenarios."""
        base_scenario = scenarios['thai_kedmanee']  # Current state (baseline)
        
        savings = {}
        
        for scenario_name, scenario_data in scenarios.items():
            if scenario_name == 'thai_kedmanee':
                continue
                
            time_saved_seconds = base_scenario['total_cost_seconds'] - scenario_data['total_cost_seconds']
            time_saved_minutes = time_saved_seconds / 60
            time_saved_hours = time_saved_seconds / 3600
            
            percentage_saved = (time_saved_seconds / base_scenario['total_cost_seconds']) * 100 if base_scenario['total_cost_seconds'] > 0 else 0.0
            
            savings[scenario_name] = {
                'time_saved_seconds': time_saved_seconds,
                'time_saved_minutes': time_saved_minutes,
                'time_saved_hours': time_saved_hours,
                'percentage_saved': percentage_saved,
                'cost_per_digit': scenario_data['total_cost_seconds'] / sum(
                    data['count'] for char, data in scenario_data['digit_costs'].items()
                ) if scenario_data['digit_costs'] else 0
            }
        
        return savings
    
    def print_comprehensive_report(self):
        """Print a comprehensive analysis report."""
        print("=" * 80)
        print("THAI CONSTITUTION TYPING COST ANALYSIS")
        print(f"Base keystroke time: {self.base_keystroke_time}s per keystroke + SHIFT penalty")
        print("=" * 80)
        
        # Get basic document stats
        stats = self.analyzer.get_statistics()
        print(f"\nDOCUMENT STATISTICS:")
        print(f"  Total characters: {stats['document_stats']['total_characters']:,}")
        print(f"  Total digits: {stats['document_stats']['total_digits']:,}")
        print(f"  Digit percentage: {stats['document_stats']['digit_percentage']:.2f}%")
        
        # Analyze all scenarios
        scenarios = self.analyze_all_scenarios()
        
        print(f"\nTYPING COST BY SCENARIO:")
        print(f"{'Scenario':<25} {'Time (min)':<12} {'Time (hrs)':<12} {'Avg/char (ms)':<15}")
        print("-" * 70)
        
        scenario_names = {
            'thai_kedmanee': 'Thai + Kedmanee',
            'intl_kedmanee': 'International + Kedmanee',
            'thai_pattajoti': 'Thai + Pattajoti',
            'intl_pattajoti': 'International + Pattajoti'
        }
        
        for key, scenario in scenarios.items():
            name = scenario_names[key]
            minutes = scenario['total_cost_minutes']
            hours = scenario['total_cost_hours']
            avg_ms = scenario['average_cost_per_char'] * 1000
            
            print(f"{name:<25} {minutes:<12.1f} {hours:<12.2f} {avg_ms:<15.1f}")
        
        # Calculate and display savings
        savings = self.calculate_savings_analysis(scenarios)
        
        print(f"\nTIME SAVINGS COMPARED TO CURRENT STATE (Thai + Kedmanee):")
        print(f"{'Alternative Scenario':<25} {'Saved (min)':<12} {'Saved (%)':<12} {'Cost/digit (ms)':<15}")
        print("-" * 70)
        
        for key, saving in savings.items():
            name = scenario_names[key]
            saved_min = saving['time_saved_minutes']
            saved_pct = saving['percentage_saved']
            cost_per_digit_ms = saving['cost_per_digit'] * 1000
            
            print(f"{name:<25} {saved_min:<12.1f} {saved_pct:<12.1f} {cost_per_digit_ms:<15.1f}")
        
        # Detailed digit analysis
        print(f"\nDIGIT-SPECIFIC COST ANALYSIS:")
        base_scenario = scenarios['thai_kedmanee']
        
        print(f"\nCurrent document uses Thai digits with these costs:")
        for digit, data in sorted(base_scenario['digit_costs'].items()):
            cost_per_digit = data['total_cost'] / data['count'] if data['count'] > 0 else 0.0
            total_cost_seconds = data['total_cost']
            print(f"  {digit}: {data['count']:,} occurrences, {cost_per_digit*1000:.1f}ms each, {total_cost_seconds:.1f}s total")
        
        # Calculate theoretical best case
        best_scenario_key = min(scenarios.keys(), key=lambda k: scenarios[k]['total_cost_seconds'])
        best_scenario = scenarios[best_scenario_key]
        
        print(f"\nOPTIMAL SCENARIO ANALYSIS:")
        print(f"  Best scenario: {scenario_names[best_scenario_key]}")
        print(f"  Total time: {best_scenario['total_cost_minutes']:.1f} minutes")
        
        # Handle case where best scenario is the baseline (current state)
        if best_scenario_key == 'thai_kedmanee':
            print(f"  Time saved vs current: 0.0 minutes")
            print(f"  Efficiency gain: 0.0%")
        else:
            print(f"  Time saved vs current: {savings[best_scenario_key]['time_saved_minutes']:.1f} minutes")
            print(f"  Efficiency gain: {savings[best_scenario_key]['percentage_saved']:.1f}%")
        
        return scenarios, savings


if __name__ == "__main__":
    import sys
    import os
    from pathlib import Path
    
    # Add src directory to path for imports
    src_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(src_dir))
    
    if len(sys.argv) < 2:
        print("Usage: python typing_cost_calculator.py <document_path> [base_keystroke_time]")
        print("Example: python typing_cost_calculator.py ../data/thai-con.txt 0.28")
        sys.exit(1)
    
    document_path = sys.argv[1]
    base_time = float(sys.argv[2]) if len(sys.argv) > 2 else 0.28
    
    if not os.path.exists(document_path):
        print(f"Error: Document not found at {document_path}")
        sys.exit(1)
    
    print("🧮 Thai Numbers Typing Cost Calculator - Standalone Test")
    print("=" * 70)
    print(f"Document: {document_path}")
    print(f"Base keystroke time: {base_time}s")
    print("=" * 70)
    
    calculator = TypingCostCalculator(document_path, base_time)
    calculator.print_comprehensive_report()
    
    print("\n✅ Typing cost calculator test completed successfully!")


def main():
    """Main function for standalone execution - wrapper for if __name__ == '__main__' block."""
    import sys
    import os
    from pathlib import Path
    
    # Add src directory to path for imports
    src_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(src_dir))
    
    if len(sys.argv) < 2:
        print("Usage: python typing_cost_calculator.py <document_path> [base_keystroke_time]")
        print("Example: python typing_cost_calculator.py ../data/thai-con.txt 0.28")
        sys.exit(1)
    
    document_path = sys.argv[1]
    base_time = float(sys.argv[2]) if len(sys.argv) > 2 else 0.28
    
    if not os.path.exists(document_path):
        print(f"Error: Document not found at {document_path}")
        sys.exit(1)
    
    print("🧮 Thai Numbers Typing Cost Calculator - Standalone Test")
    print("=" * 70)
    print(f"Document: {document_path}")
    print(f"Base keystroke time: {base_time}s")
    print("=" * 70)
    
    calculator = TypingCostCalculator(document_path, base_time)
    calculator.print_comprehensive_report()
    
    print("\n✅ Typing cost calculator test completed successfully!")