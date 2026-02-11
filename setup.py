"""
Guitar Tuner Web - Cross-platform Setup Script

This script handles:
- Creating virtual environment
- Installing dependencies
- Verifying installation
- Checking project structure
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class SetupManager:
    """Handles project setup and verification"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / ".venv"
        self.os_type = platform.system()
        self.all_good = True
    
    def print_header(self, text):
        """Print a section header"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 50}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 50}{Colors.RESET}")
    
    def print_info(self, text):
        """Print info message"""
        print(f"{Colors.CYAN}ℹ️  {text}{Colors.RESET}")
    
    def print_success(self, text):
        """Print success message"""
        print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")
    
    def print_error(self, text):
        """Print error message"""
        print(f"{Colors.RED}✗ {text}{Colors.RESET}")
        self.all_good = False
    
    def print_warning(self, text):
        """Print warning message"""
        print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")
    
    def run_command(self, cmd, shell=False):
        """Run a command and return success status"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=shell,
                cwd=self.project_root
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def check_python(self):
        """Check Python installation"""
        self.print_header("Step 1: Checking Python Installation")
        
        success, stdout, _ = self.run_command([sys.executable, "--version"])
        if success:
            version = stdout.strip()
            self.print_success(f"Python found: {version}")
            return True
        else:
            self.print_error("Python not found or not accessible")
            return False
    
    def setup_venv(self):
        """Create or verify virtual environment"""
        self.print_header("Step 2: Virtual Environment Setup")
        
        if self.venv_path.exists():
            self.print_info(f"Virtual environment already exists at {self.venv_path}")
            response = input(f"{Colors.CYAN}Recreate it? (y/n): {Colors.RESET}").strip().lower()
            if response == 'y':
                import shutil
                self.print_info("Removing existing venv...")
                shutil.rmtree(self.venv_path)
                self._create_venv()
            else:
                self.print_info("Skipping venv creation")
        else:
            self._create_venv()
        
        return self.venv_path.exists()
    
    def _create_venv(self):
        """Actually create the virtual environment"""
        self.print_info("Creating virtual environment...")
        success, _, stderr = self.run_command([sys.executable, "-m", "venv", str(self.venv_path)])
        
        if success:
            self.print_success(f"Virtual environment created at {self.venv_path}")
        else:
            self.print_error(f"Failed to create venv: {stderr}")
    
    def get_python_exe(self):
        """Get the Python executable path in the venv"""
        if self.os_type == "Windows":
            return self.venv_path / "Scripts" / "python.exe"
        else:
            return self.venv_path / "bin" / "python"
    
    def upgrade_pip(self):
        """Upgrade pip in the virtual environment"""
        self.print_header("Step 3: Upgrading pip")
        
        python_exe = self.get_python_exe()
        self.print_info("Upgrading pip to latest version...")
        
        success, _, stderr = self.run_command([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"])
        
        if success:
            self.print_success("pip upgraded successfully")
        else:
            self.print_warning(f"Failed to upgrade pip: {stderr}")
    
    def install_dependencies(self):
        """Install project dependencies"""
        self.print_header("Step 4: Installing Dependencies")
        
        req_file = self.project_root / "requirements.txt"
        
        if not req_file.exists():
            self.print_error("requirements.txt not found!")
            return False
        
        # Count requirements
        with open(req_file) as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
        self.print_info(f"Found {len(requirements)} packages to install...")
        
        python_exe = self.get_python_exe()
        success, stdout, stderr = self.run_command([str(python_exe), "-m", "pip", "install", "-r", str(req_file)])
        
        if success:
            self.print_success("All dependencies installed successfully")
            return True
        else:
            self.print_error(f"Failed to install dependencies: {stderr}")
            return False
    
    def verify_packages(self):
        """Verify that required packages are installed"""
        self.print_header("Step 5: Verifying Installation")
        
        python_exe = self.get_python_exe()
        required_modules = ["streamlit", "numpy", "scipy", "streamlit_webrtc"]
        
        all_installed = True
        for module in required_modules:
            success, _, _ = self.run_command(
                [str(python_exe), "-c", f"import {module}"]
            )
            
            if success:
                self.print_success(f"{module} is installed")
            else:
                self.print_error(f"{module} is NOT installed")
                all_installed = False
        
        return all_installed
    
    def verify_structure(self):
        """Verify project structure"""
        self.print_header("Step 6: Verifying Project Structure")
        
        required_files = [
            "app.py",
            "requirements.txt",
            "AI-Instruct.md",
            "src/core/config.py",
            "src/core/tuner.py",
            "src/audio/capture.py",
            "src/ui/header.py",
            "src/state/session.py",
        ]
        
        all_exist = True
        for file_path in required_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                self.print_success(f"{file_path} present")
            else:
                self.print_error(f"{file_path} MISSING")
                all_exist = False
        
        return all_exist
    
    def print_summary(self):
        """Print final summary and next steps"""
        self.print_header("Setup Summary")
        
        if self.all_good:
            self.print_success("Setup completed successfully!")
            print(f"\n{Colors.CYAN}Next steps:{Colors.RESET}")
            print(f"  1. Activate: {self._get_activation_command()}")
            print(f"  2. Run: streamlit run app.py")
            print(f"  3. Open browser to http://localhost:8501")
            print(f"  4. Grant microphone permissions when prompted")
            print(f"\n{Colors.CYAN}Documentation:{Colors.RESET}")
            print(f"  - See README.md for overview")
            print(f"  - See QUICKSTART.md for quick start")
            print(f"  - See AI-Instruct.md for architecture")
        else:
            self.print_error("Setup completed with errors. Check above for details.")
    
    def _get_activation_command(self):
        """Get the activation command for the current OS"""
        if self.os_type == "Windows":
            return ".venv\\Scripts\\Activate.ps1"
        else:
            return "source .venv/bin/activate"
    
    def run(self):
        """Run the entire setup process"""
        print(f"{Colors.BOLD}{Colors.CYAN}🎸 Guitar Tuner Web - Setup Script{Colors.RESET}")
        print(f"{Colors.CYAN}Platform: {self.os_type}{Colors.RESET}\n")
        
        # Run all steps
        if not self.check_python():
            self.print_error("Cannot proceed without Python")
            return False
        
        if not self.setup_venv():
            self.print_error("Failed to set up virtual environment")
            return False
        
        self.upgrade_pip()
        
        if not self.install_dependencies():
            self.print_error("Failed to install dependencies")
            return False
        
        if not self.verify_packages():
            self.print_error("Some packages failed verification")
        
        if not self.verify_structure():
            self.print_error("Some project files are missing")
        
        self.print_summary()
        
        return self.all_good


if __name__ == "__main__":
    manager = SetupManager()
    success = manager.run()
    sys.exit(0 if success else 1)
