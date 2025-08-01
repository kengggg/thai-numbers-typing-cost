# Thai Numbers Typing Cost Comparison

[![Tests](https://github.com/kengggg/thai-numbers-typing-cost/actions/workflows/ci.yml/badge.svg)](https://github.com/kengggg/thai-numbers-typing-cost/actions/workflows/ci.yml)

A focused comparison tool that automatically generates typing time comparisons between Thai digits (๐-๙) and international digits (0-9) across different keyboard layouts and typist skill levels.

## Project Overview

This tool automatically analyzes all combinations of digit types, keyboard layouts, and typist profiles to generate comprehensive comparison tables. It's designed for quick, straightforward analysis without complex configuration options.

## Project Structure

```
thai-numbers-typing-cost/
├── src/                          # Python source code
│   ├── models/                   # Data models and analysis classes
│   │   ├── keyboard_layouts.py   # Kedmanee & Pattajoti keyboard models (67+ & 78+ keys)
│   │   ├── text_analyzer.py      # Unicode-aware Thai text analysis
│   │   └── typist_profiles.py    # Shared typist skill level definitions
│   ├── calculators/              # Core calculation logic
│   │   └── typing_cost_calculator.py # Simplified cost model (base time + SHIFT penalty)
│   ├── generators/               # JSON data generation
│   │   └── json_analysis_generator.py # Comprehensive analysis data structures
│   └── main.py                   # CLI application with simplified markdown rendering
├── tests/                        # Comprehensive test suite (204 tests, 100% pass rate)
│   ├── unit/                     # Unit tests for all components
│   ├── integration/              # End-to-end workflow tests
│   ├── validation/               # Keyboard layout accuracy validation
│   └── conftest.py               # Test fixtures and configuration
├── output/                       # Generated analysis files
│   ├── analysis.json            # Comprehensive analysis data
│   └── comparison_report_*.md   # Timestamped comparison tables
├── data/                         # Input documents and reference materials
│   ├── thai-con.txt             # 2017 Thai Constitution (271 chars, 25 digits)
│   ├── TIS_820-2535,_Figure_2.jpg # Official Kedmanee layout reference
│   └── Pattajoti.gif            # Official Pattajoti layout reference
├── pytest.ini                   # Test configuration
├── tox.ini                       # Multi-environment testing (Python 3.9, 3.11, 3.12)
├── requirements.txt              # Production dependencies (minimal - standard library only)
├── requirements-test.txt         # Development and testing dependencies
└── PRD.txt                       # Project requirements document
```

## Typist Skill Levels

The analysis supports four validated typist profiles based on research data:

| Profile | Keystroke Time | Description | Usage |
|---------|----------------|-------------|-------|
| **expert** | 0.12s | Professional typist (~90 WPM), touch typing mastery | High-speed document processing |
| **skilled** | 0.20s | Experienced office worker, good typing skills | Standard office environments |
| **average** | 0.28s | Average office worker, moderate typing skills | Default baseline (most common) |
| **worst** | 1.2s | Hunt-and-peck typist, very slow typing | Conservative estimates |

## Quick Start

### Usage

The tool automatically analyzes all scenarios and generates both JSON data and comparison tables:

```bash
cd src

# Analyze document - automatically generates all comparisons
python main.py ../data/thai-con.txt

# Show available typist profiles
python main.py --list-typists
```

**That's it!** The tool automatically:
- Analyzes all 4 typist profiles (expert, skilled, average, worst)
- Compares all 4 scenarios (Thai/Intl digits × Kedmanee/Pattajoti keyboards)
- Generates comprehensive JSON data (`output/analysis.json`)
- Creates comparison table markdown report (`output/comparison_report_TIMESTAMP.md`)

### Output Files

Every analysis run creates timestamped files:

- **JSON**: `output/analysis.json` (comprehensive analysis data)
- **Markdown**: `output/comparison_report_YYYYMMDD_HHMMSS.md` (e.g., `comparison_report_20250801_120606.md`)

The markdown report contains simple comparison tables showing typing times for all scenarios:

| Typist Profile | Thai + Kedmanee | Intl + Kedmanee | Thai + Pattajoti | Intl + Pattajoti |
|----------------|-----------------|-----------------|------------------|------------------|
| Expert         | 472.4 min       | 467.7 min       | 397.4 min        | 397.4 min        |
| Skilled        | 787.3 min       | 779.6 min       | 662.4 min        | 662.4 min        |
| Average        | 1102.2 min      | 1091.4 min      | 927.3 min        | 927.3 min        |
| Worst          | 4723.9 min      | 4677.4 min      | 3974.2 min       | 3974.2 min       |

### Testing

```bash
# Run the full test suite (204 tests)
python -m pytest

# Code quality checks
tox -e format                # Check formatting
tox -e lint                  # Check linting  
```

## What The Tool Shows

The tool generates comparison tables showing typing times in minutes for each combination:

### Four Scenarios Compared
- **Thai + Kedmanee**: Thai digits (๐-๙) on Kedmanee keyboard
- **Intl + Kedmanee**: International digits (0-9) on Kedmanee keyboard  
- **Thai + Pattajoti**: Thai digits (๐-๙) on Pattajoti keyboard
- **Intl + Pattajoti**: International digits (0-9) on Pattajoti keyboard

### Four Typist Profiles Analyzed
- **Expert**: 0.12s per keystroke (professional typist)
- **Skilled**: 0.2s per keystroke (experienced office worker)
- **Average**: 0.28s per keystroke (typical office worker)
- **Worst**: 1.2s per keystroke (hunt-and-peck typist)

### Key Insight
Thai digits on Kedmanee require SHIFT key (2x penalty), making them consistently slower than other combinations.

## Technical Details

### How It Works
- **Typing Model**: Base keystroke time × SHIFT penalty (2x for Thai digits on Kedmanee)
- **Keyboard Layouts**: Validated against official TIS 820-2535 (Kedmanee) and Pattajoti standards
- **Document Analysis**: Unicode-aware Thai text processing
- **Output Format**: Clean comparison tables without cost calculations

### Dependencies
- **Python 3.8+** (uses standard library only)
- **Development**: pytest, black, isort, flake8 for testing and code quality

### Architecture
- **JSON-first**: Generates comprehensive data, renders simple comparison tables
- **204 tests**: Full test coverage with CI/CD integration
- **Multi-platform**: Tested on Python 3.9, 3.11, 3.12

## Contributing

For development:
```bash
pip install -r requirements-test.txt
python -m pytest                 # Run tests
tox -e format && tox -e lint     # Check code quality
```