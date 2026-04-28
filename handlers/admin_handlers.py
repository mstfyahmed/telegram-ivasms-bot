from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from config import Config
from database import get_all_users, get_stats
from ivasms_api import api
import logging

logger = logging.getLogger(__name__)

async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin panel"""
    user_id = update.effective_user.id
    
    if user_id not in Config.ADMIN_IDS:
        await update.message.reply_text("❌ You don't have admin access.")
        return
    
    keyboard = [
        [InlineKeyboardButton("📊 Statistics", callback_data="admin_stats")],
        [InlineKeyboardButton("👥 Active Users", callback_data="admin_users")],
        [InlineKeyboardButton("🔄 Reload API", callback_data="admin_reload")],
        [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🛡️ **Admin Panel**",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot statistics"""
    query = update.callback_query
    user_id = update.effective_user.id
    
    if user_id not in Config.ADMIN_IDS:
        await query.answer("❌ Access denied", show_alert=True)
        return
    
    try:
        stats = get_stats()
        api_status = "✅ Online" if api.check_api_status() else "❌ Offline"
        
        stats_text = f"""📊 **Bot Statistics**

👥 Total Users: {stats['total_users']}
📱 Total Numbers Assigned: {stats['total_numbers']}
✉️ Total OTPs Received: {stats['total_otps']}

🔌 IvaSms API Status: {api_status}
📍 API URL: `{Config.IVASMS_API_URL}`
"""
        
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="admin_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            stats_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        await query.answer(f"Error: {str(e)}", show_alert=True)

async def admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show active users"""
    query = update.callback_query
    user_id = update.effective_user.id
    
    if user_id not in Config.ADMIN_IDS:
        await query.answer("❌ Access denied", show_alert=True)
        return
    
    try:
        users = get_all_users()
        
        if not users:
            await query.edit_message_text("No active users yet.")
            return
        
        users_text = "👥 **Active Users**\n\n"
        for user in users[:10]:  # Show first 10
            username = user.username or "No username"
            users_text += f"• {user.first_name} (@{username})\n"
        
        if len(users) > 10:
            users_text += f"\n... and {len(users) - 10} more users"
        
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="admin_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            users_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        await query.answer(f"Error: {str(e)}", show_alert=True)
