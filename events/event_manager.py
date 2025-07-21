"""
Event Manager for Highrise bot
Centralizes all event handling
"""
from events.chat_events import ChatEvents
from events.user_events import UserEvents
from events.session_events import SessionEvents
from utils.logger import BotLogger

class EventManager:
    def __init__(self, bot):
        self.bot = bot
        self.logger = BotLogger("EventManager")
        
        # Initialize event handlers
        self.chat_events = ChatEvents(bot)
        self.user_events = UserEvents(bot)
        self.session_events = SessionEvents(bot)
        
        self.logger.info("Event Manager initialized")
    
    # Session Events
    async def on_start(self, session_metadata):
        """Delegate to session events handler"""
        await self.session_events.on_start(session_metadata)
    
    # Chat Events
    async def on_chat(self, user, message):
        """Delegate to chat events handler"""
        await self.chat_events.on_chat(user, message)
    
    # User Events
    async def on_user_join(self, user, position):
        """Delegate to user events handler"""
        await self.user_events.on_user_join(user, position)
    
    async def on_user_leave(self, user):
        """Delegate to user events handler"""
        await self.user_events.on_user_leave(user)
