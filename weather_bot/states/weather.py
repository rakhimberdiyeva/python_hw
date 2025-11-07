from aiogram.fsm.state import State, StatesGroup

class WeatherForm(StatesGroup):
    location = State()