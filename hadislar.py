import random

def get_random_hadis():
    # Eng ishonchli hadislar (asosan Buxoriy va Muslim)
    hadislar_list = [
        {"text": "«Amallar niyatga ko‘radir».", "source": "Buxoriy"},
        {"text": "«Kim Allohga va oxirat kuniga iymon keltirgan bo‘lsa, yo yaxshi gapirsin yoki jim tursin».", "source": "Buxoriy"},
        {"text": "«Alloh chiroylidir va chiroylilikni sevadi».", "source": "Muslim"},
        {"text": "«Sizlardan birortangiz o‘zi uchun yaxshi ko‘rgan narsani birodari uchun ham sog‘inmaguncha iymoni komil bo‘lmaydi».", "source": "Buxoriy"},
        {"text": "«Musulmon musulmonning birodaridir: unga zulm qilmaydi va uni yordamsiz tashlab qo‘ymaydi».", "source": "Muslim"},
        {"text": "«Qo‘li va tili bilan o‘zgalarga ozor bermagan kishi haqiqiy musulmondir».", "source": "Buxoriy"},
        {"text": "«Odamlarga rahm qilmaganga Alloh ham rahm qilmaydi».", "source": "Muslim"},
        {"text": "«Sizlarning eng yaxshingiz Qur’onni o‘rgangan va o‘rgatganingizdir».", "source": "Buxoriy"},
        {"text": "«Haqiqiy boylik molning ko‘pligi emas, balki nafsning to‘qligidir».", "source": "Buxoriy"},
        {"text": "«Alloh taolo sizlarning suratingizga emas, qalbingiz va amallaringizga qaraydi».", "source": "Muslim"},

        {"text": "«Sadaqa molni kamaytirmaydi».", "source": "Muslim"},
        {"text": "«Zulm qiyomat kuni zulmatlar bo‘lib keladi».", "source": "Buxoriy"},
        {"text": "«Kim birovning aybini yashirsa, Alloh uning aybini qiyomatda yashiradi».", "source": "Muslim"},
        {"text": "«Poklik iymonning yarmidir».", "source": "Muslim"},
        {"text": "«Eng afzal amal — vaqtida o‘qilgan namozdir».", "source": "Buxoriy"},
        {"text": "«Dunyo mo‘min uchun qamoqxona, kofir uchun jannatdir».", "source": "Muslim"},
        {"text": "«Halol ochiq-oydin, harom ham ochiq-oydindir».", "source": "Buxoriy"},
        {"text": "«Mazlumning duosidan qo‘rqing, chunki u bilan Alloh orasida parda yo‘q».", "source": "Buxoriy"},
        {"text": "«Allohga eng yoqimli amal — oz bo‘lsa ham davomli bo‘lganidir».", "source": "Muslim"},
        {"text": "«Kishi o‘zi yaxshi ko‘rganlari bilan birgadir».", "source": "Buxoriy"},

        {"text": "«Sizlarning yaxshilaringiz xulqi go‘zal bo‘lganlaringizdir».", "source": "Buxoriy"},
        {"text": "«Qiyomat kuni tarozida eng og‘ir narsa — husni xulqdir».", "source": "Termiziy"},
        {"text": "«Yaxshilikka dalolat qiluvchi uni qiluvchi kabidir».", "source": "Muslim"},
        {"text": "«Allohga va oxirat kuniga iymon keltirgan kishi qo‘shnisiga ozor bermasin».", "source": "Buxoriy"},
        {"text": "«Kichiklarimizga rahm qilmagan, kattalarimizni hurmat qilmagan bizdan emas».", "source": "Abu Dovud"},
        {"text": "«Sizlardan biringiz ovqat yeganda o‘ng qo‘li bilan yesin».", "source": "Muslim"},
        {"text": "«Kim ilm yo‘lida yursa, Alloh unga jannat yo‘lini oson qiladi».", "source": "Muslim"},
        {"text": "«Tabassum qilish ham sadaqadir».", "source": "Muslim"},
        {"text": "«Bir-biringizga hasad qilmanglar».", "source": "Muslim"},
        {"text": "«Alloh yumshoqlikni sevadi».", "source": "Muslim"},

        {"text": "«Sabr — nurdir».", "source": "Muslim"},
        {"text": "«Eng kuchli kishi — g‘azabini yuta olgan kishidir».", "source": "Buxoriy"},
        {"text": "«Kim rostgo‘y bo‘lsa, najot topadi».", "source": "Muslim"},
        {"text": "«Yaxshi so‘z sadaqadir».", "source": "Buxoriy"},
        {"text": "«Kibr jannatga kirishga to‘sqinlik qiladi».", "source": "Muslim"},
        {"text": "«Alloh bandasi uchun yengillikni xohlaydi».", "source": "Muslim"},
        {"text": "«Yolg‘on gunohlarga yetaklaydi».", "source": "Buxoriy"},
        {"text": "«Qur’on qiyomat kuni o‘z sohibiga shafoatchi bo‘ladi».", "source": "Muslim"},
        {"text": "«Har bir yaxshi ish sadaqadir».", "source": "Buxoriy"},
        {"text": "«Alloh bandaga yaxshilikni iroda qilsa, uni dinda bilimli qiladi».", "source": "Buxoriy"},
        
        {"text": "«Bandaning Robbiga eng yaqin bo‘ladigan payti — sajdada bo‘lgan paytidir. Shuning uchun sajdada ko‘proq duo qilinglar».", "source": "Muslim"},
        {"text": "«Alloh taolo Qiyomat kuni: ‘Ey Odam bolasi, Men kasal bo‘ldim, Meni ziyorat qilmading’, deydi. Banda: ‘Ey Robbim, Sen olamlarning Robbisan, qanday qilib Seni ziyorat qilaman?’ deydi. Alloh: ‘Falon bandam kasal bo‘lgan edi, agar uni ziyorat qilganingda Meni uning huzurida toparding’, deydi».", "source": "Muslim"},
        {"text": "«Kim bir mo‘minning dunyodagi qiyinchiliklaridan birini yengillatib bersa, Alloh uning qiyomatdagi qiyinchiliklaridan birini yengillashtiradi. Kim birovning aybini yashirsa, Alloh uning aybini dunyoda ham, oxiratda ham yashiradi».", "source": "Muslim"},
        {"text": "«Alloh taolo rahm qiluvchilarga rahm qiladi. Yer yuzidagilarga rahm qilinglar — osmondagi Zot sizlarga rahm qiladi».", "source": "Termiziy"},
        {"text": "«Qiyomat kuni eng qattiq azobga duchor bo‘ladigan odamlar — dunyoda odamlarni eng qattiq azoblaganlardir».", "source": "Buxoriy"},
        {"text": "«Kim yolg‘on gapirishni va unga amal qilishni tark etmasa, Alloh uning yeyishi va ichishini tark etishiga muhtoj emas».", "source": "Buxoriy"},
        {"text": "«Bandaning amali o‘limidan keyin to‘xtaydi, faqat uch narsa bundan mustasno: sadaqai joriya, foydali ilm yoki uning uchun duo qiladigan solih farzand».", "source": "Muslim"},
        {"text": "«Mo‘minning ishining hammasi ajablanarlidir. Unga bir yaxshilik yetsa — shukr qiladi va bu uning uchun yaxshilik bo‘ladi; unga bir musibat yetsa — sabr qiladi va bu ham uning uchun yaxshilik bo‘ladi».", "source": "Muslim"},
        {"text": "«Kim bir yaxshilikka niyat qilsa-yu, uni bajarmasa, Alloh unga to‘liq bir yaxshilik yozadi. Agar uni bajarsa, o‘n barobaridan yetti yuz barobarigacha yozadi».", "source": "Buxoriy"},
        {"text": "«Alloh taolo kechasi O‘z qo‘lini kunduzda gunoh qilgan bandaning tavbasi uchun, kunduz O‘z qo‘lini kechasi gunoh qilgan bandaning tavbasi uchun yoyib turadi».", "source": "Muslim"}

    ]

    selected = random.choice(hadislar_list)
    return f"📜 {selected['text']}\n\n📍 _({selected['source']})_"
