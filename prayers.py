import requests

def get_prayer_times(region):
    # Bu yerda 'region' sifatida API tushunadigan 'Karshi', 'Nukus' kabi nomlar keladi
    url = f"https://islom.uz/vaqtlar.json?region={region}"
    try:
        response = requests.get(url, timeout=10)
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
        return None
    except:
        return None
