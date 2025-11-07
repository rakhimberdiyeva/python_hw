from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.start import get_back_kb, get_start_kb

from states.weather import WeatherForm

from servises.weather import get_weather

router =Router()

@router.message(F.text == "🌤 узнать погоду")
async def location_handler(message: Message, state: FSMContext):
    await message.answer("что бы узнать погоду отправьте локацию", reply_markup=get_back_kb())
    await state.set_state(WeatherForm.location)


@router.message(F.location, WeatherForm.location)
async def weather_handler(message: Message, state: FSMContext):
    result = get_weather(message.location.latitude, message.location.longitude)
    text = f"""
        <b>⛅️Погода в вашем городе!⛅️</b>\n 
<b>погода</b>: {result["weather"][0]["description"]}
<b>температура</b>: {result["main"]["temp"]}°C 
<b>ощущается как</b>: {result["main"]["feels_like"]}°C 
<b>влажность</b>: {result["main"]["humidity"]}%
<b>видимость</b>: {result["visibility"]} метров
<b>ветер</b>: {result["wind"]["speed"]} метров/сек
    """
    await message.answer(text, reply_markup=get_start_kb())
