""Configuration settings for the Sharda Attendance Bot."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    """Application configuration."""
    # Required configuration
    SYSTEM_ID = os.getenv('SYSTEM_ID')
    EMAIL = os.getenv('EMAIL')
    APP_PASSWORD = os.getenv('APP_PASSWORD')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    
    # Optional configuration with defaults
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    HEADLESS = os.getenv('HEADLESS', 'False').lower() in ('true', '1', 't')
    CHECK_INTERVAL_HOURS = int(os.getenv('CHECK_INTERVAL_HOURS', '24'))
    
    # URLs
    LOGIN_URL = "https://student.sharda.ac.in/admin"
    ATTENDANCE_URL = "https://student.sharda.ac.in/admin/courses"
    
    # IMAP Settings
    IMAP_SERVER = "imap.gmail.com"
    SENDER_EMAIL = "ezone@shardauniversity.com"
    
    # Timeouts (in seconds)
    PAGE_LOAD_TIMEOUT = 30
    ELEMENT_TIMEOUT = 10
    
    @classmethod
    def validate(cls):
        """Validate that all required configuration is present."""
        required_vars = {
            'SYSTEM_ID': cls.SYSTEM_ID,
            'EMAIL': cls.EMAIL,
            'APP_PASSWORD': cls.APP_PASSWORD,
            'TELEGRAM_BOT_TOKEN': cls.TELEGRAM_BOT_TOKEN,
            'TELEGRAM_CHAT_ID': cls.TELEGRAM_CHAT_ID,
        }
        
        missing = [name for name, value in required_vars.items() if not value]
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        
        if not cls.EMAIL.endswith('@sharda.ac.in'):
            print("⚠️  Warning: Email does not appear to be a Sharda University email")

# Create a config instance
config = Config()
