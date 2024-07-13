import asyncio
import logging

from aiogram import Dispatcher, Bot

from config import API_TOKEN

import datab
from handlers import *



logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)

dp = Dispatcher()

async def main():
    dp.include_router(router=router)
    await datab.create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')