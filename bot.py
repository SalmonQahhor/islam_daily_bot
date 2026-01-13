from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os

from config import BOT_TOKEN
# db.py faylingizda get_all_users funksiyasi bo'lishi shart
from db import save_user, update_region, get_user, count_user, get_all_users 
from prayers import get_prayer_times
from ayat import get_random_ayat

# Sizning Telegram ID raqamingiz
ADMIN_ID = 5908568613

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

# --- ADMIN STATISTIKA FUNKSIYASI ---
async def admin_stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        try:
            count = count_user() # Jami soni
            all_users = get_all_users() # Hamma IDlar ro'yxati
            
            # Oxirgi 20 ta foydalanuvchini ajratib olish
            last_20 = all_users[-20:] 
            ids_text = ""
            for i, uid in enumerate(last_20, 1):
                ids_text += f"{i}. 🆔 `{uid}`\n"
            
            msg = (
                f"📊 *Bot statistikasi*\n\n"
                f"👥 *Jami foydalanuvchilar:* {count} ta\n\n"
                f"📝 *Oxirgi 20 ta foydalanuvchi ID-lari:*\n{ids_text}"
            )
            
            await update.message.reply_text(msg, parse_mode="MarkdownV2")
        except Exception as e:
            await update.message.reply_text(f"Xatolik: {e}")
    else:
        # Boshqalarga javob bermaydi
        pass

async def set_region_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[r] for r in REGIONS]
    await update.message.reply_text(
        "Iltimos, yashash viloyatingizni tanlang:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if text in REGIONS:
        update_region(user_id, text)
        await update.message.reply_text(
            f"✅ Viloyat muvaffaqiyatli saqlandi: {text}",
            reply_markup=main_menu_keyboard()
        )
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
    elif text == "📖 Tasodifiy oyat":
        ayat_text = get_random_ayat()
        await update.message.reply_text(f"✨ *Kun oyati:*\n\n{ayat_text}", parse_mode="Markdown")
    elif text == "📍 Viloyatni o'zgartirish":
        await set_region_request(update, context)
    else:
        await update.message.reply_text("Iltimos, menyudagi tugmalardan foydalaning.", reply_markup=main_menu_keyboard())

def main():
    token = os.getenv("BOT_TOKEN") or BOT_TOKEN
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stat", admin_stat)) # Buyruq qo'shildi
    app.add_handler(CommandHandler("region", set_region_request))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("[INFO] Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
