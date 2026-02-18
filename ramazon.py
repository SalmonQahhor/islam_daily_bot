from datetime import datetime
import pytz
from ramazon_vaqti import RAMAZON_TAQVIMI, SAHARLIK_DUOSI, IFTORLIK_DUOSI



def get_ramazon_info(text, user_region):
    try:
        uzb_tz = pytz.timezone('Asia/Tashkent')
        now = datetime.now(uzb_tz)
    except:
        now = datetime.now()

    if user_region not in RAMAZON_TAQVIMI:
        return f"⚠️ {user_region} uchun taqvim topilmadi."

    day_data = None
    possible_dates = [
        now.strftime("%Y-%m-%d"),
        now.strftime("%d-%m-%Y"),
        now.strftime("%Y.%m.%d"),
        now.strftime("%d.%m.%Y"),
        f"{now.day}-{now.month}-{now.year}",
        f"{now.year}-{now.month}-{now.day}"
    ]

    for date_str in possible_dates:
        if date_str in RAMAZON_TAQVIMI[user_region]:
            day_data = RAMAZON_TAQVIMI[user_region][date_str]
            current_date_display = date_str
            break

    if not day_data:
        return "⚠️ Bugun uchun Ramazon taqvimi mavjud emas (Ramazon oyi emas yoki tugagan)."

    if "Saharlik" in text:
        return f"🌙 *{user_region}* | {current_date_display}\n\n🌅 Saharlik: *{day_data['saharlik']}*\n\n*Duosi:* {SAHARLIK_DUOSI}"
    else:
        return f"🌟 *{user_region}* | {current_date_display}\n\n🌇 Iftorlik: *{day_data['iftorlik']}*\n\n*Duosi:* {IFTORLIK_DUOSI}"
