import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
ROOM_ID = os.getenv('ROOM_ID')
BOT_USERNAME = os.getenv('BOT_USERNAME', 'MyBot')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Validate required environment variables
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")

if not ROOM_ID:
    raise ValueError("ROOM_ID environment variable is required")

print(f"Configuration loaded:")
