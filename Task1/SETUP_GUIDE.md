# Setup Guide - Transaction Analysis Application

Complete setup instructions for Windows, macOS, and Linux.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Platform-Specific Instructions](#platform-specific-instructions)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum
- Python 3.7 or higher
- 100 MB disk space
- 2 GB RAM

### Recommended
- Python 3.9 or higher
- 500 MB disk space
- 4 GB RAM

---

## Installation Steps

### 1. Verify Python Installation

**Windows:**
```powershell
python --version
# or
python3 --version
```

**macOS/Linux:**
```bash
python3 --version
```

**Expected output:** `Python 3.x.x`

If Python is not installed, download from https://www.python.org/downloads/

### 2. Clone or Download Project

**Option A: Using Git**
```bash
git clone <repository-url>
cd transaction-analyzer
```

**Option B: Manual Download**
- Download project as ZIP
- Extract to your desired location
- Open terminal/PowerShell in project directory

### 3. Create Virtual Environment (Recommended)

**Windows:**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Verify activation:**
```bash
which python  # macOS/Linux
# or
where python  # Windows
```

Should show path inside venv directory.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

**Or manually:**
```bash
pip install pandas openpyxl matplotlib seaborn numpy
```

**Verify installation:**
```bash
python -c "import pandas, matplotlib, seaborn; print('✓ All packages installed')"
```

### 5. Verify Setup

```bash
python -c "from transaction_analyzer import TransactionAnalyzer; print('✓ Ready to use')"
```

---

## Platform-Specific Instructions

### Windows 10/11

#### Prerequisites
1. Install Python from https://www.python.org/downloads/
   - ✓ Check "Add Python to PATH" during installation
   - ✓ Check "Install pip" option

2. Open PowerShell as Administrator

#### Setup Steps
```powershell
# Navigate to project
cd path\to\transaction-analyzer

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt

# Verify
python main.py
```

#### Running Application
```powershell
# With virtual environment activated
python main.py

# Or analyze specific file
python transaction_analyzer.py your_file.xlsx
```

---

### macOS

#### Prerequisites
1. Install Python using Homebrew (recommended):
   ```bash
   brew install python3
   ```
   
   Or download from https://www.python.org/downloads/

2. Open Terminal

#### Setup Steps
```bash
# Navigate to project
cd path/to/transaction-analyzer

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify
python main.py
```

#### Running Application
```bash
# Activate virtual environment first
source venv/bin/activate

# Run application
python main.py

# Or analyze specific file
python transaction_analyzer.py your_file.xlsx
```

---

### Linux (Ubuntu/Debian)

#### Prerequisites
1. Install Python3 and pip:
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip python3-venv
   ```

2. Open Terminal

#### Setup Steps
```bash
# Navigate to project
cd path/to/transaction-analyzer

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify
python main.py
```

#### Running Application
```bash
# Activate virtual environment first
source venv/bin/activate

# Run application
python main.py

# Or analyze specific file
python transaction_analyzer.py your_file.xlsx
```

---

## Verification

### Test 1: Check Python
```bash
python --version
# Should output: Python 3.x.x
```

### Test 2: Check Packages
```bash
pip list
# Should show: pandas, openpyxl, matplotlib, seaborn, numpy
```

### Test 3: Check Application
```bash
python -c "from transaction_analyzer import TransactionAnalyzer; print('✓ OK')"
# Should output: ✓ OK
```

### Test 4: Run Sample Analysis
```bash
python sample_transactions.py
python transaction_analyzer.py sample_transactions.xlsx
```

---

## Troubleshooting

### Issue: "python: command not found" or "python not installed"

**Solution:**
1. Download Python from https://www.python.org/downloads/
2. Windows: Run installer with "Add to PATH" checked
3. macOS: Use Homebrew: `brew install python3`
4. Linux: `sudo apt-get install python3`

---

### Issue: "ModuleNotFoundError: No module named 'pandas'"

**Solution:**
```bash
# Ensure virtual environment is activated
# Windows
venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

---

### Issue: "Permission denied" on macOS/Linux

**Solution:**
```bash
# Use venv (recommended) instead of sudo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Or if needed with sudo:
sudo -H pip install -r requirements.txt
```

---

### Issue: Virtual Environment Not Activating

**Windows:**
```powershell
# Check execution policy
Get-ExecutionPolicy

# If restricted, set to RemoteSigned
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Try activation again
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
# Make sure you're in project directory
pwd  # Verify location
source venv/bin/activate

# Check if activated (should show (venv) prefix)
```

---

### Issue: Excel File Not Found

**Solution:**
```bash
# Check current directory
pwd  # macOS/Linux
cd  # Windows

# Ensure Excel file is in project directory
# Or provide full path:
python transaction_analyzer.py /path/to/your/file.xlsx
```

---

### Issue: "No module named 'matplotlib'"

**Solution:**
```bash
# Verify virtual environment is activated
which python  # Should show path to venv

# Reinstall packages
pip install --upgrade -r requirements.txt
```

---

## Uninstallation

### Remove Virtual Environment

**Windows:**
```powershell
# Deactivate first
deactivate

# Remove venv folder
Remove-Item -Recurse venv
```

**macOS/Linux:**
```bash
# Deactivate first
deactivate

# Remove venv folder
rm -rf venv
```

---

## Next Steps

After successful installation:

1. **Read Quick Start**: Open `QUICKSTART.md`
2. **Generate Sample Data**: `python sample_transactions.py`
3. **Analyze**: `python transaction_analyzer.py`
4. **Visualize**: `python visualize_transactions.py`
5. **Explore API**: Check `API_DOCUMENTATION.md`

---

## Getting Help

### Online Resources
- Python: https://www.python.org/
- Pandas: https://pandas.pydata.org/
- Matplotlib: https://matplotlib.org/

### Common Commands

```bash
# Activate virtual environment
# Windows
venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate

# Deactivate virtual environment
deactivate

# List installed packages
pip list

# Install specific package
pip install package_name

# Upgrade package
pip install --upgrade package_name

# Uninstall package
pip uninstall package_name
```

---

## Environment Variables (Optional)

For advanced users, you can set:

```bash
# Enable debug mode (shows more output)
DEBUG=1

# Specify default input file
TRANSACTION_FILE=/path/to/transactions.xlsx

# Specify output directory
OUTPUT_DIR=/path/to/output
```

---

**Last Updated**: July 2024
**Version**: 1.0
