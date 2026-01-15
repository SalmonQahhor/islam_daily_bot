import requests
import random

def to_latin(text):
    if not text: return ""
    
    # Eng muhim va muammoli harflar xaritasi
    mapping = {
        "ё": "yo", "Ё": "Yo",
        "э": "e", "Э": "E",
        "ў": "o'", "Ў": "O'",
        "қ": "q", "Қ": "Q",
        "ғ": "g'", "Ғ": "G'",
        "ҳ": "h", "Ҳ": "H",
        "ч": "ch", "Ч": "Ch",
        "ш": "sh", "Ш": "Sh",
        "я": "ya", "Я": "Ya",
        "ю": "yu", "Ю": "Yu",
        "ц": "ts", "Ц": "Ts",
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ж": "j", 
        "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", 
        "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", 
        "х": "x", "ъ": "'", "ь": "", "А": "A", "Б": "B", "В": "V", "Г": "G", 
        "Д": "D", "Е": "E", "Ж": "J", "З": "Z", "И": "I", "Й": "Y", "К": "K", 
        "Л": "L", "М": "M", "N": "N", "О": "O", "П": "P", "Р": "R", "С": "S", 
        "Т": "T", "У": "U", "Ф": "F", "Х": "X"
    }

    # "э" harfini so'z boshida yoki o'rtasida to'g'ri chiqishini ta'minlash
    # Lekin eng sodda va samarali yo'li - replace orqali o'tish
    res = text
    for cyr, lat in mapping.items():
        res = res.replace(cyr, lat)
    return res

def get_random_ayat():
    try:
        ayat_number = random.randint(1, 6236)
        url = f"https://api.alquran.cloud/v1/ayah/{ayat_number}/uz.sodik"
        res = requests.get(url).json()
        data = res["data"]
        
        # Oyatni olamiz va to'liq lotinga o'giramiz
        text_latin = to_latin(data['text'])
        
        return f"📖 {text_latin}\n\n({data['surah']['englishName']}, {data['numberInSurah']})"
    except Exception as e:
        print(f"Xato: {e}")
        return "⚠️ Oyat yuklashda xatolik yuz berdi."
