from googletrans import Translator, LANGUAGES

translator = Translator()

def translate(from_lang, text, to_lang):
    result = translator.translate(
        text,
        dest=to_lang,
        src=from_lang
    )

    return result.text

