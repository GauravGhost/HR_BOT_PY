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
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python and try again.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_virtual_environment():
    """Create a virtual environment if it doesn't exist"""
    venv_path = ".venv"
    
    if os.path.exists(venv_path):
        print(f"✅ Virtual environment already exists at {venv_path}")
        return True
    
    print("📦 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        print(f"✅ Virtual environment created at {venv_path}")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
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
        print("   .venv\\Scripts\\python.exe bot.py")
    else:  # macOS/Linux
        print("   .venv/bin/python bot.py")
    print()

def main():
    print_header()
    
    # Check Python version
    if not check_python_version():
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
