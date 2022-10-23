from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def menu(message_id,chat_id):
    docs_btn = InlineKeyboardButton('Материалы по занятиям', callback_data=f'docs {message_id} {chat_id}')
    homework_btn = InlineKeyboardButton('Домашка', callback_data=f'topical_homework {message_id} {chat_id}')
    return InlineKeyboardMarkup(row_width=1).add(docs_btn)


def subjects(message_id, info_type,chat_id):
    physics_btn = InlineKeyboardButton('Физика', callback_data=f'{info_type}-physics {message_id} {chat_id}')
    math_btn = InlineKeyboardButton('Вышмат', callback_data=f'{info_type}-math {message_id} {chat_id}')
    programming_btn = InlineKeyboardButton('Алгпрога', callback_data=f'{info_type}-programming {message_id} {chat_id}')
    return_btn = InlineKeyboardButton('Меню', callback_data=f'menu {message_id} {chat_id}')
    return InlineKeyboardMarkup(row_width=1).add(physics_btn, math_btn, programming_btn, return_btn)


def materials_by_subject(message_id, info_type,chat_id):
    literature_btn = InlineKeyboardButton('Учебная литература', callback_data=f'{info_type}-literature {message_id} {chat_id}')
    homework_btn = InlineKeyboardButton('Д/З', callback_data=f'{info_type}-homework {message_id} {chat_id}')
    done_homework_btn = InlineKeyboardButton('ГДЗ', callback_data=f'{info_type}-done_homework {message_id} {chat_id}')
    return_btn = InlineKeyboardButton('Меню', callback_data=f'menu {message_id} {chat_id}')
    return InlineKeyboardMarkup(row_width=1).add( homework_btn, return_btn)


def up_down__load_files(message_id, info_type,chat_id):
    upload_btn = InlineKeyboardButton('Загрузить файлы', callback_data=f'{info_type}-upload {message_id} {chat_id}')
    download_btn = InlineKeyboardButton('Скачать файлы', callback_data=f'{info_type}-download {message_id} {chat_id}')
    return_btn = InlineKeyboardButton('Меню', callback_data=f'menu {message_id} {chat_id}')
    return InlineKeyboardMarkup(row_width=1).add(upload_btn, download_btn, return_btn)


def homework_for_dates(message_id, info_type, dates,chat_id):
    date_btns = [InlineKeyboardButton(f'{date}', callback_data=f'{info_type}-get-{date} {message_id} {chat_id}')
                 for date in dates]
    return InlineKeyboardMarkup(row_width=1).add(*[btn for btn in date_btns])

def new_menu():
    materials = InlineKeyboardButton('Материалы',callback_data= 'materials')
    return InlineKeyboardMarkup(row_width=1).add(materials)

def new_subjects():
    physics_btn = InlineKeyboardButton('Физика', callback_data='phys')
    math_btn = InlineKeyboardButton('Вышмат', callback_data='math')
    programming_btn = InlineKeyboardButton('Алгпрога', callback_data=' prog')
    return_btn = InlineKeyboardButton('Меню', callback_data='menu')
    return InlineKeyboardMarkup(row_width=1).add(physics_btn, math_btn, programming_btn, return_btn)
def new_m_b_subject(info):
    homework_btn = InlineKeyboardButton('Д/З', callback_data=f'{info} homework')
    return_btn = InlineKeyboardButton('Меню', callback_data='menu 1')
    return InlineKeyboardMarkup(row_width=1).add(homework_btn,return_btn)
def new_updown(info):
    upload_btn = InlineKeyboardButton('Загрузить файлы', callback_data=f'{info} upload')
    download_btn = InlineKeyboardButton('Скачать файлы', callback_data=f'{info} download')
    return_btn = InlineKeyboardButton('Меню', callback_data='menu 1')
    return InlineKeyboardMarkup(row_width=1).add(upload_btn, download_btn, return_btn)
