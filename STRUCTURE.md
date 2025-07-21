# Modular Highrise Bot Structure

This bot has been restructured to be modular and easy to extend. Here's how the new structure works:

## 📁 Project Structure

```
highrise-py/
├── bot.py                 # Main bot class (simplified)
├── config.py             # Configuration management
├── run_bot.py            # Bot launcher
├── requirements.txt      # Dependencies
├── .env                 # Environment variables
│
├── events/              # Event handling system
│   ├── __init__.py
│   ├── event_manager.py  # Central event coordinator
│   ├── chat_events.py    # Chat message handling
│   ├── user_events.py    # User join/leave events
│   └── session_events.py # Bot startup events
│
├── commands/            # Command system
│   ├── __init__.py
│   ├── command_handler.py # Routes commands to handlers
│   ├── basic_commands.py  # Basic commands (hello, help)
│   └── fun_commands.py    # Fun commands (dice, flip, etc.)
│
└── utils/               # Utility functions
    ├── __init__.py
    ├── logger.py         # Logging utilities
    └── helpers.py        # Helper functions
```

## 🚀 How to Add New Features

### Adding New Commands

1. **Create a new command file** in the `commands/` folder:
   ```python
   # commands/my_commands.py
   class MyCommands:
       def __init__(self, bot):
           self.bot = bot
       
       async def my_command(self, user, message):
           await self.bot.highrise.chat("My custom response!")
   ```

2. **Register in command_handler.py**:
   ```python
   from .my_commands import MyCommands
   
   # In __init__:
   self.my_commands = MyCommands(bot)
   
   # In commands dict:
   "!mycommand": self.my_commands.my_command,
   ```

### Adding New Event Types

1. **Create event handler** in `events/` folder
2. **Add to event_manager.py** to coordinate the new events
3. **Add to bot.py** if it's a new Highrise event type

### Adding Utilities

Add helper functions to `utils/helpers.py` or create new utility files.

## 🎯 Benefits of This Structure

- **Modular**: Each feature is in its own file
- **Scalable**: Easy to add new commands and events
- **Maintainable**: Clean separation of concerns
- **Organized**: Logical folder structure
- **Extensible**: Simple to extend functionality

## 📝 Example Usage

The bot now supports these commands:
- `!hello` - Basic greeting
- `!help` - Show available commands
- `!dice` - Roll a dice
- `!flip` - Flip a coin
- `!8ball` - Magic 8-ball
- `!joke` - Random joke

## 🔧 Configuration

All configuration is still handled through the `.env` file and `config.py` as before.
