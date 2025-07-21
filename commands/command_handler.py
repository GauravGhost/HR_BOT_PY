"""
Command handler for Highrise bot
Routes commands to appropriate handlers
"""
from highrise import User
from .basic_commands import BasicCommands
from .fun_commands import FunCommands

class CommandHandler:
    def __init__(self, bot):
        self.bot = bot
        self.basic_commands = BasicCommands(bot)
        self.fun_commands = FunCommands(bot)
        
        # Command mapping
        self.commands = {
            # Basic commands
            "!hello": self.basic_commands.hello,
            "!help": self.basic_commands.help,
            "!my": self.basic_commands.my,
            
            # Fun commands
            "!dice": self.fun_commands.dice,
            "!flip": self.fun_commands.flip,
            "!8ball": self.fun_commands.magic8ball,
            "!joke": self.fun_commands.joke,
        }
    
    async def handle_command(self, user: User, message: str) -> None:
        """Handle incoming commands"""
        # Extract command (first word)
        command = message.split()[0].lower()
        
        if command in self.commands:
            await self.commands[command](user, message)
        else:
            await self.bot.highrise.chat(f"Unknown command: {command}. Type !help for available commands.")
