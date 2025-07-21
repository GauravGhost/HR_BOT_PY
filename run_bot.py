#!/usr/bin/env python3
"""
Secure launcher script for Highrise bot
This script reads credentials from .env file and launches the bot safely
"""
import os
import subprocess
import sys
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get credentials from environment
    bot_token = os.getenv('BOT_TOKEN')
    room_id = os.getenv('ROOM_ID')
    
    # Validate required environment variables
    if not bot_token:
        print("❌ Error: BOT_TOKEN not found in .env file")
        sys.exit(1)
    
    if not room_id:
        print("❌ Error: ROOM_ID not found in .env file")
        sys.exit(1)
    
    print("🚀 Starting Highrise bot...")
    print(f"📍 Room ID: {room_id}")
    print(f"🔑 Token: {'*' * 50}...{bot_token[-8:]}")
    
    try:
        subprocess.run([
            "highrise",
            "bot:Mybot",
            room_id,
            bot_token
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running bot: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Error: 'highrise' command not found. Make sure the SDK is installed.")
        print("💡 Try: pip install highrise-bot-sdk")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
