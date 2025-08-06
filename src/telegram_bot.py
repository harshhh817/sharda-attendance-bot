"""Telegram bot for Sharda Attendance Bot."""
import logging
import signal
import sys
from typing import Dict, Any, Optional

from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackContext
)

from .config import config
from .logger import logger
from .browser_automation import check_attendance

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Global variable to store the application instance
application: Optional[Application] = None

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    welcome_message = (
        f"👋 Hello {user.first_name}!\n\n"
        "I'm your Sharda Attendance Bot. Here's what I can do:\n"
        "✅ Check your attendance\n"
        "📊 Show your attendance report\n"
        "⏰ Schedule automatic checks\n\n"
        "Use /help to see all available commands."
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
🤖 *Sharda Attendance Bot Help* 🤖

*Commands:*
/start - Start the bot
/help - Show this help message
/check - Check your attendance now
/status - Show bot status and settings

*How to use:*
1. First, make sure to set up your credentials in the .env file
2. Use /check to fetch your attendance
3. The bot will send you a report with your attendance percentages

*Note:* Your credentials are stored securely and never shared.
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def check_attendance_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check attendance when the command /check is issued."""
    # Check if the user is authorized
    if not _is_authorized(update):
        await update.message.reply_text("⛔ Unauthorized access. This bot is private.")
        return
    
    # Send "typing" action
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action='typing'
    )
    
    # Send initial message
    message = await update.message.reply_text("🔄 Fetching your attendance data...")
    
    try:
        # Check attendance
        success, result = check_attendance()
        
        # Update the message with results
        if success:
            await message.edit_text(result, parse_mode='Markdown')
        else:
            await message.edit_text(f"❌ Error: {result}")
            
    except Exception as e:
        logger.error(f"Error in check_attendance_command: {e}")
        await message.edit_text("❌ An error occurred while fetching your attendance. Please try again later.")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show bot status when the command /status is issued."""
    if not _is_authorized(update):
        await update.message.reply_text("⛔ Unauthorized access. This bot is private.")
        return
    
    status_text = (
        "🟢 *Bot Status*\n\n"
        f"• *Version:* 1.0.0\n"
        f"• *System ID:* `{_mask_sensitive(config.SYSTEM_ID)}`\n"
        f"• *Email:* `{_mask_sensitive(config.EMAIL)}`\n"
        f"• *Check Interval:* {config.CHECK_INTERVAL_HOURS} hours\n"
        f"• *Headless Mode:* {'✅' if config.HEADLESS else '❌'}\n\n"
        "_Use /check to fetch your attendance now._"
    )
    
    await update.message.reply_text(status_text, parse_mode='Markdown')

async def error_handler(update: object, context: CallbackContext) -> None:
    """Log errors and handle them gracefully."""
    logger.error("Exception while handling an update:", exc_info=context.error)
    
    if update and hasattr(update, 'message') and update.message:
        await update.message.reply_text(
            "❌ An error occurred while processing your request. "
            "The error has been logged and will be investigated."
        )

def _is_authorized(update: Update) -> bool:
    """Check if the user is authorized to use the bot."""
    return str(update.effective_chat.id) == config.TELEGRAM_CHAT_ID

def _mask_sensitive(text: str, visible_chars: int = 3) -> str:
    """Mask sensitive information for display."""
    if not text:
        return "Not set"
    if len(text) <= visible_chars * 2:
        return "*" * len(text)
    return text[:visible_chars] + "*" * (len(text) - visible_chars * 2) + text[-visible_chars:]

def setup_handlers(application: Application) -> None:
    """Set up command handlers for the bot."""
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("check", check_attendance_command))
    application.add_handler(CommandHandler("status", status_command))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Log all errors
    application.add_error_handler(error_handler)

def start_bot() -> None:
    """Start the Telegram bot."""
    global application
    
    try:
        logger.info("Starting Telegram bot...")
        
        # Create the Application
        application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        
        # Set up command handlers
        setup_handlers(application)
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)
        
        # Start the Bot
        logger.info("Bot is running. Press Ctrl+C to stop.")
        application.run_polling()
        
    except Exception as e:
        logger.critical(f"Failed to start bot: {e}", exc_info=True)
        sys.exit(1)

def _signal_handler(signum, frame):
    ""Handle shutdown signals."""
    logger.info(f"Received signal {signum}, shutting down...")
    if application:
        # This will stop the polling and allow the application to exit cleanly
        logger.info("Stopping application...")
        application.stop()
    sys.exit(0)

if __name__ == "__main__":
    start_bot()
