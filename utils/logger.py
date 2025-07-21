"""
Logger utility for Highrise bot
Provides consistent logging across the application
"""
import logging
from datetime import datetime
from config import DEBUG

class BotLogger:
    def __init__(self, name="HighriseBot"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)
        
        # Create console handler
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
