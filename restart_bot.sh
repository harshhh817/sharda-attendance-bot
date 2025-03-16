#!/bin/bash

# Change to the script directory
cd "$(dirname "$0")"

# Stop the bot
./stop_bot.sh

# Wait a moment
sleep 2

# Start the bot
./start_bot.sh
