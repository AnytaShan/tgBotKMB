from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import db
import day

def create_groups_keyboard():
    groups = db.get_groups()
    # Создаем список для клавиатуры
    inline_keyboard = []

    # Группируем кнопки по две
    for i in range(0, len(groups), 2):
        row_buttons = groups[i:i + 2]  # Берем две кнопки за раз
        inline_keyboard.append(row_buttons)  # Добавляем их в список как строку

    # Создаем клавиатуру с правильным параметром
    groups_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return groups_keyboard


def create_students_keyboard(group_id):
    students = db.get_students(group_id)
    # Создаем список для клавиатуры
    inline_keyboard = []

    # Группируем кнопки по две
    for i in range(0, len(students), 2):
        row_buttons = students[i:i + 2]  # Берем две кнопки за раз
        inline_keyboard.append(row_buttons)  # Добавляем их в список как строку

    # Создаем клавиатуру с правильным параметром
    students_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return students_keyboard


btn_1 = InlineKeyboardButton(text='Да', callback_data='Yes')
btn_2 = InlineKeyboardButton(text='Нет', callback_data='No')
confirmation_kb = InlineKeyboardMarkup(inline_keyboard=[[btn_1], [btn_2]])



def create_menu_keyboard():
    menu = db.get_menu(day.get_DayOfTheWeekId())
    menu_keyboard = []

    for i in range(0, len(menu), 2):
        row_buttons = menu[i:i + 2]
        menu_keyboard.append(row_buttons)  

    menu_keyboard = InlineKeyboardMarkup(inline_keyboard=menu_keyboard)
    return menu_keyboard

# клавиатура

