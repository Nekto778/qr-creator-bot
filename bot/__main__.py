import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from .config import BOT_TOKEN
from .database import db
from .handlers import register_handlers

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    await db.init()
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    register_handlers(dp)
    try:
        await dp.start_polling(bot)
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())
