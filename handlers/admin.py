from aiogram import Router, F, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.filters import BaseFilter
from aiogram.types import Message
from .variables import bad_words

router = Router()

#фильтр проверка на админа или создателя
class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool: #возвращает булево значение
        user_id = message.from_user.id
        chat_id = -1002622439216
        chat_member = await message.bot.get_chat_member(user_id=user_id, chat_id=chat_id)
        # проверка на админа или создателя группы
        if chat_member.status in ['creator', 'administrator']:  # если это админ или создатель группы
            return True
        else:
            return False



class OrderDirection(StatesGroup): #состояния
    add_bad_word = State()
    del_bad_word = State()


@router.message(Command("help"), IsAdminFilter())
async def help_admin(message: types.Message):
    await message.answer("Команды:\n/check - посмотреть список запрещенных слов"
                         "\n/add - добавить запрещенное слово (ввод по одному слову)"
                         "\n/del - удалить запрещенное слово (ввод по одному слову)"
                         "\n/cancel - отмена операции)"
                         )



@router.message(Command("cancel"), IsAdminFilter())
async def cancel_admin(message: types.Message, state: FSMContext):
    await message.answer("Процесс отменён")
    # Устанавливаем пользователю состояние
    await state.clear()




@router.message(Command("add"), IsAdminFilter())
async def add_bad_word(message: types.Message, state: FSMContext):
    await message.answer("Введите стоп слово: (чтобы отменить команду введите: /cancel)")
    # Устанавливаем пользователю состояние
    await state.set_state(OrderDirection.add_bad_word)





@router.message(OrderDirection.add_bad_word, F.text, IsAdminFilter())
async def state_add_bad_word(message: types.Message):
    #если слово уже есть в списке
    if message.text.lower() in bad_words:
        await message.answer("Это слово уже есть")
    else:
        bad_words.append(message.text)
        await message.answer(f"Добавлено новое стоп слово")


@router.message(Command("del"), IsAdminFilter())
async def del_bad_word(message: types.Message, state: FSMContext):
    await message.answer("Введите стоп слово, которое хотите удалить: (чтобы отменить команду введите: /cancel")
    # Устанавливаем пользователю состояние
    await state.set_state(OrderDirection.del_bad_word)



@router.message(OrderDirection.del_bad_word, F.text, IsAdminFilter())
async def state_del_bad_word(message: types.Message, state: FSMContext):
    #если слово уже есть в списке
    if message.text.lower() in bad_words:
        bad_words.remove(message.text)
        await message.answer("Удалил слово из списка")
        # Устанавливаем пользователю состояние
        await state.clear()
    else:
        await message.answer(f"Нет такого слова")

@router.message(Command("check"), IsAdminFilter())
async def check_bad_words(message: types.Message):
    await message.answer("Список запрещенных слов:")
    # вывод текста в одну строку
    await message.answer(", ".join(bad_words))





