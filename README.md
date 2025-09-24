# rlooper_sim_python

[![PyPI version](https://badge.fury.io/py/rlooper-sim-python.svg)](https://badge.fury.io/py/rlooper-sim-python)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Rlooper with R-loop Peak Simulation - Python Implementation

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
# Install the package
pip install rlooper-sim-python

# Run single simulation
rlooper-sim example.fasta

# Initialize and run workflow
rlooper-workflow --init-project my_project
cd my_project
rlooper-workflow all
```

### Option 2: Install from Source

```bash
# Clone repository
git clone https://github.com/srhartono/rlooper_sim_python.git
cd rlooper_sim_python

# Install in development mode
pip install -e .

# Or install for production
pip install .
```

## Quick Start

After installation, you can use rlooper in two ways:

### 1. Single File Simulation
```bash
# Run simulation on a single FASTA file
rlooper-sim my_sequence.fasta

# Copy example files to current directory
rlooper-sim --copy-examples .
rlooper-sim example.fasta
```

### 2. Snakemake Workflow (Multiple Files)
```bash
# Initialize a new project
rlooper-workflow --init-project my_rlooper_project
cd my_rlooper_project

# Run the complete workflow
rlooper-workflow all

# Generate DAG visualization
rlooper-workflow dag

# Generate summary report
rlooper-workflow summary
```

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

#### Adding New Samples
1. Place your FASTA files in the `input/` folder
2. Add entries to `config.yaml`:
   ```yaml
   samples:
     my_sample: "my_sample.fasta"    # References input/my_sample.fasta
   ```
3. Run the workflow: `python run_workflow.py all`

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
- `python run_workflow.py dag` - Generate workflow DAG visualization

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

#### DAG Visualization (Optional)

To generate workflow diagrams as PDFs, you need to install Graphviz:

**Windows:**
```bash
# Option 1: Using Chocolatey
choco install graphviz

# Option 2: Using winget
winget install graphviz

# Option 3: Manual download from https://graphviz.org/download/
```

**macOS:**
```bash
brew install graphviz
```

**Ubuntu/Debian:**
```bash
sudo apt-get install graphviz
```

**After installing Graphviz:**
```bash
python run_workflow.py dag  # Creates dag.dot and dag.pdf
```

**Without Graphviz installed:**
- `python run_workflow.py dag` will create `dag.dot` (text format)
- View online at: http://magjac.com/graphviz-visual-editor/

