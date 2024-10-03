from aiogram.filters.command import CommandStart
from aiogram import Bot, Dispatcher, types,F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import logging
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import FSInputFile

import crud_functions
from crud_functions import *

logging.basicConfig(level=logging.INFO)
api = ""
bot = Bot(token= api)
dp = Dispatcher()

crud_functions.initiate_db()



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()



@dp.message(CommandStart())
async def cmd_start(message: types.Message):
        await message.answer('Здравствуйте! Вас приветствует калькулятор подсчета калорий! ',
          reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Рассчитать"),
                    KeyboardButton(text="Купить")
                ]
            ],
            resize_keyboard=True,
        ),
    )
@dp.message(F.text == "Рассчитать")
async def main_menu(message):
    await message.answer('Выберите опцию:',
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="Рассчитать норму калорий'", callback_data='calories'),
                                     InlineKeyboardButton(text="Формулы расчёта", callback_data='formulas'),
                                 ]
                             ],
                             resize_keyboard=True,
                         ),
                 )

@dp.message(F.text == "Купить")
async def get_buying_list(message):
    products = crud_functions.get_all_products()
    for product in products:
        await message.answer(f"Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}")
    await message.answer_document(document = FSInputFile('files/картинка.png'), caption='Название: Product1 | Описание: описание 1 | Цена: <100>')
    await message.answer_document(document=FSInputFile('files/картинка2.png'),
                                  caption='Название: Product2 | Описание: описание 2 | Цена: <200>')
    await message.answer_document(document=FSInputFile('files/картинка3.png'),
                                  caption='Название: Product3 | Описание: описание 3 | Цена: <300>')
    await message.answer_document(document=FSInputFile('files/картинка4.png'),
                                  caption='Название: Product4 | Описание: описание 4 | Цена: <400>')

    await message.answer('Выберите продукт для покупки:',
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="Продукт1", callback_data='product_buying'),
                                     InlineKeyboardButton(text="Продукт2", callback_data='product_buying'),
                                     InlineKeyboardButton(text="Продукт3", callback_data='product_buying'),
                                     InlineKeyboardButton(text="Продукт4", callback_data='product_buying'),
                                 ]
                             ],
                             resize_keyboard=True,
                         ),
                 )


@dp.callback_query(F.data =='formulas')
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer("Расчет калоррий по формуле Миффлина - Сан Жеора ")
    await call.answer()

@dp.callback_query(F.data =='product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.callback_query(F.data =='calories')
async def set_age(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите свой возраст:')
    await state.set_state(UserState.age)
    await call.answer()


@dp.message(UserState.age)
async def set_growth(message: types.Message,  state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост(см):')
    await state.set_state(UserState.growth)

@dp.message(UserState.growth)
async def set_weight(message: types.Message,  state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await state.set_state(UserState.weight)

@dp.message(UserState.weight)
async def send_calories(message: types.Message,  state: FSMContext):
    await state.update_data(weight=message.text)
    await message.answer('Введите свой пол (м/ж):')
    await state.set_state(UserState.gender)

@dp.message(UserState.gender)
async def set_gender(message: types.Message, state: FSMContext):
    global calories
    await state.update_data(gender=message.text)
    data = await state.get_data()
    age_ = int(data['age'])
    growth_ = int(data['growth'])
    weight_ = int(data['weight'])

    if data["gender"].upper() == 'Ж':
        calories = (weight_ * 10) + (6.25 * growth_) - (5 * age_) - 161

    elif data["gender"].upper() == 'М':
        calories =(weight_*10) + (6.25 * growth_) - (5* age_) + 5

    await message.answer(f"Ваша норма калорий:{calories}")
    await state.finish()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

