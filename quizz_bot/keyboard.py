from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_kb(test_number):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="A",
        callback_data=f"test_{test_number}_A"
    )
    builder.button(
        text="B",
        callback_data=f"test_{test_number}_B"
    )
    builder.button(
        text="C",
        callback_data=f"test_{test_number}_C"
    )
    builder.button(
        text="D",
        callback_data=f"test_{test_number}_D"
    )
    return builder.as_markup()

