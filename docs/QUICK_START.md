# Quick Start Guide 🚀

Get your Sharda Attendance Bot running in 5 minutes!

## Step 1: Download & Setup
```bash
# Download the project
git clone <your-repo-url>
cd attendence

# Run the automated setup
python3 setup.py
```

## Step 2: Follow the Setup Wizard
The setup script will ask for:
- Your Sharda System ID
- Your Gmail address and app password
- Your Telegram bot token
- Your Telegram chat ID

## Step 3: Start the Bot
```bash
./start_bot.sh
```

## Step 4: Test on Telegram
Send these commands to your bot:
- `/start` - Welcome message
- `/check` - Check attendance
- `/today` - Today's classes

## Need Help?

### Get Telegram Bot Token:
1. Message [@BotFather](https://t.me/botfather)
2. Send `/newbot`
3. Follow instructions

### Get Chat ID:
1. Message [@userinfobot](https://t.me/userinfobot)
2. It will reply with your chat ID

### Get Gmail App Password:
1. Go to https://myaccount.google.com/security
2. Enable 2-Factor Authentication
3. Go to "App passwords"
4. Generate password for "Mail"

## Troubleshooting
- **Bot not responding?** Run `./restart_bot.sh`
- **Login issues?** Check your System ID
- **OTP problems?** Verify Gmail app password
- **Still stuck?** Check `error.log` for details

That's it! Your bot should be working now. 🎉
