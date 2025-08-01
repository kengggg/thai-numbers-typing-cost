"""
Test configuration and fixtures for Thai Numbers Typing Cost Analysis tests.
"""

import pytest
import tempfile
import json
from pathlib import Path
from typing import Dict, Any
import sys
import os

# Add src directory to path for imports
test_dir = Path(__file__).parent
project_root = test_dir.parent
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

from models.text_analyzer import TextAnalyzer
from models.keyboard_layouts import KedmaneeLayout, PattajotiLayout
from calculators.typing_cost_calculator import TypingCostCalculator
from generators.json_analysis_generator import JSONAnalysisGenerator


@pytest.fixture(scope="session")
def project_root_path():
    """Get the project root path."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def test_data_dir(project_root_path):
    """Get the test data directory path."""
    return project_root_path / "tests" / "test_data"


@pytest.fixture(scope="session")
def sample_thai_text():
    """Sample Thai text with mixed content for testing."""
    return """พระราชบัญญัติรัฐธรรมนูญแห่งราชอาणาจักรไทย พุทธศักราช ๒๕๖๐
    
เนื่องในมงคลวาร เป็นปีที่ ๒ ในรัชกาลปัจจุบัน

ข้อมูลเพิ่มเติม:
- ปี ๒๕๖๐ เป็นปีสำคัญ
- มีการใช้ตัวเลขไทย ๑๒๓๔๕
- มีการใช้ตัวเลขอาหรับ 67890
- วันที่ ๖ เมษายน เป็นวันสำคัญ

รวม ๑๐ หน้า ในเล่มที่ ๑๓๔ ของประกาศ
"""


@pytest.fixture
def sample_thai_text_file(tmp_path, sample_thai_text):
    """Create a temporary file with sample Thai text."""
    test_file = tmp_path / "sample_thai.txt"
    test_file.write_text(sample_thai_text, encoding='utf-8')
    return str(test_file)


@pytest.fixture
def empty_text_file(tmp_path):
    """Create an empty text file for testing edge cases."""
    test_file = tmp_path / "empty.txt"
    test_file.write_text("", encoding='utf-8')
    return str(test_file)


@pytest.fixture
def text_analyzer(sample_thai_text_file):
    """Create a TextAnalyzer instance with sample data."""
    return TextAnalyzer(sample_thai_text_file)


@pytest.fixture
def kedmanee_layout():
    """Create a KedmaneeLayout instance."""
    return KedmaneeLayout()


@pytest.fixture
def pattajoti_layout():
    """Create a PattajotiLayout instance."""
    return PattajotiLayout()


@pytest.fixture
def typing_cost_calculator(sample_thai_text_file):
    """Create a TypingCostCalculator instance with sample data."""
    return TypingCostCalculator(sample_thai_text_file, base_keystroke_time=0.28)


@pytest.fixture
def json_analysis_generator(sample_thai_text_file):
    """Create a JSONAnalysisGenerator instance with sample data."""
    return JSONAnalysisGenerator(sample_thai_text_file)


@pytest.fixture
def typist_profiles():
    """Standard typist profiles for testing."""
    return {
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


@pytest.fixture
def thai_digits():
    """List of Thai digits for testing."""
    return ['๐', '๑', '๒', '๓', '๔', '๕', '๖', '๗', '๘', '๙']


@pytest.fixture
def international_digits():
    """List of international digits for testing."""
    return ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


@pytest.fixture
def sample_json_analysis_data():
    """Sample JSON analysis data structure for testing renderers."""
    return {
        "metadata": {
            "generated_at": "2025-08-01T10:00:00.000000",
            "tool_version": "3.0.0",
            "document_path": "sample_thai.txt",
            "document_stats": {
                "total_characters": 500,
                "total_digits": 25,
                "digit_percentage": 5.0,
                "thai_digits": 20,
                "international_digits": 5
            },
            "analysis_focus": "Direct comparison of Thai digits vs International digits typing costs"
        },
        "document_analysis": {
            "digit_distribution": {
                "thai_digits": {
                    "๑": 8,
                    "๒": 5,
                    "๓": 4,
                    "๔": 3
                },
                "most_frequent_digit": "๑",
                "least_frequent_digit": "๔"
            },
            "number_sequences": {
                "total_sequences": 12,
                "thai_sequences": 10,
                "average_thai_length": 1.8
            },
            "sample_contexts": [
                {
                    "number": "๑",
                    "type": "thai",
                    "context": "เมื่อวันที่ ๑ มกราคม พ.ศ. ๒๕๖๐"
                }
            ]
        },
        "typist_profiles": {
            "average": {
                "name": "Average Non-secretarial",
                "keystroke_time": 0.28,
                "description": "Average office worker, moderate typing skills (default)"
            }
        },
        "analysis_results": {
            "average": {
                "scenarios": {
                    "thai_kedmanee": {
                        "description": "Thai digits on Kedmanee keyboard (current state)",
                        "total_cost_minutes": 15.5,
                        "total_cost_hours": 0.26,
                        "keyboard_layout": "kedmanee"
                    },
                    "intl_pattajoti": {
                        "description": "International digits on Pattajoti keyboard (optimal)",
                        "total_cost_minutes": 14.0,
                        "total_cost_hours": 0.23,
                        "keyboard_layout": "pattajoti"
                    }
                },
                "comparisons": {
                    "time_saved_minutes": 1.5,
                    "efficiency_gain_percentage": 9.7,
                    "optimal_scenario": "intl_pattajoti"
                }
            }
        },
        "research_questions": {
            "q1": {
                "question": "What is the typing cost of Thai digits on Kedmanee keyboard?",
                "answer": "15.5 minutes",
                "details": {
                    "why_higher_cost": "Thai digits require SHIFT key",
                    "total_digits_typed": 20
                }
            },
            "q2": {
                "question": "What is the typing cost of international digits on Kedmanee keyboard?",
                "answer": "15.0 minutes", 
                "details": {
                    "time_saved_vs_thai": 0.5,
                    "percentage_saved": 3.2,
                    "why_faster": "No SHIFT key required"
                }
            },
            "q3": {
                "question": "What is the typing cost of Thai digits on Pattajoti keyboard?",
                "answer": "14.2 minutes",
                "details": {
                    "time_saved_vs_kedmanee": 1.3,
                    "percentage_saved": 8.4,
                    "why_faster": "Pattajoti eliminates SHIFT requirement for Thai digits"
                }
            },
            "q4": {
                "question": "What is the typing cost of international digits on Pattajoti keyboard?",
                "answer": "14.0 minutes",
                "details": {
                    "time_saved_vs_current": 1.5,
                    "percentage_saved": 9.7,
                    "status": "Most efficient configuration"
                }
            },
            "q5": {
                "question": "What is the 'LOST' productivity cost of using Thai digits?",
                "answer": "Clear and measurable inefficiency",
                "details": {
                    "per_document_loss_minutes": 1.5,
                    "efficiency_loss_percentage": 9.7,
                    "root_cause": "SHIFT penalty doubles typing cost for every Thai digit",
                    "simple_solution": "Switch to international digits (0-9)"
                }
            }
        },
        "key_findings": {
            "current_state": {
                "scenario": "Thai digits on Kedmanee keyboard",
                "time_minutes": 15.5
            },
            "optimal_state": {
                "scenario": "International digits on Pattajoti keyboard",
                "time_minutes": 14.0
            },
            "improvement": {
                "time_saved_minutes": 1.5,
                "efficiency_gain_percentage": 9.7,
                "root_cause": "Thai digits require SHIFT key on Kedmanee layout, doubling typing cost"
            }
        },
        "impact_projections": {
            "per_document_savings_minutes": 1.5,
            "per_document_savings_hours": 0.025,
            "government_scale_projections": [
                {
                    "scale": "Small Ministry",
                    "docs_per_day": 50,
                    "annual_hours_saved": 325,
                    "annual_cost_savings": 4875
                }
            ],
            "assumptions": {
                "working_days_per_year": 250,
                "hourly_labor_cost": 15
            }
        },
        "recommendations": {
            "primary": "Standardize on international digits (0-9) for all Thai government documents",
            "implementation_steps": [
                "Update document templates to use international digits",
                "Brief staff training on the change (< 1 hour)",
                "Monitor results and measure time savings",
                "Scale government-wide based on pilot success"
            ],
            "benefits": [
                "Zero cost: Uses existing keyboards and systems",
                "Universal benefit: Helps every typist regardless of skill level",
                "Immediate impact: 1.5+ minutes saved per document from day one"
            ]
        }
    }


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary output directory for testing."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    (output_dir / "reports").mkdir()
    (output_dir / "analysis").mkdir()
    return str(output_dir)


@pytest.fixture
def mock_current_time():
    """Mock current time for consistent testing."""
    from freezegun import freeze_time
    return freeze_time("2025-08-01 10:00:00")


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests for individual components")
    config.addinivalue_line("markers", "integration: Integration tests across components")
    config.addinivalue_line("markers", "validation: Validation tests for accuracy")
    config.addinivalue_line("markers", "slow: Tests that take longer to run")
    config.addinivalue_line("markers", "requires_data: Tests requiring test data files")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Add unit marker to unit tests
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Add integration marker to integration tests
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Add validation marker to validation tests
        if "validation" in str(item.fspath):
            item.add_marker(pytest.mark.validation)