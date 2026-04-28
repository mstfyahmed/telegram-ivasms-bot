#!/usr/bin/env python3
"""
Telegram IvaSms Number Distribution Bot

A bot that distributes temporary phone numbers from IvaSms panel
and forwards OTP codes to Telegram users.

Author: Sadeemali829
Repository: https://github.com/Sadeemali829/telegram-ivasms-bot
"""

import logging
import sys
import os
import threading
from flask import Flask
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.constants import ChatAction

# Import configuration
from config import Config
from utils.logger import setup_logger
from database import get_session
from ivasms_api import api

# Import handlers
from handlers.user_handlers import start, help_handler
from handlers.admin_handlers import admin_menu
from handlers.callback_handlers import button_callback

# --- Render Keep-Alive Logic ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running!", 200

def run_flask():
    # Render automatically provides a PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    # use_reloader=False is critical when running in a thread
    app.run(host='0.0.0.0', port=port, use_reloader=False)
# ------------------------------

logger = logging.getLogger(__name__)

async def error_handler(update, context):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.message:
        await update.message.reply_text(
            f"❌ An error occurred: {str(context.error)}\n\n"
            "Please try again or contact support."
        )

async def post_init(app):
    """Async initialization"""
    logger.info("🤖 Bot is starting...")
    
    # Check IvaSms API
    if api.check_api_status():
        logger.info("✅ IvaSms API connected")
    else:
        logger.warning("⚠️ IvaSms API connection failed")
    
    logger.info("✅ Bot initialization complete")

def main():
    """Start the bot"""
    try:
        # Setup logging
        setup_logger()
        logger.info("="*50)
        logger.info("🤖 Telegram IvaSms Number Distribution Bot")
        logger.info("="*50)
        
        # Validate configuration
        if not Config.BOT_TOKEN:
            logger.error("❌ BOT_TOKEN is required in .env file")
            sys.exit(1)
        
        if not api.cookies:
            logger.warning("⚠️ IvaSms cookies not found. Bot will run but may not receive OTPs")
        
        # Start Flask in a background thread BEFORE the bot polling starts
        logger.info("🌐 Starting keep-alive Flask server...")
        threading.Thread(target=run_flask, daemon=True).start()
        
        # Create application
        application = Application.builder().token(Config.BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_handler))
        application.add_handler(CommandHandler("admin", admin_menu))
        application.add_handler(CallbackQueryHandler(button_callback))
        
        # Error handler
        application.add_error_handler(error_handler)
        
        # Post init
        application.post_init = post_init
        
        # Start bot
        logger.info(f"🚀 Starting bot polling...")
        logger.info(f"📍 Bot Username: @{Config.BOT_USERNAME}")
        logger.info(f"🔌 IvaSms API: {Config.IVASMS_API_URL}")
        logger.info("Press Ctrl+C to stop\n")
        
        application.run_polling(allowed_updates=["message", "callback_query"])
    
    except KeyboardInterrupt:
        logger.info("\n⏹️ Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
