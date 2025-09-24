#!/usr/bin/env python3
"""
Release preparation script for rlooper_sim_python
Creates a frozen, reproducible release package
"""

import os
import sys
import subprocess
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

VERSION = "1.0.0"  # Update this for each release
RELEASE_NAME = f"rlooper_sim_python-v{VERSION}"

def main():
    project_dir = Path(__file__).parent.absolute()
    release_dir = project_dir / "release" / RELEASE_NAME
    
    print(f"Creating release {RELEASE_NAME}...")
    
    # Clean and create release directory
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir(parents=True, exist_ok=True)
    
    # Files to include in release
    files_to_copy = [
        "bin/",
        "input/",
        "config.yaml",
        "Snakefile", 
        "requirements.txt",
        "requirements-frozen.txt",
        "setup.py",
        "setup.sh", 
        "setup.bat",
        "run_workflow.py",
        "python_Makefile",
        "README.md",
        "LICENSE",
        "version.py"
    ]
    
    # Copy files to release directory
    for item in files_to_copy:
        src = project_dir / item
        dst = release_dir / item
        
        if src.exists():
            if src.is_dir():
                shutil.copytree(src, dst)
                print(f"Copied directory: {item}")
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                print(f"Copied file: {item}")
        else:
            print(f"Warning: {item} not found, skipping")
    
    # Create release info file
    release_info = f"""# Rlooper Simulation Python - Release {VERSION}

Release Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Version: {VERSION}

## Quick Start

1. Setup environment:
   ```
   python setup_venv.py
   ```

2. Run workflow:
   ```
   python run_workflow.py all
   ```

## Package Contents

- `bin/` - Python source code and energy data
- `input/` - Example FASTA files  
- `config.yaml` - Workflow configuration
- `Snakefile` - Snakemake workflow definition
- `requirements.txt` - Minimum dependency versions
- `requirements-frozen.txt` - Exact dependency versions (reproducible)
- `setup_venv.py` - Automatic environment setup
- `run_workflow.py` - Workflow runner
- `README.md` - Full documentation

## Reproducible Installation

For exact reproduction of this release environment:
```
python -m venv .venv
source .venv/bin/activate  # or .venv\\Scripts\\activate on Windows
pip install -r requirements-frozen.txt
```

## System Requirements

- Python 3.7 or higher
- 500MB free disk space
- 2GB RAM minimum
"""
    
    with open(release_dir / "RELEASE_INFO.md", "w") as f:
        f.write(release_info)
    
    # Create version file
    version_info = {
        "version": VERSION,
        "release_date": datetime.now().isoformat(),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    }
    
    import json
    with open(release_dir / "version.json", "w") as f:
        json.dump(version_info, f, indent=2)
    
    # Create ZIP archive
    zip_path = project_dir / "release" / f"{RELEASE_NAME}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(release_dir.parent)
                zipf.write(file_path, arc_path)
    
    print(f"\n✅ Release created successfully!")
    print(f"📁 Release directory: {release_dir}")
    print(f"📦 ZIP archive: {zip_path}")
    print(f"📝 Size: {zip_path.stat().st_size / (1024*1024):.1f} MB")
    
    print(f"\n🚀 To create GitHub release:")
    print(f"1. git tag v{VERSION}")
    print(f"2. git push origin v{VERSION}")
    print(f"3. Upload {zip_path.name} to GitHub release")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())