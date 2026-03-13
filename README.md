# EdgeRIC Documentation

This repository contains the documentation for EdgeRIC.

## Prerequisites

- Python 3.9+
- pip

## Building the Documentation Locally

### 1. Set up the virtual environment

```bash
cd docs
python3 -m venv myenv
source myenv/bin/activate
```

### 2. Install dependencies

```bash
pip install sphinx furo sphinx-tabs myst-parser
```

### 3. Build the HTML documentation

```bash
make html
```

The built documentation will be in `docs/_build/html/`.

### 4. View locally

```bash
python3 -m http.server 8000 -d _build/html
```

Then open http://localhost:8000 in your browser.

## Quick Rebuild

If the virtual environment is already set up:

```bash
cd docs
source myenv/bin/activate
make html
python3 -m http.server 8000 -d _build/html
```
Open in your browser: http://localhost:8000
## Cleaning Build Files

```bash
make clean
```
