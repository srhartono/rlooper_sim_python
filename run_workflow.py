#!/usr/bin/env python3
"""
Convenient wrapper script for running the rlooper Snakemake workflow
"""

import sys
import subprocess
import os

def get_python_executable():
    """Automatically detect the Python executable to use (venv or system)"""
    import platform
    from pathlib import Path
    
    # Get project directory
    project_dir = Path(__file__).parent.absolute()
    
    # Check for virtual environment
    if platform.system() == "Windows":
        venv_python = project_dir / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = project_dir / ".venv" / "bin" / "python"
    
    if venv_python.exists():
        return str(venv_python)
    else:
        # Fall back to system Python
        return sys.executable

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python run_workflow.py <command> [options]")
        print("\nCommands:")
        print("  all           - Run all simulations")
        print("  summary       - Generate summary report")  
        print("  clean         - Remove all output files")
        print("  dry-run       - Show what would be executed without running")
        print("  dag           - Generate workflow DAG visualization (saves as dag.dot)")
        print("\nExamples:")
        print("  python run_workflow.py all")
        print("  python run_workflow.py dry-run")
        print("  python run_workflow.py summary")
        print("  python run_workflow.py dag")
        return 1
    
    command = sys.argv[1]
    
    # Get the appropriate Python executable
    python_exe = get_python_executable()
    
    # Build snakemake command
    snakemake_cmd = [python_exe, "-m", "snakemake"]
    generate_dag = False
    
    if command == "all":
        snakemake_cmd.extend(["--cores", "1"])
    elif command == "dag":
        # Generate DAG visualization
        snakemake_cmd.extend(["--dag"])
        generate_dag = True
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
    
    if generate_dag:
        # For DAG generation, we'll save as DOT file and try to convert to PDF
        try:
            # First, run snakemake --dag to get the DOT format
            dag_process = subprocess.run(snakemake_cmd, capture_output=True, text=True)
            
            if dag_process.returncode == 0:
                # Save DOT format to file
                with open("dag.dot", "w") as f:
                    f.write(dag_process.stdout)
                print("DAG saved as dag.dot")
                
                # Try to convert to PDF using dot command
                try:
                    dot_process = subprocess.run(
                        ["dot", "-Tpdf", "-o", "dag.pdf", "dag.dot"], 
                        capture_output=True,
                        text=True
                    )
                    
                    if dot_process.returncode == 0:
                        print("DAG visualization saved as dag.pdf")
                        print("You can also view dag.dot in any text editor or online DOT viewer")
                    else:
                        print(f"Warning: Could not create PDF ({dot_process.stderr.strip()})")
                        print("DAG is available as dag.dot - you can:")
                        print("  1. View it in a text editor")
                        print("  2. Use an online DOT viewer like http://magjac.com/graphviz-visual-editor/")
                        print("  3. Install Graphviz to convert to PDF: https://graphviz.org/download/")
                        
                except FileNotFoundError:
                    print("DOT command not found, but DAG saved as dag.dot")
                    print("To convert to PDF, install Graphviz from https://graphviz.org/download/")
                    print("Then run: dot -Tpdf -o dag.pdf dag.dot")
                
                return 0
            else:
                print(f"Error running snakemake: {dag_process.stderr}")
                return dag_process.returncode
                
        except Exception as e:
            print(f"Error generating DAG: {e}")
            return 1
    else:
        # Normal execution
        result = subprocess.run(snakemake_cmd)
        return result.returncode

if __name__ == "__main__":
    sys.exit(main())