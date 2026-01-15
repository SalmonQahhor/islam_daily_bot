import re

def to_cyrillic(text):
    mapping = {"a":"а","b":"б","d":"д","e":"е","f":"ф","g":"г","h":"ҳ","i":"и","j":"ж","k":"к","l":"л","m":"м","n":"н","o":"о","p":"п","q":"қ","r":"р","s":"с","t":"т","u":"у","v":"в","x":"х","y":"й","z":"з","sh":"ш","ch":"ч","o'":"ў","g'":"ғ"}

    for k, v in mapping.items(): text = text.replace(k, v)
    return text

def to_latin(text):
    mapping = {"а":"a","б":"b","д":"d","е":"e","ф":"f","г":"g","ҳ":"h","и":"i","ж":"j","к":"k","л":"l","м":"m","н":"n","о":"o","п":"p","қ":"q","р":"r","с":"s","т":"t","у":"u","в":"v","х":"x","й":"y","з":"z","ш":"sh","ч":"ch","ў":"o'","ғ":"g'"}
    for k, v in mapping.items(): text = text.replace(k, v)
    return text
