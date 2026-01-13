import requests
from datetime import datetime

def get_prayer_times(city):
    url = "https://api.aladhan.com/v1/timingsByCity"
    params = {
        "city": city,
        "country": "Uzbekistan",
        "method": 2
    }
    res = requests.get(url, params=params).json()
    timings = res["data"]["timings"]

    return {
        "Bomdod": timings["Fajr"],
        "Peshin": timings["Dhuhr"],
        "Asr": timings["Asr"],
        "Shom": timings["Maghrib"],
        "Xufton": timings["Isha"],
    }
