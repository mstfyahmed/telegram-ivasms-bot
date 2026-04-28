# 🤖 Telegram IvaSms Number Distribution Bot

Automatically distribute phone numbers and forward OTP codes from IvaSms panel to Telegram users with a beautiful, user-friendly interface.

## 🎯 Features

- ✅ **IvaSms Panel Integration** - Fetch phone numbers from your IvaSms account
- ✅ **OTP Forwarding** - Automatically capture and forward OTP messages
- ✅ **Copy Buttons** - One-click copy for numbers and OTP codes
- ✅ **User Tracking** - Track which user has which number
- ✅ **24/7 Uptime** - Deploy on Render.com with keep-alive monitoring
- ✅ **Admin Dashboard** - Manage users and view statistics
- ✅ **Multi-Service Support** - WhatsApp, Telegram, Facebook, etc.
- ✅ **Error Handling** - Automatic error recovery and logging

## 📋 Requirements

- Python 3.8+
- Telegram Bot Token (from @BotFather)
- IvaSms Panel account with active phone numbers
- IvaSms API cookies.json file

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Sadeemali829/telegram-ivasms-bot.git
cd telegram-ivasms-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file:

```env
BOT_TOKEN=your_telegram_bot_token_here
IVASMS_API_URL=https://your-ivasms-api.onrender.com
IVASMS_PANEL_URL=https://panel.ivasms.com
DATABASE_URL=sqlite:///bot_data.db
ADMIN_IDS=123456789,987654321
LOG_LEVEL=INFO
```

### 4. Prepare IvaSms Cookies

Place your `cookies.json` file in the project root:

```json
{
  "session_id": "your_session_id",
  "auth_token": "your_auth_token"
}
```

### 5. Run Locally

```bash
python main.py
```

## 📦 Deploy to Render.com (FREE)

### Step 1: Push to GitHub

Your code is already here! The repository is set up and ready.

### Step 2: Deploy on Render.com

1. Go to [Render.com](https://render.com) and sign up
2. Click **"New +"** → **"Web Service"** (NOT Background Worker)
3. Connect your GitHub account and select `telegram-ivasms-bot` repository
4. Configure the following:
   - **Name**: `telegram-ivasms-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Instance Type**: `Free`

5. Add Environment Variables in Render dashboard:
   - `BOT_TOKEN`: Your Telegram bot token
   - `IVASMS_API_URL`: Your IvaSms API URL
   - `IVASMS_PANEL_URL`: IvaSms panel URL
   - `DATABASE_URL`: Leave as is (uses SQLite)
   - `ADMIN_IDS`: Your Telegram user IDs (comma-separated)

6. Click **"Create Web Service"**

### Step 3: Keep Bot Alive 24/7 (Free with UptimeRobot)

1. Go to [UptimeRobot.com](https://uptimerobot.com) and sign up (free)
2. Click **"Add New Monitor"**
3. Configure:
   - **Monitor Type**: `HTTP(s)`
   - **URL**: Your Render app URL (e.g., `https://telegram-ivasms-bot.onrender.com`)
   - **Monitoring Interval**: `5 minutes`
4. Save

This will ping your bot every 5 minutes to prevent it from going to sleep! ⏰

## 🎮 Bot Commands

### User Commands

- `/start` - Start the bot and see main menu
- `/request` - Request a new phone number
- `/myotp` - Check OTP for your current number
- `/mynumber` - View your assigned number
- `/cancel` - Cancel current operation
- `/help` - Get help

### Admin Commands (for ADMIN_IDS)

- `/admin` - Admin panel
- `/stats` - View bot statistics
- `/users` - List all active users
- `/broadcast [message]` - Send message to all users
- `/reload` - Reload IvaSms data

## 📊 Project Structure

```
telegram-ivasms-bot/
├── main.py                 # Main bot entry point
├── config.py              # Configuration management
├── ivasms_api.py          # IvaSms API integration
├── database.py            # Database management (SQLite)
├── handlers/
│   ├── user_handlers.py   # User command handlers
│   ├── admin_handlers.py  # Admin command handlers
│   └── callback_handlers.py # Button callback handlers
├── utils/
│   ├── logger.py          # Logging setup
│   ├── validators.py      # Input validation
│   └── helpers.py         # Helper functions
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── cookies.json.example  # Example IvaSms cookies file
└── README.md             # This file
```

## 🔧 Configuration Guide

### IvaSms API Setup

1. Get your IvaSms panel cookies:
   - Log in to your IvaSms panel
   - Open Developer Tools (F12 in browser)
   - Go to **Application** → **Cookies**
   - Copy the session cookie and save to `cookies.json`

2. Set up IvaSms API server (or use existing):
   ```bash
   # If running your own IvaSms API
   git clone https://github.com/Arslan-MD/IvaSms-api.git
   cd IvaSms-api
   pip install -r requirements.txt
   python app.py
   ```

### Telegram Bot Setup

1. Chat with [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` command
3. Choose a name (e.g., "My IvaSms Number Bot")
4. Choose a username (e.g., "my_ivasms_number_bot")
5. Copy your **API Token** and save to `.env`

## 📝 Example Usage

```
User: /start
Bot: 👋 Welcome to IvaSms Number Bot!
     
     Choose an option:
     [📱 Request Number] [📋 My Number]
     [✉️ My OTP] [❓ Help]

User: [Clicks 📱 Request Number]
Bot: 🌍 Select a country:
     [🇺🇸 USA] [🇬🇧 UK] [🇮🇳 India]

User: [Clicks 🇺🇸 USA]
Bot: 📱 Your Number:
     +1234567890
     
     [📋 Copy] [⏳ Wait for OTP]

(When OTP arrives)
Bot: ✅ Your OTP:
     123456
     
     [📋 Copy OTP]
```

## 🐛 Troubleshooting

### Bot Not Responding

1. Check if `BOT_TOKEN` is correct
2. Verify bot is running: `python main.py`
3. Check logs for errors

### IvaSms API Connection Error

1. Verify `IVASMS_API_URL` is correct
2. Check if `cookies.json` file exists and is valid
3. Ensure IvaSms API server is running
4. Test API manually: `curl https://your-api-url/`

### Numbers Not Showing

1. Check if you have active numbers in IvaSms panel
2. Verify API cookies are still valid (log in again if needed)
3. Check bot logs for API errors

## 📈 Statistics

The bot tracks:
- Total users
- Numbers distributed
- OTPs received
- Services used (WhatsApp, Telegram, etc.)
- Daily/weekly/monthly stats

Access via `/stats` command (admin only)

## 🔐 Security

- Bot tokens are stored in environment variables
- IvaSms cookies are never exposed in logs
- User data is stored securely in SQLite database
- Admin commands require verified user IDs
- All API calls are logged for debugging

## 📞 Support

For issues or feature requests:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Open an issue on GitHub
3. Contact IvaSms support for panel-related issues

## 📄 License

MIT License - Feel free to use this for personal or commercial projects.

## 🙏 Credits

- Built with [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- IvaSms API by [Arslan-MD](https://github.com/Arslan-MD/IvaSms-api)
- Deployed on [Render.com](https://render.com) with [UptimeRobot](https://uptimerobot.com)

---

**Made with ❤️ for the community**
