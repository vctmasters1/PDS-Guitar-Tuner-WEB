#!/bin/bash

# Guitar Tuner Web - Setup Script (Linux/Mac)
# This script sets up the development environment and verifies all dependencies

set -e

echo "🎸 Guitar Tuner Web - Setup Script"
echo "==================================="
echo ""

SKIP_VENV=false
FORCE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-venv)
            SKIP_VENV=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Colors for output
INFO_COLOR='\033[0;36m'      # Cyan
SUCCESS_COLOR='\033[0;32m'   # Green
ERROR_COLOR='\033[0;31m'     # Red
WARNING_COLOR='\033[1;33m'   # Yellow
NC='\033[0m'                 # No Color

info() { echo -e "${INFO_COLOR}ℹ️  $1${NC}"; }
success() { echo -e "${SUCCESS_COLOR}✓ $1${NC}"; }
error() { echo -e "${ERROR_COLOR}✗ $1${NC}"; }
warning() { echo -e "${WARNING_COLOR}⚠ $1${NC}"; }

# Step 1: Check Python installation
echo ""
echo -e "\033[0;35mStep 1: Checking Python Installation...\033[0m"
echo "========================================"

if ! command -v python3 &> /dev/null; then
    error "Python3 not found! Please install Python 3.9+ from python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
success "Python found: $PYTHON_VERSION"

# Step 2: Check if venv exists
echo ""
echo -e "\033[0;35mStep 2: Virtual Environment Setup...\033[0m"
echo "===================================="

VENV_PATH=".venv"

if [ -d "$VENV_PATH" ] && [ "$FORCE" = false ]; then
    info "Virtual environment already exists at $VENV_PATH"
    read -p "Recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        info "Removing existing venv..."
        rm -rf "$VENV_PATH"
        python3 -m venv "$VENV_PATH"
        success "New virtual environment created"
    else
        info "Skipping venv creation"
    fi
else
    if [ "$SKIP_VENV" = true ]; then
        warning "Skipping venv creation (--skip-venv flag set)"
    else
        info "Creating virtual environment..."
        python3 -m venv "$VENV_PATH"
        success "Virtual environment created at $VENV_PATH"
    fi
fi

# Step 3: Activate venv
echo ""
echo -e "\033[0;35mStep 3: Activating Virtual Environment...\033[0m"
echo "========================================="

ACTIVATE_SCRIPT="$VENV_PATH/bin/activate"

if [ ! -f "$ACTIVATE_SCRIPT" ]; then
    error "Could not find activation script at $ACTIVATE_SCRIPT"
    exit 1
fi

source "$ACTIVATE_SCRIPT"
success "Virtual environment activated"

# Step 4: Upgrade pip
echo ""
echo -e "\033[0;35mStep 4: Upgrading pip...\033[0m"
echo "========================"

info "Upgrading pip to latest version..."
python -m pip install --upgrade pip > /dev/null
success "pip upgraded"

# Step 5: Install dependencies
echo ""
echo -e "\033[0;35mStep 5: Installing Dependencies...\033[0m"
echo "=================================="

if [ ! -f "requirements.txt" ]; then
    error "requirements.txt not found!"
    exit 1
fi

info "Reading requirements from requirements.txt..."
REQUIREMENT_COUNT=$(grep -v '^#' requirements.txt | grep -v '^$' | wc -l)
info "Installing $REQUIREMENT_COUNT packages..."

pip install -r requirements.txt
success "All dependencies installed"

# Step 6: Verify installation
echo ""
echo -e "\033[0;35mStep 6: Verifying Installation...\033[0m"
echo "=================================="

REQUIRED_MODULES=("streamlit" "numpy" "scipy" "streamlit_webrtc")
ALL_GOOD=true

for module in "${REQUIRED_MODULES[@]}"; do
    if python -c "import $module" 2>/dev/null; then
        success "$module is installed"
    else
        error "$module is NOT installed"
        ALL_GOOD=false
    fi
done

# Step 7: Verify project structure
echo ""
echo -e "\033[0;35mStep 7: Verifying Project Structure...\033[0m"
echo "======================================"

REQUIRED_FILES=(
    "app.py"
    "requirements.txt"
    "AI-Instruct.md"
    "src/core/config.py"
    "src/core/tuner.py"
    "src/audio/capture.py"
    "src/ui/header.py"
    "src/state/session.py"
)

STRUCTURE_OK=true

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        success "$file present"
    else
        error "$file MISSING"
        STRUCTURE_OK=false
    fi
done

# Final Summary
echo ""
echo -e "\033[0;35mSetup Summary\033[0m"
echo "============="

if [ "$ALL_GOOD" = true ] && [ "$STRUCTURE_OK" = true ]; then
    success "Setup completed successfully!"
    echo ""
    info "Next steps:"
    echo "  1. Run: streamlit run app.py"
    echo "  2. Open browser to http://localhost:8501"
    echo "  3. Grant microphone permissions when prompted"
    echo ""
    info "Documentation: See README.md and QUICKSTART.md"
else
    error "Setup completed with errors. Check above for details."
    exit 1
fi

echo ""
