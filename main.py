from telegram import ReplyKeyboardMarkup, Update, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from otp_manager import otp_handler
from email_tool import email_handler
from number_tool import number_handler
from repeat_tool import repeat_handler

# ✅ TOKEN (এখানেই থাকবে)
TOKEN = "8658364991:AAEYny80WCZh3lgf0JMFpYhcxdiO0tE31so"

# ===== BLUE KEYBOARD SYSTEM =====
try:
    from telegram.constants import KeyboardButtonStyle
except ImportError:
    KeyboardButtonStyle = None


def get_blue_keyboard(buttons):
    if KeyboardButtonStyle:
        blue_keyboard = []
        for row in buttons:
            blue_row = [KeyboardButton(text, style=KeyboardButtonStyle.PRIMARY) for text in row]
            blue_keyboard.append(blue_row)
        return ReplyKeyboardMarkup(blue_keyboard, resize_keyboard=True)
    else:
        regular_keyboard = [[KeyboardButton(text) for text in row] for row in buttons]
        return ReplyKeyboardMarkup(regular_keyboard, resize_keyboard=True)


# ===== MAIN MENU =====
MAIN_MENU = [
    ["📲 OTP MANAGER", "📧 EMAIL TOOL"],
    ["📞 NUMBER TOOL", "🔁 REPEAT TOOL"],
    ["ℹ️ HELP"]
]


# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    start_msg = (
        "<b>╔══════════════════════╗</b>\n"
        "<b>   <tg-emoji emoji-id=\"5332586662629227075\">👨‍💻</tg-emoji> ALL-IN-ONE BOT <tg-emoji emoji-id=\"5332586662629227075\">👨‍💻</tg-emoji>   </b>\n"
        "<b>╚══════════════════════╝</b>\n\n"
        '<tg-emoji emoji-id="5345905193005371012">⚡️</tg-emoji> <b>Status:</b> <code>Online & Ready</code>\n'
        '<tg-emoji emoji-id="6206505206197261313">📊</tg-emoji> <b>System:</b> <code>High Performance</code>\n'
        '<tg-emoji emoji-id="6232999738459823976">✅</tg-emoji> <b>Access:</b> <code>Full Features Enabled</code>\n'
        "━━━━━━━━━━━━━━━━━━━━━\n"
        '<tg-emoji emoji-id="5296369303661067030">📤</tg-emoji> <i>নিচের মেনু থেকে আপনার প্রয়োজনীয় অপশনটি বেছে নিন</i>'
    )

    await update.message.reply_text(
        start_msg,
        parse_mode="HTML",
        reply_markup=get_blue_keyboard(MAIN_MENU)  # 🔵 BLUE MENU
    )


# ================= ROUTER =================
async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text if update.message.text else None

    # ===== HELP =====
    if text == "ℹ️ HELP":

        help_text = (
            "<b>╔══ <tg-emoji emoji-id=\"5332679880599418983\">ℹ️</tg-emoji> HELP PANEL ══╗</b>\n\n"
            '<tg-emoji emoji-id="6213065824576478666">👨‍💻</tg-emoji> <b>Admin & Links</b>\n\n'
            "<i>Click buttons below</i>"
        )

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👨‍💻 Admin", url="https://t.me/Sadhan_Chakma")],
            [InlineKeyboardButton("📢 Main Channel", url="https://t.me/Team_X_Run")],
            [InlineKeyboardButton("📦 APK Zone", url="https://t.me/+EflYyh6CP_AzZDBl")]
        ])

        return await update.message.reply_text(
            help_text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

    # ===== FILE =====
    if update.message.document:
        return await otp_handler(update, context)

    # ===== MENU =====
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

    # ===== BACK =====
    if text == "🔙 BACK":
        return await start(update, context)

    # ===== MODE =====
    mode = context.user_data.get("mode")

    if mode == "otp":
        await otp_handler(update, context)
    elif mode == "email":
        await email_handler(update, context)
    elif mode == "number":
        await number_handler(update, context)
    elif mode == "repeat":
        await repeat_handler(update, context)
    else:
        await update.message.reply_text(
            "❌ Unknown option",
            reply_markup=get_blue_keyboard([["🔙 BACK"]])  # 🔵 BLUE BACK
        )


# ================= RUN =================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, router))

    print("Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
