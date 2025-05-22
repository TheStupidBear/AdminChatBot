import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from handlers import admin, users


#включаем логирование
logging.basicConfig(level=logging.INFO)

bot = Bot(token="7536510978:AAGEaZ1b3xl_32IQUO1bRgEnlo7nXjx94no")
#диспетчер
dp = Dispatcher()
#подключаем роутеры
dp.include_routers(admin.router, users.router)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет. бот для ведения группы (привествие новых пользователей"
                         " и удаление нецензурной брани).")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())