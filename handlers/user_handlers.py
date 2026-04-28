from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from config import Config
from database import add_user, get_user, add_number
from ivasms_api import api
from utils.helpers import get_service_emoji, get_country_emoji
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    
    # Add user to database
    add_user(user.id, user.username, user.first_name, user.last_name)
    
    # Create main menu
    keyboard = [
        [
            InlineKeyboardButton("📱 Request Number", callback_data="request_number"),
            InlineKeyboardButton("📋 My Number", callback_data="my_number")
        ],
        [
            InlineKeyboardButton("✉️ My OTP", callback_data="my_otp"),
            InlineKeyboardButton("❓ Help", callback_data="help")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""👋 Welcome {user.first_name}!

Welcome to IvaSms Number Distribution Bot 🤖

This bot helps you get temporary phone numbers from IvaSms for:
✅ Account verification
✅ OTP reception
✅ Testing & development

Choose an option below:"""
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    logger.info(f"✅ User {user.id} started bot")

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """❓ **How to Use This Bot**

**Getting a Phone Number:**
1. Click "📱 Request Number"
2. Select a service (WhatsApp, Telegram, etc.)
3. Select a country
4. Bot will assign you a temporary number

**Receiving OTP:**
1. Use the assigned number for verification
2. When OTP arrives, click "✉️ My OTP"
3. Copy the code and use it

**Your Numbers:**
- Numbers are temporary (valid for ~5 minutes)
- One number per request
- Click "📋 My Number" to see current number

**Commands:**
/start - Main menu
/help - This help message
/cancel - Cancel operation

**Supported Services:**
📱 WhatsApp, 💬 Telegram, 👍 Facebook
📷 Instagram, 🐦 Twitter, 🔍 Google
🎵 TikTok, 💬 Discord

**Need Help?**
If you have issues or need support, please contact the administrator.

⚠️ **Important:**
- Do not share your numbers with others
- Numbers expire after use
- Use responsibly
"""
    
    await update.message.reply_text(
        help_text,
        parse_mode=ParseMode.MARKDOWN
    )

async def request_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle service selection"""
    query = update.callback_query
    await query.answer()
    
    # Create service buttons
    keyboard = []
    for service_key, service_name in list(Config.SERVICES.items())[:2]:
        keyboard.append([InlineKeyboardButton(service_name, callback_data=f"service_{service_key}")])
    for service_key, service_name in list(Config.SERVICES.items())[2:4]:
        keyboard.append([InlineKeyboardButton(service_name, callback_data=f"service_{service_key}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🔍 Select a service:",
        reply_markup=reply_markup
    )

async def request_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle country selection"""
    query = update.callback_query
    service = query.data.split('_')[1]
    
    # Store selected service
    context.user_data['service'] = service
    await query.answer()
    
    # Create country buttons
    keyboard = []
    for country_key, country_name in list(Config.COUNTRIES.items())[:2]:
        keyboard.append([InlineKeyboardButton(country_name, callback_data=f"country_{country_key}")])
    for country_key, country_name in list(Config.COUNTRIES.items())[2:4]:
        keyboard.append([InlineKeyboardButton(country_name, callback_data=f"country_{country_key}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="request_number")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    service_name = Config.SERVICES.get(service, 'Unknown')
    await query.edit_message_text(
        f"🌍 Select a country for {service_name}:",
        reply_markup=reply_markup
    )

async def assign_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Assign phone number to user"""
    query = update.callback_query
    country = query.data.split('_')[1]
    service = context.user_data.get('service', 'unknown')
    user_id = update.effective_user.id
    
    # Store selected country
    context.user_data['country'] = country
    await query.answer("⏳ Getting a number for you...")
    
    try:
        # Get latest SMS to extract available numbers
        # This is a placeholder - in real implementation, you'd get from your number pool
        phone_number = f"+1{user_id}123456"  # Placeholder
        
        # Save to database
        add_number(user_id, phone_number, service, country)
        
        # Create action buttons
        keyboard = [
            [
                InlineKeyboardButton("📋 Copy Number", callback_data=f"copy_number_{phone_number}"),
            ],
            [
                InlineKeyboardButton("⏳ Wait for OTP", callback_data="wait_otp"),
            ],
            [
                InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        service_emoji = get_service_emoji(service)
        country_emoji = get_country_emoji(country)
        
        message_text = f"""✅ **Number Assigned!**

📱 Your Phone Number:
`{phone_number}`

🔍 Service: {service_emoji} {Config.SERVICES.get(service, 'Unknown')}
🌍 Country: {country_emoji} {Config.COUNTRIES.get(country, 'Unknown')}

**Next Steps:**
1. Use this number to verify your account
2. When you receive the OTP, click "⏳ Wait for OTP"
3. Copy the code and use it

⏱️ Number expires in 5 minutes
"""
        
        await query.edit_message_text(
            message_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info(f"✅ Assigned number {phone_number} to user {user_id}")
        
    except Exception as e:
        logger.error(f"Error assigning number: {e}")
        await query.edit_message_text(
            f"❌ Error: Failed to get number\n\n{str(e)}"
        )
