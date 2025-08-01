import json

"""
Unit tests for renderer classes (Markdown and Console).

Tests rendering functionality including markdown generation, console output,
template processing, and convenience functions.
"""

import sys
from pathlib import Path

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from renderers.console_renderer import ConsoleRenderer, render_json_to_console
from renderers.markdown_renderer import (MarkdownRenderer,
                                         render_json_to_markdown)


class TestMarkdownRenderer:
    """Test suite for MarkdownRenderer class."""

    def test_initialization(self, sample_json_analysis_data):
        """Test MarkdownRenderer initialization."""
        renderer = MarkdownRenderer(sample_json_analysis_data)

        assert renderer.data == sample_json_analysis_data
        assert isinstance(renderer.data, dict)

    def test_render_header(self, sample_json_analysis_data):
        """Test header rendering."""
        renderer = MarkdownRenderer(sample_json_analysis_data)
        header = renderer._render_header()

        # Check for required elements
        assert "# Thai Numbers Typing Cost Analysis - Research Report" in header
        assert "**Generated:**" in header
        assert "**Document Analyzed:**" in header
        assert "**Analysis Tool:**" in header
        assert "**Focus:**" in header

        # Check data integration
        assert sample_json_analysis_data["metadata"]["document_path"] in header
        assert sample_json_analysis_data["metadata"]["analysis_focus"] in header

    def test_render_executive_summary(self, sample_json_analysis_data):
        """Test executive summary rendering."""
        renderer = MarkdownRenderer(sample_json_analysis_data)
        summary = renderer._render_executive_summary()

        # Check structure
        assert "## Executive Summary" in summary
        assert "### Key Findings" in summary
        assert "### The Core Problem" in summary

        # Check data integration
        key_findings = sample_json_analysis_data["key_findings"]
        assert str(key_findings["improvement"]["time_saved_minutes"]) in summary
        assert str(key_findings["improvement"]["efficiency_gain_percentage"]) in summary

        # Check markdown formatting
        assert "**Current State:**" in summary
        assert "**Optimal State:**" in summary
        assert "- **" in summary  # Bullet points

    def test_render_research_questions(self, sample_json_analysis_data):
        """Test research questions rendering."""
        renderer = MarkdownRenderer(sample_json_analysis_data)
        questions = renderer._render_research_questions()

        # Check structure
        assert "## Research Questions Answered" in questions
        assert "### Q1:" in questions
        assert "### Q2:" in questions
        assert "### Q3:" in questions
        assert "### Q4:" in questions
        assert "### Q5:" in questions

        # Check markdown formatting
        assert "**Answer:**" in questions
        assert "- **" in questions  # Bullet points with bold labels

    def test_render_impact_analysis(self, sample_json_analysis_data):
        """Test impact analysis rendering."""
        renderer = MarkdownRenderer(sample_json_analysis_data)
        impact = renderer._render_impact_analysis()

        # Check structure
        assert "## Impact Analysis: Government Scale Projections" in impact
        assert "### Scalability Analysis" in impact
        assert "### Key Impact Metrics" in impact
        assert "### Why This Matters" in impact

        # Check table formatting
        assert (
            "| Scale | Documents/Day | Annual Hours Saved | Annual Cost Savings |"
            in impact
        )
        assert "|-------|" in impact  # Table header separator

        # Check data integration
        assert (
            str(
                sample_json_analysis_data["impact_projections"][
                    "per_document_savings_minutes"
                ]
            )
            in impact
        )

    def test_render_conclusion(self, sample_json_analysis_data):
        """Test conclusion rendering."""
        renderer = MarkdownRenderer(sample_json_analysis_data)
        conclusion = renderer._render_conclusion()

        # Check structure
        assert "## Conclusion & Recommendations" in conclusion
        assert "### Clear Finding" in conclusion
        assert "### Root Cause" in conclusion
        assert "### Recommended Action" in conclusion
        assert "#### Why This Works:" in conclusion
        assert "#### Implementation Steps:" in conclusion
        assert "### Impact Projection" in conclusion
        assert "### Bottom Line" in conclusion

        # Check data integration
        key_findings = sample_json_analysis_data["key_findings"]
        assert str(key_findings["improvement"]["time_saved_minutes"]) in conclusion
        assert (
            str(key_findings["improvement"]["efficiency_gain_percentage"]) in conclusion
        )

        # Check footer
        assert "*Report generated by" in conclusion
        assert "*Research conducted" in conclusion

    def test_render_comprehensive_report(self, sample_json_analysis_data):
        """Test comprehensive report rendering."""
        renderer = MarkdownRenderer(sample_json_analysis_data)
        report = renderer.render_comprehensive_report()

        # Should contain all sections
        sections = [
            "# Thai Numbers Typing Cost Analysis - Research Report",
            "## Executive Summary",
            "## Research Questions Answered",
            "## Impact Analysis: Government Scale Projections",
            "## Conclusion & Recommendations",
        ]

        for section in sections:
            assert section in report, f"Missing section: {section}"

        # Should be substantial content
        assert len(report) > 5000  # Should be a comprehensive report

        # Should be valid markdown
        assert report.count("#") >= 10  # Multiple headers
        assert report.count("**") >= 20  # Multiple bold sections
        assert "---" in report  # Section separators

    def test_save_to_file(self, sample_json_analysis_data, tmp_path):
        """Test saving markdown to file."""
        renderer = MarkdownRenderer(sample_json_analysis_data)
        markdown_content = "# Test Markdown\n\nThis is a test."
        output_file = tmp_path / "test_output.md"

        saved_path = renderer.save_to_file(markdown_content, str(output_file))

        assert saved_path == str(output_file)
        assert output_file.exists()

        # Verify content
        content = output_file.read_text(encoding="utf-8")
        assert content == markdown_content

    def test_save_to_file_creates_directories(
        self, sample_json_analysis_data, tmp_path
    ):
        """Test that save_to_file creates necessary directories."""
        renderer = MarkdownRenderer(sample_json_analysis_data)
        markdown_content = "# Test"
        output_file = tmp_path / "nested" / "subdir" / "output.md"

        saved_path = renderer.save_to_file(markdown_content, str(output_file))

        assert saved_path == str(output_file)
        assert output_file.exists()
        assert output_file.parent.exists()

    def test_render_summary_table(self, sample_json_analysis_data):
        """Test summary table rendering."""
        renderer = MarkdownRenderer(sample_json_analysis_data)
        table = renderer.render_summary_table()

        # Check structure
        assert "## Quick Summary" in table
        assert "| Metric | Value |" in table
        assert "|--------|-------|" in table

        # Check data integration
        key_findings = sample_json_analysis_data["key_findings"]
        assert str(key_findings["improvement"]["time_saved_minutes"]) in table
        assert str(key_findings["improvement"]["efficiency_gain_percentage"]) in table

    def test_render_scenarios_comparison(self, sample_json_analysis_data):
        """Test scenarios comparison rendering."""
        # Add analysis_results to sample data for this test
        sample_json_analysis_data["analysis_results"] = {
            "average": {
                "scenarios": {
                    "thai_kedmanee": {
                        "description": "Thai digits on Kedmanee keyboard (current state)",
                        "total_cost_minutes": 100.0,
                        "total_cost_hours": 1.67,
                    },
                    "intl_pattajoti": {
                        "description": "International digits on Pattajoti keyboard (optimal)",
                        "total_cost_minutes": 90.0,
                        "total_cost_hours": 1.50,
                    },
                },
                "optimal_scenario": "intl_pattajoti",
            }
        }

        renderer = MarkdownRenderer(sample_json_analysis_data)
        comparison = renderer.render_scenarios_comparison()

        # Check structure
        assert "## Detailed Scenarios Comparison" in comparison
        assert "| Scenario | Time (minutes) | Time (hours) | Status |" in comparison
        assert "|----------|" in comparison

        # Check status indicators
        assert "🔴 Current" in comparison
        assert "🟢 Optimal" in comparison


class TestConsoleRenderer:
    """Test suite for ConsoleRenderer class."""

    def test_initialization(self, sample_json_analysis_data):
        """Test ConsoleRenderer initialization."""
        renderer = ConsoleRenderer(sample_json_analysis_data)

        assert renderer.data == sample_json_analysis_data
        assert isinstance(renderer.data, dict)

    def test_render_summary(self, sample_json_analysis_data):
        """Test summary rendering."""
        renderer = ConsoleRenderer(sample_json_analysis_data)
        summary = renderer.render_summary()

        # Check structure
        assert "THAI NUMBERS TYPING COST ANALYSIS - SUMMARY" in summary
        assert "=" * 80 in summary
        assert "KEY FINDINGS:" in summary
        assert "ROOT CAUSE:" in summary

        # Check data integration
        metadata = sample_json_analysis_data["metadata"]
        key_findings = sample_json_analysis_data["key_findings"]

        assert metadata["document_path"] in summary
        assert str(metadata["document_stats"]["total_characters"]) in summary
        assert str(key_findings["improvement"]["time_saved_minutes"]) in summary
        assert str(key_findings["improvement"]["efficiency_gain_percentage"]) in summary

    def test_render_research_questions(self, sample_json_analysis_data):
        """Test research questions rendering."""
        # Add research questions to sample data
        sample_json_analysis_data["research_questions"] = {
            "q1": {
                "question": "What is the typing cost of Thai digits?",
                "answer": "100 minutes",
                "details": {},
            },
            "q2": {
                "question": "What is the typing cost of international digits?",
                "answer": "90 minutes",
                "details": {},
            },
        }

        renderer = ConsoleRenderer(sample_json_analysis_data)
        questions = renderer.render_research_questions()

        # Check structure
        assert "RESEARCH QUESTIONS ANSWERED:" in questions
        assert "=" * 50 in questions
        assert "Q1: What is the typing cost of Thai digits?" in questions
        assert "Q2: What is the typing cost of international digits?" in questions
        assert "Answer: 100 minutes" in questions
        assert "Answer: 90 minutes" in questions

    def test_render_scenarios_table(self, sample_json_analysis_data):
        """Test scenarios table rendering."""
        # Add analysis_results to sample data
        sample_json_analysis_data["analysis_results"] = {
            "average": {
                "scenarios": {
                    "thai_kedmanee": {
                        "description": "Thai digits on Kedmanee keyboard (current state)",
                        "total_cost_minutes": 100.0,
                        "total_cost_hours": 1.67,
                    },
                    "intl_pattajoti": {
                        "description": "International digits on Pattajoti keyboard (optimal)",
                        "total_cost_minutes": 90.0,
                        "total_cost_hours": 1.50,
                    },
                },
                "optimal_scenario": "intl_pattajoti",
            }
        }

        renderer = ConsoleRenderer(sample_json_analysis_data)
        table = renderer.render_scenarios_table()

        # Check structure
        assert "TYPING COST BY SCENARIO:" in table
        assert "-" * 70 in table
        assert "Scenario" in table
        assert "Time (min)" in table
        assert "Time (hrs)" in table
        assert "Status" in table

        # Check data integration
        assert "Thai digits on Kedmanee keyboard" in table
        assert "International digits on Pattajoti keyboard" in table
        assert "CURRENT" in table
        assert "OPTIMAL" in table

    def test_render_savings_analysis(self, sample_json_analysis_data):
        """Test savings analysis rendering."""
        # Add analysis_results with savings
        sample_json_analysis_data["analysis_results"] = {
            "average": {
                "savings_analysis": {
                    "intl_pattajoti": {
                        "description": "International digits on Pattajoti keyboard (optimal)",
                        "time_saved_minutes": 10.0,
                        "percentage_saved": 10.0,
                    }
                }
            }
        }

        renderer = ConsoleRenderer(sample_json_analysis_data)
        savings = renderer.render_savings_analysis()

        # Check structure
        assert "TIME SAVINGS COMPARED TO CURRENT STATE:" in savings
        assert "-" * 70 in savings
        assert "Alternative Scenario" in savings
        assert "Saved (min)" in savings
        assert "Saved (%)" in savings

        # Check data integration
        assert "International digits on Pattajoti keyboard" in savings
        assert "10.0" in savings

    def test_render_impact_projections(self, sample_json_analysis_data):
        """Test impact projections rendering."""
        # Add impact projections to sample data
        sample_json_analysis_data["impact_projections"] = {
            "per_document_savings_minutes": 10.0,
            "government_scale_projections": [
                {
                    "scale": "Small Ministry",
                    "annual_hours_saved": 1000,
                    "annual_cost_savings": 15000,
                },
                {
                    "scale": "Large Ministry",
                    "annual_hours_saved": 5000,
                    "annual_cost_savings": 75000,
                },
            ],
        }

        renderer = ConsoleRenderer(sample_json_analysis_data)
        projections = renderer.render_impact_projections()

        # Check structure
        assert "GOVERNMENT IMPACT PROJECTIONS:" in projections
        assert "-" * 70 in projections
        assert "Based on 10.0 minutes saved per document" in projections
        assert "Scale" in projections
        assert "Annual Hours" in projections
        assert "Annual Savings" in projections

        # Check data integration
        assert "Small Ministry" in projections
        assert "Large Ministry" in projections
        assert "1,000 hours" in projections
        assert "$15,000" in projections

    def test_render_recommendations(self, sample_json_analysis_data):
        """Test recommendations rendering."""
        # Add recommendations to sample data
        sample_json_analysis_data["recommendations"] = {
            "primary_recommendation": {"action": "Switch to international digits"},
            "implementation_steps": [
                "Update templates",
                "Train staf",
                "Monitor results",
            ],
            "benefits": [
                "Zero cost implementation",
                "Immediate impact",
                "Universal benefit",
                "Scales massively",
            ],
        }

        renderer = ConsoleRenderer(sample_json_analysis_data)
        recommendations = renderer.render_recommendations()

        # Check structure
        assert "RECOMMENDATIONS:" in recommendations
        assert "PRIMARY: Switch to international digits" in recommendations
        assert "Implementation steps:" in recommendations
        assert "Key benefits:" in recommendations

        # Check data integration
        assert "1. Update templates" in recommendations
        assert "2. Train staf" in recommendations
        assert "3. Monitor results" in recommendations
        assert "• Zero cost implementation" in recommendations
        assert "• Immediate impact" in recommendations
        assert "• Universal benefit" in recommendations

    def test_render_comprehensive(self, sample_json_analysis_data):
        """Test comprehensive console rendering."""
        # Add required data sections
        sample_json_analysis_data.update(
            {
                "analysis_results": {
                    "average": {
                        "scenarios": {
                            "thai_kedmanee": {
                                "description": "Thai digits on Kedmanee keyboard (current state)",
                                "total_cost_minutes": 100.0,
                                "total_cost_hours": 1.67,
                            }
                        },
                        "savings_analysis": {},
                        "optimal_scenario": "thai_kedmanee",
                    }
                },
                "impact_projections": {
                    "per_document_savings_minutes": 10.0,
                    "government_scale_projections": [],
                },
                "recommendations": {
                    "primary_recommendation": {"action": "Test action"},
                    "implementation_steps": [],
                    "benefits": [],
                },
            }
        )

        renderer = ConsoleRenderer(sample_json_analysis_data)
        comprehensive = renderer.render_comprehensive()

        # Should contain all sections
        sections = [
            "THAI NUMBERS TYPING COST ANALYSIS - SUMMARY",
            "TYPING COST BY SCENARIO:",
            "TIME SAVINGS COMPARED TO CURRENT STATE:",
            "GOVERNMENT IMPACT PROJECTIONS:",
            "RECOMMENDATIONS:",
        ]

        for section in sections:
            assert section in comprehensive, f"Missing section: {section}"

        # Should be substantial content
        assert len(comprehensive) > 1000
        assert comprehensive.startswith("=" * 80)
        assert comprehensive.endswith("=" * 80)

    def test_render_quick_stats(self, sample_json_analysis_data):
        """Test quick stats rendering."""
        renderer = ConsoleRenderer(sample_json_analysis_data)
        stats = renderer.render_quick_stats()

        # Check format
        assert stats.startswith("⚡ Quick result:")
        assert "minutes saved per document" in stats
        assert "efficiency gain" in stats

        # Check data integration
        key_findings = sample_json_analysis_data["key_findings"]
        assert str(key_findings["improvement"]["time_saved_minutes"]) in stats
        assert str(key_findings["improvement"]["efficiency_gain_percentage"]) in stats

    def test_render_json_summary(self, sample_json_analysis_data):
        """Test JSON summary rendering."""
        renderer = ConsoleRenderer(sample_json_analysis_data)
        json_summary = renderer.render_json_summary()

        # Should be valid JSON
        parsed = json.loads(json_summary)
        assert isinstance(parsed, dict)

        # Check required keys
        required_keys = [
            "time_saved_minutes",
            "efficiency_gain_percent",
            "current_time_minutes",
            "optimal_time_minutes",
            "root_cause",
        ]

        for key in required_keys:
            assert key in parsed, f"Missing JSON key: {key}"

        # Check data integration
        key_findings = sample_json_analysis_data["key_findings"]
        assert (
            parsed["time_saved_minutes"]
            == key_findings["improvement"]["time_saved_minutes"]
        )
        assert (
            parsed["efficiency_gain_percent"]
            == key_findings["improvement"]["efficiency_gain_percentage"]
        )


class TestConvenienceFunctions:
    """Test suite for convenience functions."""

    def test_render_json_to_markdown_with_output(
        self, sample_json_analysis_data, tmp_path
    ):
        """Test render_json_to_markdown with file output."""
        output_file = tmp_path / "test_report.md"

        result = render_json_to_markdown(sample_json_analysis_data, str(output_file))

        assert result == str(output_file)
        assert output_file.exists()

        # Verify content
        content = output_file.read_text(encoding="utf-8")
        assert "# Thai Numbers Typing Cost Analysis - Research Report" in content
        assert len(content) > 1000

    def test_render_json_to_markdown_without_output(self, sample_json_analysis_data):
        """Test render_json_to_markdown without file output."""
        result = render_json_to_markdown(sample_json_analysis_data)

        assert isinstance(result, str)
        assert "# Thai Numbers Typing Cost Analysis - Research Report" in result
        assert len(result) > 1000

    @pytest.mark.parametrize(
        "format_type,expected_content",
        [
            ("summary", "THAI NUMBERS TYPING COST ANALYSIS - SUMMARY"),
            ("quick", "⚡ Quick result:"),
            ("scenarios", "TYPING COST BY SCENARIO:"),
            ("json", "time_saved_minutes"),
            ("comprehensive", "THAI NUMBERS TYPING COST ANALYSIS - SUMMARY"),
        ],
    )
    def test_render_json_to_console_formats(
        self, sample_json_analysis_data, format_type, expected_content
    ):
        """Test render_json_to_console with different format types."""
        # Add required data for scenarios format
        if format_type == "scenarios":
            sample_json_analysis_data["analysis_results"] = {
                "average": {
                    "scenarios": {
                        "thai_kedmanee": {
                            "description": "Test scenario",
                            "total_cost_minutes": 100.0,
                            "total_cost_hours": 1.67,
                        }
                    },
                    "optimal_scenario": "thai_kedmanee",
                }
            }

        # Add required data for comprehensive format
        if format_type == "comprehensive":
            sample_json_analysis_data.update(
                {
                    "analysis_results": {
                        "average": {
                            "scenarios": {
                                "thai_kedmanee": {
                                    "description": "Test",
                                    "total_cost_minutes": 100.0,
                                    "total_cost_hours": 1.67,
                                }
                            },
                            "savings_analysis": {},
                            "optimal_scenario": "thai_kedmanee",
                        }
                    },
                    "impact_projections": {
                        "per_document_savings_minutes": 10.0,
                        "government_scale_projections": [],
                    },
                    "recommendations": {
                        "primary_recommendation": {"action": "Test"},
                        "implementation_steps": [],
                        "benefits": [],
                    },
                }
            )

        result = render_json_to_console(sample_json_analysis_data, format_type)

        assert expected_content in result
        assert isinstance(result, str)
        assert len(result) > 0


class TestMainFunctions:
    """Test suite for main function execution."""

    def test_markdown_renderer_main_with_args(
        self, sample_json_analysis_data, tmp_path, monkeypatch, capsys
    ):
        """Test markdown renderer main function with arguments."""
        # Create JSON input file
        json_file = tmp_path / "input.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(sample_json_analysis_data, f)

        output_file = tmp_path / "output.md"
        test_args = ["markdown_renderer.py", str(json_file), str(output_file)]
        monkeypatch.setattr("sys.argv", test_args)

        # Import and run main
        from renderers.markdown_renderer import main

        main()

        # Check output
        captured = capsys.readouterr()
        assert "Markdown report generated:" in captured.out
        assert str(output_file) in captured.out

        # Verify file was created
        assert output_file.exists()

    def test_markdown_renderer_main_default_output(
        self, sample_json_analysis_data, tmp_path, monkeypatch, capsys
    ):
        """Test markdown renderer main function with default output."""
        # Create JSON input file
        json_file = tmp_path / "input.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(sample_json_analysis_data, f)

        test_args = ["markdown_renderer.py", str(json_file)]
        monkeypatch.setattr("sys.argv", test_args)

        # Import and run main
        from renderers.markdown_renderer import main

        main()

        captured = capsys.readouterr()
        # Should contain timestamped filename pattern: analysis_report_YYYYMMDD_HHMMSS.md
        import re

        assert re.search(r"analysis_report_\d{8}_\d{6}\.md", captured.out)

    def test_console_renderer_main_with_args(
        self, sample_json_analysis_data, tmp_path, monkeypatch, capsys
    ):
        """Test console renderer main function with arguments."""
        # Create JSON input file
        json_file = tmp_path / "input.json"

        # Add required data for comprehensive format
        sample_json_analysis_data.update(
            {
                "analysis_results": {
                    "average": {
                        "scenarios": {
                            "thai_kedmanee": {
                                "description": "Test",
                                "total_cost_minutes": 100.0,
                                "total_cost_hours": 1.67,
                            }
                        },
                        "savings_analysis": {},
                        "optimal_scenario": "thai_kedmanee",
                    }
                },
                "impact_projections": {
                    "per_document_savings_minutes": 10.0,
                    "government_scale_projections": [],
                },
                "recommendations": {
                    "primary_recommendation": {"action": "Test"},
                    "implementation_steps": [],
                    "benefits": [],
                },
            }
        )

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(sample_json_analysis_data, f)

        test_args = ["console_renderer.py", str(json_file), "summary"]
        monkeypatch.setattr("sys.argv", test_args)

        # Import and run main
        from renderers.console_renderer import main

        main()

        captured = capsys.readouterr()
        assert "THAI NUMBERS TYPING COST ANALYSIS - SUMMARY" in captured.out

    def test_main_functions_insufficient_args(self, monkeypatch, capsys):
        """Test main functions with insufficient arguments."""
        test_args = ["renderer.py"]
        monkeypatch.setattr("sys.argv", test_args)

        # Test markdown renderer
        with pytest.raises(SystemExit) as exc_info:
            from renderers.markdown_renderer import main

            main()
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Usage:" in captured.out

        # Test console renderer
        capsys.readouterr()  # Clear previous output
        with pytest.raises(SystemExit) as exc_info:
            from renderers.console_renderer import main

            main()
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Usage:" in captured.out


class TestEdgeCases:
    """Test suite for edge cases and error conditions."""

    def test_markdown_renderer_with_missing_data(self):
        """Test markdown renderer with missing data sections."""
        minimal_data = {
            "metadata": {
                "generated_at": "2025-08-01T10:00:00.000000",
                "document_path": "test.txt",
                "tool_version": "1.0.0",
                "analysis_focus": "test focus",
                "document_stats": {
                    "total_characters": 100,
                    "total_digits": 10,
                    "digit_percentage": 10.0,
                },
            },
            "key_findings": {
                "current_state": {"time_minutes": 100.0, "time_hours": 1.67},
                "optimal_state": {"time_minutes": 90.0, "time_hours": 1.50},
                "improvement": {
                    "time_saved_minutes": 10.0,
                    "efficiency_gain_percentage": 10.0,
                    "root_cause": "SHIFT key",
                },
            },
            "research_questions": {},
            "impact_projections": {
                "per_document_savings_minutes": 10.0,
                "government_scale_projections": [],
            },
            "recommendations": {
                "primary_recommendation": {"action": "Test"},
                "implementation_steps": [],
                "benefits": [],
            },
        }

        renderer = MarkdownRenderer(minimal_data)

        # Should handle gracefully without crashing
        header = renderer._render_header()
        summary = renderer._render_executive_summary()

        assert isinstance(header, str)
        assert isinstance(summary, str)

    def test_console_renderer_with_missing_data(self):
        """Test console renderer with missing data sections."""
        minimal_data = {
            "metadata": {
                "document_path": "test.txt",
                "document_stats": {
                    "total_characters": 100,
                    "total_digits": 10,
                    "digit_percentage": 10.0,
                },
            },
            "key_findings": {
                "current_state": {"time_minutes": 100.0},
                "optimal_state": {"time_minutes": 90.0},
                "improvement": {
                    "time_saved_minutes": 10.0,
                    "efficiency_gain_percentage": 10.0,
                    "root_cause": "SHIFT key",
                },
            },
        }

        renderer = ConsoleRenderer(minimal_data)

        # Should handle gracefully without crashing
        summary = renderer.render_summary()
        quick_stats = renderer.render_quick_stats()

        assert isinstance(summary, str)
        assert isinstance(quick_stats, str)

    def test_unicode_content_handling(self, tmp_path):
        """Test that renderers handle Unicode content correctly."""
        unicode_data = {
            "metadata": {
                "generated_at": "2025-08-01T10:00:00.000000",
                "document_path": "ไฟล์ไทย.txt",  # Thai filename
                "tool_version": "1.0.0",
                "analysis_focus": "การวิเคราะห์ตัวเลขไทย",  # Thai text
                "document_stats": {
                    "total_characters": 100,
                    "total_digits": 10,
                    "digit_percentage": 10.0,
                },
            },
            "key_findings": {
                "current_state": {"time_minutes": 100.0, "time_hours": 1.67},
                "optimal_state": {"time_minutes": 90.0, "time_hours": 1.50},
                "improvement": {
                    "time_saved_minutes": 10.0,
                    "efficiency_gain_percentage": 10.0,
                    "root_cause": "การใช้ปุ่ม SHIFT สำหรับตัวเลขไทย",  # Thai text
                },
            },
            "research_questions": {},
            "impact_projections": {
                "per_document_savings_minutes": 10.0,
                "government_scale_projections": [],
            },
            "recommendations": {
                "primary_recommendation": {"action": "ใช้ตัวเลขสากล"},
                "implementation_steps": [],
                "benefits": [],
            },  # Thai text
        }

        # Test markdown renderer
        md_renderer = MarkdownRenderer(unicode_data)
        md_output = md_renderer.render_comprehensive_report()

        assert "ไฟล์ไทย.txt" in md_output
        assert "การวิเคราะห์ตัวเลขไทย" in md_output
        assert "การใช้ปุ่ม SHIFT สำหรับตัวเลขไทย" in md_output

        # Test saving with Unicode
        output_file = tmp_path / "unicode_test.md"
        md_renderer.save_to_file(md_output, str(output_file))

        # Verify Unicode is preserved
        saved_content = output_file.read_text(encoding="utf-8")
        assert "ไฟล์ไทย.txt" in saved_content

        # Test console renderer
        console_renderer = ConsoleRenderer(unicode_data)
        console_output = console_renderer.render_summary()

        assert "ไฟล์ไทย.txt" in console_output
        assert "การใช้ปุ่ม SHIFT สำหรับตัวเลขไทย" in console_output


# Pytest markers
pytestmark = [pytest.mark.unit]
