import os
import random

from aiogram import Bot, Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from keyboards import mode, generate_keyboard
from countries import reversed_countries
from states import Flags, Sights, All
from config import TOKEN

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
router = Router()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FLAGS_DIR = os.path.join(BASE_DIR, 'flags')
SIGHTS_DIR = os.path.join(BASE_DIR, 'sights')

@router.message(Command('start'))
async def on_start(msg: Message):
    await msg.answer(f'Привет, {msg.from_user.full_name}\nЭто бот для отгадывания стран.\n\nВыберите режим:',
                     reply_markup=mode)

@router.message(F.text == '🏳 По флагам')
async def on_flags(msg: Message, state: FSMContext):
    keyboard, correct = await generate_keyboard(state)

    photo = FSInputFile(f'{FLAGS_DIR}\\{reversed_countries[correct]}.png')
    await bot.send_photo(msg.from_user.id, photo, caption='Выберите страну:\n\nРежим: 🏳 Флаги\nЧтобы закончить игру напишите /start', reply_markup=keyboard)

    await state.set_state(eval(f'Flags.{reversed_countries[correct]}'))

@router.message(F.text == '🕌 По достопримечательностям')
async def on_sights(msg: Message, state: FSMContext):
    keyboard, correct = await generate_keyboard(state)

    photo = FSInputFile(f'{SIGHTS_DIR}\\{reversed_countries[correct]}.jpg')
    await bot.send_photo(msg.from_user.id, photo, caption='Выберите страну:\n\nРежим: 🕌 Достопримечательности\nЧтобы закончить игру напишите /start', reply_markup=keyboard)

    await state.set_state(eval(f'Sights.{reversed_countries[correct]}'))

@router.message(F.text == '✖️ Смешанный')
async def on_sights(msg: Message, state: FSMContext):
    keyboard, correct = await generate_keyboard(state)

    if random.randint(1, 2) == 1:
        photo = FSInputFile(f'{FLAGS_DIR}\\{reversed_countries[correct]}.png')
    else:
        photo = FSInputFile(f'{SIGHTS_DIR}\\{reversed_countries[correct]}.jpg')

    await bot.send_photo(msg.from_user.id, photo, caption='Выберите страну:\n\nРежим: ✖️ Смешанный\nЧтобы закончить игру напишите /start', reply_markup=keyboard)

    await state.set_state(eval(f'All.{reversed_countries[correct]}'))

@router.message()
async def on_country(msg: Message, state: FSMContext):
    mode, correct = (await state.get_state()).split(':')

    if reversed_countries[msg.text] == correct:
        await msg.answer('✅ Правильно!')
    else:
        await msg.answer('❌ Неправильно!')
    
    if mode == 'Flags':
        await on_flags(msg, state)
    elif mode == 'Sights':
        await on_sights(msg, state)
    elif mode == 'All':
        await on_sights(msg, state)