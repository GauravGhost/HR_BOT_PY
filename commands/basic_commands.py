"""
Basic commands for Highrise bot
Contains simple greeting and help commands
"""
from highrise import User

class BasicCommands:
    def __init__(self, bot):
        self.bot = bot
    
    async def hello(self, user: User, message: str) -> None:
        """Handle !hello command"""
        try:
            await self.bot.highrise.chat(f"Hello {user.username}! 👋")
        except Exception as e:
            print(f"Error in hello command: {e}")
            await self.bot.highrise.chat("Sorry, something went wrong with the hello command.")
    
    async def help(self, user: User, message: str) -> None:
        """Handle !help command"""
        try:
            help_text = """

        
🤖 Available Commands:

📝 Basic:
• !hello - Say hello
• !help - Show this help message

🎮 Fun:
• !dice - Roll a dice (1-6)
• !flip - Flip a coin
• !8ball - Ask the magic 8-ball
• !joke - Get a random joke

More commands coming soon! 🚀
        """.strip()
            await self.bot.highrise.chat(help_text)
        except Exception as e:
            print(f"Error in help command: {e}")
            await self.bot.highrise.chat("Sorry, I couldn't display the help message right now.")

    async def my(self, user: User, message: str) -> None:
        """Handle !my command - shows coordinates for yourself or specified user"""
        try:
            room_users = (await self.bot.highrise.get_room_users()).content
            
            # Check if a specific user is mentioned with @username
            parts = message.strip().split()
            target_username = None
            
            if len(parts) > 1 and parts[1].startswith('@'):
                # Extract username without @
                target_username = parts[1][1:]  # Remove the @ symbol
            else:
                # No specific user mentioned, use the command sender
                target_username = user.username
            
            # Find the target user and their position
            target_found = False
            for user_data in room_users:
                if isinstance(user_data, tuple):
                    # Format: (User, Position)
                    user_obj = user_data[0]
                    position = user_data[1]
                    
                    if user_obj.username.lower() == target_username.lower():
                        target_found = True
                        coords_msg = f"📍 {user_obj.username}'s coordinates:\n"
                        coords_msg += f"X: {position.x} Y: {position.y} Z: {position.z} Facing: {position.facing}"
                        await self.bot.highrise.chat(coords_msg)
                        break
                else:
                    if user_data.username.lower() == target_username.lower():
                        target_found = True
                        await self.bot.highrise.chat(f"Found {user_data.username} but position data not available")
                        break
            
            if not target_found:
                if target_username == user.username:
                    await self.bot.highrise.chat("I couldn't find your position in the room.")
                else:
                    await self.bot.highrise.chat(f"User '{target_username}' not found in the room.")
                    
        except Exception as e:
            print(f"Error in my command: {e}")
            await self.bot.highrise.chat("Sorry, I couldn't get the position information right now. Please try again later.")
