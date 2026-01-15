import random

def get_random_hadis():
    # Hadislar ro'yxati (Tashqi API-ga bog'lanmasdan ishlaydi)
    hadislar_list = [
        {"text": "«Sizlarning yaxshilaringiz ahli-ayoliga yaxshilik qiladiganlaringizdir».", "source": "Termiziy"},
        {"text": "«Ikki xislat borki, ular mo‘min kishida jam bo‘lmaydi: baxillik va badxulqlik».", "source": "Termiziy"},
        {"text": "«Mo‘min kishi birodarining oynasidir».", "source": "Abu Dovud"},
        {"text": "«Alloh chiroylidir va chiroylilikni sevadi».", "source": "Muslim"},
        {"text": "«Yaxshilikka dalolat qiluvchi uni qiluvchi kabidir».", "source": "Termiziy"},
        {"text": "«Rostgo'ylikni mahkam tutinglar, zero rostgo'ylik ezgulikka boshlaydi».", "source": "Muslim"},
        {"text": "«Qayerda bo'lsang ham Allohdan qo'rq, yomonlik ketidan uni o'chiruvchi yaxshilik qil».", "source": "Termiziy"},
        {"text": "«Sizlardan birortangiz o'zi uchun yaxshi ko'rgan narsani birodari uchun ham sog'inmaguncha komil mo'min bo'la olmaydi».", "source": "Buxoriy"},
        {"text": "«Musulmon musulmonning birodaridir. Unga zulm qilmaydi, uni yordamsiz tashlab qo'ymaydi».", "source": "Muslim"},
        {"text": "«Kishi do'stining dinidadir. Shunday ekan, kim bilan do'stlashayotganiga e'tibor bersin».", "source": "Abu Dovud"},
        {"text": "«Qiyomat kuni mo'minning tarozisida husni xulqdan ko'ra og'irroq narsa bo'lmaydi».", "source": "Termiziy"},
        {"text": "«Allohga va oxirat kuniga iymon keltirgan kishi qo'shnisiga ozor bermasin».", "source": "Buxoriy"},
        {"text": "«Qo'li va tili bilan o'zgalarga ozor bermagan kishi haqiqiy musulmondir».", "source": "Buxoriy"},
        {"text": "«Iymon yetmishdan ortiq bo'lakdir, eng afzali 'La ilaha illalloh' deyishdir».", "source": "Muslim"},
        {"text": "«Kishi o'zi yaxshi ko'rganlari bilan birgadir».", "source": "Buxoriy"}
    ]
    
    selected = random.choice(hadislar_list)
    return f"📜 {selected['text']}\n\n📍 _({selected['source']})_"
