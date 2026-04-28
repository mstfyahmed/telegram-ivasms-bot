import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Config:
    """Bot Configuration"""
    
    # Telegram
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    BOT_USERNAME = os.getenv('BOT_USERNAME', 'telegram_ivasms_bot')
    
    if not BOT_TOKEN:
        raise ValueError("❌ BOT_TOKEN environment variable is required!")
    
    # IvaSms
    IVASMS_API_URL = os.getenv('IVASMS_API_URL')
    IVASMS_PANEL_URL = os.getenv('IVASMS_PANEL_URL', 'https://panel.ivasms.com')
    IVASMS_COOKIE_PATH = os.getenv('IVASMS_COOKIE_PATH', './cookies.json')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot_data.db')
    BASE_DIR = Path(__file__).parent
    DATABASE_PATH = BASE_DIR / 'bot_data.db'
    
    # Admin
    ADMIN_IDS = [int(x.strip()) for x in os.getenv('ADMIN_IDS', '').split(',') if x.strip()]
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'bot.log')
    
    # Server
    PORT = int(os.getenv('PORT', 8000))
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # Timeouts
    REQUEST_TIMEOUT = 30
    OTP_WAIT_TIMEOUT = 300  # 5 minutes
    
    # Services
    SERVICES = {
        'whatsapp': '📱 WhatsApp',
        'telegram': '💬 Telegram',
        'facebook': '👍 Facebook',
        'instagram': '📷 Instagram',
        'twitter': '🐦 Twitter',
        'google': '🔍 Google',
        'tiktok': '🎵 TikTok',
        'discord': '💬 Discord',
    }
    
    # Countries
    COUNTRIES = {
        'us': '🇺🇸 USA',
        'uk': '🇬🇧 UK',
        'ca': '🇨🇦 Canada',
        'au': '🇦🇺 Australia',
        'in': '🇮🇳 India',
        'br': '🇧🇷 Brazil',
        'mx': '🇲🇽 Mexico',
        'de': '🇩🇪 Germany',
        'fr': '🇫🇷 France',
        'ru': '🇷🇺 Russia',
    }
    
    # Messages
    MESSAGES = {
        'welcome': '👋 Welcome to IvaSms Number Distribution Bot!\n\nChoose an option:',
        'request_service': '🔍 Select a service:',
        'request_country': '🌍 Select a country:',
        'number_assigned': '✅ Number Assigned!\n\n📱 Your Number:\n`{number}`\n\nUse this number to verify your account.',
        'waiting_otp': '⏳ Waiting for OTP...\n\nThis may take a few minutes.',
        'otp_received': '✅ OTP Received!\n\n📝 Code:\n`{otp}`\n\nExpires in 5 minutes.',
        'error': '❌ Error: {error}\n\nPlease try again or contact support.',
    }

print("✅ Configuration loaded successfully!")
