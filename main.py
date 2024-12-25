import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import sys
import kb
import handlers
import db
import text
import day
import chart

router = Router()

if sys.platform == 'win32':
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
bot = Bot(token='7972577832:AAGhaJYn5eIw8gDZ2Q6YZS90mW81p12Uq-E', default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())


async def main():
    await scheduler()
    # user_id = cb.from_user.id
    # if db.get_admin(user_id) == 1:
    dp.include_router(handlers.router)
    # dp.include_router(handlers_user.user_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    


async def delete_message_after_12_hours(msg):
    await asyncio.sleep(43200)  # 12 часов в секундах
    try:
        await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    except Exception as e:
        print(e)


async def send_message():
    for chat_id in db.chat_id():
        try:
            await bot.send_message(chat_id=chat_id, text=text.choice, reply_markup=kb.create_menu_keyboard())
        except Exception as e:
            print(e)


async def send_message_admin():
    for admin in db.admin_id():
        try:
            chart.chart_create()  
            image_path = 'C:/Users/user/Desktop/tg_bot/my_plot.png' 
            image = FSInputFile(image_path)  
            await bot.send_document(chat_id=admin, document=image) 
            await bot.send_message(chat_id=admin, text=f"Всего проголосовало учеников: {chart.chart_create()}", reply_markup=kb.confirmation_admin)
            os.remove(image_path)  
            print(f"Файл {image_path} успешно удален.")
        except Exception as e:
            print(e)


async def scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_message_admin, 'cron', day_of_week='0-4', hour=9, end_date='2024-12-27',)
    scheduler.add_job(send_message, 'cron', day_of_week='0-4', hour=10, minute='10',end_date='2024-12-27',)
    scheduler.add_job(delite_selection, 'cron', day_of_week='0', hour='0', minute='0', end_date='2024-12-27',)
    scheduler.start()


async def delite_selection():
    DayOfTheWeek_id = day.get_DayOfTheWeekId()
    db.delete_old_selections(DayOfTheWeek_id)


async def delite(chat_id, message_id):
    await bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=None  
     )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    
# Запуск приложения 
