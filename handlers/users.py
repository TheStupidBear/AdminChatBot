from aiogram import Router, F, types
from aiogram.types import ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from .variables import bad_words, bad_dict
import time


router = Router()


#приветствие
@router.chat_member(ChatMemberUpdatedFilter((IS_NOT_MEMBER >> IS_MEMBER)))
async def on_user_join(event: ChatMemberUpdated):
    user = event.new_chat_member.user
    await event.answer(f"Добро пожаловать в нашу группу: {user.first_name} "
                       f"{user.last_name}")

#уход с группы
@router.chat_member(ChatMemberUpdatedFilter((IS_MEMBER >> IS_NOT_MEMBER)))
async def on_user_join(event: ChatMemberUpdated):
    user = event.new_chat_member.user
    await event.answer(f"От нас ушел(ушла): {user.first_name} "
                       f"{user.last_name}")

#считывание всех сообщений
@router.message(F.text)
async def check_text(message: types.Message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    chat_id = message.chat.id
    chat_member = await message.bot.get_chat_member(user_id=user_id, chat_id=chat_id)
    #проверка на админа или создателя группы
    if chat_member.status not in ['creator', 'administrator']: #если это не админ и не создатель группы
        if check_bad_word(message) == True: #если есть плохое слово в сообщении
            if check_bad_dict(message) == False:  # если одно нарушение
                await message.answer(
                    f"{user_name}, это ваше 1-е нарушение. После 2-го нарушения вы не сможете писать 1 час")
                # удаляем сообщение
                await message.delete()
            else:  # мьют пользователя (если уже было первое нарушение)
                time_mute = 60  # мьютим пользователя на 60 сек
                await message.bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id,
                                               until_date=time.time() + time_mute,
                                               permissions=types.ChatPermissions(can_send_messages=False))
                await message.answer(f"{user_name}, вы заблокированы на {time_mute} секунд")
                # удаляем сообщение
                await message.delete()
        else: #если нет плохого слова
            pass
    else: #если это админ
        pass


#проверка на плохое слово
def check_bad_word(message):
    list_text = message.text.lower().split() #разделяем строку на список слов
    if len(list(set(list_text) & set(bad_words))) > 0: #список совпадений
        return True
    else:
        return False

#проверка на черный список пользователей
def check_bad_dict(message):
    user_id = message.from_user.id
    if user_id in bad_dict:
        # удаляем человека из словаря
        print(bad_dict)
        del bad_dict[user_id]
        return True
    else:
        bad_dict[user_id] = 1
        return False
