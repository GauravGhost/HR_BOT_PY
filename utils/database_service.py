"""
Database Service for Highrise Bot
Provides database functionality specifically tailored for bot operations
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from utils.json_database import JSONDatabase


class BotDatabaseService:
    """
    Database service specifically designed for Highrise bot operations
    Manages user data, room statistics, commands usage, and more
    """
    
    def __init__(self, db_path: str = "bot_data"):
        self.db = JSONDatabase(db_path)
        self._initialize_tables()
    
    def _initialize_tables(self):
        """Initialize all required tables for bot operations"""
        tables = [
            "users",           # User profiles and statistics
            "room_stats",      # Room-specific statistics
            "command_usage",   # Command usage tracking
            "user_sessions",   # User session data
            "bot_config",      # Bot configuration and settings
            "moderation"       # Moderation logs and warnings
        ]
        
        for table in tables:
            if not self.db.table_exists(table):
                self.db.create_table(table)
    
    # User Management
    def register_user(self, user_id: str, username: str, **additional_data) -> str:
        """Register a new user or update existing user info"""
        existing_user = self.db.read("users", user_id)
        
        if existing_user:
            # Update existing user
            self.db.update("users", user_id, {
                "username": username,
                "last_seen": datetime.now().isoformat(),
                **additional_data
            })
            return user_id
        else:
            # Create new user
            user_data = {
                "user_id": user_id,
                "username": username,
                "first_seen": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat(),
                "total_messages": 0,
                "total_joins": 1,
                "total_time_spent": 0,  # in minutes
                "favorite_commands": [],
                "user_level": 1,
                "experience_points": 0,
                **additional_data
            }
            return self.db.create("users", user_data, user_id)
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get complete user profile"""
        return self.db.read("users", user_id)
    
    def update_user_activity(self, user_id: str, message_count: int = 1):
        """Update user activity stats"""
        user = self.get_user_profile(user_id)
        if user:
            new_message_count = user.get("total_messages", 0) + message_count
            new_exp = user.get("experience_points", 0) + (message_count * 10)
            new_level = max(1, new_exp // 100)  # Level up every 100 XP
            
            self.db.update("users", user_id, {
                "total_messages": new_message_count,
                "experience_points": new_exp,
                "user_level": new_level,
                "last_seen": datetime.now().isoformat()
            })
    
    def increment_user_joins(self, user_id: str):
        """Increment user's join count"""
        user = self.get_user_profile(user_id)
        if user:
            new_joins = user.get("total_joins", 0) + 1
            self.db.update("users", user_id, {
                "total_joins": new_joins,
                "last_seen": datetime.now().isoformat()
            })
    
    def get_top_users(self, limit: int = 10, sort_by: str = "experience_points") -> List[Dict[str, Any]]:
        """Get top users by specified criteria"""
        all_users = list(self.db.read_all("users").values())
        sorted_users = sorted(all_users, 
                            key=lambda u: u.get(sort_by, 0), 
                            reverse=True)
        return sorted_users[:limit]
    
    # Command Usage Tracking
    def log_command_usage(self, user_id: str, command: str, success: bool = True):
        """Log command usage for analytics"""
        timestamp = datetime.now().isoformat()
        command_data = {
            "user_id": user_id,
            "command": command,
            "timestamp": timestamp,
            "success": success
        }
        
        # Create unique ID for command log
        log_id = f"{user_id}_{command}_{timestamp}"
        self.db.create("command_usage", command_data, log_id)
        
        # Update user's favorite commands
        user = self.get_user_profile(user_id)
        if user and success:
            fav_commands = user.get("favorite_commands", [])
            if command in fav_commands:
                # Move to front
                fav_commands.remove(command)
            fav_commands.insert(0, command)
            # Keep only top 5 favorites
            fav_commands = fav_commands[:5]
            
            self.db.update("users", user_id, {"favorite_commands": fav_commands})
    
    def get_command_stats(self, days: int = 7) -> Dict[str, Any]:
        """Get command usage statistics for the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_commands = self.db.find("command_usage", 
            lambda record: datetime.fromisoformat(record.get("timestamp", "1970-01-01")) > cutoff_date
        )
        
        stats = {
            "total_commands": len(recent_commands),
            "successful_commands": len([c for c in recent_commands if c.get("success", False)]),
            "command_breakdown": {},
            "top_users": {}
        }
        
        # Command breakdown
        for cmd in recent_commands:
            command_name = cmd.get("command", "unknown")
            if command_name not in stats["command_breakdown"]:
                stats["command_breakdown"][command_name] = 0
            stats["command_breakdown"][command_name] += 1
        
        # Top command users
        for cmd in recent_commands:
            user_id = cmd.get("user_id", "unknown")
            if user_id not in stats["top_users"]:
                stats["top_users"][user_id] = 0
            stats["top_users"][user_id] += 1
        
        return stats
    
    # Session Management
    def start_user_session(self, user_id: str, session_metadata: Dict[str, Any] = None):
        """Start a new user session"""
        session_data = {
            "user_id": user_id,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "duration_minutes": 0,
            "messages_sent": 0,
            "commands_used": 0,
            "metadata": session_metadata or {}
        }
        
        session_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return self.db.create("user_sessions", session_data, session_id)
    
    def end_user_session(self, user_id: str):
        """End the user's current session"""
        # Find active session for user
        active_sessions = self.db.find("user_sessions", 
            lambda s: s.get("user_id") == user_id and s.get("end_time") is None
        )
        
        if active_sessions:
            session = active_sessions[0]  # Get the most recent
            session_id = session.get("_id")
            start_time = datetime.fromisoformat(session.get("start_time"))
            end_time = datetime.now()
            duration = int((end_time - start_time).total_seconds() / 60)
            
            self.db.update("user_sessions", session_id, {
                "end_time": end_time.isoformat(),
                "duration_minutes": duration
            })
            
            # Update user's total time spent
            user = self.get_user_profile(user_id)
            if user:
                total_time = user.get("total_time_spent", 0) + duration
                self.db.update("users", user_id, {"total_time_spent": total_time})
    
    def update_session_activity(self, user_id: str, messages: int = 0, commands: int = 0):
        """Update current session activity"""
        active_sessions = self.db.find("user_sessions", 
            lambda s: s.get("user_id") == user_id and s.get("end_time") is None
        )
        
        if active_sessions:
            session = active_sessions[0]
            session_id = session.get("_id")
            new_messages = session.get("messages_sent", 0) + messages
            new_commands = session.get("commands_used", 0) + commands
            
            self.db.update("user_sessions", session_id, {
                "messages_sent": new_messages,
                "commands_used": new_commands
            })
    
    # Room Statistics
    def update_room_stats(self, room_id: str, **stats):
        """Update room-specific statistics"""
        room_data = self.db.read("room_stats", room_id)
        
        if room_data:
            self.db.update("room_stats", room_id, stats)
        else:
            stats.update({
                "room_id": room_id,
                "first_tracked": datetime.now().isoformat(),
                "total_users": 0,
                "total_messages": 0,
                "peak_users": 0
            })
            self.db.create("room_stats", stats, room_id)
    
    def get_room_stats(self, room_id: str) -> Optional[Dict[str, Any]]:
        """Get room statistics"""
        return self.db.read("room_stats", room_id)
    
    # Bot Configuration
    def set_config(self, key: str, value: Any):
        """Set a configuration value"""
        config_data = {
            "key": key,
            "value": value,
            "updated_at": datetime.now().isoformat()
        }
        
        existing = self.db.read("bot_config", key)
        if existing:
            self.db.update("bot_config", key, config_data)
        else:
            self.db.create("bot_config", config_data, key)
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        config = self.db.read("bot_config", key)
        return config.get("value", default) if config else default
    
    # Moderation
    def add_warning(self, user_id: str, reason: str, moderator: str = "system"):
        """Add a warning to a user"""
        warning_data = {
            "user_id": user_id,
            "reason": reason,
            "moderator": moderator,
            "timestamp": datetime.now().isoformat(),
            "active": True
        }
        
        # Generate unique warning ID with microseconds to avoid collisions
        timestamp = datetime.now()
        warning_id = f"{user_id}_warning_{timestamp.strftime('%Y%m%d_%H%M%S')}_{timestamp.microsecond}"
        return self.db.create("moderation", warning_data, warning_id)
    
    def get_user_warnings(self, user_id: str, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get warnings for a user"""
        warnings = self.db.find("moderation", lambda w: w.get("user_id") == user_id)
        
        if active_only:
            warnings = [w for w in warnings if w.get("active", True)]
        
        return sorted(warnings, key=lambda w: w.get("timestamp", ""), reverse=True)
    
    def clear_user_warnings(self, user_id: str):
        """Clear all warnings for a user"""
        warnings = self.get_user_warnings(user_id, active_only=True)
        for warning in warnings:
            warning_id = warning.get("_id")
            self.db.update("moderation", warning_id, {"active": False})
    
    # Analytics and Reporting
    def get_database_summary(self) -> Dict[str, Any]:
        """Get a summary of all database statistics"""
        stats = self.db.get_stats()
        
        summary = {
            "database_stats": stats,
            "user_count": self.db.count("users"),
            "total_sessions": self.db.count("user_sessions"),
            "total_commands": self.db.count("command_usage"),
            "room_count": self.db.count("room_stats"),
            "total_warnings": len(self.db.find("moderation", lambda w: w.get("active", True))),
        }
        
        # Top users
        top_users = self.get_top_users(5)
        summary["top_users_by_xp"] = [
            {"username": u.get("username"), "xp": u.get("experience_points", 0)} 
            for u in top_users
        ]
        
        return summary
    
    def cleanup_old_data(self, days: int = 30):
        """Clean up old session and command data"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Clean old sessions
        old_sessions = self.db.find("user_sessions", 
            lambda s: s.get("end_time") and 
            datetime.fromisoformat(s.get("end_time")) < cutoff_date
        )
        
        for session in old_sessions:
            self.db.delete("user_sessions", session.get("_id"))
        
        # Clean old command logs
        old_commands = self.db.find("command_usage", 
            lambda c: datetime.fromisoformat(c.get("timestamp", "1970-01-01")) < cutoff_date
        )
        
        for command in old_commands:
            self.db.delete("command_usage", command.get("_id"))
        
        return len(old_sessions) + len(old_commands)
