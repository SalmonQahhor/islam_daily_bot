from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os
import asyncio
import random

from config import BOT_TOKEN
from db import save_user, update_region, get_user, count_user, get_all_users, check_task_limit 
from prayers import get_prayer_times
from ayat import get_random_ayat
from amallar import AMALLAR 

try:
    from hadislar import get_random_hadis
except ImportError:
    def get_random_hadis(): return "📜 Hadislar fayli topilmadi."

ADMIN_ID = 5908568613
is_broadcasting = False

def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("📅 Bugungi namoz vaqtlari")],
        [KeyboardButton("📖 Tasodifiy oyat"), KeyboardButton("📜 Tasodifiy hadis")],
        [KeyboardButton("📍 Viloyatni o'zgartirish")],
        [KeyboardButton("✨ Bugungi amal"), KeyboardButton("📊 Statistika (admin)")] 
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

REGIONS = [
    "Toshkent", "Andijon", "Buxoro", "Farg'ona", "Jizzax",
    "Namangan", "Navoiy", "Qashqadaryo", "Qoraqalpog'iston",
    "Samarqand", "Sirdaryo", "Surxondaryo", "Xorazm"
]

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🆘 *Yordam markazi*\n\n"
        "Agar botda xatolik yuz bersa, quyidagilarni bajaring:\n"
        "1. /start buyrug'ini bosing.\n"
        "2. Viloyatingizni qayta tanlang.\n\n"
        "Bot orqali namoz vaqtlari, oyat va hadislar olishingiz mumkin."
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def send_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_broadcasting
    if update.effective_user.id == ADMIN_ID:
        is_broadcasting = True
        await update.message.reply_text("📝 Xabarni yuboring (rasm, matn, enter saqlanadi):")

async def handle_admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_broadcasting
    if update.effective_user.id == ADMIN_ID and is_broadcasting:
        if update.message.text == "/send": return False
        
        all_users = get_all_users()
        count, blocked = 0, 0
        status_msg = await update.message.reply_text(f"⏳ Yuborilmoqda: 0/{len(all_users)}")
        
        for uid in all_users:
            try:
                await update.message.copy(chat_id=uid)
                count += 1
                if count % 10 == 0:
                    await status_msg.edit_text(f"⏳ Yuborilmoqda: {count}/{len(all_users)}")
                await asyncio.sleep(0.05)
            except:
                blocked += 1
        
        is_broadcasting = False
        await update.message.reply_text(f"✅ Tugadi\nQabul qildi: {count}\nBlokladi: {blocked}")
        return True
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)
    await update.message.reply_text(
        f"Assalomu alaykum, {user.first_name}!\nIltimos, viloyatingizni tanlang:",
        reply_markup=ReplyKeyboardMarkup([[r] for r in REGIONS], resize_keyboard=True)
    )

async def admin_stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        user_list = get_all_users()
        await update.message.reply_text(f"📊 Jami foydalanuvchilar: {len(user_list)} ta")

async def set_region_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[r] for r in REGIONS]
    await update.message.reply_text("Viloyatni tanlang:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await handle_admin_broadcast(update, context): return
    
    text = update.message.text
    user_id = update.effective_user.id
    user_data = get_user(user_id)

    if not user_data and text != "/start":
        await update.message.reply_text("⚠️ /start bosing")
        return

    if text in REGIONS:
        update_region(user_id, text)
        times = get_prayer_times(text)
        if times:
            msg = f"✅ Saqlandi: {text}\n"
            for k, v in times.items(): msg += f"🔸 {k}: {v}\n"
            await update.message.reply_text(msg, reply_markup=main_menu_keyboard())
    
    elif text == "📅 Bugungi namoz vaqtlari":
        user_region = user_data.get("region")
        if not user_region: await set_region_request(update, context)
        else:
            times = get_prayer_times(user_region)
            if times:
                msg = f"🕌 {user_region} vaqtlari:\n"
                for k, v in times.items(): msg += f"🔸 {k}: {v}\n"
                await update.message.reply_text(msg)

    elif text == "📖 Tasodifiy oyat":
        await update.message.reply_text(get_random_ayat())

    elif text == "📜 Tasodifiy hadis":
        await update.message.reply_text(get_random_hadis())

    elif text == "📍 Viloyatni o'zgartirish":
        await set_region_request(update, context)

    elif text == "✨ Bugungi amal":
        result = check_task_limit(user_id)
        if result <= 2:
            vazifa = random.choice(AMALLAR)
            await update.message.reply_text(f"✅ {vazifa}\nImkoniyat: {2-result}")
        else:
            await update.message.reply_text("🛑 Limit tugadi")

    elif text == "📊 Statistika (admin)":
        await admin_stat(update, context)

def main():
    token = os.getenv("BOT_TOKEN") or BOT_TOKEN
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("send", send_all))
    app.add_handler(CommandHandler("stat", admin_stat))
    app.add_handler(MessageHandler((filters.TEXT | filters.PHOTO | filters.VIDEO) & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
