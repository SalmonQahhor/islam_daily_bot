from datetime import datetime
from ramazon_vaqti import RAMAZON_TAQVIMI, SAHARLIK_DUOSI, IFTORLIK_DUOSI



def get_ramazon_info(text, user_region):
    today_date = datetime.now().strftime("%Y-%m-%d")
    
    if user_region not in RAMAZON_TAQVIMI:
        return f"⚠️ {user_region} uchun taqvim topilmadi."
        
    if today_date not in RAMAZON_TAQVIMI[user_region]:
        return "⚠️ Bugun uchun Ramazon taqvimi mavjud emas (Ramazon oyi emas yoki tugagan)."

    vaqtlar = RAMAZON_TAQVIMI[user_region][today_date]

    if "Saharlik" in text:
        return f"🌙 *{user_region}* | {today_date}\n\n🌅 Saharlik: *{vaqtlar['saharlik']}*\n\n*Duosi:* {SAHARLIK_DUOSI}"
    else:
        return f"🌟 *{user_region}* | {today_date}\n\n🌇 Iftorlik: *{vaqtlar['iftorlik']}*\n\n*Duosi:* {IFTORLIK_DUOSI}"
