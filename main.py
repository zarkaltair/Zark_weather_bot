# Version bot for deploy to heroku
# Import all need libraries for the bot
import os
import pyowm
import asyncio
import logging
import datetime

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.types import ParseMode
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.utils.executor import start_webhook

from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from apscheduler.schedulers.asyncio import AsyncIOScheduler


# Create log string
logging.basicConfig(level=logging.INFO)

# Config for bot
TOKEN = os.environ['TOKEN']
WEBHOOK_HOST = 'https://zark-weather-bot.herokuapp.com'
WEBHOOK_PATH = '/webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')
CHAT_ID = 252027450


# Create main config for bot
loop = asyncio.get_event_loop()
bot = Bot(token=TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, loop=loop)


# Array of cities
arr = ['Москва', 'Екатеринбург', 'Петухово', 'Омск', 'Новосибирск', 'Шерегеш']


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
        # status = weather.get_status()
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


# Create function which process command /goodbye
@dp.message_handler(commands=['goodbye'])
async def process_goodbye_command(message: types.Message):
    message_text = 'Давай покеда!'
    await bot.send_message(message.chat.id, message_text)


# State machine, get state city
class Form(StatesGroup):
    City = State()


# Create function which process command /city
@dp.message_handler(commands=["city"])
async def town(message: types.Message, state: FSMContext):
    # Conversation's entry point
    await Form.City.set()
    await message.answer('Hi bro, enter name of the city where you want to know weather:')


# Create function which process entered message
@dp.message_handler(state=Form.City)
async def get_city(message: types.Message, state: FSMContext):
    logging.info('Start entering city')
    # Process name city
    city = message.text
    await message.answer(f'You are entered city: {city}')
    await state.update_data(city=city)
    try:
        logging.info('Try entering city to pyowm')
        msg = get_weather([city])
        await bot.send_message(message.chat.id, msg, reply_to_message_id=message.message_id)
        await state.finish()
    except:
        await state.finish()
        msg = "What the fuck is this? Such city dosn't exist!!!"
        await bot.send_message(message.chat.id, msg, reply_to_message_id=message.message_id)

'''
# Create function which process any text message from user
@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.chat.id, msg.text)

# Create function which process any message from user
@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    message_text = 'What the fuck is this?'
    await msg.reply(message_text)


# Define the function that sends weather to the chat on a schedule
@dp.message_handler()
async def sched():
    msg = get_weather(arr)
    await bot.send_message(chat_id=CHAT_ID, text=msg)


# Create scheduler with interval 1 day
scheduler = AsyncIOScheduler()
scheduler.add_job(sched, 'cron', day_of_week='mon-sun', hour=16, minute=25)
scheduler.start()
'''


# Create the function to startup my bot
async def on_startup(dp):
    # msg = "<code>I'm started, matherfucker!!!</code>"
    # await bot.send_message(chat_id=CHAT_ID, text=msg)
    await bot.set_webhook(WEBHOOK_URL)


# Create the function to shutdown my bot
async def on_shutdown(dp):
    # msg = "<code>I'm finished, matherfucker!!!</code>"
    # await bot.send_message(chat_id=CHAT_ID, text=msg)
    await bot.close()


# Main script
if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=WEBAPP_HOST, port=WEBAPP_PORT)


'''
start - start command
weather - get weather
city - get city weather
goodbye - bye
'''