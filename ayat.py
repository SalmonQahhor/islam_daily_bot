import requests
import random

def to_latin(text):
    cyr_to_lat = {
        "ш":"sh","Ш":"Sh","ч":"ch","Ч":"Ch","ў":"o'","Ў":"O'","ғ":"g'","Ғ":"G'",
        "а":"a","б":"b","д":"d","е":"e","ф":"f","г":"g","ҳ":"h","и":"i","ж":"j",
        "к":"k","л":"l","м":"m","н":"n","о":"o","п":"p","қ":"q","р":"r","с":"s",
        "т":"t","у":"u","в":"v","х":"x","й":"y","з":"z","А":"A","Б":"B","Д":"D",
        "Е":"E","Ф":"F","Г":"G","Ҳ":"H","И":"I","Ж":"J","К":"K","Л":"L","М":"M",
        "Н":"N","О":"O","П":"P","Қ":"Q","Р":"R","С":"S","Т":"T","У":"U","В":"V","Х":"X","Й":"Y","З":"Z"
    }
    for k, v in cyr_to_lat.items():
        text = text.replace(k, v)
    return text

def get_random_ayat():
    try:
        ayat_number = random.randint(1, 6236)
        url = f"https://api.alquran.cloud/v1/ayah/{ayat_number}/uz.sodik"
        res = requests.get(url).json()
        data = res["data"]
        
        # Kirillcha matnni olamiz
        text_cyrillic = data['text']
        # Uni lotinga o'giramiz
        text_latin = to_latin(text_cyrillic)
        
        return f"📖 {text_latin}\n\n({data['surah']['englishName']}, {data['numberInSurah']})"
    except:
        return "⚠️ Oyat yuklashda xatolik yuz berdi."
