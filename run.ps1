# Guitar Tuner Web - PowerShell Launcher
# This script sets up and runs the Guitar Tuner web app

$Host.UI.RawUI.BackgroundColor = "Black"
$Host.UI.RawUI.ForegroundColor = "Green"
Clear-Host

Write-Host ""
Write-Host "======================================"
Write-Host "  [*] Guitar Tuner Web - Launcher"
Write-Host "======================================"
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path ".venv")) {
    Write-Host "[!] Virtual environment not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run setup first:" -ForegroundColor Yellow
    Write-Host "  .\setup.ps1" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Press Enter to close"
    exit 1
}

# Activate virtual environment
$activateScript = ".\.venv\Scripts\Activate.ps1"
if (-not (Test-Path $activateScript)) {
    Write-Host "[!] Failed to find activation script" -ForegroundColor Red
    Read-Host "Press Enter to close"
    exit 1
}

try {
    & $activateScript
} catch {
    Write-Host "[!] Failed to activate virtual environment" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host "Press Enter to close"
    exit 1
}

Write-Host "[+] Virtual environment activated" -ForegroundColor Green

# Check if streamlit is installed
try {
    python -c "import streamlit" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Streamlit not found"
    }
} catch {
    Write-Host "[!] Streamlit not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run setup first:" -ForegroundColor Yellow
    Write-Host "  .\setup.ps1" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Press Enter to close"
    exit 1
}

Write-Host "[+] Dependencies verified" -ForegroundColor Green
Write-Host ""
Write-Host "Starting Guitar Tuner Web..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening browser to http://localhost:8501" -ForegroundColor Yellow
Write-Host "(If browser doesn't open, manually navigate to that address)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "======================================"
Write-Host ""

# Run the Streamlit app
try {
    & streamlit run app.py --logger.level=warning
    $exitCode = $LASTEXITCODE
} catch {
    Write-Host ""
    Write-Host "[!] Application error occurred:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Check the error message above for details." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "If you need help, see:" -ForegroundColor Yellow
    Write-Host "  - SETUP_GUIDE.md" -ForegroundColor Cyan
    Write-Host "  - README.md" -ForegroundColor Cyan
    Write-Host "  - AI-Instruct.md" -ForegroundColor Cyan
    Write-Host ""
    $exitCode = 1
}

# Restore colors
$Host.UI.RawUI.ForegroundColor = [System.ConsoleColor]::White

Write-Host ""
if ($exitCode -eq 0) {
    Write-Host "[+] Application closed normally" -ForegroundColor Green
} else {
    Write-Host "[!] Application exited with error code: $exitCode" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to close this window"
exit $exitCode
