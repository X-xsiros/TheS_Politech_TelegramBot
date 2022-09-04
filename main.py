import logging
import os

from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv


if os.path.exists('.env'):
    load_dotenv('.env')

BOT_KEY = os.getenv('API_TOKEN')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_KEY)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'menu'])
async def send_menu(message: types.Message):
    await message.reply('Работаю - значит не трогай')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
