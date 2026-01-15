import requests
import random

def get_random_ayat():
    try:
        ayat_number = random.randint(1, 6236)
        url = f"https://api.alquran.cloud/v1/ayah/{ayat_number}/uz.sodik"
        res = requests.get(url).json()
        data = res["data"]
        # Faqat matnni qaytaramiz, alifboni bot.py o'zi finalize_text orqali to'g'irlaydi
        return f"📖 {data['text']}\n\n({data['surah']['englishName']}, {data['numberInSurah']})"
    except Exception as e:
        print(f"Oyat olishda xato: {e}")
        return "⚠️ Oyat yuklashda xatolik yuz berdi."
