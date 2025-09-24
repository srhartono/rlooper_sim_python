# rlooper_sim_python
Rlooper Sim Python Implementation

## Synopsis

### Original Usage (standalone)
`python main.py example.fasta`

### Snakemake Workflow Usage (recommended)

This project now includes a Snakemake workflow that automates the execution of rlooper simulations on multiple FASTA files.

#### Prerequisites
- Python 3.7 or higher

#### Setup (One-time)
Choose one of the following setup methods:

**Method 1: Automatic setup (recommended)**
```bash
python setup_venv.py
```

**Method 2: Manual setup**
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Method 3: Platform-specific scripts**
- Windows: `setup_venv.bat`
- Unix/Linux: `bash setup_venv.sh`

#### Quick Start
1. **Setup** (first time only): `python setup_venv.py`
2. **Configure** your input files in `config.yaml`
3. **Run** the workflow:

```bash
python run_workflow.py all
```

**Alternative methods:**
- Direct Snakemake: `snakemake --cores 1` (if activated manually)
- With venv activation: 
  ```bash
  # Windows
  .venv\Scripts\activate
  python run_workflow.py all
  
  # Unix/macOS  
  source .venv/bin/activate
  python run_workflow.py all
  ```

#### Project Structure
```
rlooper_sim_python/
├── input/                    # FASTA input files
│   ├── example.fasta
│   └── example_short.fasta
├── bin/                      # Python source code and energy data
│   ├── main.py
│   ├── simulation.py
│   ├── model.py
│   ├── gene.py
│   ├── structure.py
│   └── energy.csv
├── results/                  # Output directory (created by workflow)
├── config.yaml              # Workflow configuration
├── Snakefile                # Workflow definition
└── run_workflow.py          # Convenience wrapper script
```

#### Configuration
Edit `config.yaml` to specify your FASTA files (relative to the `input/` folder):
```yaml
samples:
  sample1: "sample1.fasta"
  sample2: "sample2.fasta" 
  example: "example.fasta"
  example_short: "example_short.fasta"
```

#### Available Commands

**Using wrapper script:**
- `python run_workflow.py all` - Run all simulations
- `python run_workflow.py summary` - Generate summary report
- `python run_workflow.py clean` - Remove all output files
- `python run_workflow.py dry-run` - Show what would be executed

**Direct Snakemake commands:**
- `snakemake --cores 1` - Run all simulations
- `snakemake create_summary --cores 1` - Generate summary report
- `snakemake clean` - Remove all output files

#### Output Structure
```
results/
├── <sample_name>/
│   ├── rlooper_output.csv    # Main simulation results
│   ├── rlooper_peaks.csv     # Identified peaks
│   └── energy.csv            # Copy of energy parameters
└── summary_report.txt        # Summary of all samples
```

#### Workflow Features
- **Organized Structure**: Input files in `input/`, code in `bin/`, outputs in `results/`
- **Parallel Processing**: Run multiple FASTA files simultaneously
- **Organized Output**: Each sample gets its own results directory
- **Dependency Management**: Automatically handles Python module dependencies
- **Summary Reports**: Generate consolidated summaries of all results
- **Reproducible**: Version-controlled workflow definition

#### Adding New Samples
1. Place your FASTA files in the `input/` folder
2. Add entries to `config.yaml`:
   ```yaml
   samples:
     my_sample: "my_sample.fasta"    # References input/my_sample.fasta
   ```
3. Run the workflow: `python run_workflow.py all`