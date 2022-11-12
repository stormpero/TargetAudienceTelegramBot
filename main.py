from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import PollAnswer
from aiogram.utils import executor
import datetime

from excel_output import add_result_to_excel
from json_parser import read_json_questions

import config

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

questions_list = read_json_questions()
answers = []
question_num = 0


@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    answers.append(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
    await msg.answer_poll(questions_list[question_num]['question'],
                          questions_list[question_num]['answers'],
                          is_anonymous=False)


@dp.poll_answer_handler()
async def handle_poll_answer(quiz_answer: PollAnswer):
    global question_num, answers
    answers.append(questions_list[question_num]['answers'][quiz_answer.option_ids[0]])
    question_num = question_num + 1
    print(answers)
    if question_num >= len(questions_list):
        # add_result_to_excel(answers)
        question_num = 0
        answers = []
        await bot.send_message(quiz_answer.user.id, "Благодарим Вас за прохождение опроса!")
    else:
        await bot.send_poll(quiz_answer.user.id, questions_list[question_num]['question'],
                            questions_list[question_num]['answers'], type='regular',
                            is_anonymous=False)


async def on_startup(dispatcher):
    await dispatcher.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить опрос"),
        ]
    )


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
