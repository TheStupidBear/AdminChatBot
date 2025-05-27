import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from handlers import admin, users


#включаем логирование
logging.basicConfig(level=logging.INFO)

#ищем токен в файле env
load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
#диспетчер
dp = Dispatcher()
#подключаем роутеры
dp.include_routers(admin.router, users.router)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет. бот для ведения группы (приветствие новых пользователей"
                         " и удаление нецензурной брани).")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())