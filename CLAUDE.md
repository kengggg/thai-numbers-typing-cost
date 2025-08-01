# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a focused comparison tool that automatically generates typing time comparisons between Thai digits (๐-๙) and international digits (0-9) across different keyboard layouts and typist skill levels. The tool is designed for simplicity with automatic analysis of all scenarios.

## Current Architecture (v4.0 - Simplified)

### Core Components
1. **Models** (`src/models/`): Core data structures
   - `keyboard_layouts.py`: Kedmanee and Pattajoti keyboard layouts (validated against official standards)
   - `text_analyzer.py`: Unicode-aware Thai text processing
   - `typist_profiles.py`: Four typist skill levels (expert/skilled/average/worst)

2. **Calculators** (`src/calculators/`): Typing cost computation
   - `typing_cost_calculator.py`: Simple model with SHIFT penalty (2x for Thai digits on Kedmanee)

3. **Generators** (`src/generators/`): JSON data generation
   - `json_analysis_generator.py`: Comprehensive analysis data for all scenarios

4. **Main** (`src/main.py`): Simplified CLI that automatically:
   - Analyzes all 4 typist profiles
   - Compares all 4 scenarios (Thai/Intl digits × Kedmanee/Pattajoti)
   - Generates JSON and comparison table markdown

### Simplified Architecture Principles

**Automatic Analysis**: No complex options - always analyzes everything:
- All typist profiles automatically included
- All keyboard/digit combinations compared
- Both JSON and markdown output generated

**Clean Output Format**: Simple comparison tables showing typing times:
- No cost calculations or research narrative
- Raw data in easy-to-read table format
- Timestamped files to prevent overwrites

**Robust Testing**: 250 test cases covering:
- **Unit tests**: All core components
- **Integration tests**: Simplified CLI workflows
- **Validation tests**: Keyboard layout accuracy

## Common Commands

### Simplified CLI (Only Two Commands)
```bash
cd src

# Main usage - automatically analyzes all scenarios and generates all outputs
python main.py ../data/thai-con.txt

# Utility command - show available typist profiles
python main.py --list-typists
```

**That's it!** The tool automatically:
- Analyzes all 4 typist profiles (expert, skilled, average, worst)
- Compares all 4 scenarios (Thai/Intl digits × Kedmanee/Pattajoti keyboards)
- Generates comprehensive JSON data (`output/analysis.json`)
- Creates comparison table markdown (`output/comparison_report_TIMESTAMP.md`)

### Testing and Development (250 Tests)
```bash
# Run full test suite
pytest                                   # All 250 tests

# Code quality checks
tox -e format                            # Check formatting (black + isort)
tox -e format-fix                        # Auto-fix formatting
tox -e lint                              # Check linting (flake8)
tox                                      # Test Python 3.9, 3.11, 3.12
```

## Key Implementation Details

### SHIFT Penalty Logic (Core Finding)
The main difference between scenarios is the SHIFT key requirement:
- **Thai digits on Kedmanee require SHIFT** → 2x typing cost penalty
- **Thai digits on Pattajoti do NOT require SHIFT** → 1x typing cost
- **International digits on both layouts** → 1x typing cost (no SHIFT needed)

### Typist Profiles
Four skill levels defined in `src/models/typist_profiles.py`:
- **expert**: 0.12s per keystroke (90 WPM professional)
- **skilled**: 0.20s per keystroke (experienced office worker)  
- **average**: 0.28s per keystroke (typical office worker - default)
- **worst**: 1.2s per keystroke (hunt-and-peck typist)

### Output Files
- **JSON**: `output/analysis.json` (comprehensive analysis data)
- **Markdown**: `output/comparison_report_YYYYMMDD_HHMMSS.md` (timestamped comparison tables)

### Simple Comparison Table Format
The markdown output shows raw timing data in clean tables:
```markdown
| Typist Profile | Thai + Kedmanee | Intl + Kedmanee | Thai + Pattajoti | Intl + Pattajoti |
|----------------|-----------------|-----------------|------------------|------------------|
| Expert         | 472.4 min       | 467.7 min       | 397.4 min        | 397.4 min        |
| Skilled        | 787.3 min       | 779.6 min       | 662.4 min        | 662.4 min        |
| Average        | 1102.2 min      | 1091.4 min      | 927.3 min        | 927.3 min        |
| Worst          | 4723.9 min      | 4677.4 min      | 3974.2 min       | 3974.2 min       |
```

## Development Notes

### Testing
- **250 tests** covering all components with 100% pass rate
- **Validation tests** ensure keyboard layouts match official standards
- **Integration tests** verify simplified CLI workflow

### Code Quality Requirements
- **Standard library only** (no external dependencies for core functionality)
- **Type hints required** for all new functions
- **All tests must pass** before changes are accepted
- **UTF-8 encoding** essential for Thai character processing

### Making Changes
1. **Run tests first**: `pytest` (ensure all 250 tests pass)
2. **Make changes**: Follow existing patterns and conventions
3. **Validate changes**: `pytest tests/validation/ -v` for keyboard modifications
4. **Check code quality**: `tox -e format && tox -e lint`
5. **Update docs**: README.md and CLAUDE.md if user-facing changes

This is a focused, reliable comparison tool designed for simplicity and automatic comprehensive analysis.