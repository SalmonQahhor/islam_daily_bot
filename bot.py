from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from config import BOT_TOKEN
from db import save_user, update_region, get_user
from prayers import get_prayer_times
from ayat import get_random_ayat

# Doimiy menyu tugmalari
def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("📅 Bugungi namoz vaqtlari")],
        [KeyboardButton("📖 Tasodifiy oyat"), KeyboardButton("📍 Viloyatni o'zgartirish")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Viloyatlar menyusi
REGIONS = [
    "Toshkent", "Andijon", "Buxoro", "Farg'ona", "Jizzax",
    "Namangan", "Navoiy", "Qashqadaryo", "Qoraqalpog'iston",
    "Samarqand", "Sirdaryo", "Surxondaryo", "Xorazm"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_user.id)
    await update.message.reply_text(
        f"Assalomu alaykum, {update.effective_user.first_name}!\n"
        "Namoz vaqtlari va Oyatlar botiga xush kelibsiz.",
        reply_markup=main_menu_keyboard()
    )

async def set_region_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[r] for r in REGIONS]
    await update.message.reply_text(
        "Iltimos, yashash viloyatingizni tanlang:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    # 1. Viloyat tanlangan bo'lsa
    if text in REGIONS:
        update_region(user_id, text)
        await update.message.reply_text(
            f"✅ Viloyat muvaffaqiyatli saqlandi: {text}",
            reply_markup=main_menu_keyboard()
        )

    # 2. Namoz vaqtlari tugmasi
    elif text == "📅 Bugungi namoz vaqtlari":
        user = get_user(user_id)
        if not user or not user.get("region"):
            await set_region_request(update, context)
        else:
            times = get_prayer_times(user["region"])
            msg = f"🕌 *{user['region']}* uchun namoz vaqtlari:\n\n"
            for k, v in times.items():
                msg += f"🔸 *{k}:* {v}\n"
            await update.message.reply_text(msg, parse_mode="Markdown")

    # 3. Oyat tugmasi
    elif text == "📖 Tasodifiy oyat":
        ayat_text = get_random_ayat()
        await update.message.reply_text(f"✨ *Kun oyati:*\n\n{ayat_text}", parse_mode="Markdown")

    # 4. Viloyatni o'zgartirish tugmasi
    elif text == "📍 Viloyatni o'zgartirish":
        await set_region_request(update, context)

    else:
        await update.message.reply_text("Iltimos, menyudagi tugmalardan foydalaning.", reply_markup=main_menu_keyboard())

# Botni sozlash
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("region", set_region_request))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    print("[INFO] Bot ishga tushdi...")
    app.run_polling()