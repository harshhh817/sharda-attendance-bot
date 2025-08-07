#!/bin/bash

# Change to the project root directory
cd "$(dirname "$0")/.."

# Check if the bot is already running
if pgrep -f "python3 src/telegram_bot_handler.py" > /dev/null; then
    echo "Bot is already running."
else
    echo "Starting bot..."
    nohup python3 src/telegram_bot_handler.py > output.log 2> error.log &
    echo "Bot started with PID: $!"
fi
