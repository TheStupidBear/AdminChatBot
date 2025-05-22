
from aiogram import Router, F, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from .variables import bad_words

router = Router()

class OrderDirection(StatesGroup): #состояния
    add_bad_word = State()
    del_bad_word = State()


@router.message(Command("cancel"))
async def add_bad_word(message: types.Message, state: FSMContext):
    await message.answer("Процесс отменён")
    # Устанавливаем пользователю состояние
    await state.clear()

@router.message(Command("add"))
async def add_bad_word(message: types.Message, state: FSMContext):
    await message.answer("Введите стоп слово: (чтобы отменить команду введите: /cancel)")
    # Устанавливаем пользователю состояние
    await state.set_state(OrderDirection.add_bad_word)

@router.message(OrderDirection.add_bad_word, F.text)
async def add_bad_word(message: types.Message):
    #если слово уже есть в списке
    if message.text.lower() in bad_words:
        await message.answer("Это слово уже есть")
    else:
        bad_words.append(message.text)
        await message.answer(f"Добавлено новое стоп слово")


@router.message(Command("del"))
async def add_bad_word(message: types.Message, state: FSMContext):
    await message.answer("Введите стоп слово, которое хотите удалить: (чтобы отменить команду введите: /cancel")
    # Устанавливаем пользователю состояние
    await state.set_state(OrderDirection.del_bad_word)

@router.message(OrderDirection.del_bad_word, F.text)
async def add_bad_word(message: types.Message, state: FSMContext):
    #если слово уже есть в списке
    if message.text.lower() in bad_words:
        bad_words.remove(message.text)
        await message.answer("Удалил слово из списка")
        # Устанавливаем пользователю состояние
        await state.clear()
    else:
        await message.answer(f"Нет такого слова")

@router.message(Command("check"))
async def add_bad_word(message: types.Message):
    await message.answer("Список запрещенных слов:")
    #вывод текста в одну строку
    await message.answer(", ".join(bad_words))

