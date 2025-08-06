# Sharda Attendance Bot

A Python bot that automatically checks your attendance percentage at Sharda University and notifies you via Telegram.

## Features

- 🔐 Secure login using system ID and OTP
- 📊 Fetches attendance data from the Sharda portal
- 📱 Sends notifications via Telegram
- 🔄 Can be scheduled to run automatically
- 🔒 Secure credential management using environment variables

## Prerequisites

- Python 3.8+
- Chrome browser installed
- A Telegram bot token (get from [@BotFather](https://t.me/botfather))
- App password for your Sharda email

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sharda-attendance-bot.git
   cd sharda-attendance-bot
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the bot by creating a `.env` file:
   ```bash
   cp .env.example .env
   ```
   Then edit the `.env` file with your credentials.

## Usage

### Running the Bot

```bash
# Run the bot directly
python -m src.bot

# Or use the helper script
./start_bot.sh
```

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
# Required
SYSTEM_ID=your_system_id
EMAIL=your_email@sharda.ac.in
APP_PASSWORD=your_app_password
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# Optional (with defaults)
LOG_LEVEL=INFO
HEADLESS=False  # Set to True for server use
```

## Scheduling

To run the bot daily, you can set up a cron job (Linux/macOS) or Task Scheduler (Windows).

### Linux/macOS

```bash
# Edit crontab
crontab -e

# Add this line to run daily at 9 AM
0 9 * * * cd /path/to/sharda-attendance-bot && ./start_bot.sh
```

## Security Notes

- Never commit your `.env` file
- Use app-specific passwords instead of your main email password
- Keep your Telegram bot token private

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
