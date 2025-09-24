#!/usr/bin/env python3
"""
Command-line interface for rlooper sim workflow.
"""

import sys
import os
import argparse
import subprocess
import tempfile
import shutil
from pathlib import Path

def get_package_path():
    """Get the path to the package directory."""
    return Path(__file__).parent

def create_workflow_files(work_dir):
    """Create necessary workflow files in the working directory."""
    package_dir = get_package_path()
    
    # Copy Snakefile
    snakefile_src = package_dir.parent / "Snakefile"
    if snakefile_src.exists():
        shutil.copy2(snakefile_src, work_dir / "Snakefile")
    
    # Create config.yaml if it doesn't exist
    config_file = work_dir / "config.yaml"
    if not config_file.exists():
        config_content = '''samples:
  example: "example.fasta"
  example_short: "example_short.fasta"
'''
        config_file.write_text(config_content)
    
    # Create input directory and copy examples
    input_dir = work_dir / "input"
    input_dir.mkdir(exist_ok=True)
    
    examples_dir = package_dir / "examples"
    for fasta_file in examples_dir.glob("*.fasta"):
        dest_file = input_dir / fasta_file.name
        if not dest_file.exists():
            shutil.copy2(fasta_file, dest_file)
    
    # Create bin directory and copy Python files
    bin_dir = work_dir / "bin"
    bin_dir.mkdir(exist_ok=True)
    
    # Copy Python modules
    for py_file in package_dir.glob("*.py"):
        if py_file.name not in ["__init__.py", "cli.py", "workflow.py", "version.py"]:
            shutil.copy2(py_file, bin_dir / py_file.name)
    
    # Copy energy.csv
    energy_src = package_dir / "data" / "energy.csv"
    if energy_src.exists():
        shutil.copy2(energy_src, bin_dir / "energy.csv")

def get_python_executable():
    """Get the appropriate Python executable."""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # We're in a virtual environment
        return sys.executable
    else:
        # Try to use current Python
        return sys.executable

def run_snakemake(args_list, work_dir):
    """Run Snakemake with the given arguments."""
    python_exe = get_python_executable()
    
    try:
        cmd = [python_exe, "-m", "snakemake"] + args_list
        print(cmd)
        result = subprocess.run(cmd, cwd=work_dir, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Snakemake failed with return code {e.returncode}", file=sys.stderr)
        return e.returncode
    except FileNotFoundError:
        print("Error: Snakemake not found. Please install with: pip install snakemake", file=sys.stderr)
        return 1

def main():
    """Main CLI entry point for rlooper workflow."""
    parser = argparse.ArgumentParser(
        description="Rlooper Simulation Snakemake Workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  all         Run all simulations
  summary     Generate summary report  
  dag         Generate workflow DAG visualization
  clean       Remove all output files
  dry-run     Show what would be executed

Examples:
  rlooper-workflow all                   # Run all simulations
  rlooper-workflow dag                   # Generate DAG
  rlooper-workflow --init-project /path  # Initialize project in directory
        """
    )
    
    parser.add_argument("command", nargs="?", default="all",
                       choices=["all", "summary", "dag", "clean", "dry-run"],
                       help="Command to run")
    parser.add_argument("--cores", "-j", type=int, default=1,
                       help="Number of cores to use (default: 1)")
    parser.add_argument("--init-project", metavar="DIR",
                       help="Initialize a new rlooper project in the specified directory")
    parser.add_argument("--work-dir", metavar="DIR", default=".",
                       help="Working directory (default: current directory)")
    
    args = parser.parse_args()
    
    # Handle project initialization
    if args.init_project:
        project_dir = Path(args.init_project)
        project_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Initializing rlooper project in: {project_dir}")
        create_workflow_files(project_dir)
        
        print("Project initialized successfully!")
        print(f"To run the workflow:")
        print(f"  cd {project_dir}")
        print(f"  rlooper-workflow all")
        return 0
    
    # Set up working directory
    work_dir = Path(args.work_dir).resolve()
    
    # Check if Snakefile exists, if not create workflow files
    if not (work_dir / "Snakefile").exists():
        print("Setting up workflow files...")
        create_workflow_files(work_dir)
    
    # Map commands to Snakemake arguments
    command_map = {
        "all": ["--cores", str(args.cores)],
        "summary": ["create_summary", "--cores", str(args.cores)],
        "dag": ["--dag", "--cores", str(args.cores)],
        "clean": ["clean", "--cores", str(args.cores)],
        "dry-run": ["--dry-run", "--cores", str(args.cores)],
    }
    
    if args.command not in command_map:
        parser.error(f"Unknown command: {args.command}")
    
    snakemake_args = command_map[args.command]
    print(snakemake_args)
    run_snakemake(snakemake_args, work_dir)
   
    # Special handling for DAG
    if args.command == "dag":
        # Try to generate the DAG using snakemake
        try:
            python_exe = get_python_executable()

            from . import dag_fallback
            
            dag_file = work_dir / "dag.dot"
            dag_fallback.main(dag_file)
            # with open(dag_file, 'w') as f:
                # f.write(dag_content)
                
            print("✅ DAG generated using fallback method: dag.dot")

        except Exception as e:
            print(f"⚠️  Snakemake failed ({e}), using fallback DAG generation...")

            with open(work_dir / "dag.dot", "w") as dag_file:
                cmd = [python_exe, "-m", "snakemake", "--dag"]
                result = subprocess.run(cmd, cwd=work_dir, stdout=dag_file, stderr=subprocess.PIPE, text=True)
                
            if result.returncode == 0:
                print("✅ DAG file generated: dag.dot")
                
                # Try to generate PDF with Graphviz
                try:
                    subprocess.run(["dot", "-Tpdf", "dag.dot", "-o", "dag.pdf"], 
                                 cwd=work_dir, check=True, capture_output=True)
                    print("✅ DAG PDF generated: dag.pdf")
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print("ℹ️  Graphviz not available. You can view dag.dot online at:")
                    print("   http://magjac.com/graphviz-visual-editor/")
                # return 0
            else:
                print("⚠️  Snakemake DAG generation failed, trying fallback method...")
       
        except Exception as e:
            print(f"❌ Fallback DAG generation failed: {e}")
            return 1
    

if __name__ == "__main__":
    sys.exit(main())