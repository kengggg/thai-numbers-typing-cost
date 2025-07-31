#!/usr/bin/env python3
"""
Thai Numbers Typing Cost Analysis - Easy Runner Script

Simple wrapper to run the analysis from the project root directory.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Run the Thai Numbers Typing Cost Analysis from project root."""
    
    # Get project root directory
    project_root = Path(__file__).parent
    src_dir = project_root / "src"
    data_file = project_root / "data" / "thai-con.txt"
    
    # Change to src directory for execution
    os.chdir(src_dir)
    
    # Auto-add markdown report generation for comprehensive analyses
    args = sys.argv[1:]
    comprehensive_flags = ['--compare-all', '--compare-weights']
    is_comprehensive = any(flag in args for flag in comprehensive_flags)
    
    # Add markdown report by default for comprehensive analyses (unless explicitly disabled)
    if is_comprehensive and '--no-markdown' not in args and '--markdown-report' not in args:
        args.append('--markdown-report')
    
    # Forward all arguments to main.py
    cmd = [sys.executable, "main.py", str(data_file)] + args
    
    print("=" * 80)
    print("THAI NUMBERS TYPING COST ANALYSIS")
    print("=" * 80)
    print(f"Project Root: {project_root}")
    print(f"Data File: {data_file}")
    print(f"Output Directory: {project_root}/output/")
    print(f"Command: {' '.join(cmd)}")
    print("=" * 80)
    
    # Execute the analysis
    try:
        result = subprocess.run(cmd, check=True)
        print("\n" + "=" * 80)
        print("✅ ANALYSIS COMPLETED SUCCESSFULLY!")
        print(f"📁 Results saved to: {project_root}/output/")
        print("=" * 80)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"\n❌ ANALYSIS FAILED: {e}")
        return e.returncode
    except KeyboardInterrupt:
        print(f"\n⚠️  ANALYSIS INTERRUPTED")
        return 1

if __name__ == "__main__":
    sys.exit(main())