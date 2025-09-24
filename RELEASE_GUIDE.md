# Release Guide for rlooper_sim_python

## Automated Release Process

### 1. Tag and Push
```bash
# Update version in version.py if needed
# Commit all changes first
git add -A
git commit -m "Prepare for release v1.0.0"
git push

# Create and push tag
git tag v1.0.0
git push origin v1.0.0
```

The GitHub Actions workflow will automatically:
- Create a virtual environment
- Generate frozen requirements
- Build the release package
- Create a GitHub release with the ZIP file

### 2. Manual Release Process (Alternative)

If you prefer manual control:

```bash
# 1. Create frozen requirements
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip freeze > requirements-frozen.txt

# 2. Create release package
python create_release.py

# 3. Create git tag
git tag v1.0.0
git push origin v1.0.0

# 4. Upload to GitHub
# - Go to GitHub repository > Releases > Create Release
# - Choose tag v1.0.0
# - Upload the ZIP file from release/ directory
```

## Release Checklist

Before creating a release:

- [ ] All tests pass
- [ ] Documentation is up to date
- [ ] Version number updated in `version.py`
- [ ] CHANGELOG updated
- [ ] Example files work correctly
- [ ] Cross-platform compatibility tested

## Version Numbering

Follow semantic versioning (semver):
- `v1.0.0` - Major release
- `v1.1.0` - Minor release (new features)
- `v1.0.1` - Patch release (bug fixes)

## Release Contents

Each release includes:
- Complete source code
- Frozen requirements for reproducibility
- Example FASTA files
- Cross-platform setup scripts
- Documentation
- License

## Distribution Options

1. **GitHub Releases** (recommended)
   - Automatic with GitHub Actions
   - Easy download and installation
   - Version tracking

2. **PyPI Package** (future consideration)
   - `pip install rlooper-sim-python`
   - Easier installation for Python users

3. **Conda Package** (future consideration)
   - `conda install -c your-channel rlooper-sim-python`
   - Better for scientific users

## User Installation

Users can install the release in several ways:

```bash
# Method 1: Download and extract ZIP
# Extract rlooper_sim_python-v1.0.0.zip
python setup.py

# Method 2: Git clone specific version
git clone --branch v1.0.0 https://github.com/srhartono/rlooper_sim_python.git
cd rlooper_sim_python
python setup.py

# Method 3: Reproducible installation
pip install -r requirements-frozen.txt
```