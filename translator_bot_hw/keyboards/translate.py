from aiogram.utils.keyboard import InlineKeyboardBuilder

data = {
    'en': '🇺🇸',  # English
    'es': '🇪🇸',  # Spanish
    'fr': '🇫🇷',  # French
    'de': '🇩🇪',  # German
    'zh-cn': '🇨🇳',  # Chinese (Simplified)
    'ja': '🇯🇵',  # Japanese
    'ru': '🇷🇺',  # Russian
    'ar': '🇸🇦',  # Arabic
    'pt': '🇵🇹',  # Portuguese
    'hi': '🇮🇳'   # Hindi
}

def get_from_lang_kb():
    builder = InlineKeyboardBuilder()
    for lang, flag in data.items():
        builder.button(text=flag, callback_data=f"from_lang_{lang}")

    builder.adjust(5 ,5)

    return builder.as_markup(resize_keyboard=True)

def get_to_lang_kb():
    builder = InlineKeyboardBuilder()
    for lang, flag in data.items():
        builder.button(text=flag, callback_data=f"to_lang_{lang}")

    builder.adjust(5 ,5)

    return builder.as_markup(resize_keyboard=True)