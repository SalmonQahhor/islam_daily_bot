import requests

def get_prayer_times(city):
    url = "https://api.aladhan.com/v1/timingsByCity"
    params = {
        "city": city,
        "country": "Uzbekistan",
        "method": 3,       
        "school": 1        
    }
    
    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status() # Agar 404 yoki 500 xato bo'lsa, error beradi
        data = res.json()
        
        timings = data["data"]["timings"]

        return {
            "Bomdod": timings["Fajr"],
            "Peshin": timings["Dhuhr"],
            "Asr": timings["Asr"],
            "Shom": timings["Maghrib"],
            "Xufton": timings["Isha"],
        }
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        return None
