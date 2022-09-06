import logging
import os

from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv

import keyboards as kb  # do your keyboards HERE!

if os.path.exists('.env'):
    load_dotenv('.env')  # call me if you don't have one

BOT_KEY = os.getenv('API_TOKEN')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_KEY)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'menu'])
async def send_menu(message: types.Message):
    '''Main menu entry and nothing else'''
    await message.answer('Меню', reply_markup=kb.menu(message.message_id))


@dp.callback_query_handler()
async def subject_menu(callback_query: types.CallbackQuery):
    '''Subject menu is a hub for a homework, docs and literature sections;
    There is a data format for reply markups which looks like:
    Section-subject-kind_of_docs'''

    info_type, bot_msg = callback_query.data.split()[0], int(callback_query.data.split()[1]) + 1
    # this string could fuck up our bot one day, search "last_message" or smth like that command plz...

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=bot_msg)
    await bot.answer_callback_query(callback_query.id)  # have no fucking clue what is this for

    if info_type == 'menu':
        await bot.send_message(callback_query.from_user.id, 'Меню', reply_markup=kb.menu(bot_msg))
        return  # menu exit
    if 'docs-' in info_type:
        await bot.send_message(callback_query.from_user.id, 'Выбери материалы',
                               reply_markup=kb.materials_by_subject(bot_msg, info_type.split('-')[0]))
        return  # materials section entry
    await bot.send_message(callback_query.from_user.id, 'Выбери предмет',
                           reply_markup=kb.subjects(bot_msg, info_type.split('-')[0]))  # subject entry


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
