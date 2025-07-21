@echo off
REM Cross-platform runner script for Highrise bot (Windows version)
REM This script activates the virtual environment and runs the bot

echo 🚀 Highrise Bot Launcher
echo ================================

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Error: Virtual environment not found at .venv\Scripts\activate.bat
    echo 💡 Please create a virtual environment first:
    echo    python -m venv .venv
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo ❌ Error: .env file not found
    echo 💡 Please create a .env file with BOT_TOKEN and ROOM_ID
    pause
    exit /b 1
)

echo ✅ Found virtual environment: .venv\Scripts\activate.bat
echo ✅ Found .env file

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

if errorlevel 1 (
    echo ❌ Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment activated

REM Check if requirements are installed
echo 🔍 Checking dependencies...
python -c "import highrise" 2>nul
if errorlevel 1 (
    echo ⚠️  highrise-bot-sdk not found, installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo ✅ Dependencies ready
echo.

REM Run the bot
echo 🤖 Starting Highrise bot...
python run_bot.py

REM Capture exit code
set EXIT_CODE=%errorlevel%

if %EXIT_CODE% equ 0 (
    echo ✅ Bot exited successfully
) else (
    echo ❌ Bot exited with error code: %EXIT_CODE%
)

pause
exit /b %EXIT_CODE%
