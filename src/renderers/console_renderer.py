#!/usr/bin/env python3
"""
Console Renderer for Thai Numbers Typing Cost Analysis

Converts structured JSON analysis data into formatted console output.
Provides clean, readable console presentation of analysis results.
"""

from typing import Any, Dict


class ConsoleRenderer:
    """Renders JSON analysis data to formatted console output."""

    def __init__(self, analysis_data: Dict[str, Any]):
        self.data = analysis_data

    def render_summary(self) -> str:
        """Render concise summary for console output."""
        metadata = self.data.get("metadata", {})
        key_findings = self.data.get("key_findings", {})
        document_stats = metadata.get("document_stats", {})

        # Safe extraction with defaults
        document_path = metadata.get("document_path", "Unknown document")
        total_chars = document_stats.get("total_characters", 0)
        total_digits = document_stats.get("total_digits", 0)
        digit_percentage = document_stats.get("digit_percentage", 0.0)

        current_state = key_findings.get("current_state", {})
        optimal_state = key_findings.get("optimal_state", {})
        improvement = key_findings.get("improvement", {})

        current_time = current_state.get("time_minutes", "Unknown")
        optimal_time = optimal_state.get("time_minutes", "Unknown")
        time_saved = improvement.get("time_saved_minutes", "Unknown")
        efficiency_gain = improvement.get("efficiency_gain_percentage", "Unknown")
        root_cause = improvement.get(
            "root_cause", "Thai digits require SHIFT key on Kedmanee layout"
        )

        content = []
        content.append("=" * 80)
        content.append("THAI NUMBERS TYPING COST ANALYSIS - SUMMARY")
        content.append("=" * 80)
        content.append("")
        content.append(f"Document: {document_path}")
        content.append(f"Characters analyzed: {total_chars:,}")
        content.append(f"Digits found: {total_digits:,} ({digit_percentage}%)")
        content.append("")
        content.append("KEY FINDINGS:")
        content.append("-" * 40)
        content.append(f"  Current cost (Thai + Kedmanee): {current_time} minutes")
        content.append(f"  Optimal cost (Intl + Pattajoti): {optimal_time} minutes")
        content.append(f"  Time saved per document: {time_saved} minutes")
        content.append(f"  Efficiency improvement: {efficiency_gain}%")
        content.append("")
        content.append(f"ROOT CAUSE: {root_cause}")
        content.append("")

        return "\\n".join(content)

    def render_research_questions(self) -> str:
        """Render research questions and answers."""
        questions = self.data.get("research_questions", {})

        content = []
        content.append("RESEARCH QUESTIONS ANSWERED:")
        content.append("=" * 50)
        content.append("")

        for q_id, question in questions.items():
            content.append(f"{q_id.upper()}: {question['question']}")
            content.append(f"Answer: {question['answer']}")
            content.append("")

        return "\\n".join(content)

    def render_scenarios_table(self) -> str:
        """Render scenarios comparison table."""
        # Use average typist results
        results = self.data["analysis_results"]["average"]
        scenarios = results["scenarios"]
        key_findings = self.data.get("key_findings", {})
        improvement = key_findings.get("improvement", {})

        content = []
        content.append("TYPING COST BY SCENARIO:")
        content.append("-" * 70)
        content.append(
            f"{'Scenario':<30} {'Time (min)':<12} {'Time (hrs)':<12} {'Status':<15}"
        )
        content.append("-" * 70)

        for scenario_key, scenario in scenarios.items():
            status = "CURRENT" if scenario_key == "thai_kedmanee" else ""
            status = (
                "OPTIMAL" if scenario_key == results["optimal_scenario"] else status
            )

            content.append(
                f"{scenario['description']:<30} {scenario['total_cost_minutes']:<12.1f} {scenario['total_cost_hours']:<12.2f} {status:<15}"
            )

        content.append("")

        # Add key findings information that tests expect
        time_saved = improvement.get("time_saved_minutes", "Unknown")
        efficiency_gain = improvement.get("efficiency_gain_percentage", "Unknown")
        content.append(
            f"KEY FINDINGS: {time_saved} minutes saved per document ({efficiency_gain}% efficiency gain)"
        )
        content.append("")

        return "\\n".join(content)

    def render_savings_analysis(self) -> str:
        """Render savings analysis."""
        results = self.data["analysis_results"]["average"]
        savings = results["savings_analysis"]

        content = []
        content.append("TIME SAVINGS COMPARED TO CURRENT STATE:")
        content.append("-" * 70)
        content.append(
            f"{'Alternative Scenario':<30} {'Saved (min)':<12} {'Saved (%)':<12}"
        )
        content.append("-" * 70)

        for _, saving in savings.items():
            content.append(
                f"{saving['description']:<30} {saving['time_saved_minutes']:<12.1f} {saving['percentage_saved']:<12.1f}"
            )

        content.append("")
        return "\\n".join(content)

    def render_impact_projections(self) -> str:
        """Render government impact projections."""
        impact = self.data["impact_projections"]

        content = []
        content.append("GOVERNMENT IMPACT PROJECTIONS:")
        content.append("-" * 70)
        content.append(
            f"Based on {impact['per_document_savings_minutes']} minutes saved per document"
        )
        content.append("")
        content.append(f"{'Scale':<20} {'Annual Hours':<15} {'Annual Savings':<15}")
        content.append("-" * 50)

        for projection in impact["government_scale_projections"]:
            content.append(
                f"{projection['scale']:<20} {projection['annual_hours_saved']:,.0f} hours     ${projection['annual_cost_savings']:,.0f}"
            )

        content.append("")
        return "\\n".join(content)

    def render_recommendations(self) -> str:
        """Render recommendations."""
        recommendations = self.data["recommendations"]

        content = []
        content.append("RECOMMENDATIONS:")
        content.append("-" * 40)
        content.append(
            f"PRIMARY: {recommendations['primary_recommendation']['action']}"
        )
        content.append("")
        content.append("Implementation steps:")
        for i, step in enumerate(recommendations["implementation_steps"], 1):
            content.append(f"  {i}. {step}")
        content.append("")
        content.append("Key benefits:")
        for benefit in recommendations["benefits"][:3]:  # Show top 3 benefits
            content.append(f"  • {benefit}")
        content.append("")

        return "\\n".join(content)

    def render_comprehensive(self) -> str:
        """Render comprehensive console output."""
        sections = [
            self.render_summary(),
            "",
            self.render_scenarios_table(),
            self.render_savings_analysis(),
            self.render_research_questions(),
            "",
            self.render_impact_projections(),
            self.render_recommendations(),
            "=" * 80,
        ]

        return "\\n".join(sections)

    def render_quick_stats(self) -> str:
        """Render quick summary stats."""
        key_findings = self.data.get("key_findings", {})
        metadata = self.data.get("metadata", {})
        document_stats = metadata.get("document_stats", {})

        # Safe extraction with defaults
        time_saved = key_findings.get("improvement", {}).get(
            "time_saved_minutes", "Unknown"
        )
        efficiency_gain = key_findings.get("improvement", {}).get(
            "efficiency_gain_percentage", "Unknown"
        )
        total_digits = document_stats.get("total_digits", 0)
        document_path = metadata.get("document_path", "Unknown document")

        content = []
        content.append(
            f"⚡ Quick result: {time_saved} minutes saved per document ({efficiency_gain}% efficiency gain)"
        )
        content.append(f"📄 Document: {document_path} ({total_digits} digits analyzed)")
        content.append(
            "🎯 Solution: Switch to international digits (0-9) for immediate efficiency improvement"
        )

        return "\\n".join(content)

    def render_json_summary(self) -> str:
        """Render a JSON-style summary for debugging."""
        key_findings = self.data["key_findings"]

        summary = {
            "time_saved_minutes": key_findings["improvement"]["time_saved_minutes"],
            "efficiency_gain_percent": key_findings["improvement"][
                "efficiency_gain_percentage"
            ],
            "current_time_minutes": key_findings["current_state"]["time_minutes"],
            "optimal_time_minutes": key_findings["optimal_state"]["time_minutes"],
            "root_cause": key_findings["improvement"]["root_cause"],
        }

        import json

        return json.dumps(summary, indent=2, ensure_ascii=False)


def render_json_to_console(
    json_data: Dict[str, Any], format_type: str = "comprehensive"
) -> str:
    """Convenience function to render JSON to console format."""
    renderer = ConsoleRenderer(json_data)
    # pylint: disable=no-else-return
    if format_type == "summary":
        return renderer.render_summary()
    elif format_type == "quick":
        return renderer.render_quick_stats()
    elif format_type == "scenarios":
        return renderer.render_scenarios_table()
    elif format_type == "json":
        return renderer.render_json_summary()
    else:
        return renderer.render_comprehensive()


def main() -> None:
    """Main function for standalone execution."""
    import json
    import sys

    if len(sys.argv) < 2:
        print("Usage: python console_renderer.py <json_file> [format_type]")
        print("Format types: comprehensive (default), summary, quick, scenarios, json")
        sys.exit(1)

    json_file = sys.argv[1]
    format_type = sys.argv[2] if len(sys.argv) > 2 else "comprehensive"

    # Load JSON data
    with open(json_file, "r", encoding="utf-8") as f:
        analysis_data = json.load(f)

    # Render to console
    console_output = render_json_to_console(analysis_data, format_type)
    print(console_output)


if __name__ == "__main__":
    main()
