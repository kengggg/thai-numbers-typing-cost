# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive research analysis tool that quantifies the typing cost difference between Thai digits (๐-๙) and international digits (0-9) in Thai government documents. The system has evolved into a mature JSON-first architecture with reliable testing infrastructure (264 tests, 100% pass rate) and comprehensive validation against official keyboard standards.

## Current Architecture (v3.0+)

### JSON-First Architecture
The system implements complete data/presentation separation with robust testing:

1. **Models** (`src/models/`): Core data structures and analysis logic
   - `keyboard_layouts.py`: `KedmaneeLayout` (67+ keys) and `PattajotiLayout` (78+ keys), validated against TIS 820-2535 and Pattajoti standards
   - `text_analyzer.py`: Unicode-aware Thai document analysis with context extraction (80-character window)
   - `typist_profiles.py`: Shared typist skill level definitions (expert/skilled/average/worst)

2. **Calculators** (`src/calculators/`): Simplified computation engine
   - `typing_cost_calculator.py`: Clean cost model focused on SHIFT penalty (2x for Thai digits on Kedmanee) with bidirectional digit conversion

3. **Generators** (`src/generators/`): Comprehensive JSON data generation  
   - `json_analysis_generator.py`: Structured analysis data with metadata, document analysis, research questions, recommendations, and impact projections

4. **Renderers** (`src/renderers/`): Multi-format output rendering
   - `markdown_renderer.py`: JSON-to-markdown with focused research reports  
   - `console_renderer.py`: JSON-to-console with multiple output formats (summary, quick, scenarios, comprehensive)

### Key Architectural Decisions (Current State)

**Simplified Cost Model**: Clean research-focused approach using only:
- Base keystroke time (0.28s default, varying by typist skill level)
- SHIFT penalty (2x cost for Thai digits on Kedmanee layout only)
- Removed ergonomic multipliers for cleaner academic presentation

**JSON-First Workflow**: 
- Generate structured analysis data as portable JSON
- Render to multiple formats (markdown, console) from same data source
- Enables data/presentation separation and comprehensive testing

**Comprehensive Testing**: 264 test cases (100% pass rate):
- **Unit tests** (185): All core components individually tested
- **Integration tests** (54): End-to-end CLI workflows and JSON architecture
- **Validation tests** (25): Keyboard layout accuracy against official standards

**Shared Modules**: `typist_profiles.py` resolves circular imports and centralizes skill level definitions

## Common Commands

### Modern JSON-First Workflow (Primary)
```bash
# Generate comprehensive JSON analysis (recommended approach)
cd src
python main.py ../data/thai-con.txt --output-json analysis.json --compare-all

# Render to multiple formats from same JSON data
python main.py --render-from-json analysis.json --format markdown
python main.py --render-from-json analysis.json --format console

# Direct format generation (combines generation + rendering)
python main.py ../data/thai-con.txt --format markdown --compare-all
python main.py ../data/thai-con.txt --format console --typist expert
```

### CLI Workflow Options (Simplified)
```bash
cd src
python main.py ../data/thai-con.txt                        # Basic analysis (average typist)
python main.py ../data/thai-con.txt --compare-all          # All typist skill levels
python main.py ../data/thai-con.txt --format markdown      # Generate focused research report
python main.py ../data/thai-con.txt --typist expert        # Specific typist analysis
python main.py --list-typists                              # Show available profiles
```

### Testing and Validation (264 Tests, 100% Pass Rate)
```bash
# Comprehensive test suite
pytest                                    # Full test suite (264 tests)
pytest tests/unit/                        # Unit tests (185 tests)
pytest tests/integration/                 # Integration tests (54 tests)
pytest tests/validation/                  # Validation tests (25 tests)

# Test with coverage and quality assurance
pytest --cov=src --cov-report=html --cov-fail-under=90
pytest --cov=src --cov-report=term-missing

# Multi-environment testing (simplified)
tox                                       # Test Python 3.9, 3.11, 3.12

# Code quality (minimal set)
tox -e format                             # Check code formatting (black + isort)
tox -e format-fix                         # Auto-fix code formatting
tox -e lint                               # Basic code linting (flake8)
```

## Critical Implementation Details

### SHIFT Penalty Logic (Core Research Finding)
The fundamental research discovery depends on accurate SHIFT penalty implementation:
- **Thai digits on Kedmanee require SHIFT** → 2x typing cost penalty
- **Thai digits on Pattajoti do NOT require SHIFT** → 1x typing cost (normal)
- **International digits on both layouts** → 1x typing cost (no SHIFT needed)
- This creates the measurable 15.8% efficiency difference driving policy recommendations

### Digit Conversion System  
The `TypingCostCalculator` includes comprehensive bidirectional mapping:
```python
thai_to_intl_map = {'๐': '0', '๑': '1', '๒': '2', ...}
intl_to_thai_map = {'0': '๐', '1': '๑', '2': '๒', ...}
```
This enables the 4-scenario analysis framework: (Thai/Intl digits) × (Kedmanee/Pattajoti layouts)

### Typist Profiles (Shared Module)
Centralized in `src/models/typist_profiles.py` to resolve circular imports:
- **expert**: 0.12s (90 WPM professional typist)
- **skilled**: 0.20s (experienced office worker)  
- **average**: 0.28s (moderate typing skills - default baseline)
- **worst**: 1.2s (hunt-and-peck typist - conservative estimates)

### Output Structure and File Management
- **JSON files**: Structured analysis data for portability and reprocessing
- **Markdown reports**: Automatically timestamped (format: `analysis_report_YYYYMMDD_HHMMSS.md`) to prevent overwrites and enable historical tracking
- **Console output**: Multiple formats (summary, quick, scenarios, comprehensive)
- **Output directories**: `output/analysis/` and `output/reports/` (cleaned for fresh runs)
- **Timestamp extraction**: Filenames use analysis generation time from JSON metadata for consistency

### Research Context and Findings
The analysis answers 5 specific research questions from `PRD.txt`:
1. **Q1-Q4**: Typing costs for each scenario (Thai/Intl × Kedmanee/Pattajoti)
2. **Q5**: Quantified "LOST" productivity cost (0.2 minutes per document, 15.8% efficiency loss)

**Key Finding**: 15.8% efficiency gain achievable by switching from Thai digits on Kedmanee to Thai digits on Pattajoti (OR international digits on either layout).

## Data Dependencies and Validation

### Primary Resources
- **Benchmark Document**: `data/thai-con.txt` (2017 Thai Constitution - 271 characters, 25 digits)
- **Keyboard References**: 
  - `data/TIS_820-2535,_Figure_2.jpg` (Official Kedmanee layout)
  - `data/Pattajoti.gif` (Official Pattajoti layout)
- **Visual Validation**: Keyboard models verified against these official images

### Testing Quality Assurance
- **264 comprehensive test cases** with 100% pass rate (validated via `pytest --collect-only`)
- **Cross-validation**: Multiple test approaches ensure consistent results
- **Standard compliance**: Adherence to Thai keyboard layout standards (TIS 820-2535)
- **Unicode validation**: Proper Thai character recognition and processing
- **Performance testing**: Scalability validation with large documents

## Development Notes and Best Practices

### Keyboard Layout Modifications
When modifying keyboard layouts in `src/models/keyboard_layouts.py`:
1. **Run validation tests**: `pytest tests/validation/ -v` (25 validation tests)
2. **Verify finger assignments**: Must match standard touch typing practices
3. **Confirm SHIFT requirements**: Critical for research accuracy
4. **Check Pattajoti digit order**: Must be correct sequence (๒๓๔๕๗๘๙๐๑๖)  
5. **Validate character coverage**: Ensure comprehensive Thai character support

### Code Quality Standards
- **No external dependencies**: Uses only Python standard library for core functionality
- **Type hints required**: All new functions must include proper type annotations
- **Testing requirement**: All changes must maintain 100% test pass rate
- **Unicode support**: UTF-8 encoding essential for Thai character processing
- **Documentation updates**: User-facing changes require README.md/CLAUDE.md updates

### Testing and Validation Workflow
```bash
# Before making changes - verify current state
pytest                                    # All 264 tests should pass

# After making changes - comprehensive validation  
pytest tests/validation/ -v              # Keyboard layout accuracy
pytest tests/unit/ -v                    # Component functionality
pytest tests/integration/ -v             # End-to-end workflows
pytest --cov=src --cov-report=term-missing # Coverage verification

# Code quality and consistency
```

### Common Development Tasks

#### Adding New Features
1. **Create tests first**: Follow TDD approach for new functionality
2. **Update typist profiles**: Modify `src/models/typist_profiles.py` if needed
3. **JSON schema**: Ensure new data fits existing JSON structure
4. **Multi-format rendering**: Update both markdown and console renderers
5. **Documentation**: Update README.md and CLAUDE.md with new capabilities

#### Debugging Analysis Issues
1. **Check test data**: Verify `data/thai-con.txt` content and encoding
2. **Validate JSON output**: Use `python main.py --format json` for structured debugging
3. **Test individual components**: Use `pytest tests/unit/test_[component].py -v`
4. **Verify keyboard mappings**: Check character coverage in validation tests

#### Performance Optimization
1. **Test current performance**: Run the full test suite
2. **Profile memory usage**: Large document processing validation
3. **Test multi-environment**: `tox` for Python 3.9, 3.11, 3.12 compatibility
4. **Validate Unicode handling**: Ensure efficient Thai character processing

## Project Maturity Indicators

### Quality Metrics
- **264 test cases** with 100% pass rate (reliable testing)
- **Multi-environment support**: Python 3.9, 3.11, 3.12 across operating systems
- **Comprehensive validation**: Official keyboard standard compliance

### Architecture Maturity
- **Clean separation of concerns**: Models, calculators, generators, renderers
- **Portable data format**: JSON-first approach enables integration
- **Extensive error handling**: Graceful degradation and fault tolerance
- **Modular design**: Independent components with clear interfaces
- **Documentation completeness**: README.md and CLAUDE.md reflect current state

This codebase represents a focused research tool with reliable testing infrastructure and validated results suitable for policy recommendations in Thai government document processing optimization.