"""
Fun commands for Highrise bot
Contains entertainment and interactive commands
"""
from highrise import User
import random

class FunCommands:
    def __init__(self, bot):
        self.bot = bot
    
    async def dice(self, user: User, message: str) -> None:
        """Handle !dice command - roll a random number"""
        result = random.randint(1, 6)
        await self.bot.highrise.chat(f"🎲 {user.username} rolled a {result}!")
    
    async def flip(self, user: User, message: str) -> None:
        """Handle !flip command - flip a coin"""
        result = random.choice(["Heads", "Tails"])
        await self.bot.highrise.chat(f"🪙 {user.username} flipped: {result}!")
    
    async def magic8ball(self, user: User, message: str) -> None:
        """Handle !8ball command - magic 8 ball responses"""
        responses = [
            "Yes, definitely! ✨",
            "No way! ❌", 
            "Maybe... 🤔",
            "Ask again later 🔮",
            "Without a doubt! 💯",
            "Very unlikely 😅",
            "The stars say yes! ⭐",
            "I wouldn't count on it 🤷‍♀️"
        ]
        response = random.choice(responses)
        await self.bot.highrise.chat(f"🎱 Magic 8-Ball says: {response}")
    
    async def joke(self, user: User, message: str) -> None:
        """Handle !joke command - tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything! 😄",
            "What do you call a fake noodle? An impasta! 🍝",
            "Why did the scarecrow win an award? He was outstanding in his field! 🌾",
            "What do you call a bear with no teeth? A gummy bear! 🐻"
        ]
        joke = random.choice(jokes)
        await self.bot.highrise.chat(f"😂 {joke}")
