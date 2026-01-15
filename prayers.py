import requests
from bs4 import BeautifulSoup

def get_prayer_times(region):
    # Sayt islom.uz bilan bir xil ma'lumot beradi va barqaror ishlaydi
    url = f"https://namozvaqti.uz/shahar/{region.lower()}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Saytdagi vaqtlar joylashgan id yoki class'larni qidiramiz
            # namozvaqti.uz dagi vaqtlar odatda 'time' klassida bo'ladi
            times_divs = soup.find_all('p', class_='time')
            
            if len(times_divs) >= 6:
                return {
                    "Bomdod": times_divs[0].get_text(strip=True),
                    "Quyosh": times_divs[1].get_text(strip=True),
                    "Peshin": times_divs[2].get_text(strip=True),
                    "Asr":    times_divs[3].get_text(strip=True),
                    "Shom":   times_divs[4].get_text(strip=True),
                    "Xufton": times_divs[5].get_text(strip=True)
                }
            else:
                # Agar klasslar topilmasa, boshqa usulni sinab ko'ramiz
                print("Vaqtlar topilmadi (sayt strukturasi o'zgargan bo'lishi mumkin)")
                return None
        else:
            print(f"Server xatosi: {response.status_code}")
            return None
    except Exception as e:
        print(f"Xatolik: {e}")
        return None
