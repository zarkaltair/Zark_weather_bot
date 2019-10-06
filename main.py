# Import all need libraries for the bot
# import json
# import apiai
import pyowm
import asyncio
import logging
# import requests
import datetime

# from bs4 import BeautifulSoup
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import TOKEN
from config import PROXY_URL
# from config import TOKEN_DIALOGFLOW


# Create log string
logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s', level=logging.INFO)

# pass to bot token and proxy url
bot = Bot(token=TOKEN, proxy=PROXY_URL)
# bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def get_weather(arr):
    answer = ''
    for i in arr:
        owm = pyowm.OWM('70732ac514bf006244ac74c5f31de5aa', language='ru')
        town = i
        obs = owm.weather_at_place(town)
        weather = obs.get_weather()
        temp = weather.get_temperature('celsius')['temp']
        temp = round(temp)
        wind = weather.get_wind()['speed']
        wind = round(wind)
        status = weather.get_detailed_status()
        answer += f'<b>{town}</b>\nt: {temp} °C, w: {wind} м/с, {status}.\n'
    return answer


# Create function which process connand /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Привет!\nИспользуй /help, чтобы узнать список доступных команд!')


# Create function which process connand /help
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = text('Я могу ответить на следующие команды:', '/weather', '/goodbye', sep='\n')
    await message.reply(msg, parse_mode=ParseMode.HTML)


# Create function which process connand /weather
@dp.message_handler(commands=['weather'])
async def process_weather_command(message: types.Message):
    arr = ['Москва', 'Екатеринбург', 'Омск', 'Петухово', 'Тамань', 'Шерегеш']#, 'Тамань' 'Шерегеш',
    msg = get_weather(arr)
    await bot.send_message(message.chat.id, msg, reply_to_message_id=message.message_id, parse_mode=ParseMode.HTML)


# Create function which process connand /goodbye
@dp.message_handler(commands=['goodbye'])
async def process_goodbye_command(message: types.Message):
    message_text = pre(emojize('Давай покеда! :sunglasses:'))
    await bot.send_message(message.chat.id, message_text, parse_mode=ParseMode.MARKDOWN)


# Create function which process any text message from user
@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.chat.id, msg.text)


# Create function which process any message from user
@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    message_text = text(emojize('Я не знаю, что с этим делать :astonished:'),
                        italic('\nЯ просто напомню,'), 'что есть',
                        code('команда'), '/help')
    await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)


# Define the function that sends weather to the chat on a schedule
@dp.message_handler()
async def sched():
    arr = ['Москва', 'Екатеринбург', 'Омск', 'Петухово', 'Шерегеш']
    msg = get_weather(arr)
    await bot.send_message(chat_id=252027450, text=msg, parse_mode=ParseMode.HTML)


# Create scheduler with interval 1 day
scheduler = AsyncIOScheduler()
scheduler.add_job(sched, 'cron', day_of_week='mon-sun', hour=16, minute=25)
scheduler.start()


if __name__ == '__main__':
    executor.start_polling(dp)