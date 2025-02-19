import random

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

from countries import countries

mode = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🏳 По флагам')],
        [KeyboardButton(text='🕌 По достопримечательностям')],
        [KeyboardButton(text='✖️ Смешанный')]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите режим игры"
)

async def generate_keyboard(state: FSMContext):
    _countries = countries.copy()
    if (await state.get_state()):
        correct = list(_countries.keys())[random.randint(0, len(_countries)-1)]
        while correct == (await state.get_state()).split(':')[1]:
            correct = list(_countries.keys())[random.randint(0, len(_countries)-1)]
        correct = _countries.pop(correct)
    else:
        correct = _countries.pop(list(_countries.keys())[random.randint(0, len(_countries)-1)])
    _correct = random.randint(1, 4)

    buttons = []
    for i in range(1, 5):
        if i == _correct:
            buttons.append([KeyboardButton(text=correct)])
        else:
            buttons.append([KeyboardButton(text=_countries.pop(list(_countries.keys())[random.randint(0, len(_countries)-1)]))])

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )

    return (keyboard, correct)