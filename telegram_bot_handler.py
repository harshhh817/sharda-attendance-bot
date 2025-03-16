import logging
import subprocess
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Your Telegram Bot Token (same as in your autologin.py)
TELEGRAM_BOT_TOKEN = "7688760570:AAFxql5tfEBIkBvwche2Zj_74zRUuVlS7rY"
# Your Telegram Chat ID (for security - only you can control the bot)
AUTHORIZED_CHAT_ID = "6244107851"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    if str(update.effective_chat.id) != AUTHORIZED_CHAT_ID:
        await update.message.reply_text("Unauthorized access denied.")
        return
        
    await update.message.reply_text('Hi! I can help you check your attendance. Use /check to run the attendance script.')

async def run_attendance_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Run the attendance check script when /check command is issued."""
    if str(update.effective_chat.id) != AUTHORIZED_CHAT_ID:
        await update.message.reply_text("Unauthorized access denied.")
        return
        
    await update.message.reply_text('Starting attendance check... I will notify you with the results.')
    
    # Run the script in a separate thread to avoid blocking the bot
    def run_script():
        try:
            subprocess.run(["python3", "autologin.py"], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Script execution failed: {e}")
    
    thread = threading.Thread(target=run_script)
    thread.start()

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("check", run_attendance_check))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()
    
    logging.info("Bot started. Press Ctrl+C to stop.")

if __name__ == "__main__":
    main()
