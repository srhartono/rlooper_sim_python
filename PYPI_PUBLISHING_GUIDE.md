# PyPI Publishing Guide for rlooper-sim-python

## Prerequisites

1. **Create PyPI Accounts:**
   - TestPyPI: https://test.pypi.org/account/register/
   - Production PyPI: https://pypi.org/account/register/

2. **Install required tools** (already done):
   ```bash
   pip install build twine
   ```

## Step 1: Test on TestPyPI (Recommended First)

### Upload to TestPyPI
```bash
# Build the package (already done)
python -m build

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*
```

You'll be prompted for:
- Username: Your TestPyPI username
- Password: Your TestPyPI password (or API token)

### Test Installation from TestPyPI
```bash
# Create a new virtual environment to test
python -m venv test_env
test_env\Scripts\activate  # Windows

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ rlooper-sim-python

# Test the commands
rlooper-sim --list-examples
rlooper-workflow --help
```

## Step 2: Publish to Production PyPI

### Upload to Production PyPI
```bash
# Upload to production PyPI
python -m twine upload dist/*
```

### Test Installation from PyPI
```bash
# In a new environment
pip install rlooper-sim-python

# Test installation
rlooper-sim --list-examples
rlooper-workflow --init-project test_project
```

## API Tokens (Recommended)

Instead of username/password, use API tokens:

### For TestPyPI:
1. Go to https://test.pypi.org/manage/account/token/
2. Create new API token with scope for your project
3. Use `__token__` as username and the token as password

### For Production PyPI:
1. Go to https://pypi.org/manage/account/token/
2. Create new API token
3. Use `__token__` as username and the token as password

## Configure ~/.pypirc (Optional)

Create `~/.pypirc` file for easier uploads:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = your_pypi_api_token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = your_testpypi_api_token
```

Then you can upload with:
```bash
# Test
twine upload --repository testpypi dist/*

# Production
twine upload dist/*
```

## Package Information

- **Package Name:** `rlooper-sim-python`
- **Version:** 1.0.0
- **CLI Commands:**
  - `rlooper-sim` - Single file simulation
  - `rlooper-workflow` - Snakemake workflow management

## Next Version Updates

For future versions:
1. Update version in `rlooper_sim_python/version.py`
2. Update version in `pyproject.toml`
3. Add changelog entry
4. Build and upload new version

## Verification

After publishing, verify:
1. Package appears on PyPI: https://pypi.org/project/rlooper-sim-python/
2. Installation works: `pip install rlooper-sim-python`
3. CLI commands work properly
4. Documentation renders correctly