from datetime import datetime
import pytz
from ramazon_vaqti import RAMAZON_TAQVIMI, SAHARLIK_DUOSI, IFTORLIK_DUOSI



def get_ramazon_info(text, user_region):
    try:
        uzb_tz = pytz.timezone('Asia/Tashkent')
        now = datetime.now(uzb_tz)
    except:
        now = datetime.now()

    f1 = now.strftime("%Y-%m-%d")
    f2 = now.strftime("%d-%m-%Y")
    f3 = now.strftime("%Y-%m-%e").replace(" ", "")

    if user_region not in RAMAZON_TAQVIMI:
        return f"⚠️ {user_region} uchun taqvim topilmadi."

    data = RAMAZON_TAQVIMI[user_region].get(f1) or \
           RAMAZON_TAQVIMI[user_region].get(f2) or \
           RAMAZON_TAQVIMI[user_region].get(f3)

    if not data:
        return "⚠️ Bugun uchun Ramazon taqvimi mavjud emas (Ramazon oyi emas yoki tugagan)."

    if "Saharlik" in text:
        return f"🌙 *{user_region}* | {now.strftime('%d-%m-%Y')}\n\n🌅 Saharlik: *{data['saharlik']}*\n\n*Duosi:* {SAHARLIK_DUOSI}"
    else:
        return f"🌟 *{user_region}* | {now.strftime('%d-%m-%Y')}\n\n🌇 Iftorlik: *{data['iftorlik']}*\n\n*Duosi:* {IFTORLIK_DUOSI}"
