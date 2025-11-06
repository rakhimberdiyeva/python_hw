from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_lang_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="🇷🇺", callback_data="lang_ru")
    builder.button(text="🇬🇧", callback_data="lang_en")
    builder.button(text="🇺🇿", callback_data="lang_uz")


    return builder.as_markup(resize_keyboard=True)