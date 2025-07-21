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
        await self.bot.highrise.chat(f"Hello {user.username}! 👋")
    
    async def help(self, user: User, message: str) -> None:
        """Handle !help command"""
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
