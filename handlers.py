from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import  InlineKeyboardMarkup
import text
import kb
import db
import day
import main


from apscheduler.schedulers.asyncio import AsyncIOScheduler

router = Router()
scheduler = AsyncIOScheduler()

# запуск приложения
@router.message(Command("start"))
async def start_handler(msg: Message):
    user_id = msg.from_user.id
    if db.examination_start(user_id) == 1:
        await msg.answer(f"Привет! А я уже знаком с тобой :)")
    else:
        await msg.answer(text.start)
        db.get_groups()
        await msg.answer(text.acquaintance.format(name=msg.from_user.full_name), reply_markup=kb.groups_keyboard)


# Обработчик выбора группы
@router.callback_query(lambda call: call.data.startswith("group_"))
async def show_students(call: types.CallbackQuery):
    group_id = call.data.split("_")[1]  # Извлекаем ID группы
    student_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [button] for button in db.get_students(group_id)
    ])
    await call.message.answer(text.acquaintance_student.format(name=call.from_user.full_name), reply_markup=student_keyboard)
    await main.delite(call.from_user.id, call.message.message_id)

# Обработчик выбора студента
@router.callback_query(lambda call: call.data.startswith("student_"))
async def remember_student(call: types.CallbackQuery):
    student_name = call.data.split("_")[1]
    telegram_id = call.from_user.id
    if db.examination_student(student_name) == 0:
        await call.message.answer(f"Я уже знаком с этим студентом и он - не ты. Попробуй снова")
    else: 
        db.telegram_id(telegram_id, student_name)
        await call.message.answer(text.telegram_id.format(name=call.from_user.full_name))
        await main.delite(call.from_user.id, call.message.message_id)

# Обработчик выбора блюда
@router.callback_query(lambda call: call.data.startswith("dishes_"))
async def remember_delishe(call: types.CallbackQuery):
    student_id = db.chat_student_id(call.from_user.id)
    dishes_id = call.data.split("_")[1]
    DayOfTheWeek_id = await main.send_message()# тут ошибка -----------------------------------------------
    print(DayOfTheWeek_id)
    db.get_selection(student_id, dishes_id, DayOfTheWeek_id)
    await call.message.answer(text.thanks.format(name=call.from_user.full_name))
    await main.delite(call.from_user.id, call.message.message_id)


