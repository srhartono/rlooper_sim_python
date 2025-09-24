# Snakemake workflow for rlooper simulation
import os
import sys
import platform
from pathlib import Path

configfile: "config.yaml"

def get_python_executable():
    """Automatically detect the Python executable to use (venv or system)"""
    # Get project directory (where Snakefile is located)
    project_dir = Path(workflow.basedir).absolute()
    
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

# Define the target rule that specifies all final outputs
rule all:
    input:
        expand("results/{sample}/rlooper_output.csv", sample=config["samples"]),
        expand("results/{sample}/rlooper_peaks.csv", sample=config["samples"])

# Rule to run rlooper simulation for each FASTA file
rule run_rlooper_simulation:
    input:
        fasta = lambda wildcards: f"input/{config['samples'][wildcards.sample]}"
    output:
        peaks = "results/{sample}/rlooper_peaks.csv",
        output_data = "results/{sample}/rlooper_output.csv"
    params:
        output_dir = "results/{sample}"
    log:
        "logs/{sample}/rlooper_simulation.log"
    run:
        import os
        import subprocess
        import sys
        from pathlib import Path
        
        # Create output directory
        os.makedirs(params.output_dir, exist_ok=True)
        
        # Create log directory  
        os.makedirs(os.path.dirname(log[0]), exist_ok=True)
        
        # Get absolute paths
        fasta_path = os.path.abspath(input.fasta)
        log_path = os.path.abspath(log[0])
        output_dir = os.path.abspath(params.output_dir)
        python_exe = get_python_executable()
        
        # Run the rlooper simulation using the installed CLI
        cmd = [python_exe, "-m", "rlooper_sim_python.cli", 
               fasta_path, "--output-dir", output_dir]
        
        print(f"Running: {' '.join(cmd)}")
        
        with open(log_path, 'w') as log_file:
            result = subprocess.run(cmd, stdout=log_file, stderr=subprocess.STDOUT)
        
        if result.returncode != 0:
            print(f"Simulation failed for {wildcards.sample}. Check log: {log_path}")
            # Read and display the error log
            with open(log_path, 'r') as f:
                print(f.read())
            sys.exit(1)
        else:
            print(f"Simulation completed for {wildcards.sample}")

# Rule to create a summary report of all results
rule create_summary:
    input:
        expand("results/{sample}/rlooper_output.csv", sample=config["samples"]),
        expand("results/{sample}/rlooper_peaks.csv", sample=config["samples"])
    output:
        "results/summary_report.txt"
    run:
        import os
        from datetime import datetime
        
        with open(output[0], 'w') as f:
            f.write("Rlooper Simulation Summary Report\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n")
            
            for sample in config["samples"]:
                f.write(f"Sample: {sample}\n")
                
                output_file = f"results/{sample}/rlooper_output.csv"
                if os.path.exists(output_file):
                    with open(output_file) as csvf:
                        lines = sum(1 for _ in csvf) - 1  # subtract header
                    f.write(f"  - Output records: {lines}\n")
                
                peaks_file = f"results/{sample}/rlooper_peaks.csv"
                if os.path.exists(peaks_file):
                    with open(peaks_file) as csvf:
                        lines = sum(1 for _ in csvf) - 1  # subtract header
                    f.write(f"  - Peak records: {lines}\n")
                
                f.write("\n")

# Rule to clean all outputs
rule clean:
    run:
        import shutil
        import os
        
        if os.path.exists("results"):
            shutil.rmtree("results")
        if os.path.exists("logs"):
            shutil.rmtree("logs")
        print("🧹 Cleaned all output files and directories")