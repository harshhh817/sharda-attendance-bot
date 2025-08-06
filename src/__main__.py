""Main entry point for the Sharda Attendance Bot."""
import sys
from .logger import logger
from .config import config

def main():
    """Run the bot."""
    try:
        # Validate configuration
        config.validate()
        
        # Import here to avoid circular imports
        from .telegram_bot import start_bot
        
        # Start the bot
        start_bot()
        
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
