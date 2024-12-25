from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
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
    if db.get_admin(user_id) == 1:
        await msg.answer(text= f"{msg.from_user.full_name}, вы зарегестрированы как админ. По будням в 9:00 я буду присылать статистику выбранных блюд")
    else:
        if db.examination_start(user_id) == 1:
            await msg.answer(f"Привет! А я уже знаком с тобой :)")
        else:
            await msg.answer(text.start)
            db.get_groups()
            await msg.answer(text.acquaintance.format(name=msg.from_user.full_name), reply_markup=kb.create_groups_keyboard())



# Обработчик выбора группы
@router.callback_query(lambda call: call.data.startswith("group_"))
async def show_students(call: types.CallbackQuery):
    user_id = call.from_user.id
    if db.get_admin(user_id) == 1:
        group_id = call.data.split("_")[1]  # Извлекаем ID группы
        data = day.get_DayOfTheWeekId() - 1
        text = db.admin_info(group_id, data)
        text_message = "\n".join(text)
        await call.message.answer(text_message)
    else:
        group_id = call.data.split("_")[1]  # Извлекаем ID группы
        await call.message.answer(text.acquaintance_student.format(name=call.from_user.full_name), reply_markup=kb.create_students_keyboard(group_id))
        await main.delite(call.from_user.id, call.message.message_id) 
    
   
# Обработчик выбора студента
@router.callback_query(lambda call: call.data.startswith("student_"))
async def remember_student(call: types.CallbackQuery):
    if call.data.startswith("student_") == call.data.startswith("student_000"): #выбор кнопки "назад"
        await main.delite(call.from_user.id, call.message.message_id)
        await call.message.answer(text.back2.format(name=call.from_user.full_name), reply_markup=kb.create_groups_keyboard())
    else:
        student_name = call.data.split("_")[1]
        telegram_id = call.from_user.id
        if db.examination_student(student_name) == 0:   #студент уже записан в бд под другим id
            await call.message.answer(f"Я уже знаком с этим студентом и он - не ты. Попробуй снова")
        else: 
            await call.message.answer(f"Ты {student_name}, правильно?", reply_markup=kb.confirmation_kb)
            await call.message.answer(text.student2.format(name=call.from_user.full_name))
            await main.delite(call.from_user.id, call.message.message_id)
            @router.callback_query(lambda call: call.data.startswith("Yes"))  #подтверждение выбора студента
            async def confirmation_student(call: types.CallbackQuery): 
                db.telegram_id(telegram_id, student_name)
                await call.message.answer(text.telegram_id.format(name=call.from_user.full_name))
                await main.delite(call.from_user.id, call.message.message_id)
            @router.callback_query(lambda call: call.data.startswith("No"))  #подтверждение выбора студента
            async def confirmation_no_student(call: types.CallbackQuery):
                await call.message.answer("Попробуй снова")
                await main.delite(call.from_user.id, call.message.message_id)
                group_id = db.group_id(student_name)
                await call.message.answer(text.acquaintance_student2.format(name=call.from_user.full_name), reply_markup=kb.create_students_keyboard(group_id))



# Обработчик выбора блюда
@router.callback_query(lambda call: call.data.startswith("dishes_"))
async def remember_delishe(call: types.CallbackQuery):    
    student_id = db.chat_student_id(call.from_user.id)
    dishes_id = call.data.split("_")[1]
    DayOfTheWeek_id = day.get_DayOfTheWeekId()
    db.get_selection(student_id, dishes_id, DayOfTheWeek_id)
    await call.message.answer(text.thanks.format(name=call.from_user.full_name))
    await main.delite(call.from_user.id, call.message.message_id)


@router.callback_query(lambda call: call.data.startswith("detailed"))
async def show_students(call: types.CallbackQuery):
    await call.message.answer(text="Выберете группу, подробности голосования которой хотите увидеть:",reply_markup=kb.create_groups_keyboard()) 


