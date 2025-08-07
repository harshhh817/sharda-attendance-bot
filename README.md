# Sharda University Attendance Bot 🤖

An automated Telegram bot that helps Sharda University students check their attendance, view timetables, and get today's classes without manually logging into the portal.

## 🎬 Demo Video

> **Watch the bot in action!** This demo shows all 4 commands working seamlessly.

[![Demo Video](https://img.shields.io/badge/📹-Watch_Demo_Video-blue?style=for-the-badge&logo=youtube)](https://youtu.be/demo-video-link)

**Demo Features:**
- ✅ Automated login to Sharda portal
- ✅ Today's classes with times and rooms
- ✅ Attendance percentages for all courses
- ✅ Full timetable with screenshots
- ✅ Real-time Telegram responses

*Note: Replace the demo video link above with your actual video URL*

## 🎬 Demo & Features

### 📱 Bot Commands in Action

| Command | Description | Demo |
|---------|-------------|------|
| `/start` | Welcome message and available commands | ![Start Command](demo_images/start_command.png) |
| `/today` | Get today's class schedule with times and rooms | ![Today's Classes](demo_images/todays_classes.png) |
| `/check` | Check attendance percentages for all courses | ![Attendance Check](demo_images/attendance_check.png) |
| `/timetable` | Get full weekly timetable with screenshots | ![Timetable](demo_images/timetable.png) |

### ✨ Key Features

- 🤖 **Automated Login**: Automatically logs into Sharda E-Zone portal
- 📊 **Attendance Check**: Fetches and displays attendance percentages for all courses
- 📅 **Today's Classes**: Shows today's class schedule from the home page
- 📋 **Full Timetable**: Displays complete weekly timetable (when available)
- 📧 **Email OTP**: Automatically retrieves OTP from Gmail for authentication
- 📱 **Telegram Integration**: All results sent directly to your Telegram
- 🖼️ **Screenshots**: Automatic capture and sending of timetable images
- ⚡ **Real-time Updates**: Instant notifications and responses

## Prerequisites

- Python 3.7+
- Chrome browser installed
- Gmail account (for OTP retrieval)
- Telegram account
- Sharda University student account

## 🚀 Quick Start

### ⚙️ Easy Setup Process

![Setup Process](demo_images/setup_process.png)

**Setup Time: 5 minutes** ⏱️

### 📋 Setup Instructions
```bash
git clone <your-repo-url>
cd attendence
```

### 2. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Configure Your Settings

Edit the following files with your personal information:

#### `autologin.py`
```python
SYSTEM_ID = "YOUR_SYSTEM_ID"  # Your Sharda System ID
GMAIL_USER = "your.email@gmail.com"  # Your Gmail address
GMAIL_PASSWORD = "your-app-password"  # Gmail App Password
```

#### `fetch_otp.py`
```python
GMAIL_USER = "your.email@gmail.com"  # Your Gmail address
GMAIL_PASSWORD = "your-app-password"  # Gmail App Password
```

#### `imap.py`
```python
GMAIL_USER = "your.email@gmail.com"  # Your Gmail address
GMAIL_PASSWORD = "your-app-password"  # Gmail App Password
```

#### `telegram_bot_handler.py`
```python
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"  # Your Telegram bot token
AUTHORIZED_CHAT_ID = "YOUR_CHAT_ID"    # Your Telegram chat ID
```

#### `fetch_timetable.py`
```python
SYSTEM_ID = "YOUR_SYSTEM_ID"  # Your Sharda System ID
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"  # Your Telegram bot token
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"      # Your Telegram chat ID
```

#### `fetch_today_classes.py`
```python
SYSTEM_ID = "YOUR_SYSTEM_ID"  # Your Sharda System ID
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"  # Your Telegram bot token
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"      # Your Telegram chat ID
```

### 4. Create a Telegram Bot

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow instructions
3. Copy the bot token and add it to the configuration files
4. Start a chat with your bot and send `/start`
5. Get your chat ID by messaging [@userinfobot](https://t.me/userinfobot)

### 5. Set Up Gmail App Password

1. Go to your Google Account settings
2. Enable 2-Factor Authentication
3. Generate an App Password for "Mail"
4. Use this password in the configuration files

### 6. Start the Bot

```bash
# Make scripts executable
chmod +x start_bot.sh stop_bot.sh restart_bot.sh

# Start the bot
./start_bot.sh
```

## 🎯 What You Get

![Features Overview](demo_images/features_overview.png)

## 📱 Usage

Once the bot is running, send these commands to your Telegram bot:

- `/start` - Welcome message and available commands
- `/check` - Check attendance for all courses
- `/today` - Get today's class schedule
- `/timetable` - Get full weekly timetable

## Troubleshooting

### Common Issues

1. **"Could not find timetable table"**
   - The timetable page structure may have changed
   - Try using `/today` instead for today's classes

2. **"Gmail authentication failed"**
   - Check your Gmail app password
   - Ensure 2FA is enabled on your Google account

3. **"Bot not responding"**
   - Check if the bot process is running: `ps aux | grep telegram_bot_handler`
   - Restart with: `./restart_bot.sh`

4. **"Chrome driver issues"**
   - Update Chrome browser
   - Check Chrome driver compatibility

### Logs

- Check `error.log` for error messages
- Check `output.log` for general output
- Check `page_source.html` for debugging page structure

## Security Notes

- Never share your Gmail app password or Telegram bot token
- Keep your System ID private
- The bot only responds to your authorized chat ID

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is for educational purposes. Use responsibly and in accordance with your institution's policies.
