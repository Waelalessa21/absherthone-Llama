from deep_translator import GoogleTranslator

def translate_to_arabic(text):
    return GoogleTranslator(source='auto', target='ar').translate(text)
