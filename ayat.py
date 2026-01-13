import requests
import random

def get_random_ayat():
    ayat_number = random.randint(1, 6236)
    url = f"https://api.alquran.cloud/v1/ayah/{ayat_number}/uz.sodik"
    res = requests.get(url).json()
    data = res["data"]

    return f"📖 {data['text']}\n\n({data['surah']['englishName']}, {data['numberInSurah']})"
