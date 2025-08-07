# Deployment Guide 🌐

Different ways to deploy your Sharda Attendance Bot

## Local Deployment (Recommended for Beginners)

### macOS/Linux
```bash
# Clone and setup
git clone <your-repo-url>
cd attendence
python3 setup.py
./start_bot.sh
```

### Windows
```bash
# Install WSL or use Git Bash
git clone <your-repo-url>
cd attendence
python setup.py
./start_bot.sh
```

## Cloud Deployment

### Heroku (Free Tier Available)
1. Create Heroku account
2. Install Heroku CLI
3. Create `Procfile`:
```
worker: python telegram_bot_handler.py
```
4. Deploy:
```bash
heroku create your-bot-name
git push heroku main
heroku ps:scale worker=1
```

### Railway (Free Tier Available)
1. Connect your GitHub repo
2. Add environment variables in Railway dashboard
3. Deploy automatically

### DigitalOcean Droplet ($5/month)
1. Create Ubuntu droplet
2. SSH into server
3. Install dependencies:
```bash
sudo apt update
sudo apt install python3 python3-pip chromium-browser
```
4. Clone and setup bot
5. Use `screen` or `systemd` to keep bot running

### AWS EC2 (Free Tier Available)
1. Launch Ubuntu instance
2. Install dependencies
3. Setup bot with systemd service

## Systemd Service (Linux/macOS)

Create `/etc/systemd/system/sharda-bot.service`:
```ini
[Unit]
Description=Sharda Attendance Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/attendence
ExecStart=/usr/bin/python3 telegram_bot_handler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable sharda-bot
sudo systemctl start sharda-bot
sudo systemctl status sharda-bot
```

## Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

# Install Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x *.sh

CMD ["./start_bot.sh"]
```

Build and run:
```bash
docker build -t sharda-bot .
docker run -d --name sharda-bot sharda-bot
```

## Environment Variables

For cloud deployment, set these environment variables:
```bash
SYSTEM_ID=your-system-id
GMAIL_USER=your-email@gmail.com
GMAIL_PASSWORD=your-app-password
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
```

## Monitoring & Maintenance

### Logs
- Check logs: `tail -f output.log`
- Error logs: `tail -f error.log`

### Health Check
Create a simple health check endpoint:
```python
# Add to telegram_bot_handler.py
async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running! ✅")
```

### Auto-restart
Use `crontab` for periodic restarts:
```bash
# Edit crontab
crontab -e

# Add line to restart every 6 hours
0 */6 * * * cd /path/to/attendence && ./restart_bot.sh
```

## Security Considerations

1. **Never commit sensitive data** to Git
2. **Use environment variables** for credentials
3. **Restrict bot access** to authorized users only
4. **Regular updates** for dependencies
5. **Monitor logs** for suspicious activity

## Cost Comparison

| Platform | Cost | Ease of Setup | Reliability |
|----------|------|---------------|-------------|
| Local | Free | Easy | Good |
| Heroku | Free-$7/month | Easy | Good |
| Railway | Free-$5/month | Easy | Good |
| DigitalOcean | $5/month | Medium | Excellent |
| AWS EC2 | Free-$10/month | Hard | Excellent |

## Troubleshooting Deployment

### Common Issues:
1. **Chrome not found**: Install Chrome/Chromium
2. **Permission denied**: Check file permissions
3. **Port conflicts**: Change port or kill existing processes
4. **Memory issues**: Increase RAM allocation
5. **Network timeouts**: Check firewall settings

### Debug Commands:
```bash
# Check if bot is running
ps aux | grep telegram_bot_handler

# Check logs
tail -f output.log error.log

# Test individual components
python3 autologin.py
python3 fetch_otp.py
```
