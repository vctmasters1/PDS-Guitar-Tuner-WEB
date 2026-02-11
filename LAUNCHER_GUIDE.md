# Guitar Tuner Web - How to Run

## Quick Start (Easiest)

Double-click one of these files:
- **launch.vbs** - Opens the app with automatic browser window (RECOMMENDED)
- OR **run.bat** - Opens the app with visible command window

## What Each File Does

### launch.vbs
- Double-click to launch
- Opens the app server
- Automatically opens your browser to http://localhost:8501
- Shows status messages in a command window
- Press Ctrl+C to stop the server

### run.bat  
- Double-click to launch
- Opens the app server in a command window
- Automatically opens your browser to http://localhost:8501
- Press Ctrl+C to stop the server

### run.ps1
- Right-click the file and select "Run with PowerShell"
- Opens the app server with colored status messages
- Automatically opens your browser to http://localhost:8501
- Press Ctrl+C to stop the server

## Troubleshooting

If the app doesn't start:
1. Make sure you ran setup.ps1 first (see SETUP_GUIDE.md)
2. Check that the .venv folder exists in the project directory
3. Run setup.ps1 again to verify dependencies are installed

If the browser doesn't open:
1. Manually navigate to http://localhost:8501 in your browser
2. The app should be running there

If you get a PORT error:
1. Another app is using port 8501
2. Close the other app and try again
3. OR modify the port in the command line (see SETUP_GUIDE.md)
