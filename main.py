from telegram import ReplyKeyboardMarkup, Update, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import telegram # ভার্সন চেক করার জন্য
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# আপনার আগের ইমপোর্টগুলো
from otp_manager import otp_handler
from email_tool import email_handler
from number_tool import number_handler
from repeat_tool import repeat_handler
try:
    from job_number_tool import job_number_handler
except ImportError:
    job_number_handler = None

# ✅ TOKEN
TOKEN = "8665839751:AAHRUZvLh0aY-LKRTYG_lpasQ8biNGR3Sg0"

# ✅ উন্নত ব্লু কিবোর্ড সিস্টেম
# হোস্টিংয়ে অনেক সময় সরাসরি ইমপোর্ট কাজ করে না, তাই ভেতরে চেক করা হয়েছে।
def get_blue_keyboard(buttons):
    try:
        from telegram.constants import KeyboardButtonStyle
        has_style = True
    except ImportError:
        has_style = False

    if has_style and KeyboardButtonStyle:
        blue_keyboard = []
        for row in buttons:
            # প্রতিটি বাটনকে PRIMARY (Blue) স্টাইল দেওয়া হচ্ছে
            blue_row = [KeyboardButton(text=str(text), style=KeyboardButtonStyle.PRIMARY) for text in row]
            blue_keyboard.append(blue_row)
        return ReplyKeyboardMarkup(blue_keyboard, resize_keyboard=True)
    else:
        # Fallback: যদি লাইব্রেরি পুরনো হয়
        regular_keyboard = [[KeyboardButton(text=str(text)) for text in row] for row in buttons]
        return ReplyKeyboardMarkup(regular_keyboard, resize_keyboard=True)

# ===== MAIN MENU =====
MAIN_MENU = [
    ["📲 OTP MANAGER", "📧 EMAIL TOOL"],
    ["📞 NUMBER TOOL", "🔁 REPEAT TOOL"],
    ["📱 NUMBERS"],
    ["ℹ️ HELP"]
]

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    start_msg = (
        "<b>╔══════════════════════╗</b>\n"
        "<b>   <tg-emoji emoji-id=\"5332586662629227075\">👨‍💻</tg-emoji> ALL-IN-ONE BOT <tg-emoji emoji-id=\"5332586662629227075\">👨‍💻</tg-emoji>   </b>\n"
        "<b>╚══════════════════════╝</b>\n\n"
        f'<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> <b>Status:</b> <code>Online</code>\n'
        f'<tg-emoji emoji-id="6206505206197261313">📊</tg-emoji> <b>Version:</b> <code>{telegram.__version__}</code>\n'
        "━━━━━━━━━━━━━━━━━━━━━\n"
        '<tg-emoji emoji-id="5296369303661067030">📤</tg-emoji> <i>নিচের মেনু থেকে আপনার প্রয়োজনীয় অপশনটি বেছে নিন</i>'
    )

    await update.message.reply_text(
        start_msg,
        parse_mode="HTML",
        reply_markup=get_blue_keyboard(MAIN_MENU)
    )

# ================= ROUTER =================
async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        mode = context.user_data.get("mode")
        if mode == "job_number" and job_number_handler:
            return await job_number_handler(update, context)
        return

    text = update.message.text if update.message and update.message.text else None

    if text == "ℹ️ HELP":
        help_text = (
            "<b>╔══ <tg-emoji emoji-id=\"5332679880599418983\">ℹ️</tg-emoji> HELP PANEL ══╗</b>\n\n"
            "<i>Click buttons below to contact admin or join channels.</i>"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👨‍💻 Admin", url="https://t.me/Sadhan_Chakma")],
            [InlineKeyboardButton("📢 Main Channel", url="https://t.me/Team_X_Run")],
            [InlineKeyboardButton("📦 APK Zone", url="https://t.me/+EflYyh6CP_AzZDBl")]
        ])
        return await update.message.reply_text(help_text, parse_mode="HTML", reply_markup=keyboard)

    if text == "🔙 BACK":
        return await start(update, context)

    # মেইন মেনু রাউটিং
    if text == "📲 OTP MANAGER":
        context.user_data["mode"] = "otp"
        return await otp_handler(update, context)
    if text == "📧 EMAIL TOOL":
        context.user_data["mode"] = "email"
        return await email_handler(update, context)
    if text == "📞 NUMBER TOOL":
        context.user_data["mode"] = "number"
        return await number_handler(update, context)
    if text == "🔁 REPEAT TOOL":
        context.user_data["mode"] = "repeat"
        return await repeat_handler(update, context)
    if text == "📱 NUMBERS":
        context.user_data["mode"] = "job_number"
        if job_number_handler:
            return await job_number_handler(update, context)
        else:
            return await update.message.reply_text("❌ Job Tool missing!")

    # ফাইল হ্যান্ডলিং
    if update.message and update.message.document:
        mode = context.user_data.get("mode")
        if mode == "job_number" and job_number_handler:
            return await job_number_handler(update, context)
        else:
            return await otp_handler(update, context)

    # মোড অনুযায়ী হ্যান্ডলার কল
    mode = context.user_data.get("mode")
    handlers = {
        "otp": otp_handler,
        "email": email_handler,
        "number": number_handler,
        "repeat": repeat_handler
    }

    if mode in handlers:
        await handlers[mode](update, context)
    elif mode == "job_number" and job_number_handler:
        await job_number_handler(update, context)
    else:
        if update.message and not update.message.document:
            await update.message.reply_text(
                "❌ Unknown option or Invalid action",
                reply_markup=get_blue_keyboard([["🔙 BACK"]])
            )

# ================= RUN =================
def main():
    # প্রিন্ট স্টেটমেন্ট যাতে রেলওয়ে লগে ভার্সন দেখা যায়
    print(f"Starting Bot with Library Version: {telegram.__version__}")
    
    app = ApplicationBuilder().token(TOKEN).build() 
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(router))
    app.add_handler(MessageHandler(filters.ALL, router))

    print("Bot is successfully running...")
    app.run_polling()

if __name__ == "__main__":
    main()
