import asyncio
import json
import os

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot

from search import get_response
from validator import validate_message

load_dotenv()

TOKEN = os.environ['TOKEN']
bot = AsyncTeleBot(TOKEN)


@bot.message_handler(commands=['start'])
async def start_command(message):
    example = str('{"dt_from": "2022-09-01T00:00:00",\n"dt_upto": "2022-12-31T23:59:00",\n"group_type": "month"}')
    start_message = (f'<b>Тестовое задание</b>'
                     f'\n\nПодсчёт суммы всех выплат по временным промежуткам'
                     f'\n\nПример входных данных:'
                     f'\n{example}')

    await bot.send_message(message.chat.id, start_message, parse_mode='HTML')


@bot.message_handler(content_types=['text'])
async def get_result(message):
    validated = validate_message(message.text)  # валидация запроса

    if validated is True:
        # await bot.send_message(message.chat.id, 'Поиск...')
        result = await get_response(eval(message.text))
        await bot.send_message(message.chat.id, json.dumps(result), parse_mode='HTML')
    else:
        await bot.send_message(message.chat.id, validated)


asyncio.run(bot.infinity_polling())
