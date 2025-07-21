"""
Chat events handler for Highrise bot
Handles all chat-related events and command processing
"""
from highrise import User
from commands.command_handler import CommandHandler

class ChatEvents:
    def __init__(self, bot):
        self.bot = bot
        self.command_handler = CommandHandler(bot)
    
    async def on_chat(self, user: User, message: str) -> None:
        """Called when someone sends a chat message"""
        print(f"{user.username}: {message}")
        
        # Check if it's a command (starts with !)
        if message.startswith("!"):
            await self.command_handler.handle_command(user, message)
        else:
            # Handle regular chat messages here if needed
            pass
