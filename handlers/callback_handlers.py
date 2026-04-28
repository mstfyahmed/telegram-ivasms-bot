from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from config import Config
from database import get_user
from handlers.user_handlers import request_service, request_country, assign_number, start as user_start
from handlers.admin_handlers import admin_menu, admin_stats, admin_users
import logging

logger = logging.getLogger(__name__)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all button callbacks"""
    query = update.callback_query
    data = query.data
    
    try:
        # User handlers
        if data == "request_number":
            await request_service(update, context)
        
        elif data == "my_number":
            user = get_user(update.effective_user.id)
            if user and user.current_number:
                message = f"📱 Your Current Number:\n\n`{user.current_number}`"
                keyboard = [[InlineKeyboardButton("📋 Copy", callback_data=f"copy_{user.current_number}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
            else:
                await query.answer("You don't have an assigned number yet. Request one!", show_alert=True)
        
        elif data == "my_otp":
            user = get_user(update.effective_user.id)
            if user and user.current_number:
                await query.answer("⏳ Checking for OTP...")
                # In real implementation, check database for OTP
                await query.edit_message_text("No OTP received yet. Please wait...")
            else:
                await query.answer("Request a number first!", show_alert=True)
        
        elif data == "help":
            help_text = """❓ **How to Use**

1. Click "📱 Request Number"
2. Select service and country
3. Get your temporary number
4. Use for verification
5. Check "✉️ My OTP" when code arrives
"""
            keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(help_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        
        elif data.startswith("service_"):
            await request_country(update, context)
        
        elif data.startswith("country_"):
            await assign_number(update, context)
        
        elif data.startswith("copy_"):
            # Copy to clipboard is handled by Telegram client
            await query.answer("Copied to clipboard!", show_alert=False)
        
        elif data == "back_to_menu":
            await user_start(update, context)
        
        # Admin handlers
        elif data == "admin_menu":
            await admin_menu(update, context)
        
        elif data == "admin_stats":
            await admin_stats(update, context)
        
        elif data == "admin_users":
            await admin_users(update, context)
        
        else:
            logger.warning(f"Unknown callback data: {data}")
    
    except Exception as e:
        logger.error(f"Error handling callback: {e}")
        await query.answer(f"Error: {str(e)}", show_alert=True)
