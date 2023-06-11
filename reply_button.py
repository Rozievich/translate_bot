from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_btn():
    btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    btn.add(KeyboardButton('Settings ⚙️'), KeyboardButton('👨🏻‍💻 Admin'))
    return btn


def admin_btn():
    btn = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
    btn.add(KeyboardButton('📊 Statistika'), KeyboardButton("🗣 Reklama"), KeyboardButton('👤 Add admin'),
            KeyboardButton('❌ Delete admin'), KeyboardButton('Back ⬅️'))
    return btn


def one_lang():
    btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
    btn.add(KeyboardButton("🇬🇧 English"), KeyboardButton('🇷🇺 Russian'), KeyboardButton('🇺🇿 Uzbek'),
            KeyboardButton('🇹🇷 Turkish'), KeyboardButton('🇩🇪 German'), KeyboardButton('🇫🇷 French'))
    return btn
