from aiogram.dispatcher.filters.state import StatesGroup, State


class Form(StatesGroup):
    Text = State()
    Image = State()
