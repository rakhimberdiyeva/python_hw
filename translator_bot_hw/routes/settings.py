from aiogram import Router, F
from aiogram.types import Message

from keyboards.start import get_back_kb
from keyboards.settings import get_lang_kb

router = Router()
@router.message(F.text == "⚙️ настройки")
async def send_welcome(message: Message):
    await message.answer("настройки", reply_markup=get_back_kb())
    await message.answer("выберите язык", reply_markup=get_lang_kb())