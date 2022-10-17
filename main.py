import logging
import os
import datetime

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv
from sqlalchemy.orm import Session

import data.keyboards as kb  # do your keyboards HERE!
from data.db_session import global_init, create_session
from data.groups import Groups
from data.homework import Homework

if os.path.exists('.env'):
    load_dotenv('.env')  # call AlkoKovad if you don't have one

BOT_KEY = os.getenv('API_TOKEN')
STORAGE_ID = -1001461174439

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_KEY)
dp = Dispatcher(bot, storage=storage)


class HomeworkSendState(StatesGroup):
    homework_files_state = State()
    homework_files_state2 = State()
    homework_files_state_download = State()

class DeadlineWriteState(StatesGroup):
    deadline_date = State()
    deadline_text = State()


@dp.message_handler(commands=['start', 'menu'])
async def send_menu(message: types.Message):
    """Main menu entry command and nothing else."""

    db_sess = create_session()
    group_ids = [chat.group_chat_id for chat in db_sess.query(Groups).all()]

    if str(message.chat.id) in group_ids:
        await message.answer('В общих чатах эти команды недоступны, '
                             'потому что для меня они всё равно что интимны.')
    elif int(message.chat.id) > 0:
        await message.answer('Меню', reply_markup=kb.menu(message.message_id))
    else:
        group = Groups()
        group.group_chat_id = message.chat.id
        db_sess.add(group)
        db_sess.commit()


@dp.callback_query_handler()
async def subject_menu(callback_query: types.CallbackQuery):
    """Subject menu is a hub for a homework, docs and literature sections;
    There is a data format for reply markups which looks like:
    Section-subject-kind_of_docs"""

    db_sess: Session = create_session()
    homework_list = db_sess.query(Homework).all()
    dates = [homework.deadline for homework in homework_list]


    info_type, bot_msg = callback_query.data.split()[0], int(callback_query.data.split()[1]) + 1
    # this string could fuck up our bot one day, search "last_message" or smth like that command plz...

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=bot_msg)
    await bot.answer_callback_query(callback_query.id)  # have no fucking clue what is this for

    if info_type == 'menu':
        await bot.send_message(callback_query.from_user.id, 'Меню', reply_markup=kb.menu(bot_msg))

        return  # menu exit
    if 'get' in info_type:

        db_sess = create_session()
        deaddata = info_type[-10:]


        user = '@' + callback_query.from_user.username
        group = db_sess.query(Groups).filter(Groups.members.like(f'%{user}%')).first()
        homework_download = db_sess.query(Homework).filter(Homework.group_chat_id == group.group_chat_id,Homework.deadline == deaddata)

        for i in homework_download:
            await bot.forward_message(callback_query.from_user.id,STORAGE_ID,i.homework_id)

        db_sess.commit()
        return
    if 'docs-' in info_type:
        if len(info_type.split('-')) == 3:
            await bot.send_message(callback_query.from_user.id, 'Выбери действие',
                                   reply_markup=kb.up_down__load_files(bot_msg, info_type))
            return

        if len(info_type.split('-')) == 4:

            if 'upload' in info_type:
                await bot.send_message(callback_query.from_user.id,
                                       'Укажи дату в формате YY-MM-DD и приложи файлы')
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

    try:
        await state.update_data(deadline_date=message.text)
    except Exception as e:
        await bot.send_message(message.chat.id, f'Ошибка: {e}')
    await bot.send_message(message.chat.id,'Отправь файлы')
    await HomeworkSendState.homework_files_state2.set()


@dp.message_handler(state=HomeworkSendState.homework_files_state2, content_types=['text','photo','document'])
async def upload_homework2(message: types.message, state: FSMContext):
    db_sess = create_session()
    user = '@' + message.from_user.username
    group = db_sess.query(Groups).filter(Groups.members.like(f'%{user}%')).first()

    await state.update_data(homework=message)
    data = await state.get_data()
    deadline_date = datetime.datetime.strptime(data['deadline_date'], '%Y-%m-%d')

    try:

        if data['homework'].document is not None:
            msg = await bot.send_document(STORAGE_ID, document=data['homework'].document.file_id, caption=deadline_date)
            db_sess.add(
                Homework(group_chat_id=group.group_chat_id, deadline=deadline_date, homework_id=msg["message_id"],
                         some_text='Смотри дз'))
        elif data['homework'].text is not None:
            msg = await bot.send_message(STORAGE_ID, f"{deadline_date},{ data['homework'].text},")
            db_sess.add(Homework(group_chat_id=group.group_chat_id, deadline=deadline_date, homework_id= msg["message_id"],
                                     some_text= 'Смотри дз'))

        elif data['homework'].photo is not None:
            msg = await bot.send_photo(STORAGE_ID,  photo=data['homework'].photo[-1].file_id, caption= deadline_date)
            db_sess.add(
                Homework(group_chat_id=group.group_chat_id, deadline=deadline_date, homework_id=msg["message_id"],
                         some_text='Смотри дз'))

        await state.finish()
        db_sess.commit()
    except Exception as e:
        print(f"error: {e}")


@dp.message_handler(commands=['alldeadlines'])
async def alldeadlines(message: types.Message):
    db_sess = create_session()
    user = '@' + message.from_user.username
    group = db_sess.query(Groups).filter(Groups.members.like(f'%{user}%')).first()
    deadlines = db_sess.query(Homework).filter(
        Homework.group_chat_id == group.group_chat_id).all()

    if deadlines == []:
        await bot.send_message(message.chat.id, f'Дедлайнов нет для группы:{group.group_chat_id}')
    else:
        deadlines = db_sess.query(Homework).filter(
            Homework.group_chat_id == group.group_chat_id)
        await bot.send_message(message.chat.id, 'Дедлыйны:')
        for c in deadlines:
            await bot.send_message(message.chat.id,
                                   f'\n Дата {c.deadline}\n Id Дз {c.homework_id}\n Суть  {c.some_text}')

    db_sess.commit()


@dp.message_handler(commands=['adddeadline'])
async def adddeadline(message: types.Message):
    await bot.send_message(message.chat.id, 'Введи дедлайн в формате YYYY-MM-DD')
    await DeadlineWriteState.deadline_date.set()


@dp.message_handler(state=DeadlineWriteState.deadline_date)
async def get_ddate(message: types.Message, state: FSMContext):
    if len(message.text) == 10 and type(int(message.text.split('-')[0])) == int:
        await state.update_data(deadline_date=message.text)
        await bot.send_message(message.chat.id, 'Введи суть деделайна')
        await DeadlineWriteState.deadline_text.set()
    else:
        await message.reply(f"Неверный формат{len(message.text.split('-'))}{message.text.split('-')}")


@dp.message_handler(state=DeadlineWriteState.deadline_text)
async def get_dtext(message: types.Message, state: FSMContext):
    await state.update_data(deadline_text=message.text)
    data = await state.get_data()
    db_sess = create_session()
    user = '@' + message.from_user.username
    group = db_sess.query(Groups).filter(Groups.members.like(f'%{user}%')).first()
    deadline_date = datetime.datetime.strptime(data['deadline_date'], '%Y-%m-%d')
    try:
        db_sess.add(Homework(group_chat_id=group.group_chat_id, deadline=deadline_date, homework_id=os.urandom(5),
                             some_text=data['deadline_text']))
        print(type(group.group_chat_id), type(deadline_date), type(os.urandom(5)))
    except Exception as e:
        await message.reply(f'{e}')
    await message.reply('Дедлайн успешно создан')
    db_sess.commit()
    await state.finish()


@dp.message_handler(commands=['deadline'])
async def deadline(message: types.Message):
    db_sess = create_session()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    user = '@' + message.from_user.username

    group = db_sess.query(Groups).filter(Groups.members.like(f'%{user}%')).first()

    deadlines = db_sess.query(Homework).filter(
        Homework.group_chat_id == group.group_chat_id, Homework.deadline == tomorrow).all()

    if deadlines == []:
        await bot.send_message(message.chat.id, f'Дедлайнов на завтра нет для группы:{group.group_chat_id}')
    else:
        deadlines = db_sess.query(Homework).filter(
            Homework.group_chat_id == group.group_chat_id, Homework.deadline == tomorrow)
        for c in deadlines:
            await bot.send_message(message.chat.id,
                                   f'Дедлайны на завтра\n Дата {c.deadline}\n Id Дз {c.homework_id}\n Суть  {c.some_text}')

    db_sess.commit()


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
    if db_sess.query(Groups).filter(Groups.group_chat_id == message.chat.id).first():
        group = db_sess.query(Groups).filter(Groups.group_chat_id == message.chat.id).first()
        if '@' + message.from_user.username + ' ' not in group.members and message.from_user.username != 'None':
            group.members += '@' + message.from_user.username + ' '
        elif message.from_user.username == 'None':
            await bot.send_message(message.chat.id, 'Пидор, быстро сука завел юзернэйм! АТОБАН')
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
