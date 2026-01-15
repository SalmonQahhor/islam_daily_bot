from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os
import asyncio

from config import BOT_TOKEN
# db.py faylingizda update_lang funksiyasi bo'lishi kerak
from db import save_user, update_region, get_user, get_all_users, update_lang 
from prayers import get_prayer_times
from ayat import get_random_ayat
# Transliteratsiya funksiyalari
from uz_utils import finalize_text 

try:
    from hadislar import get_random_hadis
except ImportError:
    def get_random_hadis(): return "📜 Hadislar fayli topilmadi."

ADMIN_ID = 5908568613

# Barcha interfeys matnlari
TEXTS = {
    "latin": {
        "start": "Assalomu alaykum! Namoz vaqtlari botiga xush kelibsiz.\nIltimos, viloyatingizni tanlang:",
        "menu_prayer": "📅 Bugungi namoz vaqtlari",
        "menu_ayat": "📖 Tasodifiy oyat",
        "menu_hadis": "📜 Tasodifiy hadis",
        "menu_region": "📍 Viloyatni o'zgartirish",
        "menu_lang": "🔤 Кирилл alifbosiga",
        "menu_stat": "📊 Statistika (admin)",
        "source": "\n🌐 Manba: aladhan.com API\n(Xufton va Bomdodda biroz farq bo'lishi mumkin)",
        "select_region": "Iltimos, yashash viloyatingizni tanlang:",
        "region_saved": "✅ Viloyat saqlandi: ",
        "error": "❌ Ma'lumot olishda xatolik.",
        "lang_changed": "✅ Alifbo o'zgartirildi!"
    },
    "cyrillic": {
        "start": "Ассалому алайкум! Намоз вақтлари ботига хуш келибсиз.\nИлтимос, вилоятингизни танланг:",
        "menu_prayer": "📅 Бугунги намоз вақтлари",
        "menu_ayat": "📖 Тасодифий оят",
        "menu_hadis": "📜 Тасодифий ҳадис",
        "menu_region": "📍 Вилоятни ўзгартириш",
        "menu_lang": "🔤 Lotin alifbosiga",
        "menu_stat": "📊 Статистика (admin)",
        "source": "\n🌐 Манба: aladhan.com API\n(Хуфтон ва Бомдодда бироз фарқ бўлиши мумкин)",
        "select_region": "Илтимос, яшаш вилоятингизни танланг:",
        "region_saved": "✅ Вилоят сақланди: ",
        "error": "❌ Маълумот олишда хатолик.",
        "lang_changed": "✅ Алифбо ўзгартирилди!"
    }
}

REGIONS = [
    "Toshkent", "Andijon", "Buxoro", "Farg'ona", "Jizzax",
    "Namangan", "Navoiy", "Qashqadaryo", "Qoraqalpog'iston",
    "Samarqand", "Sirdaryo", "Surxondaryo", "Xorazm"
]

def main_menu_keyboard(lang, user_id):
    t = TEXTS[lang]
    keyboard = [
        [KeyboardButton(t["menu_prayer"])],
        [KeyboardButton(t["menu_ayat"]), KeyboardButton(t["menu_hadis"])],
        [KeyboardButton(t["menu_region"]), KeyboardButton(t["menu_lang"])]
    ]
    if user_id == ADMIN_ID:
        keyboard.append([KeyboardButton(t["menu_stat"])])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id) # db.py da lang default 'latin' bo'lishi kerak
    lang = "latin"
    
    await update.message.reply_text(
        TEXTS[lang]["start"],
        reply_markup=ReplyKeyboardMarkup([[r] for r in REGIONS], resize_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    user_data = get_user(user_id)

    if not user_data and text != "/start":
        await update.message.reply_text("⚠️ /start")
        return

    # Foydalanuvchi tilini aniqlaymiz (bazadan)
    lang = user_data.get("lang", "latin") if user_data else "latin"
    t = TEXTS[lang]

    # --- ALIFBONI ALMASHTIRISH ---
    if text in ["🔤 Кирилл alifbosiga", "🔤 Lotin alifbosiga"]:
        new_lang = "cyrillic" if lang == "latin" else "latin"
        update_lang(user_id, new_lang)
        await update.message.reply_text(TEXTS[new_lang]["lang_changed"], 
                                       reply_markup=main_menu_keyboard(new_lang, user_id))

    # --- VILOYAT TANLASH ---
    elif text in REGIONS:
        update_region(user_id, text)
        times = get_prayer_times(text)
        if times:
            msg = f"{t['region_saved']} *{text}*\n\n🕌 *Bugungi vaqtlar:*\n"
            for k, v in times.items():
                # Namoz nomlarini ham o'girish
                msg += f"🔸 *{finalize_text(k, lang)}:* {v}\n"
            msg += t["source"]
            await update.message.reply_text(finalize_text(msg, lang), parse_mode="Markdown", 
                                           reply_markup=main_menu_keyboard(lang, user_id))

    # --- NAMOZ VAQTLARI ---
    elif text == t["menu_prayer"]:
        region = user_data.get("region")
        if not region:
            await update.message.reply_text(t["select_region"])
        else:
            times = get_prayer_times(region)
            if times:
                msg = f"🕌 *{region}*:\n\n"
                for k, v in times.items():
                    msg += f"🔸 *{finalize_text(k, lang)}:* {v}\n"
                msg += t["source"]
                await update.message.reply_text(finalize_text(msg, lang), parse_mode="Markdown")

    # --- OYAT (Kirilldan Lotin/Kirillga) ---
    elif text == t["menu_ayat"]:
        ayat = get_random_ayat() # API dan Kirillda keladi
        final_ayat = finalize_text(ayat, lang)
        await update.message.reply_text(final_ayat, parse_mode="Markdown")

    # --- HADIS (Lotindan Lotin/Kirillga) ---
    elif text == t["menu_hadis"]:
        hadis = get_random_hadis() # Fayldan Lotinda keladi
        final_hadis = finalize_text(hadis, lang)
        await update.message.reply_text(final_hadis, parse_mode="Markdown")

    # --- BOSHQA TUGMALAR ---
    elif text == t["menu_region"]:
        await update.message.reply_text(t["select_region"], 
                                       reply_markup=ReplyKeyboardMarkup([[r] for r in REGIONS], resize_keyboard=True))

    elif text == t["menu_stat"]:
        all_users = get_all_users()
        msg = f"👥 Jami: {len(all_users)}"
        await update.message.reply_text(finalize_text(msg, lang))

    else:
        await update.message.reply_text("❓", reply_markup=main_menu_keyboard(lang, user_id))

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
