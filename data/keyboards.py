from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def menu(message_id):
    literature_btn = InlineKeyboardButton('Учебная литература', callback_data=f'literature {message_id}')
    docs_btn = InlineKeyboardButton('Материалы по занятиям', callback_data=f'docs {message_id}')
    homework_btn = InlineKeyboardButton('Домашка', callback_data=f'homework {message_id}')
    return InlineKeyboardMarkup(row_width=1).add(literature_btn, docs_btn, homework_btn)


def subjects(message_id, info_type):
    physics_btn = InlineKeyboardButton('Физика', callback_data=f'{info_type}-physics {message_id}')
    math_btn = InlineKeyboardButton('Вышмат', callback_data=f'{info_type}-math {message_id}')
    programming_btn = InlineKeyboardButton('Алгпрога', callback_data=f'{info_type}-programming {message_id}')
    return_btn = InlineKeyboardButton('Меню', callback_data=f'menu {message_id}')
    return InlineKeyboardMarkup(row_width=1).add(physics_btn, math_btn, programming_btn, return_btn)


def materials_by_subject(message_id, info_type):
    materials_btn = InlineKeyboardButton('материалы к дз', callback_data=f'{info_type}-materials {message_id}')
    homework_btn = InlineKeyboardButton('Д/З', callback_data=f'{info_type}-homework {message_id}')
    done_homework_btn = InlineKeyboardButton('ГДЗ', callback_data=f'{info_type}-done_homework {message_id}')
    return_btn = InlineKeyboardButton('Меню', callback_data=f'menu {message_id}')
    return InlineKeyboardMarkup(row_width=1).add(materials_btn, homework_btn, done_homework_btn, return_btn)