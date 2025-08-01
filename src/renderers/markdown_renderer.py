#!/usr/bin/env python3
"""
Markdown Renderer for Thai Numbers Typing Cost Analysis

Converts structured JSON analysis data into focused markdown reports.
Separates presentation logic from data generation for better portability.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class MarkdownRenderer:
    """Renders JSON analysis data to focused markdown reports."""

    def __init__(self, analysis_data: Dict[str, Any]):
        self.data = analysis_data

    def render_comprehensive_report(self) -> str:
        """Render complete focused research report in markdown."""
        sections = [
            self._render_header(),
            self._render_executive_summary(),
            self._render_research_questions(),
            self._render_impact_analysis(),
            self._render_conclusion(),
        ]

        return "\n".join(sections)

    def _render_header(self) -> str:
        """Render report header."""
        metadata = self.data.get("metadata", {})

        # Safe extraction with defaults
        generated_at = metadata.get("generated_at", datetime.now().isoformat())
        try:
            generated_time = datetime.fromisoformat(generated_at).strftime(
                "%B %d, %Y at %H:%M:%S"
            )
        except (ValueError, TypeError):
            generated_time = "Unknown"

        document_path = metadata.get("document_path", "Unknown document")
        tool_version = metadata.get("tool_version", "Unknown version")
        analysis_focus = metadata.get(
            "analysis_focus",
            "Thai digits vs International digits typing cost comparison",
        )

        return f"""# Thai Numbers Typing Cost Analysis - Research Report

**Generated:** {generated_time}
**Document Analyzed:** 2017 Thai Constitution ({document_path})
**Analysis Tool:** Thai Numbers Typing Cost Analysis CLI v{tool_version}
**Focus:** {analysis_focus}

---
"""

    def _render_executive_summary(self) -> str:
        """Render executive summary section."""
        metadata = self.data.get("metadata", {})
        key_findings = self.data.get("key_findings", {})
        document_stats = metadata.get("document_stats", {})

        # Safe extraction with defaults
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

        return f"""## Executive Summary

This research directly compares the typing cost of Thai digits (๐-๙) versus international digits (0-9) in Thai government documents. The analysis uses the 2017 Thai Constitution as a real-world benchmark.

### Key Findings

- **Document Scale:** {total_chars:,} characters analyzed, {total_digits:,} digits found ({digit_percentage}% of document)
- **Current State:** Thai digits on Kedmanee keyboard = {current_time} minutes typing time
- **Optimal State:** International digits on Pattajoti keyboard = {optimal_time} minutes typing time
- **Time Savings:** {time_saved} minutes saved per document ({efficiency_gain}% efficiency gain)
- **Root Cause:** {root_cause}

### The Core Problem

**Thai digits on Kedmanee keyboard require the SHIFT key**, creating a 2x typing cost penalty compared to international digits. This fundamental inefficiency impacts every digit typed in Thai government documents.

---
"""

    def _render_research_questions(self) -> str:
        """Render research questions and answers."""
        questions = self.data.get("research_questions", {})

        content = "## Research Questions Answered\n\n"

        # Skip if no questions available
        if not questions:
            content += "*(Research questions will be generated when comprehensive analysis is run)*\n\n"
            content += "---\n"
            return content

        # Q1
        q1 = questions.get("q1", {})
        if q1:
            q1_details = q1.get("details", {})
            content += f"""### Q1: {q1.get('question', 'Unknown question')}
**Answer:** {q1.get('answer', 'Unknown answer')}
- **Why higher cost:** {q1_details.get('why_higher_cost', 'Unknown')}
- **Total digits typed:** {q1_details.get('total_digits_typed', 0):,} occurrences

"""

        # Q2
        q2 = questions.get("q2", {})
        if q2:
            q2_details = q2.get("details", {})
            content += f"""### Q2: {q2.get('question', 'Unknown question')}
**Answer:** {q2.get('answer', 'Unknown answer')}
- **Time saved vs Thai digits:** {q2_details.get('time_saved_vs_thai', 'Unknown')} minutes ({q2_details.get('percentage_saved', 'Unknown')}%)
- **Why faster:** {q2_details.get('why_faster', 'Unknown')}

"""

        # Q3
        q3 = questions.get("q3", {})
        if q3:
            q3_details = q3.get("details", {})
            content += f"""### Q3: {q3.get('question', 'Unknown question')}
**Answer:** {q3.get('answer', 'Unknown answer')}
- **Time saved vs Kedmanee:** {q3_details.get('time_saved_vs_kedmanee', 'Unknown')} minutes ({q3_details.get('percentage_saved', 'Unknown')}%)
- **Why faster:** {q3_details.get('why_faster', 'Unknown')}

"""

        # Q4
        q4 = questions.get("q4", {})
        if q4:
            q4_details = q4.get("details", {})
            content += f"""### Q4: {q4.get('question', 'Unknown question')}
**Answer:** {q4.get('answer', 'Unknown answer')}
- **Time saved vs current state:** {q4_details.get('time_saved_vs_current', 'Unknown')} minutes ({q4_details.get('percentage_saved', 'Unknown')}%)
- **Status:** {q4_details.get('status', 'Unknown')}

"""

        # Q5
        q5 = questions.get("q5", {})
        if q5:
            q5_details = q5.get("details", {})
            content += f"""### Q5: {q5.get('question', 'Unknown question')}
**Answer:** {q5.get('answer', 'Unknown answer')}
- **Per document loss:** {q5_details.get('per_document_loss_minutes', 'Unknown')} minutes wasted
- **Efficiency loss:** {q5_details.get('efficiency_loss_percentage', 'Unknown')}% vs optimal
- **Root cause:** {q5_details.get('root_cause', 'Unknown')}
- **Simple solution:** {q5_details.get('simple_solution', 'Unknown')}

"""

        content += "---\n"

        return content

    def _render_impact_analysis(self) -> str:
        """Render impact projections."""
        impact = self.data.get("impact_projections", {})

        # Safe extraction with defaults
        per_doc_savings = impact.get("per_document_savings_minutes", "Unknown")
        projections = impact.get("government_scale_projections", [])
        assumptions = impact.get("assumptions", {})
        working_days = assumptions.get("working_days_per_year", 250)
        hourly_cost = assumptions.get("hourly_labor_cost", 15)

        content = f"""## Impact Analysis: Government Scale Projections

Based on {per_doc_savings} minutes saved per document (switching from Thai digits to international digits):

### Scalability Analysis

| Scale | Documents/Day | Annual Hours Saved | Annual Cost Savings |
|-------|---------------|-------------------|---------------------|
"""

        for projection in projections:
            scale = projection.get("scale", "Unknown")
            docs_per_day = projection.get("docs_per_day", 0)
            hours_saved = projection.get("annual_hours_saved", 0)
            cost_savings = projection.get("annual_cost_savings", 0)
            content += f"| **{scale}** | {docs_per_day} docs | {hours_saved:,.0f} hours | ${cost_savings:,.0f} |\n"

        efficiency_gain = (
            self.data.get("key_findings", {})
            .get("improvement", {})
            .get("efficiency_gain_percentage", "Unknown")
        )

        content += f"""
*Based on {working_days} working days/year, ${hourly_cost}/hour labor cost*

### Key Impact Metrics

- **Per-document efficiency gain:** {efficiency_gain}%
- **Implementation cost:** Nearly zero (template updates + brief training)
- **Payback period:** Immediate (first document processed)
- **Scalability:** Linear - benefits multiply with document volume
- **Risk:** Minimal - international digits are universally supported

### Why This Matters

1. **Immediate benefit:** Every document typed saves {per_doc_savings} minutes
2. **Cumulative impact:** Thousands of hours saved annually at scale
3. **Zero infrastructure cost:** Uses existing keyboards and systems
4. **Universal applicability:** Benefits every typist regardless of skill level

---
"""

        return content

    def _render_conclusion(self) -> str:
        """Render conclusion and recommendations."""
        recommendations = self.data.get("recommendations", {})
        key_findings = self.data.get("key_findings", {})
        impact = self.data.get("impact_projections", {})

        # Safe extraction with defaults
        improvement = key_findings.get("improvement", {})
        time_saved = improvement.get("time_saved_minutes", "Unknown")
        efficiency_gain = improvement.get("efficiency_gain_percentage", "Unknown")

        # Get the largest scale projection for dramatic effect
        projections = impact.get("government_scale_projections", [])
        largest_projection = projections[-1] if projections else {}

        primary_recommendation = recommendations.get(
            "primary",
            "Standardize on international digits (0-9) for all Thai government documents",
        )

        content = f"""## Conclusion & Recommendations

### Clear Finding

**Using Thai digits in government documents creates unnecessary typing inefficiency.** The analysis shows {time_saved} minutes wasted per document ({efficiency_gain}% inefficiency) due to the SHIFT key requirement for Thai digits on standard keyboards.

### Root Cause

The problem is simple: **Thai digits require the SHIFT key on Kedmanee keyboards**, doubling the typing cost for every digit. International digits (0-9) require no SHIFT key, making them twice as fast to type.

### Recommended Action

**{primary_recommendation}**

#### Why This Works:
"""

        benefits = recommendations.get("benefits", [])
        for benefit in benefits:
            if ":" in benefit:
                content += f"- **{benefit.split(':')[0]}**: {benefit.split(':', 1)[1].strip()}\n"
            else:
                content += f"- {benefit}\n"

        content += """
#### Implementation Steps:
"""

        steps = recommendations.get("implementation_steps", [])
        for i, step in enumerate(steps, 1):
            content += f"{i}. **{step}**\n"

        content += """
### Impact Projection

"""
        if largest_projection:
            hours_saved = largest_projection.get("annual_hours_saved", 0)
            cost_savings = largest_projection.get("annual_cost_savings", 0)
            content += f"At government scale ({hours_saved:,.0f} hours saved annually), this simple change could save ${cost_savings:,.0f} per year in productivity costs while requiring virtually zero implementation investment.\n\n"
        else:
            content += "Government-scale implementation would provide significant productivity improvements with minimal implementation cost.\n\n"

        tool_version = self.data.get("metadata", {}).get("tool_version", "Unknown")

        content += f"""### Bottom Line

**This is a no-brainer policy change.** The research provides clear evidence that switching to international digits eliminates an unnecessary typing inefficiency that costs the Thai government time and resources. The solution is simple, cost-free, and immediately beneficial.

---

*Report generated by Thai Numbers Typing Cost Analysis Tool v{tool_version}*
"""

        # Safe date handling
        metadata = self.data.get("metadata", {})
        generated_at = metadata.get("generated_at", "")
        if generated_at:
            try:
                research_date = datetime.fromisoformat(generated_at).strftime(
                    "%B %d, %Y"
                )
                content += f"*Research conducted {research_date}*\n\n"
            except (ValueError, TypeError):
                content += "*Research conducted recently*\n\n"
        else:
            content += "*Research conducted recently*\n\n"

        return content

    def save_to_file(self, markdown_content: str, output_path: str) -> str:
        """Save markdown content to file."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        return output_path

    def render_summary_table(self) -> str:
        """Render a quick summary table of key metrics."""
        key_findings = self.data["key_findings"]

        return f"""## Quick Summary

| Metric | Value |
|--------|-------|
| Current typing time | {key_findings['current_state']['time_minutes']} minutes |
| Optimal typing time | {key_findings['optimal_state']['time_minutes']} minutes |
| Time saved per document | {key_findings['improvement']['time_saved_minutes']} minutes |
| Efficiency improvement | {key_findings['improvement']['efficiency_gain_percentage']}% |
| Root cause | {key_findings['improvement']['root_cause']} |
"""

    def render_scenarios_comparison(self) -> str:
        """Render detailed scenarios comparison."""
        # Get average typist results
        results = self.data["analysis_results"]["average"]
        scenarios = results["scenarios"]

        content = """## Detailed Scenarios Comparison

| Scenario | Time (minutes) | Time (hours) | Status |
|----------|----------------|--------------|--------|
"""

        for scenario_key, scenario in scenarios.items():
            status = "🔴 Current" if scenario_key == "thai_kedmanee" else ""
            status = (
                "🟢 Optimal" if scenario_key == results["optimal_scenario"] else status
            )

            content += f"| {scenario['description']} | {scenario['total_cost_minutes']} | {scenario['total_cost_hours']} | {status} |\n"

        return content


def render_json_to_markdown(json_data: Dict[str, Any], output_path: str = None) -> str:
    """Convenience function to render JSON to markdown and optionally save."""
    renderer = MarkdownRenderer(json_data)
    markdown_content = renderer.render_comprehensive_report()

    if output_path:
        renderer.save_to_file(markdown_content, output_path)
        return output_path

    return markdown_content


def main():
    """Main function for standalone execution."""
    import json
    import sys

    if len(sys.argv) < 2:
        print("Usage: python markdown_renderer.py <json_file> [output_markdown_file]")
        sys.exit(1)

    json_file = sys.argv[1]

    # Load JSON data
    with open(json_file, "r", encoding="utf-8") as f:
        analysis_data = json.load(f)

    # Generate timestamped filename if not provided
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        timestamp = (
            analysis_data["metadata"]["generated_at"]
            .replace(":", "")
            .replace("-", "")
            .replace("T", "_")
            .split(".")[0]
        )
        # Always generate reports in proper output directory, not current working directory
        import os

        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "..", "output"
        )
        output_file = os.path.join(output_dir, f"analysis_report_{timestamp}.md")

    # Render to markdown
    saved_path = render_json_to_markdown(analysis_data, output_file)

    print(f"Markdown report generated: {saved_path}")
    print(
        f"Key insight: {analysis_data['key_findings']['improvement']['time_saved_minutes']} minutes saved per document"
    )


if __name__ == "__main__":
    main()
