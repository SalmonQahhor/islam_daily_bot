# 🌙 Islam Daily Bot

Ushbu Telegram bot foydalanuvchilarga kundalik namoz vaqtlari, Qur'ondan tasodifiy oyatlar va hadislar yetkazib berish uchun mo'ljallangan. Bot O'zbekistonning barcha viloyatlarini qo'llab quvvatlaydi.


## ✨ Xususiyatlari

* **📅 Namoz Vaqtlari:**  AlAdhan API orqali O'zbekistonning 13 ta hududi uchun aniq vaqtlar.
* **📍 Viloyatni o'zgartirish**  Viloyatni o'zgartirib, o'sha joy uchun namoz vaqti chiqaradi.
* **📖 Oyatlar:**  6236 ta oyatdan tasodifiy bittasini chiqarib beradi
* **📜 Hadislar:**  Tasodifiy sahix hadislar bo'limi.
* **📊 Admin Panel:**  Jami foydalanuvchilar sonini ko'rish (Faqat o'zim uchun)



## 🛠 Texnologiyalar

* **Til:** Python 3.14
* **Kutubxona:** `python-telegram-bot` (JobQueue bilan)
* **Ma'lumotlar bazasi:** MySQL (Railway MySQL)
* **Vaqt zonasi:** `pytz` (Asia/Tashkent)
* **API:** AlAdhan (Prayer Times) 


## 📂 Fayllar strukturasi

```text
islam_bot
│
├─ bot.py            # Asosiy Telegram bot kodi
├─ db.py             # Database uchun 
├─ config.py         # BOT_TOKEN va DB_CONFIG
├─ prayers.py        # Namoz vaqtlarini olish funksiyalari
├─ ayat.py           # Oyatlarni olish funksiyalari
├─ hadislar.py       # Hadis olish funksiyasi
├─ requirements.txt  # Python kutubxonalar ro‘yxati
└─ README.md         # Loyihaning tavsifi
