#!/usr/bin/env python3
"""
Command-line interface for rlooper simulation.
"""

import sys
import os
import argparse
from pathlib import Path

def get_data_path():
    """Get the path to the package data directory."""
    package_dir = Path(__file__).parent
    return package_dir / "data"

def get_examples_path():
    """Get the path to the package examples directory."""
    package_dir = Path(__file__).parent
    return package_dir / "examples"

def main():
    """Main CLI entry point for rlooper simulation."""
    parser = argparse.ArgumentParser(
        description="Rlooper Simulation Python",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:zz
  rlooper-sim example.fasta              # Run simulation on single file
  rlooper-sim --list-examples            # Show available example files
  rlooper-sim --copy-examples /path/to/  # Copy example files to directory
        """
    )
    
    parser.add_argument("fasta_file", nargs="?", help="FASTA file to process")
    parser.add_argument("--list-examples", action="store_true", 
                       help="List available example files")
    parser.add_argument("--copy-examples", metavar="DIR", 
                       help="Copy example files to specified directory")
    parser.add_argument("--energy-csv", 
                       help="Path to energy CSV file (default: use package data)")
    parser.add_argument("--output-dir", default=".", 
                       help="Output directory for results (default: current directory)")
    
    args = parser.parse_args()
    
    # Handle list examples
    if args.list_examples:
        examples_path = get_examples_path()
        print("Available example files:")
        for fasta_file in examples_path.glob("*.fasta"):
            print(f"  {fasta_file.name}")
        return 0
    
    # Handle copy examples
    if args.copy_examples:
        import shutil
        examples_path = get_examples_path()
        dest_dir = Path(args.copy_examples)
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        copied_files = []
        for fasta_file in examples_path.glob("*.fasta"):
            dest_file = dest_dir / fasta_file.name
            shutil.copy2(fasta_file, dest_file)
            copied_files.append(fasta_file.name)
        
        print(f"Copied {len(copied_files)} example files to {dest_dir}:")
        for file in copied_files:
            print(f"  {file}")
        return 0
    
    # Require FASTA file for simulation
    if not args.fasta_file:
        parser.error("FASTA file is required for simulation")
    
    # Check if FASTA file exists
    fasta_path = Path(args.fasta_file)
    if not fasta_path.exists():
        print(f"Error: FASTA file '{args.fasta_file}' not found", file=sys.stderr)
        return 1
    
    # Set up energy CSV path
    if args.energy_csv:
        energy_csv = Path(args.energy_csv)
        if not energy_csv.exists():
            print(f"Error: Energy CSV file '{args.energy_csv}' not found", file=sys.stderr)
            return 1
    else:
        energy_csv = get_data_path() / "energy.csv"
    
    # Import and run the simulation
    try:
        from .main import main as run_simulation
        
        # Change to output directory
        original_dir = os.getcwd()
        output_dir = Path(args.output_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        os.chdir(output_dir)
        
        # Set up sys.argv for the original main function - use relative path from output dir
        fasta_absolute = fasta_path.resolve()
        sys.argv = ["rlooper-sim", str(fasta_absolute)]
        
        # Copy energy.csv to current directory if needed
        local_energy = Path("energy.csv")
        if not local_energy.exists():
            import shutil
            shutil.copy2(energy_csv, local_energy)
        
        # Run the simulation
        result = run_simulation()
        
        # Change back to original directory
        os.chdir(original_dir)
        
        print(f"Simulation completed. Results saved in: {output_dir}")
        return result if result is not None else 0
        
    except ImportError as e:
        print(f"Error importing simulation module: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error running simulation: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())