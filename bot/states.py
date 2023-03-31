from aiogram.dispatcher.filters.state import StatesGroup, State


# Класс состояний user-а
class UserStatesGroup(StatesGroup):
    start = State()
    talks = State()
    update_model = State()
    logs = State()
