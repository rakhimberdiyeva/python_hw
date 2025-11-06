from aiogram.fsm.state import State, StatesGroup


class TransForm(StatesGroup):
     from_lang = State()
     trans_text = State()
     to_lang = State()