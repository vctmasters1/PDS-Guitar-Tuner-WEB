# Guitar Tuner Web - Setup Script (Windows PowerShell)
# This script sets up the development environment and verifies all dependencies

param(
    [switch]$SkipVenv = $false,
    [switch]$Force = $false
)

$ErrorActionPreference = "Stop"
Write-Host "🎸 Guitar Tuner Web - Setup Script" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Colors for output
$InfoColor = "Cyan"
$SuccessColor = "Green"
$ErrorColor = "Red"
$WarningColor = "Yellow"

function Write-Info { Write-Host "ℹ️  $args" -ForegroundColor $InfoColor }
function Write-Success { Write-Host "✓ $args" -ForegroundColor $SuccessColor }
function Write-Error-Custom { Write-Host "✗ $args" -ForegroundColor $ErrorColor }
function Write-Warning { Write-Host "⚠ $args" -ForegroundColor $WarningColor }

# Step 1: Check Python installation
Write-Host ""
Write-Host "Step 1: Checking Python Installation..." -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta

try {
    $pythonVersion = python --version 2>&1
    Write-Success "Python found: $pythonVersion"
} catch {
    Write-Error-Custom "Python not found! Please install Python 3.9+ from python.org"
    exit 1
}

# Step 2: Check if venv exists
Write-Host ""
Write-Host "Step 2: Virtual Environment Setup..." -ForegroundColor Magenta
Write-Host "====================================" -ForegroundColor Magenta

$venvPath = ".venv"
$venvExists = Test-Path $venvPath

if ($venvExists -and -not $Force) {
    Write-Info "Virtual environment already exists at $venvPath"
    $response = Read-Host "Recreate it? (y/n)"
    if ($response -ne "y") {
        Write-Info "Skipping venv creation"
    } else {
        Write-Info "Removing existing venv..."
        Remove-Item -Recurse -Force $venvPath
        python -m venv $venvPath
        Write-Success "New virtual environment created"
    }
} else {
    if ($SkipVenv) {
        Write-Warning "Skipping venv creation (-SkipVenv flag set)"
    } else {
        Write-Info "Creating virtual environment..."
        python -m venv $venvPath
        Write-Success "Virtual environment created at $venvPath"
    }
}

# Step 3: Activate venv
Write-Host ""
Write-Host "Step 3: Activating Virtual Environment..." -ForegroundColor Magenta
Write-Host "=========================================" -ForegroundColor Magenta

$activateScript = Join-Path $venvPath "Scripts" "Activate.ps1"

if (Test-Path $activateScript) {
    & $activateScript
    Write-Success "Virtual environment activated"
} else {
    Write-Error-Custom "Could not find activation script at $activateScript"
    exit 1
}

# Step 4: Upgrade pip
Write-Host ""
Write-Host "Step 4: Upgrading pip..." -ForegroundColor Magenta
Write-Host "========================" -ForegroundColor Magenta

Write-Info "Upgrading pip to latest version..."
python -m pip install --upgrade pip 2>&1 | Out-Null
Write-Success "pip upgraded"

# Step 5: Install dependencies
Write-Host ""
Write-Host "Step 5: Installing Dependencies..." -ForegroundColor Magenta
Write-Host "==================================" -ForegroundColor Magenta

if (-not (Test-Path "requirements.txt")) {
    Write-Error-Custom "requirements.txt not found!"
    exit 1
}

Write-Info "Reading requirements from requirements.txt..."
$requirementCount = @(Get-Content requirements.txt | Where-Object { $_ -and -not $_.StartsWith("#") }).Count
Write-Info "Installing $requirementCount packages..."

pip install -r requirements.txt
Write-Success "All dependencies installed"

# Step 6: Verify installation
Write-Host ""
Write-Host "Step 6: Verifying Installation..." -ForegroundColor Magenta
Write-Host "==================================" -ForegroundColor Magenta

$requiredModules = @("streamlit", "numpy", "scipy", "streamlit-webrtc")
$allGood = $true

foreach ($module in $requiredModules) {
    try {
        python -c "import $module" 2>&1 | Out-Null
        Write-Success "$module is installed"
    } catch {
        Write-Error-Custom "$module is NOT installed"
        $allGood = $false
    }
}

# Step 7: Verify project structure
Write-Host ""
Write-Host "Step 7: Verifying Project Structure..." -ForegroundColor Magenta
Write-Host "======================================" -ForegroundColor Magenta

$requiredFiles = @(
    "app.py",
    "requirements.txt",
    "AI-Instruct.md",
    "src/core/config.py",
    "src/core/tuner.py",
    "src/audio/capture.py",
    "src/ui/header.py",
    "src/state/session.py"
)

$structureOk = $true

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Success "$file present"
    } else {
        Write-Error-Custom "$file MISSING"
        $structureOk = $false
    }
}

# Final Summary
Write-Host ""
Write-Host "Setup Summary" -ForegroundColor Magenta
Write-Host "=============" -ForegroundColor Magenta

if ($allGood -and $structureOk) {
    Write-Success "Setup completed successfully!"
    Write-Host ""
    Write-Info "Next steps:"
    Write-Host "  1. Run: streamlit run app.py"
    Write-Host "  2. Open browser to http://localhost:8501"
    Write-Host "  3. Grant microphone permissions when prompted"
    Write-Host ""
    Write-Info "Documentation: See README.md and QUICKSTART.md"
} else {
    Write-Error-Custom "Setup completed with errors. Check above for details."
    exit 1
}

Write-Host ""
