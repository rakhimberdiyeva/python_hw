from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_start_kb(lang: str = "ru"):
    builder = ReplyKeyboardBuilder()
    builder.button(text="🔍 перевод")
    builder.button(text="👥 о нас")
    builder.button(text="📚 история")
    builder.button(text="⚙️ настройки")

    builder.adjust(1, 3)
    return builder.as_markup(resize_keyboard=True)


def get_back_kb(lang: str = "ru"):
    builder = ReplyKeyboardBuilder()
    builder.button(text="⏪ назад")
    return builder.as_markup(resize_keyboard=True)