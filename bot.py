from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os
import asyncio

from config import BOT_TOKEN
from db import save_user, update_region, get_user, count_user, get_all_users 
from prayers import get_prayer_times
from ayat import get_random_ayat
# Hadislar funksiyasini import qilamiz (hadislar.py fayli bo'lishi kerak)
try:
    from hadislar import get_random_hadis
except ImportError:
    def get_random_hadis(): return "📜 Hadislar fayli topilmadi."

ADMIN_ID = 5908568613

def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("📅 Bugungi namoz vaqtlari")],
        [KeyboardButton("📖 Tasodifiy oyat"), KeyboardButton("📜 Tasodifiy hadis")],
        [KeyboardButton("📍 Viloyatni o'zgartirish"), KeyboardButton("📊 Statistika (admin)")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

REGIONS = [
    "Toshkent", "Andijon", "Buxoro", "Farg'ona", "Jizzax",
    "Namangan", "Navoiy", "Qashqadaryo", "Qoraqalpog'iston",
    "Samarqand", "Sirdaryo", "Surxondaryo", "Xorazm"
]

# --- 3-USUL: YORDAM KOMANDASI ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🆘 *Yordam markazi*\n\n"
        "Agar botda xatolik yuz bersa, quyidagilarni bajaring:\n"
        "1. /start buyrug'ini bosing.\n"
        "2. Viloyatingizni qayta tanlang.\n\n"
        "Bot orqali namoz vaqtlari, oyat va hadislar olishingiz mumkin."
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# --- ADMIN UCHUN XABAR YUBORISH (/send) ---
async def send_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        if context.args:
            text_to_send = " ".join(context.args)
            all_users = get_all_users()
            count = 0
            await update.message.reply_text(f"⏳ Xabar {len(all_users)} kishiga yuborilmoqda...")
            
            for uid in all_users:
                try:
                    await context.bot.send_message(chat_id=uid, text=text_to_send)
                    count += 1
                    await asyncio.sleep(0.05) # Telegram bloklamasligi uchun
                except: continue
            
            await update.message.reply_text(f"✅ Xabar {count} ta foydalanuvchiga yetkazildi.")
        else:
            await update.message.reply_text("⚠️ Namuna: `/send Xabar matni`", parse_mode="Markdown")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)
    print(f"🚀 [START] ID: {user.id} | Ism: {user.first_name}")
    
    await update.message.reply_text(
        f"Assalomu alaykum, {user.first_name}!\n"
        "Namoz vaqtlari, Oyatlar va Hadislar botiga xush kelibsiz.\n"
        "Iltimos, viloyatingizni tanlang:",
        reply_markup=ReplyKeyboardMarkup([[r] for r in REGIONS], resize_keyboard=True)
    )

async def admin_stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        user_list = get_all_users()
        total_count = len(user_list)
        msg = f"📊 *Bot statistikasi*\n\n👥 *Jami foydalanuvchilar:* {total_count} ta"
        await update.message.reply_text(msg, parse_mode="Markdown")

async def set_region_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[r] for r in REGIONS]
    await update.message.reply_text(
        "Iltimos, yashash viloyatingizni tanlang:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    user_id = user.id


    # --- 4-USUL: BAZADA BORLIGINI TEKSHIRISH ---
    user_data = get_user(user_id)
    if not user_data and text != "/start":
        await update.message.reply_text(
            "⚠️ *Bot tizimi yangilandi!*\n\n"
            "Botdan foydalanish uchun iltimos qaytadan /start buyrug'ini bosing.",
            parse_mode="Markdown"
        )
        return

    if text in REGIONS:
        update_region(user_id, text)
        print(f"📍 [REGION] ID: {user_id} | Viloyat: {text}")
        
        # Viloyat tanlangach avtomatik namoz vaqtini chiqarish
        times = get_prayer_times(text)
        msg = f"✅ Viloyat saqlandi: *{text}*\n\n🕌 *Bugungi vaqtlar:*\n"
        for k, v in times.items():
            msg += f"🔸 *{k}:* {v}\n"
        
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=main_menu_keyboard())

    elif text == "📅 Bugungi namoz vaqtlari":
        if not user_data or not user_data.get("region"):
            await set_region_request(update, context)
        else:
            times = get_prayer_times(user_data["region"])
            msg = f"🕌 *{user_data['region']}* uchun namoz vaqtlari:\n\n"
            for k, v in times.items():
                msg += f"🔸 *{k}:* {v}\n"
            await update.message.reply_text(msg, parse_mode="Markdown")

    elif text == "📖 Tasodifiy oyat":
        ayat_text = get_random_ayat()
        await update.message.reply_text(f"✨ *Tasodifiy oyati:*\n\n{ayat_text}", parse_mode="Markdown")

    elif text == "📜 Tasodifiy hadis":
        hadis_text = get_random_hadis()
        await update.message.reply_text(f"✨ *Tasodifiy hadis:*\n\n{hadis_text}", parse_mode="Markdown")

    elif text == "📍 Viloyatni o'zgartirish":
        await set_region_request(update, context)
    
    elif text == "📊 Statistika":
        await admin_stat(update, context)

    else:
        await update.message.reply_text("Iltimos, menyudagi tugmalardan foydalaning.", reply_markup=main_menu_keyboard())

def main():
    token = os.getenv("BOT_TOKEN") or BOT_TOKEN
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stat", admin_stat))
    app.add_handler(CommandHandler("send", send_all)) # Admin broadcast
    app.add_handler(CommandHandler("region", set_region_request))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("[INFO] Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
