"""
User events handler for Highrise bot
Handles user join/leave events
"""
from highrise import User
from highrise.models import Position

class UserEvents:
    def __init__(self, bot):
        self.bot = bot
    
    async def on_user_join(self, user: User, position: Position) -> None:
        """Called when a user joins the room"""
        print(f"{user.username} joined the room at position {position}")
        await self.bot.highrise.chat(f"Welcome {user.username}! 🎉")
    
    async def on_user_leave(self, user: User) -> None:
        """Called when a user leaves the room"""
        print(f"{user.username} left the room")
