"""
Session events handler for Highrise bot
Handles bot startup and session-related events
"""
from highrise.models import SessionMetadata
from config import BOT_USERNAME

class SessionEvents:
    def __init__(self, bot):
        self.bot = bot
    
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        """Called when the bot starts and connects to the room"""
        print(f"Bot {BOT_USERNAME} has started!")
        print(f"Session metadata: {session_metadata}")
        
        # Send a welcome message when the bot joins
        await self.bot.highrise.chat("Hello everyone! I'm now online! 👋")
