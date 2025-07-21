#!/usr/bin/env python3
"""
Setup script for Highrise Bot
This script helps new users set up the bot quickly
"""

import os
import sys
import subprocess
import shutil

def print_header():
    print("=" * 60)
    print("🤖 HIGHRISE BOT SETUP SCRIPT")
    print("   Compatible with Python 3.8 - 3.11")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible, auto-restart with Python 3.11 if needed"""
    version = sys.version_info
    
    # If we're running on Python 3.12+ but 3.11 is available, restart with 3.11
    if version.major > 3 or (version.major == 3 and version.minor > 11):
        print(f"⚠️  Detected Python {version.major}.{version.minor}.{version.micro} (too new)")
        print("🔄 Attempting to restart with Python 3.11...")
        
        try:
            if os.name == 'nt':  # Windows
                # Try to restart with py -3.11
                subprocess.run(["py", "-3.11", __file__] + sys.argv[1:], check=True)
                return "restarted"
            else:  # macOS/Linux
                subprocess.run(["python3.11", __file__] + sys.argv[1:], check=True)
                return "restarted"
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Python 3.11 not found!")
            print("   Please install Python 3.11 and try again.")
            print("   Or run manually: py -3.11 setup.py")
            return False
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade to Python 3.8-3.11 and try again.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected (compatible)")
    return True

def create_virtual_environment():
    """Create a virtual environment if it doesn't exist"""
    venv_path = ".venv"
    
    if os.path.exists(venv_path):
        print(f"✅ Virtual environment already exists at {venv_path}")
        return True
    
    print("📦 Creating virtual environment with Python 3.11...")
    try:
        # Try using py launcher for Python 3.11 on Windows
        if os.name == 'nt':
            subprocess.run(["py", "-3.11", "-m", "venv", venv_path], check=True)
        else:
            # For macOS/Linux, try python3.11 first, fallback to python3
            try:
                subprocess.run(["python3.11", "-m", "venv", venv_path], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                subprocess.run(["python3", "-m", "venv", venv_path], check=True)
        
        print(f"✅ Virtual environment created at {venv_path}")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        print("   Make sure Python 3.11 is installed and try running manually:")
        print("   py -3.11 -m venv .venv")
        return False
    except FileNotFoundError:
        print("❌ Python 3.11 not found!")
        print("   Please install Python 3.11 or run manually:")
        print("   py -3.11 -m venv .venv")
        return False

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    # Determine the correct pip path based on OS
    if os.name == 'nt':  # Windows
        pip_path = os.path.join(".venv", "Scripts", "pip.exe")
    else:  # macOS/Linux
        pip_path = os.path.join(".venv", "bin", "pip")
    
    try:
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages")
        print("   Try running manually: pip install -r requirements.txt")
        return False

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    env_file = ".env"
    example_file = ".env.example"
    
    if os.path.exists(env_file):
        print("✅ .env file already exists")
        return True
    
    if not os.path.exists(example_file):
        print("❌ .env.example file not found!")
        return False
    
    print("📝 Creating .env file from template...")
    try:
        shutil.copy(example_file, env_file)
        print("✅ .env file created from template")
        print()
        print("🔧 IMPORTANT: You need to edit .env with your bot credentials:")
        print()
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def show_next_steps():
    """Show what the user needs to do next"""
    print("🎉 Setup complete! Next steps:")
    print()
    print("1. 📝 Edit your .env file:")
    print("   - Open .env in a text editor")
    print("   - Replace 'your_bot_token_here' with your actual bot token")
    print("   - Replace 'your_room_id_here' with your actual room ID")
    print()
    print("2. 🏃 Run your bot:")
    if os.name == 'nt':  # Windows
        print("   For Windows: .\\run.bat")
    else:  # macOS/Linux
        print("   For macOS/Linux: ./run.sh")
    print()

def main():
    print_header()
    
    # Check Python version
    version_check = check_python_version()
    if version_check == "restarted":
        return 0
    elif not version_check:
        return 1
    
    # Create virtual environment
    if not create_virtual_environment():
        return 1
    
    # Install requirements
    if not install_requirements():
        return 1
    
    # Create .env file
    if not create_env_file():
        return 1
    
    show_next_steps()
    return 0

if __name__ == "__main__":
    sys.exit(main())
