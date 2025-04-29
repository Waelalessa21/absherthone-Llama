from spellchecker import SpellChecker

def correct_spelling(text):
    spell = SpellChecker()
    words = text.split()
    corrected_words = []
    for word in words:
        if word.lower() in spell:
            corrected_words.append(word)
        else:
            corrected_words.append(spell.correction(word) or word)
    return " ".join(corrected_words)
