import requests
import random

def get_random_hadis():
    try:
        url = "https://raw.githubusercontent.com/u-saidov/hadis-json/main/hadislar.json"
        
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Kelgan ro'yxatdan bittasini tasodifiy tanlaymiz
            selected = random.choice(data)
            return f"📜 {selected['text']}\n\n📍 _({selected['source']})_"
        else:
            raise Exception("API xatosi")
            
    except Exception as e:
        print(f"Xato: {e}")
        # Zaxira hadis (agar internet uzilsa)
        return "📜 «Yaxshilikka dalolat qiluvchi uni qiluvchi kabidir». (Termiziy)"
