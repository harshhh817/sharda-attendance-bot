# Sharda Attendance Bot 🤖

An automated Telegram bot that helps Sharda University students check their attendance, view timetables, and get today's classes without manually logging into the portal.

## ✨ Features

- 🤖 **Automated Login** - Secure login to Sharda E-Zone portal
- 📊 **Attendance Check** - Get attendance percentages for all courses
- 📅 **Today's Classes** - View today's schedule with times and rooms
- 📋 **Full Timetable** - Access complete weekly timetable
- 📧 **Email OTP** - Automatic OTP retrieval from Gmail
- 📱 **Telegram Integration** - All results sent directly to Telegram
- 🖼️ **Screenshots** - Automatic capture and sending of timetable images

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Chrome browser
- Gmail account (for OTP)
- Telegram account
- Sharda University account

### Setup (5 minutes)

1. **Clone the repository**
   ```bash
   git clone https://github.com/harshhh817/sharda-attendance-bot.git
   cd sharda-attendance-bot
   ```

2. **Run the setup wizard**
   ```bash
   python3 setup.py
   ```

3. **Start the bot**
   ```bash
   ./scripts/start_bot.sh
   ```

4. **Test on Telegram**
   Send `/start` to your bot

## 📱 Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message and available commands |
| `/check` | Check attendance for all courses |
| `/today` | Get today's class schedule |
| `/timetable` | Get full weekly timetable |

## 📁 Project Structure

```
sharda-attendance-bot/
├── README.md              # This file
├── setup.py               # Setup wizard
├── requirements.txt       # Python dependencies
├── config_template.py     # Configuration template
├── .gitignore            # Git ignore rules
├── scripts/              # Bot management scripts
│   ├── start_bot.sh
│   ├── stop_bot.sh
│   └── restart_bot.sh
├── docs/                 # Documentation
│   ├── QUICK_START.md
│   ├── DEPLOYMENT.md
│   └── SHARING_GUIDE.md
└── src/                  # Bot source code
    ├── telegram_bot_handler.py
    ├── autologin.py
    ├── fetch_otp.py
    ├── fetch_today_classes.py
    ├── fetch_timetable.py
    └── imap.py
```

## 🔧 Configuration

The setup wizard will help you configure:
- **System ID** - Your Sharda University System ID
- **Gmail credentials** - For OTP retrieval
- **Telegram bot token** - From @BotFather
- **Telegram chat ID** - Your chat ID

## 📚 Documentation

- **[Quick Start Guide](docs/QUICK_START.md)** - Get started in 5 minutes
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Deploy to cloud platforms
- **[Sharing Guide](docs/SHARING_GUIDE.md)** - Share with other students

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is for educational purposes. Use responsibly and in accordance with your institution's policies.

## ⚠️ Disclaimer

This bot is designed to help students stay organized. Please attend your classes regularly and use this tool responsibly.
