""" Main module of aiogram 3.3.0 bot.
    https://mastergroosha.github.io/aiogram-3-guide/messages/
    https://docs.aiogram.dev/en/latest/api/types/chat.html
"""

import asyncio
from os import getenv

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db.engine import engine, Base
from handlers import _top_router

load_dotenv()

bot = Bot(getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
scheduler = AsyncIOScheduler()


async def main():
    """main method"""
    scheduler.start()
    dp.include_routers(_top_router.router)
    Base.metadata.create_all(engine)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Nicely shutting down ...")