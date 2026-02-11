# How to Run Guitar Tuner Web

## Quick Start - Easiest Methods

### Option 1: Double-Click `run.bat` (Windows) ✅ RECOMMENDED

1. **Find** `run.bat` in the project folder
2. **Double-click** it
3. The app will automatically start and open in your browser
4. Your terminal will stay open so you can see any errors
5. **Press Ctrl+C** in the terminal to stop the server

### Option 2: Use PowerShell Script

1. **Open PowerShell** in the project folder
2. **Run:**
   ```powershell
   .\run.ps1
   ```
3. The app will start automatically
4. Browser will open to `http://localhost:8501`
5. **Press Ctrl+C** to stop

### Option 3: Manual Command Line

```bash
# Activate virtual environment
.venv\Scripts\activate.bat          # Windows CMD
# OR
.\.venv\Scripts\Activate.ps1        # Windows PowerShell
# OR
source .venv/bin/activate           # macOS/Linux

# Start the app
streamlit run app.py
```

---

## What Each Script Does

### `run.bat` (Windows Batch)
- ✅ Automatically activates virtual environment
- ✅ Checks if dependencies are installed
- ✅ Starts the Streamlit app
- ✅ Keeps window open (shows errors/info)
- ✅ Waits for Enter before closing

### `run.ps1` (PowerShell)
- ✅ Same as `run.bat` but with color-coded output
- ✅ Better error messages
- ✅ Easier to read

---

## Troubleshooting

### Window closes immediately when double-clicking `run.bat`

**Solution:** Virtual environment not set up. Run setup first:
```powershell
.\setup.ps1
```

### "Port already in use" error

**Solution:** Run on a different port:
```bash
streamlit run app.py --server.port 8502
```

### "Python not found" error

**Solution:** Python isn't in your PATH. Do this:
1. Open the `run.bat` file with a text editor
2. Change the first two lines to use full path to Python:
   ```
   "C:\Users\YourUsername\AppData\Local\Programs\Python\Python313\python.exe" -m venv .venv
   ```
3. Save and try again

### Browser doesn't open automatically

**Solution:** Manually navigate to `http://localhost:8501` in your browser

---

## After Launch

Once the app is running:

1. ✅ Your browser should open to `http://localhost:8501`
2. ✅ Grant microphone permissions when prompted
3. ✅ Select your tuning reference (default: 440 Hz)
4. ✅ Pluck a guitar string
5. ✅ Watch the tuning feedback!

---

## Stopping the App

- **In Windows:** Press `Ctrl+C` in the terminal
- **Browser:** Just close the browser tab (app continues in terminal)
- **Full stop:** Press `Ctrl+C`, then close the terminal window

---

## Next Time

After first setup, you can just double-click `run.bat` anytime you want to use the tuner!

Happy tuning! 🎸🎵
