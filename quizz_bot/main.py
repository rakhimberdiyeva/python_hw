import asyncio
import json
from itertools import count

from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
from keyboard import get_kb

bot = Bot(token="")
dp = Dispatcher()

answers = {}
count_correct = 0


with open("questions.json", "r") as f:
    questions = json.load(f)


@dp.message(CommandStart())
async def start_handler(message: Message):
    answers.clear()
    await message.answer(f'{questions[0]["question"]} \nA: {questions[0]["answer_a"]} \nB: {questions[0]["answer_b"]} \nC: {questions[0]["answer_c"]} \nD: {questions[0]["answer_d"]}', reply_markup=get_kb(1))


@dp.callback_query(F.data.startswith("test"))
async def quizz(cb: CallbackQuery):
    _, number, answer = cb.data.split("_")
    n = int(number)

    answers[n] = answer

    if len(questions) > n:
        await cb.message.edit_text(f'{questions[n]["question"]} \nA: {questions[n]["answer_a"]} \nB: {questions[n]["answer_b"]} \nC: {questions[n]["answer_c"]} \nD: {questions[n]["answer_d"]}', reply_markup=get_kb(n + 1))
    else:
        reply_markup = None
        correct, checked = check_correct(answers)
        await cb.message.answer(f"вы закончили тест. Ваши результаты: {correct}")
        await cb.message.answer(checked)



def check_correct(answers: dict):
    checked = ""
    count_correct = 0
    for key, value in answers.items():
        checked += f'{key}. {questions[key - 1]["question"]} \nyour answer: {value} \ncorrect answer: {questions[key - 1]["correct_answer"]}\n\n'
        if value == questions[key - 1]["correct_answer"]:
            count_correct += 1
    return count_correct, checked




async def main():
    await dp.start_polling(bot)
    await asyncio.sleep(100)

if __name__ == "__main__":
    asyncio.run(main())