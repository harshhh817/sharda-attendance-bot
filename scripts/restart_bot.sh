#!/bin/bash

# Change to the project root directory
cd "$(dirname "$0")/.."

# Stop the bot
./scripts/stop_bot.sh

# Wait a moment
sleep 2

# Start the bot
./scripts/start_bot.sh
