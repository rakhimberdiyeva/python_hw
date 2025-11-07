from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

from configs import TOKEN

from routers.start import router as start_router
from routers.weather import router as weather_router
from routers.about import router as about_router

properties = DefaultBotProperties(
    parse_mode=ParseMode.HTML
)

bot = Bot(TOKEN, default=properties)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(weather_router)
dp.include_router(about_router)
