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
        fasta = lambda wildcards: f"input/{config['samples'][wildcards.sample]}",
        energy = "bin/energy.csv",
        # Python module dependencies
        main_script = "bin/main.py",
        simulation_module = "bin/simulation.py",
        model_module = "bin/model.py", 
        gene_module = "bin/gene.py",
        structure_module = "bin/structure.py"
    output:
        peaks = "results/{sample}/rlooper_peaks.csv",
        output_data = "results/{sample}/rlooper_output.csv"
    params:
        output_dir = "results/{sample}"
    log:
        "logs/{sample}/rlooper_simulation.log"
    run:
        import os
        import shutil
        
        # Create output directory
        os.makedirs(params.output_dir, exist_ok=True)
        
        # Create log directory
        os.makedirs(os.path.dirname(log[0]), exist_ok=True)
        
        # Change to output directory
        original_dir = os.getcwd()
        os.chdir(params.output_dir)
        
        try:
            # Copy energy.csv to output directory (required by simulation)
            shutil.copy2(os.path.join(original_dir, "bin/energy.csv"), "energy.csv")
            
            # Run the rlooper simulation
            import subprocess
            fasta_path = os.path.join(original_dir, input.fasta)
            main_path = os.path.join(original_dir, "bin/main.py")
            log_path = os.path.join(original_dir, log[0])
            python_exe = get_python_executable()
            
            # Set PYTHONPATH to include the bin directory
            env = os.environ.copy()
            env['PYTHONPATH'] = os.path.join(original_dir, "bin")
            
            with open(log_path, 'w') as log_file:
                result = subprocess.run([python_exe, main_path, fasta_path], 
                                      stdout=log_file, stderr=subprocess.STDOUT, env=env)
            
            # Move outputs to current directory if they were created in the parent
            if os.path.exists(os.path.join(original_dir, "rlooper_output.csv")):
                shutil.move(os.path.join(original_dir, "rlooper_output.csv"), "rlooper_output.csv")
            if os.path.exists(os.path.join(original_dir, "rlooper_peaks.csv")):
                shutil.move(os.path.join(original_dir, "rlooper_peaks.csv"), "rlooper_peaks.csv")
                
        finally:
            # Return to original directory
            os.chdir(original_dir)

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