"""
Helper functions for Highrise bot
Contains utility functions used across the application
"""
from typing import List, Optional

def format_user_list(users: List[str]) -> str:
    """Format a list of usernames for display"""
    if not users:
        return "No users"
    elif len(users) == 1:
        return users[0]
    elif len(users) == 2:
        return f"{users[0]} and {users[1]}"
    else:
        return f"{', '.join(users[:-1])}, and {users[-1]}"

def parse_command_args(message: str) -> tuple[str, List[str]]:
    """Parse command and arguments from a message"""
    parts = message.split()
    command = parts[0].lower() if parts else ""
    args = parts[1:] if len(parts) > 1 else []
    return command, args

def is_valid_room_id(room_id: str) -> bool:
    """Check if a room ID is valid format"""
    return len(room_id) == 24 and all(c in '0123456789abcdef' for c in room_id.lower())

def truncate_message(message: str, max_length: int = 256) -> str:
    """Truncate message to fit Highrise chat limits"""
    if len(message) <= max_length:
        return message
    return message[:max_length-3] + "..."
