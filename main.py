from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import sys
import kb
import handlers
import db
import text
import day

router = Router()

if sys.platform == 'win32':
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
bot = Bot(token='TOKEN', default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())



async def main():
    await scheduler()
    dp.include_router(handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    


tasks = {}

async def delete_message_after_12_hours(msg):
    await asyncio.sleep(43200)  # 12 часов в секундах
    try:
        await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    except Exception as e:
        print(e)

async def send_message():
    for chat_id in db.chat_id():
        try:
            print(chat_id)
            msg = await bot.send_message(chat_id=chat_id, text=text.choice, reply_markup=kb.dishes_keyboard)
            task = asyncio.create_task(delete_message_after_12_hours(msg))
            tasks[msg.message_id] = task
        except Exception as e:
            print(e)



async def scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_message, 'cron', day_of_week='0-4', hour=13, minute='9', end_date='2024-12-27',)
    scheduler.add_job(delite_selection, day='*/10', hour='0', minute='0', end_date='2024-12-27',)
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
