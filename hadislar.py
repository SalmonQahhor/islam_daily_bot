import requests
import random

def get_random_hadis():
    try:
        # Tasodifiy hadis API (O'zbekcha)
        res = requests.get("https://hadis-api-uz.vercel.app/api/hadith/random", timeout=5).json()
        return f"{res['hadith']}\n\n📍 _({res['source']})_"
    except:
        return "📜 «Yaxshilikka dalolat qiluvchi uni qiluvchi kabidir». (Termiziy)"
