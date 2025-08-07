# Configuration Template for Sharda Attendance Bot
# Copy this file to config.py and fill in your details

# Sharda University System ID (found in your student portal)
SYSTEM_ID = "YOUR_SYSTEM_ID_HERE"

# Gmail credentials for OTP retrieval
GMAIL_USER = "your.email@gmail.com"
GMAIL_PASSWORD = "your-gmail-app-password"  # Generate from Google Account settings

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Get from @BotFather
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"      # Get from @userinfobot

# Optional: Customize bot behavior
BOT_NAME = "Sharda Attendance Bot"
AUTHORIZED_USERS = [TELEGRAM_CHAT_ID]  # Add multiple chat IDs for shared access

# Optional: Notification settings
SEND_SCREENSHOTS = True  # Set to False to disable screenshot sending
SCREENSHOT_QUALITY = "high"  # "low", "medium", "high"

# Optional: Timing settings
LOGIN_TIMEOUT = 30  # seconds to wait for login
OTP_TIMEOUT = 60    # seconds to wait for OTP email
PAGE_LOAD_TIMEOUT = 20  # seconds to wait for page loads
