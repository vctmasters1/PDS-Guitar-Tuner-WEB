# Setup Guide - Guitar Tuner Web

Welcome! This guide will help you get the Guitar Tuner Web project up and running on your machine.

## Prerequisites

Before running the setup script, ensure you have:

- **Python 3.9 or later** installed
- **Git** (optional, but recommended)
- A **modern web browser** (Chrome, Firefox, Edge, Safari)
- A **microphone** for audio input

### Check Python Installation

Open your terminal/PowerShell and run:

```bash
python --version
```

If Python is not found, download and install it from [python.org](https://www.python.org/downloads/)

---

## Quick Setup (Recommended)

### Windows (PowerShell)

1. **Open PowerShell** in the project directory
2. **Run the setup script:**
   ```powershell
   .\setup.ps1
   ```
3. **Follow the prompts** to set up the environment
4. **Activate the virtual environment:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
5. **Start the application:**
   ```powershell
   streamlit run app.py
   ```

### macOS / Linux

1. **Open Terminal** in the project directory
2. **Make the script executable:**
   ```bash
   chmod +x setup.sh
   ```
3. **Run the setup script:**
   ```bash
   ./setup.sh
   ```
4. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```
5. **Start the application:**
   ```bash
   streamlit run app.py
   ```

### Cross-Platform (Python Script)

1. **Open terminal/PowerShell** in the project directory
2. **Run the Python setup script:**
   ```bash
   python setup.py
   ```
3. **Activate the virtual environment:**
   - **Windows:** `.\.venv\Scripts\Activate.ps1`
   - **macOS/Linux:** `source .venv/bin/activate`
4. **Start the application:**
   ```bash
   streamlit run app.py
   ```

---

## Manual Setup (If Scripts Don't Work)

If you prefer to set up manually or the scripts encounter issues:

### Step 1: Create Virtual Environment

```bash
python -m venv .venv
```

### Step 2: Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### Step 3: Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Verify Installation

```bash
python -c "import streamlit; import numpy; import scipy; print('✓ All dependencies installed')"
```

### Step 6: Run the Application

```bash
streamlit run app.py
```

---

## Troubleshooting

### Issue: "Python not found" or "ModuleNotFoundError"

**Solution:** Ensure you're using the correct Python in the virtual environment:

```bash
# Windows
.\.venv\Scripts\python.exe -m pip list

# macOS/Linux
./.venv/bin/python -m pip list
```

### Issue: Port 8501 already in use

**Solution:** Run Streamlit on a different port:

```bash
streamlit run app.py --server.port 8502
```

### Issue: Microphone not accessing

**Solution:**
1. Check browser permissions (look for icon in address bar)
2. Try a different browser
3. Verify your microphone works on your system

### Issue: Virtual Environment Activation Fails (Windows PowerShell)

**Solution:** If you get an execution policy error, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

### Issue: Module not found after installation

**Solution:** Make sure the virtual environment is activated:

```bash
# Check if activated (should show .venv prefix)
python -m site

# If not, activate it:
# Windows: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate

# Then reinstall:
pip install -r requirements.txt
```

---

## What the Setup Scripts Do

### setup.py (Cross-platform)
- ✓ Checks Python installation
- ✓ Creates virtual environment
- ✓ Upgrades pip
- ✓ Installs dependencies from requirements.txt
- ✓ Verifies all required packages
- ✓ Checks project structure integrity

### setup.ps1 (Windows PowerShell)
- Same as setup.py, with Windows-specific activation

### setup.sh (macOS/Linux)
- Same as setup.py, with Unix-specific activation

---

## Verifying Your Setup

After setup, verify everything is working:

```bash
# 1. Check virtual environment is active
which python    # macOS/Linux
where python    # Windows PowerShell

# 2. Check dependencies
pip list

# 3. Verify project structure
ls -la          # macOS/Linux
dir             # Windows

# 4. Check Python imports
python -c "from src.ui import *; from src.core import *; print('✓ Imports OK')"
```

---

## Running the Application

Once setup is complete:

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Features you should see:
- ⚙️ Sidebar with tuning settings
- 🎸 Six guitar string rows with target frequencies
- ⌨️ Interactive vertical piano keyboard
- 🎤 Microphone input status

---

## Next Steps

1. **Read the documentation:**
   - [README.md](README.md) - Project overview
   - [QUICKSTART.md](QUICKSTART.md) - Quick start guide
   - [AI-Instruct.md](AI-Instruct.md) - Architecture & guidelines

2. **Try the tuner:**
   - Grant microphone access when prompted
   - Select a tuning preset
   - Pluck a guitar string near your microphone
   - Watch the tuning indicator

3. **Adjust settings:**
   - Try different temperament systems (Equal vs Just Intonation)
   - Adjust the tuning tolerance
   - Explore the interactive piano keyboard

---

## Getting Help

- Check [AI-Instruct.md](AI-Instruct.md) for architecture details
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- Check error messages in the terminal/console

---

## Project Structure Reference

After setup, your project should look like:

```
Guitar-Tuner-WEB/
├── .venv/                  # Virtual environment (created by setup)
├── app.py                  # Main Streamlit app
├── requirements.txt        # Dependencies
├── setup.ps1              # Windows setup script
├── setup.sh               # macOS/Linux setup script
├── setup.py               # Cross-platform setup script
├── README.md              # Project readme
├── QUICKSTART.md          # Quick start guide
├── AI-Instruct.md         # Architecture guidelines
├── src/
│   ├── core/              # Core business logic
│   ├── audio/             # Audio processing
│   ├── ui/                # User interface
│   └── state/             # Session state
└── .old/                  # Archived files (git ignored)
```

---

## Happy Tuning! 🎸

If you have issues, refer to the troubleshooting section above or check the project documentation.
