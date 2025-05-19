import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# تنظیمات
TOKEN = "توکن_ربات_شما"  # جایگزین کنید
CHANNEL_USERNAME = "@DLNeon"  # کانال شما
ADMIN_ID = 123456789  # آیدی عددی شما (از @userinfobot بگیرید)

# فونت‌های مختلف
FONTS = {
    "bold": "**{}**",
    "italic": "_{}_",
    "code": "`{}`",
    "strike": "~{}~",
    "backtick": "`{}`"
}

# بررسی عضویت کاربر در کانال
async def is_member(user_id, context: CallbackContext):
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# دستور /start
async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await is_member(user_id, context):
        keyboard = [[InlineKeyboardButton("🔹 عضو شدم", callback_data="check_join")]]
        await update.message.reply_text(
            f"⚠️ برای استفاده از ربات، باید در کانال {CHANNEL_USERNAME} عضو باشید!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text("✅ خوش آمدید! یک متن بفرستید تا آن را با فونت‌های مختلف برای شما بفرستم.")

# بررسی عضویت کاربر (با اینلاین باتن)
async def check_join(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    if await is_member(user_id, context):
        await query.answer("✅ حالا می‌توانید از ربات استفاده کنید!")
        await query.edit_message_text("خوش آمدید! یک متن بفرستید تا آن را با فونت‌های مختلف برای شما بفرستم.")
    else:
        await query.answer("❌ هنوز عضو کانال نشده‌اید!", show_alert=True)

# پردازش متن کاربر و ارسال فونت‌ها
async def handle_text(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await is_member(user_id, context):
        keyboard = [[InlineKeyboardButton("🔹 عضو شدم", callback_data="check_join")]]
        await update.message.reply_text(
            f"⚠️ برای استفاده از ربات، باید در کانال {CHANNEL_USERNAME} عضو باشید!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    text = update.message.text
    responses = []
    for font_name, font_pattern in FONTS.items():
        formatted_text = font_pattern.format(text)
        responses.append(f"**{font_name}:** {formatted_text}")

    await update.message.reply_text("\n".join(responses), parse_mode="Markdown")

# تنظیمات لاگ و اجرای ربات
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(check_join, pattern="^check_join$"))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()