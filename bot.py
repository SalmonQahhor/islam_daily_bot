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
    def get_random_hadis():
        return "📜 Hadislar fayli topilmadi."

ADMIN_ID = 5908568613
is_broadcasting = False
waiting_for_feedback = {}  

REGIONS = [
    "Toshkent", "Andijon", "Buxoro", "Farg'ona", "Jizzax",
    "Namangan", "Navoiy", "Qashqadaryo", "Qoraqalpog'iston",
    "Samarqand", "Sirdaryo", "Surxondaryo", "Xorazm"
]


# Keyboards
def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("🌙 Ramazon 2026")],
        [KeyboardButton("📅 Bugungi namoz vaqtlari")],
        [KeyboardButton("📖 Tasodifiy oyat"), KeyboardButton("📜 Tasodifiy hadis")],
        [KeyboardButton("📍 Viloyatni o'zgartirish"), KeyboardButton("✨ Bugungi amal")],
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
        return f"⚠️ {user_region} uchun ma'lumot topilmadi."

    if today_str not in RAMAZON_TAQVIMI[user_region]:
        return "⚠️ Hozir Ramazon oyi emas yoki bugun uchun taqvim topilmadi (19-fevraldan boshlanadi)."

    data = RAMAZON_TAQVIMI[user_region][today_str]

    if text == "🌅 Saharlik vaqti":
        return f"🌙 *{user_region}* | {today_str}\n\n🌅 Saharlik (Og'iz yopish): *{data['saharlik']}*\n\n🤲 *Duosi:* {SAHARLIK_DUOSI}"
    else:
        return f"🌟 *{user_region}* | {today_str}\n\n🌇 Iftorlik (Og'iz ochish): *{data['iftorlik']}*\n\n🤲 *Duosi:* {IFTORLIK_DUOSI}"



async def send_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_broadcasting
    if update.effective_user.id == ADMIN_ID:
        is_broadcasting = True
        await update.message.reply_text("📝 Xabarni yuboring (Rasm, video yoki matn). Formatlar saqlanadi.")


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
        print(f"📢 [BROADCAST] Sent: {count} | Blocked: {blocked}")
        await update.message.reply_text(f"✅ Tugadi\nQabul qildi: {count}\nBlokladi: {blocked}")
        return True
    return False



async def send_feedback_to_admin(user_id, user_name, text, context):
    msg = f"📩 #FIKR_VA_TAKLIF\n\n👤 <b>Kimdan:</b> {user_name}\n🆔 <b>ID:</b> <code>{user_id}</code>\n\n📝 <b>Xabar:</b> {text}"
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=msg, parse_mode="HTML")
    except Exception as e:
        print(f"❌ Admin feedbackni olmadi: {e}")



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)
    print(f"🚀 [START] ID: {user.id} | Name: {user.first_name}")
    await update.message.reply_text(
        f"Assalomu alaykum, {user.first_name}!\nRamazon 2026 va Namoz vaqtlari botiga xush kelibsiz.\nViloyatni tanlang:",
        reply_markup=ReplyKeyboardMarkup([[r] for r in REGIONS], resize_keyboard=True)
    )


async def admin_stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        user_list = get_all_users()
        await update.message.reply_text(f"📊 Jami foydalanuvchilar: {len(user_list)} ta")


async def set_region_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[r] for r in REGIONS]
    await update.message.reply_text("Viloyatni tanlang:",
                                    reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if await handle_admin_broadcast(update, context): return

    text = update.message.text
    user = update.effective_user
    user_id = user.id
    user_data = get_user(user_id)

    
    if user_id in waiting_for_feedback and waiting_for_feedback[user_id]:
        print(f"✍️ [FEEDBACK_SENT] ID: {user_id}")
        await send_feedback_to_admin(user_id, user.first_name, text, context)
        waiting_for_feedback[user_id] = False  
        await update.message.reply_text("✅ Rahmat! Xabaringiz adminga yuborildi.", reply_markup=main_menu_keyboard())
        return

    
    if not user_data and text not in REGIONS and text != "/start":
        await update.message.reply_text("⚠️ Iltimos, avval viloyatni tanlang.")
        return



    
    if text in REGIONS:
        update_region(user_id, text)
        print(f"📍 [REGION] ID: {user_id} | Region: {text}")
        times = get_prayer_times(text)
        if times:
            msg = f"✅ Viloyat: {text}\n"
            for k, v in times.items(): msg += f"🔸 {k}: {v}\n"
            await update.message.reply_text(msg, reply_markup=main_menu_keyboard())

    
    elif text == "🌙 Ramazon 2026":
        print(f"🌙 [RAMADAN_MENU] ID: {user_id}")
        await update.message.reply_text("Ramazon bo'limi (2026):", reply_markup=ramazon_menu_keyboard())

    
    elif text in ["🌅 Saharlik vaqti", "🌇 Iftorlik vaqti"]:
        print(f"🕒 [RAMADAN_TIME] ID: {user_id} | Type: {text}")
        user_region = user_data.get("region", "Toshkent")
        msg = get_ramazon_info(text, user_region)
        await update.message.reply_text(msg, parse_mode="Markdown")

    
    elif text == "✍️ Fikr va Taklif":
        print(f"📩 [FEEDBACK_REQ] ID: {user_id}")
        waiting_for_feedback[user_id] = True
        await update.message.reply_text("Taklif yoki fikringizni yozib qoldiring:",
                                        reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🔙 Orqaga")]],
                                                                         resize_keyboard=True))

    # Orqaga qaytish
    elif text == "🔙 Orqaga":
        if user_id in waiting_for_feedback: waiting_for_feedback[user_id] = False
        await update.message.reply_text("Asosiy menyu:", reply_markup=main_menu_keyboard())

    
    elif text == "📅 Bugungi namoz vaqtlari":
        user_region = user_data.get("region")
        if not user_region:
            await set_region_request(update, context)
        else:
            times = get_prayer_times(user_region)
            if times:
                msg = f"🕌 {user_region} vaqtlari:\n"
                for k, v in times.items(): msg += f"🔸 {k}: {v}\n"
                await update.message.reply_text(msg)

    elif text == "📖 Tasodifiy oyat":
        await update.message.reply_text(get_random_ayat(), parse_mode="Markdown")

    elif text == "📜 Tasodifiy hadis":
        await update.message.reply_text(get_random_hadis(), parse_mode="Markdown")

    elif text == "📍 Viloyatni o'zgartirish":
        await set_region_request(update, context)

    elif text == "✨ Bugungi amal":
        result = check_task_limit(user_id)
        if result <= 2:
            vazifa = random.choice(AMALLAR)
            await update.message.reply_text(f"✅ {vazifa}\nImkoniyat: {2 - result}")
        else:
            await update.message.reply_text("🛑 Bugungi limit tugadi.")

    elif text == "📊 Statistika (admin)":
        await admin_stat(update, context)

    else:
        # Tushunarsiz xabar kelsa
        if is_broadcasting: return  
        await update.message.reply_text("Menyudan foydalaning.", reply_markup=main_menu_keyboard())


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
