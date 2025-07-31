# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a research analysis tool that quantifies the typing cost difference between Thai digits (๐-๙) and international digits (0-9) in Thai government documents. The analysis uses the 2017 Thai Constitution as a benchmark to compare typing efficiency across different keyboard layouts (Kedmanee vs Pattajoti) and typist skill levels.

## Core Architecture

### Multi-Layer Analysis Pipeline
The codebase follows a layered architecture with clear separation of concerns:

1. **Models** (`src/models/`): Core data structures and business logic
   - `keyboard_layouts.py`: Implements `KedmaneeLayout` and `PattajotiLayout` classes with detailed key mappings (67+ and 78+ keys respectively) based on official TIS 820-2535 and Pattajoti standards
   - `text_analyzer.py`: Analyzes Thai documents to extract digit statistics and contexts

2. **Calculators** (`src/calculators/`): Computation engine
   - `typing_cost_calculator.py`: Core analysis engine that runs 4 scenarios (Thai/International digits × Kedmanee/Pattajoti layouts) and calculates typing costs with digit conversion capabilities

3. **Reporters** (`src/reporters/`): Output generation
   - `markdown_reporter.py`: Generates comprehensive markdown reports with date/time naming (e.g., `Thai_Numbers_Typing_Cost_Analysis_Report_20250731_115551.md`)

### Key Design Patterns

**Keyboard Layout Modeling**: Uses inheritance with `ThaiKeyboardLayout` base class, where each key is modeled as a `KeyInfo` object containing:
- SHIFT requirements (critical: Thai digits require SHIFT on Kedmanee but not on Pattajoti)
- Ergonomic factors (finger position, hand, row difficulty multipliers)
- Character mappings validated against official keyboard layout images

**Dual Calculation Modes**: The system supports both "weighted" (includes ergonomic difficulty multipliers) and "unweighted" (conservative baseline using only SHIFT penalty) calculations for research flexibility.

**Typist Profile System**: Four predefined profiles (expert: 0.12s, skilled: 0.20s, average: 0.28s, worst: 1.2s keystroke times) representing different skill levels.

## Common Commands

### Quick Analysis (Recommended)
```bash
# From project root - generates markdown reports automatically
python run_analysis.py --compare-all                    # All typist levels
python run_analysis.py --compare-weights                # Weighted vs unweighted
python run_analysis.py --compare-all --compare-weights  # Full comprehensive analysis
```

### Advanced Analysis
```bash
cd src
python main.py ../data/thai-con.txt                           # Basic analysis (average typist, weighted)
python main.py ../data/thai-con.txt --typist expert --no-weights  # Expert with unweighted mode
python main.py ../data/thai-con.txt --compare-weights         # Compare calculation modes
python main.py ../data/thai-con.txt --keyboard-only           # Keyboard comparison only
python main.py ../data/thai-con.txt --text-only               # Text analysis only
```

### Validation and Testing
```bash
cd src
python validation_tests.py                            # Run 4 validation tests (finger positions, SHIFT requirements, etc.)
python -c "from models.keyboard_layouts import *; compare_layouts()"  # Quick keyboard comparison
```

## Critical Implementation Details

### SHIFT Penalty Logic
The core research finding depends on the SHIFT penalty implementation:
- Thai digits on Kedmanee require SHIFT → 2x typing cost
- Thai digits on Pattajoti do NOT require SHIFT → 1x typing cost
- This creates the fundamental efficiency difference measured in the research

### Digit Conversion System
The `TypingCostCalculator` includes bidirectional conversion between Thai and international digits:
```python
thai_to_intl_map = {'๐': '0', '๑': '1', '๒': '2', ...}
```
This enables the 4-scenario analysis by converting document content on-the-fly.

### Output Structure
- Text files: `output/analysis/` and `output/reports/`
- Markdown reports: `output/Thai_Numbers_Typing_Cost_Analysis_Report_{timestamp}.md`
- Reports auto-generate for `--compare-all` or `--compare-weights` unless `--no-markdown` is specified

### Research Context
The analysis answers 5 specific research questions from `PRD.txt` about typing costs, with the key finding being a 3.2% efficiency gain (weighted mode) or 10.5% (unweighted mode) by switching from Thai digits on Kedmanee to international digits on Pattajoti layouts.

## Data Dependencies

- **Primary Document**: `data/thai-con.txt` (2017 Thai Constitution - 197,482 characters, 2,323 digits)
- **Keyboard References**: `data/TIS_820-2535,_Figure_2.jpg` (Kedmanee), `data/Pattajoti.gif` (Pattajoti)
- **Validation**: Models verified against these official keyboard layout images

## Development Notes

When modifying keyboard layouts, always run `python validation_tests.py` to ensure:
1. Finger position assignments match standard touch typing
2. SHIFT requirements are correctly implemented
3. Pattajoti digit order is correct (๒๓๔๕๗๘๙๐๑๖)
4. Character coverage is comprehensive

The codebase uses only Python standard library (no external dependencies) and is designed for Python 3.7+.