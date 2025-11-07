from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.start import get_back_kb

router = Router()

@router.message(F.text == "👥 о нас")
async def about_handler(message: Message):
    text = """
    <b>🧠O нас</b>
Добро пожаловать! Этот бот создан, чтобы быстро и удобно узнавать погоду в любом городе.
Мы показываем точный прогноз, температуру, влажность, скорость ветра и другие данные — всё в одном сообщении.
Просто введи название города, и бот мгновенно подскажет, что тебя ждёт за окном ☀️🌧❄️

🔗 <b>GitHub:</b> https://github.com/rakhimberdiyeva
📫 <b>Email:</b> malikarakh07@gmail.com 
    """
    await message.answer(text, reply_markup=get_back_kb())