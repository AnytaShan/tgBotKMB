from aiogram.types import InlineKeyboardMarkup
import db
import day

groups_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [button] for button in db.get_groups()
])


dishes_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [button] for button in db.get_menu(day.get_DayOfTheWeekId())])

# клавиатура

