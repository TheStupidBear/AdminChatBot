import asyncio
import logging
import time

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from handlers import admin


#включаем логирование
logging.basicConfig(level=logging.INFO)

bot = Bot(token="7536510978:AAGEaZ1b3xl_32IQUO1bRgEnlo7nXjx94no")
#диспетчер
dp = Dispatcher()
#подключаем роутеры
dp.include_routers(admin.router)
#слова-исключения
bad_words = ["бля", "пизда", "нахуй", "в пизду", "пидор", "пидар", "хуй", "пиздец", "ебучий", "хуйня", "ебаная"]
#стоп словарь
bad_dict = {}


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет. бот для ведения группы (привествие новых пользователей"
                         " и удаление нецензурной брани).")

#приветствие
@dp.chat_member(ChatMemberUpdatedFilter((IS_NOT_MEMBER >> IS_MEMBER)))
async def on_user_join(event: ChatMemberUpdated):
    user = event.new_chat_member.user
    await event.answer(f"Добро пожаловать в нашу группу: {user.first_name} "
                       f"{user.last_name}")

#уход с группы
@dp.chat_member(ChatMemberUpdatedFilter((IS_MEMBER >> IS_NOT_MEMBER)))
async def on_user_join(event: ChatMemberUpdated):
    user = event.new_chat_member.user
    await event.answer(f"От нас ушел(ушла): {user.first_name} "
                       f"{user.last_name}")

#считывание всех сообщений
# @dp.message(F.text)
# async def check_text(message: types.Message):
#     user_name = message.from_user.first_name
#     user_id = message.from_user.id
#     chat_id = message.chat.id
#     chat_member = await bot.get_chat_member(user_id=user_id, chat_id=chat_id)
#     #проверка на админа или создателя группы
#     if chat_member.status not in ['creator', 'administrator']: #если это не админ и не создатель группы
#         if check_bad_word(message) == True: #если есть плохое слово в сообщении
#             if check_bad_dict(message) == False:  # если одно нарушение
#                 await message.answer(
#                     f"{user_name}, это ваше 1-е нарушение. После 2-го нарушения вы не сможете писать 1 час")
#                 # удаляем сообщение
#                 await message.delete()
#             else:  # мьют пользователя (если уже было первое нарушение)
#                 time_mute = 60  # мьютим пользователя на 60 сек
#                 await bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id,
#                                                until_date=time.time() + time_mute,
#                                                permissions=types.ChatPermissions(can_send_messages=False))
#                 await message.answer(f"{user_name}, вы заблокированы на {time_mute} секунд")
#                 # удаляем сообщение
#                 await message.delete()
#         else: #если нет плохого слова
#             pass
#     else: #если это админ
#         pass


#проверка на плохое слово
def check_bad_word(message):
    if message.text.lower() in bad_words:
        return True
    else:
        return False

#проверка на черный список пользователей
def check_bad_dict(message):
    global bad_dict
    user_id = message.from_user.id
    if user_id in bad_dict:
        # удаляем человека из словаря
        print(bad_dict)
        del bad_dict[user_id]
        return True
    else:
        bad_dict[user_id] = 1
        return False


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())