#!/usr/bin/env bash
# setup_venv.sh - Portable virtual environment setup script

set -e

# Project directory (where this script is located)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

echo "Setting up virtual environment for rlooper_sim_python..."
echo "Project directory: $PROJECT_DIR"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed or not in PATH"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists at $VENV_DIR"
fi

# Determine the activation script path based on OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    ACTIVATE_SCRIPT="$VENV_DIR/Scripts/activate"
    PYTHON_EXE="$VENV_DIR/Scripts/python.exe"
else
    # Unix-like (Linux/macOS)
    ACTIVATE_SCRIPT="$VENV_DIR/bin/activate"
    PYTHON_EXE="$VENV_DIR/bin/python"
fi

# Activate virtual environment and install requirements
echo "Installing requirements..."
source "$ACTIVATE_SCRIPT"
pip install --upgrade pip
pip install -r "$PROJECT_DIR/requirements.txt"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment:"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
    echo "  Windows: .venv\\Scripts\\activate"
    echo "  PowerShell: .venv\\Scripts\\Activate.ps1"
else
    echo "  source .venv/bin/activate"
fi
echo ""
echo "To run the workflow:"
echo "  python run_workflow.py all"
echo ""