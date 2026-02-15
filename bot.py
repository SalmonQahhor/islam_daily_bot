from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os
import asyncio
import random
from datetime import datetime

from config import BOT_TOKEN
from db import save_user, update_region, get_user, get_all_users, check_task_limit 
from prayers import get_prayer_times
from ayat import get_random_ayat
from amallar import AMALLAR 
from ramazon_vaqti import RAMAZON_TAQVIMI, SAHARLIK_DUOSI, IFTORLIK_DUOSI

try:
    from hadislar import get_random_hadis
except ImportError:
    def get_random_hadis(): return "📜 Hadislar fayli topilmadi."

ADMIN_ID = 5908568613
is_broadcasting = False
waiting_for_feedback = {}

REGIONS = [
    "Toshkent", "Andijon", "Buxoro", "Farg'ona", "Jizzax",
    "Namangan", "Navoiy", "Qashqadaryo", "Qoraqalpog'iston",
    "Samarqand", "Sirdaryo", "Surxondaryo", "Xorazm"
]


def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("🌙 Ramazon 2026")],
        [KeyboardButton("📍 Viloyatni o'zgartirish"), KeyboardButton("📅 Namoz Vaqti")],
        [KeyboardButton("📖 Tasodifiy oyat"), KeyboardButton("📜 Tasodifiy hadis")],
        [KeyboardButton("✨ Bugungi amal")],
        [KeyboardButton("📊 Statistika (admin)"), KeyboardButton("✍️ Fikr va Taklif")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def ramazon_menu_keyboard():
    keyboard = [
        [KeyboardButton("🌅 Saharlik vaqti"), KeyboardButton("🌇 Iftorlik vaqti")],
        [KeyboardButton("🔙 Orqaga")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)



def get_ramazon_info(text, user_region):
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    if user_region not in RAMAZON_TAQVIMI:
        return f"⚠️ *{user_region}* uchun ma'lumot topilmadi."
    
    if today_str not in RAMAZON_TAQVIMI[user_region]:
         return "⚠️ *Hozir Ramazon oyi emas!* \n\nUshbu bo'lim 19-fevraldan boshlab ishga tushadi. 😊"

    data = RAMAZON_TAQVIMI[user_region][today_str]
    
    if text == "🌅 Saharlik vaqti":
        return (f"🌙 *{user_region}* | {today_str}\n\n"
                f"🌅 *Saharlik (Og'iz yopish):* `{data['saharlik']}`\n\n"
                f"🤲 *Saharlik duosi:*\n_{SAHARLIK_DUOSI}_")
    else:
        return (f"🌟 *{user_region}* | {today_str}\n\n"
                f"🌇 *Iftorlik (Og'iz ochish):* `{data['iftorlik']}`\n\n"
                f"🤲 *Iftorlik duosi:*\n_{IFTORLIK_DUOSI}_")

    
async def send_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_broadcasting
    if update.effective_user.id == ADMIN_ID:
        is_broadcasting = True
        await update.message.reply_text("📝 *Xabarni yuboring:*\n\nRasm, video yoki matnli xabaringiz barcha foydalanuvchilarga aynan qanday bo'lsa, shunday yetkaziladi.", parse_mode="Markdown")

    
async def handle_admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_broadcasting
    if update.effective_user.id == ADMIN_ID and is_broadcasting:
        if update.message.text == "/send": return False
        
        all_users = get_all_users()
        count, blocked = 0, 0
        status_msg = await update.message.reply_text(f"⏳ Xabar {len(all_users)} kishiga yuborilmoqda...")
        
        for uid in all_users:
            try:
                await update.message.copy(chat_id=uid)
                count += 1
                if count % 10 == 0:
                    await status_msg.edit_text(f"⏳ Yuborilmoqda: `{count}/{len(all_users)}`")
                await asyncio.sleep(0.05)
            except:
                blocked += 1
        
        is_broadcasting = False
        await update.message.reply_text(f"✅ *Xabar yetkazildi!*\n\n👤 Qabul qildi: `{count}`\n🚫 Bloklaganlar: `{blocked}`", parse_mode="Markdown")
        return True
    return False

    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)
    print(f"🚀 [START] ID: {user.id} | Ism: {user.first_name}")
    await update.message.reply_text(
        f"Assalomu alaykum, *{user.first_name}*!\n\n"
        "Islam Daily Botga xush kelibsiz.\n\n"
        "Iltimos, yashash viloyatingizni tanlang:",
        reply_markup=ReplyKeyboardMarkup([[r] for r in REGIONS], resize_keyboard=True),
        parse_mode="Markdown"
    )


async def admin_stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        user_list = get_all_users()
        await update.message.reply_text(f"📊 *Jami foydalanuvchilar:* `{len(user_list)}` ta", parse_mode="Markdown")

    
async def set_region_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[r] for r in REGIONS]
    await update.message.reply_text("📍 *Viloyatingizni tanlang:*", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True), parse_mode="Markdown")

    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await handle_admin_broadcast(update, context): return
    
    text = update.message.text
    user = update.effective_user
    user_id = user.id
    user_data = get_user(user_id)

    if user_id in waiting_for_feedback and waiting_for_feedback[user_id]:
        if text == "🔙 Orqaga":
            waiting_for_feedback[user_id] = False
            await update.message.reply_text("🏠 *Asosiy menyu:*", reply_markup=main_menu_keyboard(), parse_mode="Markdown")
            return
        
        print(f"✍️ [FEEDBACK] ID: {user_id}")
        msg = f"📩 *Yangi taklif!*\n\n👤 *Kimdan:* {user.first_name}\n🆔 *ID:* `{user_id}`\n📝 *Xabar:* {text}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=msg, parse_mode="Markdown")
        
        waiting_for_feedback[user_id] = False
        await update.message.reply_text("✅ *Rahmat!* Xabaringiz adminga yetkazildi.", reply_markup=main_menu_keyboard(), parse_mode="Markdown")
        return

    if not user_data and text not in REGIONS and text != "/start":
        await update.message.reply_text("⚠️ *Iltimos, avval viloyatni tanlang.*", parse_mode="Markdown")
        return

    if text in REGIONS:
        update_region(user_id, text)
        print(f"📍 [REGION] ID: {user_id} | {text}")
        times = get_prayer_times(text)
        if times:
            msg = f"✅ Viloyat saqlandi: *{text}*\n\n🕌 *Bugungi namoz vaqtlari:*\n"
            for k, v in times.items(): msg += f"🔸 *{k}:* {v}\n"
            await update.message.reply_text(msg, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

    elif text == "🌙 Ramazon 2026":
        print(f"🌙 [RAMADAN] ID: {user_id}")
        await update.message.reply_text("🌙 *Ramazon 2026* bo'limiga xush kelibsiz!", reply_markup=ramazon_menu_keyboard(), parse_mode="Markdown")

  elif text in ["🌅 Saharlik vaqti", "🌇 Iftorlik vaqti"]:
        print(f"🕒 [RAMADAN_TIME] ID: {user_id} | {text}")
        user_region = user_data.get("region", "Toshkent")
        msg = get_ramazon_info(text, user_region)
        
        msg += f"\n\n📚 *Manba:* Sajda.com Ramazon taqvimi (2026)."
        
        await update.message.reply_text(msg, parse_mode="Markdown")

    elif text == "✍️ Fikr va Taklif":
        print(f"📩 [FEEDBACK_REQ] ID: {user_id}")
        waiting_for_feedback[user_id] = True
        await update.message.reply_text("📝 *Taklif yoki fikringizni yozib qoldiring:*", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🔙 Orqaga")]], resize_keyboard=True), parse_mode="Markdown")

    elif text == "📍 Viloyatni o'zgartirish":
        print(f"⚙️ [CHANGE_REGION] ID: {user_id}")
        await set_region_request(update, context)

   elif text == "📅 Namoz Vaqti":
        print(f"🕒 [PRAYER] ID: {user_id}")
        user_region = user_data.get("region")
        times = get_prayer_times(user_region)
        if times:
            msg = f"🕌 *{user_region}* shahri namoz vaqtlari:\n"
            msg += f"📅 _Bugun: {datetime.now().strftime('%d-%m-%Y')}_\n\n"
            
            for k, v in times.items(): 
                msg += f"🔸 *{k}:* `{v}`\n"
            
            msg += f"\n📍 *Manba:* O'zbekiston Musulmonlari idorasi taqvimi asosida."
            msg += f"\n⚠️ _Eslatma: Vaqtlar Aladhan API orqali olinmoqda._"
            
            await update.message.reply_text(msg, parse_mode="Markdown")

    elif text == "✨ Bugungi amal":
        print(f"🌟 [AMAL] ID: {user_id}")
        result = check_task_limit(user_id)
        if result <= 3:
            vazifa = random.choice(AMALLAR)
            await update.message.reply_text(f"🌟 *Bugungi tavsiya etilgan amal:*\n\n✅ {vazifa}\n\nℹ️ _Yana {2-result} ta amal olishingiz mumkin._", parse_mode="Markdown")
        else:
            await update.message.reply_text("🛑 *Bugun uchun limit tugadi.*", parse_mode="Markdown")

    elif text == "📖 Tasodifiy oyat":
        print(f"📖 [AYAT] ID: {user_id}")
        await update.message.reply_text(f"✨ *Qur'oni Karimdan oyat:*\n\n{get_random_ayat()}", parse_mode="Markdown")

    elif text == "📜 Tasodifiy hadis":
        print(f"📜 [HADIS] ID: {user_id}")
        await update.message.reply_text(f"✨ *Hadisi sharif:*\n\n{get_random_hadis()}", parse_mode="Markdown")

    elif text == "🔙 Orqaga":
        print(f"🔙 [BACK] ID: {user_id}")
        if user_id in waiting_for_feedback: waiting_for_feedback[user_id] = False
        await update.message.reply_text("🏠 *Asosiy menyu:*", reply_markup=main_menu_keyboard(), parse_mode="Markdown")

    elif text == "📊 Statistika (admin)":
        await admin_stat(update, context)
    
    else:
        if not is_broadcasting:
            await update.message.reply_text("🏠 *Iltimos, menyudagi tugmalardan foydalaning.*", reply_markup=main_menu_keyboard(), parse_mode="Markdown")


def main():
    token = os.getenv("BOT_TOKEN") or BOT_TOKEN
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("send", send_all))
    app.add_handler(CommandHandler("stat", admin_stat))
    app.add_handler(MessageHandler((filters.TEXT | filters.PHOTO | filters.VIDEO) & ~filters.COMMAND, handle_message))

    print("[INFO] Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
