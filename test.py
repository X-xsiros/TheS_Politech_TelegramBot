import logging
import os
import datetime
import time
import threading
from threading import Lock

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import data.keyboards as kb  # do your keyboards HERE!
from data.db_session import global_init, create_session
from data.groups import Groups
from data.homework import Homework

if os.path.exists('.env'):
    load_dotenv('.env')  # call AlkoKovad if you don't have one

BOT_KEY = os.getenv('API_TOKEN')
STORAGE_ID = -1001461174439

lock = threading.Lock()
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_KEY)
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()

class Menu(StatesGroup):
    Menu_State_1 = State()
    Menu_State_2 = State()
    Menu_State_3 = State()
    Menu_State_4 = State()

@dp.message_handler(commands=['start','menu'])
async def start(message: types.Message,state: FSMContext):
    user_id = message.from_user.id
    chat = message.chat.id
    msg = await bot.send_message(chat, 'Привет,я TheS, буду рад помочь тебе)')
    msg_id = msg['message_id']
    await state.update_data(user_id = user_id,chat = chat,msg_id = msg_id)
    time.sleep(5)
    await bot.edit_message_text('Начнем, пожалуй',chat,msg_id)
    await Menu.Menu_State_1.set()

@dp.message_handler(state=Menu.Menu_State_1)
async def main_menu(message: types.Message,state: FSMContext,callback_query: types.CallbackQuery):
    data = await state.get_data()
    await bot.delete_message(data['chat'],data['msg_id'])
    msg = await bot.send_message(data['chat'],'Меню',reply_markup=kb.new_menu())
    if callback_query.data == 'materials':
        await Menu.Menu_State_2.set()
        await  state.update_data(msg_id= msg['message_id'])

@dp.message_handler(state=Menu.Menu_State_2)
async def materials(message: types.Message,state: FSMContext,callback_query: types.CallbackQuery):
    data = await state.get_data()
    await bot.delete_message(data['chat'],data['msg_id'])
    msg = await bot.send_message(data['chat'],'Выбери предмет',reply_markup=kb.new_subjects())
    info = callback_query.data
    await  state.update_data(msg_id=msg['message_id'],info = info)
    await Menu.Menu_State_3.set()

@dp.message_handler(state = Menu.Menu_State_3)
async def materials_by_subject(message: types.Message,state: FSMContext,callback_query: types.CallbackQuery):
    data = await state.get_data()
    await bot.delete_message(data['chat'],data['msg_id'])
    msg = await bot.send_message(data['chat'], 'Выбери действие', reply_markup=kb.new_m_b_subject(data['info'])


    await  state.update_data(msg_id=msg['message_id'], info=info)