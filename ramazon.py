from datetime import datetime
import pytz
from ramazon_vaqti import RAMAZON_TAQVIMI, SAHARLIK_DUOSI, IFTORLIK_DUOSI

def get_ramazon_info(text, user_region):
    try:
        uzb_tz = pytz.timezone('Asia/Tashkent')
        now = datetime.now(uzb_tz)
    except:
        now = datetime.now()

    target_region = None
    for region in RAMAZON_TAQVIMI.keys():
        if user_region.lower() in region.lower():
            target_region = region
            break
    
    if not target_region:
        return f"⚠️ {user_region} uchun taqvim topilmadi."

    day_data = None
    dates_in_db = list(RAMAZON_TAQVIMI[target_region].keys())
    
    possible_formats = [
        now.strftime("%Y-%m-%d"),
        now.strftime("%d-%m-%Y"),
        now.strftime("%Y.%m.%d"),
        now.strftime("%d.%m.%Y"),
        f"{now.day}-{now.month}-{now.year}",
        f"{now.year}-{now.month}-{now.day}",
        f"{now.day:02d}-{now.month:02d}-{now.year}"
    ]

    for f in possible_formats:
        if f in RAMAZON_TAQVIMI[target_region]:
            day_data = RAMAZON_TAQVIMI[target_region][f]
            found_date = f
            break

    if not day_data:
        return f"⚠️ Bugun ({now.strftime('%d-%m-%Y')}) uchun ma'lumot topilmadi. Bazadagi sana formati mos kelmadi."

    s_key = "saharlik" if "saharlik" in day_data else "Saharlik"
    i_key = "iftorlik" if "iftorlik" in day_data else "Iftorlik"

    if "Saharlik" in text:
        return f"🌙 *{target_region}* | {found_date}\n\n🌅 Saharlik: *{day_data.get(s_key, 'Noma`lum')}*\n\n*Duosi:* {SAHARLIK_DUOSI}"
    else:
        return f"🌟 *{target_region}* | {found_date}\n\n🌇 Iftorlik: *{day_data.get(i_key, 'Noma`lum')}*\n\n*Duosi:* {IFTORLIK_DUOSI}"
