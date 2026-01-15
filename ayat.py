import requests
import random
from trans import to_latin  

def get_random_ayat(lang="latin"):
    try:
        ayat_number = random.randint(1, 6236)
        url = f"https://api.alquran.cloud/v1/ayah/{ayat_number}/uz.sodik"
        res = requests.get(url).json()
        data = res["data"]
        
        text = data['text']
        surah_name = data['surah']['englishName']
        ayah_num = data['numberInSurah']
        
       
        if lang == "latin":
            text = to_latin(text)
            final_msg = f"📖 {text}\n\n({surah_name}, {ayah_num})"
        else:
            final_msg = f"📖 {text}\n\n({surah_name}, {ayah_num})"
            
        return final_msg
    except:
        return "⚠️ Xatolik yuz berdi."
