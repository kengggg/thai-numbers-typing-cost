# Thai Numbers Typing Cost Analysis

A comprehensive analysis tool for comparing typing costs between Thai digits (๐-๙) and international digits (0-9) across different keyboard layouts and typist skill levels.

## Project Structure

```
thai-numbers-typing-cost/
├── src/                          # Python source code
│   ├── models/                   # Data models and analysis classes
│   │   ├── keyboard_layouts.py   # Keyboard layout models (Kedmanee, Pattajoti)
│   │   └── text_analyzer.py      # Text analysis functionality
│   ├── calculators/              # Core calculation logic
│   │   └── typing_cost_calculator.py
│   └── main.py                   # Main CLI application
├── output/                       # Generated analysis files
│   ├── reports/                  # Summary reports and comparisons
│   └── analysis/                 # Detailed analysis data
├── data/                         # Input documents and keyboard layouts
│   ├── thai-con.txt             # 2017 Thai Constitution (benchmark)
│   ├── TIS_820-2535,_Figure_2.jpg # Official Kedmanee layout (TIS standard)
│   └── Pattajoti.gif            # Official Pattajoti layout
└── PRD.txt                       # Project requirements document
```

## Typist Skill Levels

The analysis supports four different typist profiles:

| Profile | Keystroke Time | Description |
|---------|----------------|-------------|
| **expert** | 0.12s | Professional typist (~90 WPM), touch typing mastery |
| **skilled** | 0.20s | Experienced office worker, good typing skills |
| **average** | 0.28s | Average office worker, moderate typing skills (default) |
| **worst** | 1.2s | Hunt-and-peck typist, very slow typing |

## Calculation Modes

The analysis supports two calculation modes:

### **Weighted Mode (Default)**
- Applies ergonomic difficulty multipliers based on finger position
- Pinky fingers: 20% harder (1.2x cost)
- Ring fingers: 10% harder (1.1x cost)  
- Index/Middle: Baseline (1.0x cost)
- Plus SHIFT penalty (2x cost for Thai digits on Kedmanee)

### **Unweighted Mode**
- Uses only base keystroke time and SHIFT penalty
- All fingers treated equally (1.0x difficulty)
- Cleaner baseline for research credibility
- Only well-established factors (base time + SHIFT penalty)

## Quick Start

The easiest way to run the analysis:

```bash
# From project root directory - Run full analysis with default settings
python run_analysis.py

# Compare all typist skill levels  
python run_analysis.py --compare-all

# Compare weighted vs unweighted calculations
python run_analysis.py --compare-weights

# Expert typist with unweighted mode
python run_analysis.py --typist expert --no-weights

# Show available options
python run_analysis.py --help
```

**Output Location**: All results are saved to `output/` directory in the project root.
**Markdown Reports**: Comprehensive reports automatically generated with date/time naming (e.g., `Thai_Numbers_Typing_Cost_Analysis_Report_20250731_115551.md`)

## Advanced Usage

### Basic Analysis

```bash
# Run analysis with default (average) typist, weighted mode
cd src
python main.py ../data/thai-con.txt

# Analyze with expert typist, unweighted mode
python main.py ../data/thai-con.txt --typist expert --no-weights

# Compare weighted vs unweighted for average typist
python main.py ../data/thai-con.txt --compare-weights
```

### Comparative Analysis

```bash
# Compare all typist skill levels
cd src
python main.py ../data/thai-con.txt --compare-all

# Custom output directory
python main.py ../data/thai-con.txt --output ../custom_output/
```

### Specialized Analysis

```bash
# Only text analysis
cd src
python main.py ../data/thai-con.txt --text-only

# Only keyboard comparison
python main.py ../data/thai-con.txt --keyboard-only

# List available typist profiles
python main.py --list-typists
```

### Validation

```bash
# Validate keyboard layout model accuracy
cd src
python validation_tests.py

# Quick keyboard layout comparison
python -c "from models.keyboard_layouts import *; compare_layouts()"
```

### Help

```bash
cd src
python main.py --help
```

## Key Findings

Based on analysis of the 2017 Thai Constitution (197,482 characters, 2,323 digits):

### Current State vs Optimal
- **Current**: Thai digits + Kedmanee keyboard
- **Optimal**: International digits + Pattajoti keyboard
- **Efficiency gain**: 3.2% across all typist skill levels

### Time Savings by Typist Level
| Typist Level | Current Time | Optimal Time | Time Saved | 
|--------------|--------------|--------------|------------|
| Expert (90 WPM) | 6.5 hours | 6.3 hours | 12.5 minutes |
| Skilled | 10.9 hours | 10.5 hours | 20.9 minutes |
| Average | 15.3 hours | 14.8 hours | 29.2 minutes |
| Worst | 65.4 hours | 63.3 hours | 125.1 minutes |

### Root Causes
1. **Thai digits on Kedmanee require SHIFT key** (2x typing cost penalty)
2. **Suboptimal key positioning** for frequently used digits
3. **Pattajoti layout eliminates SHIFT penalty** for Thai digits
4. **International digits more accessible** on both keyboard layouts

## Research Questions Answered

1. **Q1**: Thai numbers on Kedmanee → 15.25 hours (average typist)
2. **Q2**: International numbers on Kedmanee → 15.05 hours (1.3% faster)
3. **Q3**: Thai numbers on Pattajoti → 14.79 hours (3.0% faster)
4. **Q4**: International numbers on Pattajoti → 14.76 hours (3.2% faster)
5. **Q5**: "LOST" cost = 29.2 minutes per document, 3.2% inefficiency

## Policy Recommendations

### Immediate (High Impact, Low Cost)
- Standardize on international digits (0-9) for all new documents
- Update document templates and style guides
- Train staff on efficient number entry practices

### Short-term (6-12 months)
- Migrate existing document workflows to international digits
- Develop automated conversion tools for legacy documents
- Consider Pattajoti keyboard layout for Thai-heavy environments

### Long-term (1-2 years)
- Government-wide policy on digital document number formatting
- Integration with document processing systems
- Cost-benefit analysis for hardware/software updates

## Technical Details

### Methodology
- **Document Analysis**: 2017 Thai Constitution as benchmark (197,482 characters)
- **Keyboard Modeling**: Official TIS 820-2535 (Kedmanee) and Pattajoti layouts
- **Visual Validation**: Models verified against actual keyboard layout images
- **Cost Calculation**: Base keystroke time + difficulty multipliers + SHIFT penalties
- **Statistical Analysis**: All 2,323 digit occurrences analyzed individually

### Official References
- **TIS 820-2535**: Thai Keyboard Layout Standard (Kedmanee) - `data/TIS_820-2535,_Figure_2.jpg`
- **Pattajoti Layout**: Thai-optimized keyboard layout - `data/Pattajoti.gif`
- **Validation Tests**: Comprehensive accuracy testing - `src/validation_tests.py`

### Model Accuracy
The keyboard layout models have been validated against official standards:
- ✅ **Finger assignments**: Match standard touch typing practices
- ✅ **SHIFT requirements**: Thai digits require SHIFT on Kedmanee only
- ✅ **Character coverage**: 67+ keys (Kedmanee), 78+ keys (Pattajoti)
- ✅ **Digit order**: Correct Pattajoti sequence (๒๓๔๕๗๘๙๐๑๖)

Run validation: `cd src && python validation_tests.py`

### Assumptions
- Base keystroke times from University of Michigan study (0.28s average)
- SHIFT character penalty: 2x base cost (as specified in PRD)
- Ergonomic factors: Row difficulty and finger position multipliers
- Touch typing finger assignments for international digits

### Limitations
- Single document sample (constitution may not represent all government docs)
- Ergonomic multipliers based on general typing principles
- Individual typing variation exists beyond skill level categories
- Conservative estimates (don't include context switching or cognitive overhead)

## Government Impact Projections

**National Scale Estimates:**
- **Government-wide adoption**: ~122,000 hours saved annually
- **Estimated cost savings**: ~$1.8M USD annually (at $15/hour)
- **Efficiency improvement**: 3.2% across all document processing

## Files Generated

The analysis creates several output files:

### Reports (`output/reports/`)
- `comparative_analysis.txt`: Summary across all typist skill levels

### Analysis Data (`output/analysis/`)
- `text_analysis.txt`: Detailed character and digit analysis
- `typing_cost_[profile].txt`: Typing cost analysis for each skill level
- `keyboard_comparison_[profile].txt`: Keyboard layout comparisons

## Dependencies

- Python 3.7+
- Standard library only (no external dependencies)

## License

Research project for Thai government document processing optimization.