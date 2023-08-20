import aiogram.types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def menu(message_id):
    docs_btn = InlineKeyboardButton('Материалы по занятиям', callback_data=f'docs {message_id}')
    homework_btn = InlineKeyboardButton('Домашка', callback_data=f'topical_homework {message_id}')
    score_btn = InlineKeyboardButton('Баллы на вышмате',callback_data=f'score {message_id}')
    return InlineKeyboardMarkup(row_width=1).add(docs_btn,score_btn)


def subjects(message_id, info_type,subjects):
    physics_btn = InlineKeyboardButton('Физика', callback_data=f'{info_type}-physics {message_id}')
    math_btn = InlineKeyboardButton('Вышмат', callback_data=f'{info_type}-math {message_id}')
    programming_btn = InlineKeyboardButton('Алгпрога', callback_data=f'{info_type}-programming {message_id}')
    return_btn = InlineKeyboardButton('Меню', callback_data=f'menu {message_id}')
    subjects_btn = [InlineKeyboardButton(f'{Subject}',callback_data=f'{info_type}-{Subject} {message_id}') for Subject in subjects]
    return InlineKeyboardMarkup(row_width=1).add(*[btn for btn in subjects_btn])



def materials_by_subject(message_id, info_type):
    literature_btn = InlineKeyboardButton('Учебная литература', callback_data=f'{info_type}-literature {message_id}')
    homework_btn = InlineKeyboardButton('Д/З', callback_data=f'{info_type}-homework {message_id}')
    check_btn = InlineKeyboardButton('Посещаемость', callback_data=f'{info_type}-check {message_id}')
    return_btn = InlineKeyboardButton('Меню', callback_data=f'menu {message_id}')
    return InlineKeyboardMarkup(row_width=1).add( homework_btn,check_btn, return_btn)


def up_down__load_files(message_id, info_type):
    upload_btn = InlineKeyboardButton('Загрузить файлы', callback_data=f'{info_type}-upload {message_id}')
    download_btn = InlineKeyboardButton('Скачать файлы', callback_data=f'{info_type}-download {message_id}')
    return_btn = InlineKeyboardButton('Меню', callback_data=f'menu {message_id}')
    return InlineKeyboardMarkup(row_width=1).add(upload_btn, download_btn, return_btn)


def homework_for_dates(message_id, info_type, dates):
    date_btns = [InlineKeyboardButton(f'{date}', callback_data=f'{info_type}-get-{date} {message_id}')
                 for date in dates]
    return InlineKeyboardMarkup(row_width=1).add(*[btn for btn in date_btns])
def score_chose(message_id, info_type):
    my_score_btn = InlineKeyboardButton('Мои баллы',callback_data=f'{info_type}-my {message_id}')
    edit_score_btn = InlineKeyboardButton('Редактировать баллы',callback_data=f'{info_type}-edit {message_id}')
    all_score_btn = InlineKeyboardButton('Все баллы',callback_data=f'{info_type}-all {message_id}')
    return_btn = InlineKeyboardButton('Меню', callback_data=f'menu {message_id}')
    return InlineKeyboardMarkup(row_width=1).add(my_score_btn,edit_score_btn,all_score_btn,return_btn)
def score_edit(message_id, info_type,names):
    name_btn = [InlineKeyboardButton(f'{name}',callback_data=f'{info_type}-ns-{name} {message_id}') for name in names]
    return InlineKeyboardMarkup(row_width=1).add(*[btn for btn in name_btn])
def check(message_id, info_type):
    star_btn = InlineKeyboardButton('Обьявить общий сбор хомячков',callback_data=f'{info_type}-starbtn {message_id}')
    stud_btn = InlineKeyboardButton('Староста, отметь пожалуйста',callback_data=f'{info_type}-studbtn {message_id}')
    return_btn = InlineKeyboardButton('Меню', callback_data=f'menu {message_id}')
    return InlineKeyboardMarkup(row_width=1).add(star_btn,stud_btn,return_btn)
def locate():
    button = aiogram.types.KeyboardButton("Share Position", request_location=True)
    return aiogram.types.ReplyKeyboardMarkup(row_width=1).add(button)