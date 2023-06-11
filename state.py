from aiogram.dispatcher.filters.state import StatesGroup, State


class DeleteState(StatesGroup):
    delete = State()


class UserState(StatesGroup):
    comments = State()


class AdminState(StatesGroup):
    comment = State()


class RekState(StatesGroup):
    reklama = State()


class SetLang(StatesGroup):
    one_lang = State()
    two_lang = State()
