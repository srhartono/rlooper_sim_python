#!/usr/bin/env python3
"""
setup_venv.py - Cross-platform virtual environment setup script
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def main():
    # Get project directory (where this script is located)
    project_dir = Path(__file__).parent.absolute()
    venv_dir = project_dir / ".venv"
    
    print("Setting up virtual environment for rlooper_sim_python...")
    print(f"Project directory: {project_dir}")
    
    # Check if Python is available
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"Using Python: {result.stdout.strip()}")
    except subprocess.CalledProcessError:
        print("Error: Python is not available")
        return 1
    
    # Create virtual environment if it doesn't exist
    if not venv_dir.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
    else:
        print(f"Virtual environment already exists at {venv_dir}")
    
    # Determine Python executable in venv based on platform
    if platform.system() == "Windows":
        python_exe = venv_dir / "Scripts" / "python.exe"
        activate_script = venv_dir / "Scripts" / "activate.bat"
        activate_ps1 = venv_dir / "Scripts" / "Activate.ps1"
    else:
        python_exe = venv_dir / "bin" / "python"
        activate_script = venv_dir / "bin" / "activate"
    
    # Install requirements
    print("Installing requirements...")
    requirements_file = project_dir / "requirements.txt"
    
    # Upgrade pip first
    subprocess.run([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"], 
                   check=True)
    
    # Install requirements
    if requirements_file.exists():
        subprocess.run([str(python_exe), "-m", "pip", "install", "-r", 
                       str(requirements_file)], check=True)
    else:
        print("Warning: requirements.txt not found")
    
    print("\n✅ Setup complete!")
    print("\nTo activate the virtual environment:")
    
    if platform.system() == "Windows":
        print(f"  Command Prompt: {activate_script}")
        print(f"  PowerShell: {activate_ps1}")
    else:
        print(f"  source {activate_script}")
    
    print("\nTo run the workflow:")
    print("  python run_workflow.py all")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())