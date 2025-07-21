#!/bin/bash
"""
Cross-platform runner script for Highrise bot
This script activates the virtual environment and runs the bot
"""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Highrise Bot Launcher${NC}"
echo "================================"

# Detect operating system
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || [[ "$OS" == "Windows_NT" ]]; then
    # Windows (Git Bash, WSL, etc.)
    VENV_ACTIVATE=".venv/Scripts/activate"
    PYTHON_CMD="python"
else
    # Unix-like systems (Linux, macOS)
    VENV_ACTIVATE=".venv/bin/activate"
    PYTHON_CMD="python3"
fi

# Check if virtual environment exists
if [ ! -f "$VENV_ACTIVATE" ]; then
    echo -e "${RED}❌ Error: Virtual environment not found at $VENV_ACTIVATE${NC}"
    echo -e "${YELLOW}💡 Please create a virtual environment first:${NC}"
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || [[ "$OS" == "Windows_NT" ]]; then
        echo "   python -m venv .venv"
    else
        echo "   python3 -m venv .venv"
    fi
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Error: .env file not found${NC}"
    echo -e "${YELLOW}💡 Please create a .env file with BOT_TOKEN and ROOM_ID${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Found virtual environment: $VENV_ACTIVATE${NC}"
echo -e "${GREEN}✅ Found .env file${NC}"

# Activate virtual environment
echo -e "${YELLOW}🔄 Activating virtual environment...${NC}"
source "$VENV_ACTIVATE"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error: Failed to activate virtual environment${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Check if requirements are installed
echo -e "${YELLOW}🔍 Checking dependencies...${NC}"
if ! $PYTHON_CMD -c "import highrise" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  highrise-bot-sdk not found, installing dependencies...${NC}"
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Error: Failed to install dependencies${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ Dependencies ready${NC}"
echo ""

# Run the bot
echo -e "${BLUE}🤖 Starting Highrise bot...${NC}"
$PYTHON_CMD run_bot.py

# Capture exit code
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Bot exited successfully${NC}"
else
    echo -e "${RED}❌ Bot exited with error code: $EXIT_CODE${NC}"
fi

exit $EXIT_CODE
