# Railway Deployment Guide 🚀

Deploy your Sharda Attendance Bot to Railway for 24/7 operation!

## Step 1: Fork the Repository
1. Go to https://github.com/harshhh817/sharda-attendance-bot
2. Click "Fork" to create your own copy
3. Clone your forked repository

## Step 2: Create Railway Account
1. Go to https://railway.app
2. Sign up with your GitHub account
3. Click "New Project"

## Step 3: Connect Your Repository
1. Select "Deploy from GitHub repo"
2. Choose your forked repository
3. Railway will automatically detect it's a Python project

## Step 4: Add Environment Variables
In Railway dashboard, go to "Variables" tab and add:

```
SYSTEM_ID=your-sharda-system-id
GMAIL_USER=your-email@gmail.com
GMAIL_PASSWORD=your-gmail-app-password
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
```

## Step 5: Deploy
1. Railway will automatically start deploying
2. Wait for the build to complete
3. Your bot is now running 24/7!

## Step 6: Test Your Bot
1. Send `/start` to your Telegram bot
2. Try `/check` to test attendance
3. Try `/today` to get today's classes

## Troubleshooting
- Check Railway logs if bot doesn't respond
- Ensure all environment variables are set correctly
- Make sure your Gmail app password is correct

Your bot will now run continuously, even when your laptop is off! 🎉
