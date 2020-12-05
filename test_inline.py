# Version bot for test on localhost
# Import all need libraries for the bot
import pyowm
import hashlib
import asyncio
import logging
import datetime

from aiogram import Bot, types
from aiogram.utils import executor
# from aiogram.types import ParseMode
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType

from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle

from apscheduler.schedulers.asyncio import AsyncIOScheduler


TOKEN = '639237490:AAFgastOyZtYYsD9pGg5iNOsVvAOjE5MeFU'


# Create log string
logging.basicConfig(level=logging.INFO)

# pass to bot token and proxy url
loop = asyncio.get_event_loop()
bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, loop=loop)

# Array of cities
arr = ['Москва', 'Екатеринбург', 'Петухово', 'Омск', 'Новосибирск', 'Шерегеш', 'Верх-Катавка']


# Function for get weather
def get_weather(arr_towns):
    answer = ''
    for town in arr_towns:
        owm = pyowm.OWM('70732ac514bf006244ac74c5f31de5aa', language='ru')
        town = town
        obs = owm.weather_at_place(town)
        weather = obs.get_weather()
        temp = round(weather.get_temperature('celsius')['temp'])
        wind = round(weather.get_wind()['speed'])
        status = weather.get_detailed_status()
        answer += f'<b>{town}</b>\n<code>t: {temp} °C, w: {wind} м/с, {status}.</code>\n'
    return answer


# Create function which process command /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    msg = """Hello! I'm a bot that will help you find out the weather.
If you want to know weather in a city tap to command /city and then enter name of the town.
Else you might try to tap /help command."""
    await message.reply(msg)


# Create function which process command /help
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = 'Available the next commands:\n/start\n/weather\n/city\n/goodbye'
    await message.reply(msg)


# Create function which process command /weather
@dp.message_handler(commands=['weather'])
async def process_weather_command(message: types.Message):
    msg = get_weather(arr)
    await bot.send_message(message.chat.id, msg, reply_to_message_id=message.message_id)


@dp.inline_handler()
async def inline_query_process(inline_query: InlineQuery):
    query = inline_query.query
    query = query.strip().lower()
    input_content = InputTextMessageContent(get_weather([query.capitalize()]))
    result_id: str = hashlib.md5(query.encode()).hexdigest()
    item = InlineQueryResultArticle(
        id=result_id,
        title=f'Town {query.capitalize()}',
        input_message_content=input_content,
    )

    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)


# Define the function that sends weather to the chat on a schedule
@dp.message_handler()
async def sched(arr):
    msg = get_weather(arr)
    await bot.send_message(chat_id=252027450, text=msg)


# Create the function to startup my bot
async def on_startup(dp):
    msg = "<code>I'm started, matherfucker!!!</code>"
    await bot.send_message(chat_id=252027450, text=msg)


# Create the function to shutdown my bot
async def on_shutdown(dp):
    await bot.close()


# Main script
if __name__ == '__main__':
#    sched()
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

'''
start - start command
weather - get weather
city - get city weather
goodbye - bye
'''

