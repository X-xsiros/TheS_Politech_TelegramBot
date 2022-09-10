import logging
import os

from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv

import data.keyboards as kb  # do your keyboards HERE!
from data.db_session import global_init, create_session
from data.groups import Groups

if os.path.exists('.env'):
    load_dotenv('.env')  # call me if you don't have one

BOT_KEY = os.getenv('API_TOKEN')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_KEY)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'menu'])
async def send_menu(message: types.Message):
    """Main menu entry command and nothing else."""

    db_sess = create_session()
    groups = [chat.group_chat_id for chat in db_sess.query(Groups).all()]

    if str(message.chat.id) in groups:
        await message.answer('В общих чатах эти команды недоступны, '
                             'потому что для меня они всё равно что интимны.')
    else:
        await message.answer('Меню', reply_markup=kb.menu(message.message_id))
    db_sess.commit()


@dp.callback_query_handler()
async def subject_menu(callback_query: types.CallbackQuery):
    """Subject menu is a hub for a homework, docs and literature sections;
    There is a data format for reply markups which looks like:
    Section-subject-kind_of_docs"""

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


@dp.message_handler(commands=['alarm'])
async def alarm_command(message: types.Message):
    """Just a command which doing that king of thing in chat: @all"""

    db_sess = create_session()
    group = db_sess.query(Groups).filter(Groups.group_chat_id == message.chat.id).first()
    await bot.send_message(message.chat.id, group.members)


@dp.message_handler()
async def usernames_capture(message: types.Message):
    """This function captures usernames from messages in group chats,
    then it makes or opens a new group usernames file, next it checks
    if the username is already in, if not the function write it down."""

    db_sess = create_session()
    try:
        group = db_sess.query(Groups).filter(Groups.group_chat_id == message.chat.id).first()
        if not group:
            group = Groups(group_chat_id=message.chat.id)
            db_sess.add(group)
        if '@' + message.from_user.username + ' ' not in group.members and message.from_user.username != 'None':
            group.members += '@' + message.from_user.username + ' '
        elif message.from_user.username not in group.members:
            await bot.send_message(message.chat.id, 'Пидор, быстро сука завел юзернэйм! АТОБАН')
    except Exception as e:
        print(e)
    db_sess.commit()


def db_connect():
    """DataBase connection"""

    db_name = 'db/db.sqlite'
    global_init(db_name)


if __name__ == '__main__':
    db_connect()
    executor.start_polling(dp, skip_updates=True)
