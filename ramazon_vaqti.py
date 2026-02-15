from datetime import datetime, timedelta

# Andijon vaqtlari (Baza) 
# Format: (Sana, Saharlik, Iftorlik)
ANDIJON_DATA = [
    ("2026-02-19", "05:44", "17:55"),
    ("2026-02-20", "05:43", "17:56"),
    ("2026-02-21", "05:42", "17:57"),
    ("2026-02-22", "05:40", "17:59"),
    ("2026-02-23", "05:39", "18:00"),
    ("2026-02-24", "05:38", "18:01"),
    ("2026-02-25", "05:36", "18:02"),
    ("2026-02-26", "05:35", "18:03"),
    ("2026-02-27", "05:33", "18:04"),
    ("2026-02-28", "05:32", "18:05"),
    ("2026-03-01", "05:30", "18:07"),
    ("2026-03-02", "05:29", "18:08"),
    ("2026-03-03", "05:27", "18:09"),
    ("2026-03-04", "05:26", "18:10"),
    ("2026-03-05", "05:24", "18:11"),
    ("2026-03-06", "05:23", "18:12"),
    ("2026-03-07", "05:21", "18:13"),
    ("2026-03-08", "05:20", "18:15"),
    ("2026-03-09", "05:18", "18:16"),
    ("2026-03-10", "05:16", "18:17"),
    ("2026-03-11", "05:15", "18:18"),
    ("2026-03-12", "05:13", "18:19"),
    ("2026-03-13", "05:11", "18:20"),
    ("2026-03-14", "05:10", "18:21"),
    ("2026-03-15", "05:08", "18:22"),
    ("2026-03-16", "05:06", "18:23"),
    ("2026-03-17", "05:05", "18:24"),
    ("2026-03-18", "05:03", "18:25"),
    ("2026-03-19", "05:01", "18:27"),
]

# 2. Viloyatlar bo'yicha vaqt farqlari (Daqiqa hisobida Andijonga nisbatan)
# Manba: O'zbekiston Musulmonlari idorasi taqvimlari asosidagi standart farqlar
REGION_OFFSETS = {
    "Andijon": 0,
    "Namangan": 1,
    "Farg'ona": 3,
    "Toshkent": 13,
    "Sirdaryo": 15,
    "Jizzax": 18,
    "Samarqand": 21,
    "Surxondaryo": 20, 
    "Qashqadaryo": 24,
    "Navoiy": 27,
    "Buxoro": 29,
    "Xorazm": 45,
    "Qoraqalpog'iston": 48
}

# 3. Yordamchi funksiya: Vaqtga daqiqa qo'shish
def add_minutes(time_str, minutes):
    t = datetime.strptime(time_str, "%H:%M")
    new_time = t + timedelta(minutes=minutes)
    return new_time.strftime("%H:%M")

# 4. Asosiy lug'atni generatsiya qilish
RAMAZON_TAQVIMI = {}

for region, offset in REGION_OFFSETS.items():
    RAMAZON_TAQVIMI[region] = {}
    for sana, sahar, iftor in ANDIJON_DATA:
        sahar_new = add_minutes(sahar, offset)
        iftor_new = add_minutes(iftor, offset)
        
        RAMAZON_TAQVIMI[region][sana] = {
            "saharlik": sahar_new,
            "iftorlik": iftor_new
        }

# 5. Duolar
SAHARLIK_DUOSI = (
    "Navaytu an asuma sovma shahri ramazona minal fajri ilal mag'ribi, "
    "xolisan lillahi ta'ala. Allohu akbar.\n\n"
    "Ma'nosi: Ramazon oyining ro'zasini subhdan to kun botguncha tutmoqni niyat qildim. "
    "Xolis Alloh uchun. Alloh buyukdir."
)

IFTORLIK_DUOSI = (
    "Allohumma laka sumtu va bika amantu va 'alayka tavakkaltu va 'ala rizqika aftartu, "
    "fag'firli ya g'offaru ma qoddamtu va ma axxortu.\n\n"
    "Ma'nosi: Ey Alloh, ushbu ro'zamni Sen uchun tutdim va Senga iymon keltirdim va "
    "Senga tavakkal qildim va bergan rizqing bilan iftor qildim."
)
