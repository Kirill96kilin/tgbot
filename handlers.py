from aiogram.filters.command import Command
from aiogram import Router, types, F

from aiogram.utils.keyboard import ReplyKeyboardBuilder


import datab
from question import quiz_data

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))


@router.message(F.text=="Начать игру")

@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer(f"Давайте начнем квиз!")
    await datab.new_quiz(message)



@router.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):

    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    await callback.message.answer("Верно!")
    current_question_index = await datab.get_quiz_index(callback.from_user.id)
    current_score = await datab.get_user_score(callback.from_user.id)
    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    current_score += 1
    await datab.update_quiz_index(callback.from_user.id, current_question_index)
    await datab.update_user_score(callback.from_user.id, current_score)

    if current_question_index < len(quiz_data):
        await datab.get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен!\nВаш результат: {current_score} правильных ответов")



@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await datab.get_quiz_index(callback.from_user.id)
    current_score = await datab.get_user_score(callback.from_user.id)
    correct_option = datab.quiz_data[current_question_index]['correct_option']

    await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await datab.update_quiz_index(callback.from_user.id, current_question_index)
    await datab.update_user_score(callback.from_user.id, current_score)


    if current_question_index < len(quiz_data):
        await datab.get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен!\nВаш результат: {current_score} правильных ответов")


@router.message(Command("help"))
async def cmd_start(message: types.Message):
    await message.answer("Команды бота: \n\start - начать взаимодействие с ботом\n\help - открыть помощь\n\quiz - начать игру")
