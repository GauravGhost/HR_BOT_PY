from highrise import BaseBot, User
from highrise.models import SessionMetadata, ChatRequest, Position
from events.event_manager import EventManager
from utils.logger import BotLogger

class Mybot(BaseBot):
    def __init__(self):
        super().__init__()
        self.logger = BotLogger("Mybot")
        self.event_manager = EventManager(self)
        self.logger.info("Bot initialized with modular event system")
    
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        """Called when the bot starts and connects to the room"""
        await self.event_manager.on_start(session_metadata)
    
    async def on_chat(self, user: User, message: str) -> None:
        """Called when someone sends a chat message"""
        await self.event_manager.on_chat(user, message)
    
    async def on_user_join(self, user: User, position: Position) -> None:
        """Called when a user joins the room"""
        await self.event_manager.on_user_join(user, position)
    
    async def on_user_leave(self, user: User) -> None:
        """Called when a user leaves the room"""
        await self.event_manager.on_user_leave(user)