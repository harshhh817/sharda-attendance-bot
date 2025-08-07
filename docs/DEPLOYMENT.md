# Cloud Deployment Guide 🌐

Deploy your Sharda Attendance Bot to run 24/7 in the cloud, even when your laptop is off!

## 🚀 Quick Deploy Options

### Option 1: Railway (Recommended - Free Tier)
**Best for beginners - No credit card required**

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**
   ```bash
   # Fork this repository to your GitHub account
   # Then connect Railway to your forked repo
   ```

3. **Add Environment Variables**
   In Railway dashboard, add these variables:
   ```
   SYSTEM_ID=your-system-id
   GMAIL_USER=your-email@gmail.com
   GMAIL_PASSWORD=your-app-password
   TELEGRAM_BOT_TOKEN=your-bot-token
   TELEGRAM_CHAT_ID=your-chat-id
   ```

4. **Deploy**
   - Railway will automatically detect Python
   - Add `chromium-browser` buildpack
   - Deploy and your bot runs 24/7!

### Option 2: Heroku (Free Tier Available)
**Popular platform with good free tier**

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Windows
   # Download from heroku.com
   ```

2. **Create Heroku App**
   ```bash
   heroku login
   heroku create your-bot-name
   ```

3. **Add Buildpacks**
   ```bash
   heroku buildpacks:add heroku/python
   heroku buildpacks:add https://github.com/heroku/heroku-buildpack-google-chrome
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set SYSTEM_ID=your-system-id
   heroku config:set GMAIL_USER=your-email@gmail.com
   heroku config:set GMAIL_PASSWORD=your-app-password
   heroku config:set TELEGRAM_BOT_TOKEN=your-bot-token
   heroku config:set TELEGRAM_CHAT_ID=your-chat-id
   ```

5. **Deploy**
   ```bash
   git push heroku main
   heroku ps:scale worker=1
   ```

### Option 3: DigitalOcean Droplet ($5/month)
**Most reliable - Full control**

1. **Create Droplet**
   - Ubuntu 22.04 LTS
   - Basic plan ($5/month)
   - Add SSH key

2. **Connect and Setup**
   ```bash
   ssh root@your-droplet-ip
   
   # Update system
   apt update && apt upgrade -y
   
   # Install dependencies
   apt install -y python3 python3-pip chromium-browser git
   ```

3. **Clone and Setup Bot**
   ```bash
   git clone https://github.com/harshhh817/sharda-attendance-bot.git
   cd sharda-attendance-bot
   python3 setup.py
   ```

4. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/sharda-bot.service
   ```

   Add this content:
   ```ini
   [Unit]
   Description=Sharda Attendance Bot
   After=network.target

   [Service]
   Type=simple
   User=root
   WorkingDirectory=/root/sharda-attendance-bot
   ExecStart=/usr/bin/python3 src/telegram_bot_handler.py
   Restart=always
   RestartSec=10
   Environment=DISPLAY=:99

   [Install]
   WantedBy=multi-user.target
   ```

5. **Start Service**
   ```bash
   sudo systemctl enable sharda-bot
   sudo systemctl start sharda-bot
   sudo systemctl status sharda-bot
   ```

### Option 4: AWS EC2 (Free Tier Available)
**Enterprise-grade hosting**

1. **Launch EC2 Instance**
   - Amazon Linux 2
   - t2.micro (free tier)
   - Configure security groups

2. **Connect and Setup**
   ```bash
   ssh -i your-key.pem ec2-user@your-instance-ip
   
   # Install dependencies
   sudo yum update -y
   sudo yum install -y python3 python3-pip chromium-headless
   ```

3. **Deploy Bot**
   ```bash
   git clone https://github.com/harshhh817/sharda-attendance-bot.git
   cd sharda-attendance-bot
   python3 setup.py
   ```

4. **Setup PM2 for Process Management**
   ```bash
   npm install -g pm2
   pm2 start src/telegram_bot_handler.py --name sharda-bot --interpreter python3
   pm2 startup
   pm2 save
   ```

## 🔧 Environment Variables

For all cloud deployments, set these environment variables:

```bash
# Required
SYSTEM_ID=your-sharda-system-id
GMAIL_USER=your-email@gmail.com
GMAIL_PASSWORD=your-gmail-app-password
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id

# Optional
LOG_LEVEL=INFO
HEADLESS=True
```

## 📊 Cost Comparison

| Platform | Cost | Ease | Reliability | Best For |
|----------|------|------|-------------|----------|
| **Railway** | Free-$5/month | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Beginners |
| **Heroku** | Free-$7/month | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Quick deploy |
| **DigitalOcean** | $5/month | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Reliability |
| **AWS EC2** | Free-$10/month | ⭐⭐ | ⭐⭐⭐⭐⭐ | Enterprise |

## 🛠️ Troubleshooting

### Common Issues:

1. **Chrome/Chromium not found**
   ```bash
   # Add to your deployment
   apt install -y chromium-browser
   # or
   yum install -y chromium-headless
   ```

2. **Environment variables not set**
   - Check your platform's environment variable settings
   - Ensure all required variables are set

3. **Bot not responding**
   ```bash
   # Check logs
   heroku logs --tail  # Heroku
   railway logs        # Railway
   journalctl -u sharda-bot -f  # Systemd
   ```

4. **Memory issues**
   - Upgrade to a larger plan
   - Optimize Chrome settings for headless mode

## 🔒 Security Best Practices

1. **Never commit credentials**
   - Use environment variables
   - Keep .env files out of git

2. **Regular updates**
   - Update dependencies regularly
   - Monitor for security patches

3. **Access control**
   - Use strong passwords
   - Enable 2FA on all accounts

## 📈 Monitoring

### Health Checks
Add this to your bot for monitoring:
```python
async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running! ✅")
```

### Logs
- **Heroku**: `heroku logs --tail`
- **Railway**: `railway logs`
- **DigitalOcean**: `journalctl -u sharda-bot -f`
- **AWS**: CloudWatch logs

## 🎯 Recommended Setup

**For Students (Free):**
1. Use Railway (free tier)
2. Easy setup, no credit card
3. Automatic deployments

**For Reliability ($5/month):**
1. Use DigitalOcean Droplet
2. Full control, always online
3. Professional hosting

Your bot will now run 24/7, even when your laptop is off! 🚀
