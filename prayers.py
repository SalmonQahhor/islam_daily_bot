import requests

def get_prayer_times(region):
    url = f"https://islamprior.uz/api/v1/prayer-times?region={region}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            timings = data['times']
            
            return {
                "Bomdod": timings["tong_saharlik"],
                "Peshin": timings["peshin"],
                "Asr": timings["asr"],
                "Shom": timings["shom_iftor"],
                "Xufton": timings["hufton"]
            }
        else:
            print(f"Xatolik: API javob bermadi (Status: {response.status_code})")
            return None
    except Exception as e:
        print(f"Ulanishda xato: {e}")
        return None
