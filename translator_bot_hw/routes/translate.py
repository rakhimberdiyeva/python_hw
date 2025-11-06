from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states.translate import TransForm

from keyboards.translate import get_from_lang_kb,get_to_lang_kb
from keyboards.start import get_back_kb, get_start_kb

from services.translate import translate

router = Router()

@router.message(F.text == "🔍 перевод")
async def search_handler(message: Message, state: FSMContext):
    await message.answer("ПЕРЕВОД",  reply_markup=get_back_kb())
    await message.answer("с какого языка вы хотите перевести", reply_markup=get_from_lang_kb())
    await state.set_state(TransForm.from_lang)

@router.callback_query(F.data.startswith("from_lang_"), TransForm.from_lang)
async def from_lang_handler(cb: CallbackQuery, state: FSMContext):
    _, _, from_lang = cb.data.split("_")
    await state.update_data(from_lang=from_lang)

    await state.set_state(TransForm.trans_text)
    await cb.message.answer("введите текст который хотите перевести")


@router.message(F.text, TransForm.trans_text)
async def trans_text_handler(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)

    await state.set_state(TransForm.to_lang)
    await message.answer("на какой язык вы хотите перевести", reply_markup=get_to_lang_kb())


@router.callback_query(F.data.startswith("to_lang_"), TransForm.to_lang)
async def to_lang_handler(cb: CallbackQuery, state: FSMContext):
    _, _, to_lang = cb.data.split("_")
    await state.update_data(to_lang=to_lang)

    await cb.message.answer("результат", reply_markup=get_start_kb())
    data = await state.get_data()
    result = translate(data.get("from_lang"), data.get("text"), data.get("to_lang"))
    await cb.message.answer(result)



