# Deploy Trading Bot to Fly.io

## Prerequisites
- Install [Fly.io CLI](https://fly.io/docs/hands-on/install-flyctl/)
- Sign up for a free Fly.io account

## Installation Steps

### 1. Install Fly.io CLI

**macOS:**
```bash
brew install flyctl
```

**Or using curl:**
```bash
curl -L https://fly.io/install.sh | sh
```

### 2. Login to Fly.io
```bash
flyctl auth login
```
This will open a browser for authentication.

### 3. Launch Your App

Navigate to your project directory and run:
```bash
flyctl launch
```

When prompted:
- **App Name**: Press Enter to use `trading-bot` or choose your own
- **Region**: Choose `sin` (Singapore) for best performance in Vietnam
- **Would you like to set up a Postgresql database?**: No
- **Would you like to set up an Upstash Redis database?**: No
- **Would you like to deploy now?**: Yes

### 4. Deploy Your App

If you didn't deploy during launch, or want to redeploy:
```bash
flyctl deploy
```

### 5. Check Status

```bash
# View app status
flyctl status

# View logs
flyctl logs

# Open app in browser
flyctl open
```

## Environment Variables (Optional)

If you want to store Discord webhook URL as environment variable:

```bash
flyctl secrets set DISCORD_WEBHOOK_URL="your_webhook_url_here"
```

Then update `trading_bot.py` to read from environment:
```python
import os
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', 'YOUR_DISCORD_WEBHOOK_URL_HERE')
```

## Monitoring

```bash
# View real-time logs
flyctl logs -a trading-bot

# SSH into the machine
flyctl ssh console

# Scale machines
flyctl scale count 1
```

## Free Tier Limits

Fly.io free tier includes:
- Up to 3 shared-cpu-1x 256mb VMs
- 160GB outbound data transfer
- Perfect for this trading bot!

## Updating Your Bot

When you make changes:
```bash
flyctl deploy
```

## Stopping/Starting

```bash
# Stop the app
flyctl apps stop trading-bot

# Start the app
flyctl apps start trading-bot
```

## Troubleshooting

If deployment fails:
1. Check logs: `flyctl logs`
2. Verify Dockerfile is correct
3. Ensure all dependencies are in requirements.txt
4. Check app status: `flyctl status`

## Cost

This bot should run completely FREE on Fly.io's free tier! 🎉
