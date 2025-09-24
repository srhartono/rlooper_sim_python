#!/usr/bin/env python3
"""
Convenient wrapper script for running the rlooper Snakemake workflow
"""

import sys
import subprocess
import os

def main():
    # Get the virtual environment python path
    venv_python = "C:/cygwin64/home/srhar/rlooper_sim_python/.venv/Scripts/python.exe"
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python run_workflow.py <command> [options]")
        print("\nCommands:")
        print("  all           - Run all simulations")
        print("  summary       - Generate summary report")  
        print("  clean         - Remove all output files")
        print("  dry-run       - Show what would be executed without running")
        print("\nExamples:")
        print("  python run_workflow.py all")
        print("  python run_workflow.py dry-run")
        print("  python run_workflow.py summary")
        return 1
    
    command = sys.argv[1]
    
    # Build snakemake command
    snakemake_cmd = [venv_python, "-m", "snakemake"]
    
    if command == "all":
        snakemake_cmd.extend(["--cores", "1"])
    elif command == "summary":
        snakemake_cmd.extend(["create_summary", "--cores", "1"])
    elif command == "clean":
        snakemake_cmd.extend(["clean", "--cores", "1"])
    elif command == "dry-run":
        snakemake_cmd.extend(["--dry-run", "--cores", "1"])
    else:
        print(f"Unknown command: {command}")
        return 1
    
    # Add any additional arguments
    if len(sys.argv) > 2:
        snakemake_cmd.extend(sys.argv[2:])
    
    # Run snakemake
    print(f"Running: {' '.join(snakemake_cmd)}")
    result = subprocess.run(snakemake_cmd)
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())