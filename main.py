import logging
import os

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv

import data.keyboards as kb  # do your keyboards HERE!
from data.db_session import global_init, create_session
from data.groups import Groups
from data.homework import Homework

if os.path.exists('.env'):
    load_dotenv('.env')  # call AlkoKovad if you don't have one

BOT_KEY = os.getenv('API_TOKEN')

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_KEY)
dp = Dispatcher(bot, storage=storage)


class HomeworkSendState(StatesGroup):
    homework_files_state = State()


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

    db_sess = create_session()
    homework_list = db_sess.query(Homework).all()
    dates = [homework.deadline for homework in homework_list]

    info_type, bot_msg = callback_query.data.split()[0], int(callback_query.data.split()[1]) + 1
    # this string could fuck up our bot one day, search "last_message" or smth like that command plz...

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=bot_msg)
    await bot.answer_callback_query(callback_query.id)  # have no fucking clue what is this for

    if info_type == 'menu':
        await bot.send_message(callback_query.from_user.id, 'Меню', reply_markup=kb.menu(bot_msg))
        return  # menu exit
    if 'docs-' in info_type:
        if len(info_type.split('-')) == 3:
            await bot.send_message(callback_query.from_user.id, 'Выбери действие',
                                   reply_markup=kb.up_down__load_files(bot_msg, info_type))
            return
        if len(info_type.split('-')) == 4:

            if 'upload' in info_type:
                await bot.send_message(callback_query.from_user.id,
                                       'Укажи дату в формате DD.MM.YY и приложи файлы')
                await HomeworkSendState.homework_files_state.set()
                return  # upload homework entry
            if 'download' in info_type:
                await bot.send_message(callback_query.from_user.id, 'Ваше ДЗ по дедлайнам хозяин',
                                       reply_markup=kb.homework_for_dates(bot_msg, info_type, dates))
                return  # download homework entry

        await bot.send_message(callback_query.from_user.id, 'Выбери материалы',
                               reply_markup=kb.materials_by_subject(bot_msg, info_type))

        return  # materials section entry
    await bot.send_message(callback_query.from_user.id, 'Выбери предмет',
                           reply_markup=kb.subjects(bot_msg, info_type.split('-')[0]))  # subject entry


@dp.message_handler(state=HomeworkSendState.homework_files_state)
async def upload_homework(message: types.message, state: FSMContext):
    await state.update_data(homework=message)
    data = await state.get_data()
    await bot.send_message(message.chat.id, f'{data["homework"]} вот твоя хуйня')
    await bot.send_message(message.chat.id, f'{search_user_in_groups(data["homework"].from_user.username)} вот тебе сука')
    await state.finish()


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
        if not group and message.chat.id != search_user_in_groups(message.from_user.username) and \
                message.chat.id[0] == '-':
            group = Groups(group_chat_id=message.chat.id)
            db_sess.add(group)
        if '@' + message.from_user.username + ' ' not in group.members and message.from_user.username != 'None':
            group.members += '@' + message.from_user.username + ' '
        elif message.from_user.username not in group.members:
            await bot.send_message(message.chat.id, 'Пидор, быстро сука завел юзернэйм! АТОБАН')
    except Exception as e:
        print(e)
    db_sess.commit()


def search_user_in_groups(username):
    db_sess = create_session()
    groups = db_sess.query(Groups).all()
    for group in groups:
        if username in group.members:
            return group.group_chat_id


def db_connect():
    """DataBase connection"""

    db_name = 'db/db.sqlite'
    global_init(db_name)


if __name__ == '__main__':
    db_connect()
    executor.start_polling(dp, skip_updates=True)
