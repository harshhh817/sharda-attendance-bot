#!/bin/bash

# Find and kill the bot process
BOT_PID=$(pgrep -f "python3 telegram_bot_handler.py")

if [ -n "$BOT_PID" ]; then
    echo "Stopping bot with PID: $BOT_PID"
    kill $BOT_PID
    echo "Bot stopped."
else
    echo "Bot is not running."
fi
