from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def menu(message_id):
    docs_btn = InlineKeyboardButton('Материалы по занятиям', callback_data=f'docs {message_id}')
    homework_btn = InlineKeyboardButton('Домашка', callback_data=f'topical_homework {message_id}')
    return InlineKeyboardMarkup(row_width=1).add(docs_btn)


def subjects(message_id, info_type):
    physics_btn = InlineKeyboardButton('Физика', callback_data=f'{info_type}-physics {message_id}')
    math_btn = InlineKeyboardButton('Вышмат', callback_data=f'{info_type}-math {message_id}')
    programming_btn = InlineKeyboardButton('Алгпрога', callback_data=f'{info_type}-programming {message_id}')
    return_btn = InlineKeyboardButton('Меню', callback_data=f'menu {message_id}')
    return InlineKeyboardMarkup(row_width=1).add(physics_btn, math_btn, programming_btn, return_btn)


def materials_by_subject(message_id, info_type):
    literature_btn = InlineKeyboardButton('Учебная литература', callback_data=f'{info_type}-literature {message_id}')
    homework_btn = InlineKeyboardButton('Д/З', callback_data=f'{info_type}-homework {message_id}')
    done_homework_btn = InlineKeyboardButton('ГДЗ', callback_data=f'{info_type}-done_homework {message_id}')
    return_btn = InlineKeyboardButton('Меню', callback_data=f'menu {message_id}')
    return InlineKeyboardMarkup(row_width=1).add( homework_btn, return_btn)


def up_down__load_files(message_id, info_type):
    upload_btn = InlineKeyboardButton('Загрузить файлы', callback_data=f'{info_type}-upload {message_id}')
    download_btn = InlineKeyboardButton('Скачать файлы', callback_data=f'{info_type}-download {message_id}')
    return_btn = InlineKeyboardButton('Меню', callback_data=f'menu {message_id}')
    return InlineKeyboardMarkup(row_width=1).add(upload_btn, download_btn, return_btn)


def homework_for_dates(message_id, info_type, dates):
    date_btns = [InlineKeyboardButton(f'{date}', callback_data=f'{info_type}-get-{date} {message_id}')
                 for date in dates]
    return InlineKeyboardMarkup(row_width=1).add(*[btn for btn in date_btns])
