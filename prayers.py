import requests

def get_prayer_times(region):
    # API manzili (islom.uz viloyatlar uchun)
    url = f"https://islom.uz/vaqtlar.json?region={region}"
    
    # Brauzer ekanligimizni ko'rsatamiz, aks holda server bloklaydi
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            times = data['times']
            
            return {
                "Bomdod": times["tong_saharlik"],
                "Quyosh": times["quyosh"],
                "Peshin": times["peshin"],
                "Asr":    times["asr"],
                "Shom":   times["shom_iftor"],
                "Xufton": times["hufton"]
            }
        else:
            print(f"API xatosi: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ulanishda xato: {e}")
        return None
