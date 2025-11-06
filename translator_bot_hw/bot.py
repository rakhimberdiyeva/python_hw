from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

from configs import TOKEN

from routes.start import router as start_handler
from routes.about import router as about_handler
from routes.settings import router as settings_handler
from routes.translate import router as translate_handler




properties = DefaultBotProperties(
    parse_mode=ParseMode.HTML,
)

bot = Bot(TOKEN, default=properties)
dp = Dispatcher()

dp.include_router(start_handler)
dp.include_router(about_handler)
dp.include_router(settings_handler)
dp.include_router(translate_handler)