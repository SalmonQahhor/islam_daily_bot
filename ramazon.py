from datetime import datetime, timedelta
from ramazon_vaqti import RAMAZON_TAQVIMI, SAHARLIK_DUOSI, IFTORLIK_DUOSI


def get_ramazon_info(text, user_region):
    now_utc = datetime.utcnow()
    uzb_now = now_utc + timedelta(hours=5)
    today_date = uzb_now.strftime("%Y-%m-%d")

    if user_region not in RAMAZON_TAQVIMI:
        return f"⚠️ {user_region} uchun taqvim topilmadi."

    vaqtlar = RAMAZON_TAQVIMI[user_region].get(today_date)

    if not vaqtlar:
        return f"⚠️ Bugun ({today_date}) uchun taqvim mavjud emas. Taqvim 19-fevraldan boshlanadi."

    if "Saharlik" in text:
        return f"🌙 *{user_region}* | {today_date}\n\n🌅 Saharlik: *{vaqtlar['saharlik']}*\n\n*Duosi:* {SAHARLIK_DUOSI}"
    else:
        return f"🌟 *{user_region}* | {today_date}\n\n🌇 Iftorlik: *{vaqtlar['iftorlik']}*\n\n*Duosi:* {IFTORLIK_DUOSI}"
