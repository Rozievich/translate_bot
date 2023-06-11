import logging

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import BotCommand
from translate import Translator

from database import create_table, cur, con
from editdata import data_edit
from reply_button import main_btn, admin_btn, one_lang
from state import DeleteState, UserState, AdminState, RekState, SetLang

logging.basicConfig(level=logging.INFO)

TOKEN = '6191316739:AAGA7OSmgnTayqa3lG38hDkd2JX8-QcXr_A'
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

translator = Translator(from_lang='uz', to_lang='en')
lang_dict = {"🇬🇧 English": 'en', '🇷🇺 Russian': 'ru', '🇺🇿 Uzbek': 'uz', '🇹🇷 Turkish': 'tr', '🇩🇪 German': 'de',
             '🇫🇷 French': 'fr'}


@dp.message_handler(commands=['start'])
async def start_handler(msg: types.Message):
    await bot.set_my_commands([BotCommand('start', 'Qayta ishga tushirish!'), BotCommand('help', 'Yordam olish!')])
    query = 'SELECT * FROM users WHERE user_id = %s'  # noqa
    cur.execute(query, (str(msg.from_user.id),))
    if not cur.fetchone():
        query = 'INSERT INTO users(user_id, name, username) VALUES (%s, %s, %s)'  # noqa
        cur.execute(query, (str(msg.from_user.id), msg.from_user.first_name, msg.from_user.username))
        con.commit()
    await msg.answer(
        text='Translate botga xush kelibsiz 🤖\n'
             'Iltimos til sozlamalarini belgilang ⚙️\nBot standart sozlamalari Uzbek to English ✅',
        reply_markup=main_btn())


@dp.message_handler(commands='mainadminsecret')
async def main_admin(msg: types.Message):
    query = 'SELECT * FROM admins'  # noqa
    cur.execute(query)
    users = cur.fetchall()
    id_s = []
    for i in users:
        id_s.append(int(i[1]))
    if not id_s:
        try:
            query = 'INSERT INTO admins(user_id) VALUES (%s)'  # noqa
            cur.execute(query, (str(msg.from_user.id),))
            con.commit()
        except:  # noqa
            await msg.answer(text='Nimadir xato Ketdi!')
    else:
        await msg.answer(text='Admin Allaqachon mavjud!')


@dp.message_handler(commands=['help'])
async def help_handler(msg: types.Message):
    await msg.answer(
        text="Agar tarjima qilishda qandaydir muammolar bo'lsa kiritgan matningiz til sozlamalariga mos kelishini tekshirib ko'ring! ✍️\n\nVa botga 500 belgidan ko'p bo'lmagan matn kiritishingizni so'raymiz! ✅\n\nTarjimada muammolar kuzatilsa Adminga murojat qiling! 👨🏻‍💻\n\nBiz muammolarni tez orada bartaraf etamiz! ⏳")  # noqa


@dp.message_handler(Text('Settings ⚙️'))
async def settings_lang(msg: types.Message):
    await SetLang.one_lang.set()
    await msg.answer("Sozlamalar Bo'limiga xush kelibsiz ⚙️\n\nMatningiz tilini tanlang: ", reply_markup=one_lang())


@dp.message_handler(state=SetLang.one_lang)
async def one_langs(msg: types.Message, state: FSMContext):
    if lang_dict.get(msg.text):
        async with state.proxy() as data:
            data['one'] = lang_dict[msg.text]
        await SetLang.two_lang.set()
        await msg.answer(text="Qaysi Tilga tarjima qilmoqchsiz: ", reply_markup=one_lang())
    else:
        await msg.answer(text="Bunday til mavjud emas!")


@dp.message_handler(state=SetLang.two_lang)
async def two_langs(msg: types.Message, state: FSMContext):
    if lang_dict.get(msg.text):
        global translator
        async with state.proxy() as data:
            data['two'] = lang_dict[msg.text]
            translator = Translator(from_lang=data['one'], to_lang=data['two'])
        await bot.send_message(msg.from_user.id, text="Til Sozlamalari O'rnatildi!", reply_markup=main_btn())
        await state.finish()
    else:
        await msg.answer(text="Katta Xato Brat!")


@dp.message_handler(Text('👨🏻‍💻 Admin'))
async def admin_handler(msg: types.Message):
    query = 'SELECT * FROM admins'  # noqa
    cur.execute(query)
    users = cur.fetchall()
    id_s = []
    for i in users:
        id_s.append(int(i[1]))
    if msg.from_user.id in id_s:
        await msg.answer(text=f'{msg.from_user.first_name} admin sahifaga xush kelibsiz!',
                         reply_markup=admin_btn())  # noqa
    else:
        await UserState.comments.set()
        await msg.answer(text='Talab va Takliflaringizni yozib qoldiring!')  # noqa


@dp.message_handler(state=UserState.comments)
async def user_comments(msg: types.Message, state):
    await msg.answer(text="Fikrlar adminga jo'natildi!")  # noqa
    query = 'SELECT * FROM admins'  # noqa
    cur.execute(query)
    users = cur.fetchall()
    id_s = []
    for i in users:
        id_s.append(int(i[1]))
    for i in id_s:
        await bot.send_message(i,
                               f"ID: {msg.from_user.id}\nName: {msg.from_user.first_name}\nUsername: {msg.from_user.username}\nFikrlar: {msg.text}")  # noqa
    await state.finish()


@dp.message_handler(Text("📊 Statistika"))
async def statistika(msg: types.Message):
    query = 'SELECT * FROM users'  # noqa
    cur.execute(query)
    users = cur.fetchall()
    await msg.answer(text=f'Foydalanuvchilar Soni: {len(users)}')


@dp.message_handler(Text("🗣 Reklama"))
async def reklama_handler(msg: types.Message):
    await RekState.reklama.set()
    await msg.answer(text="Reklama Bo'limi!")


@dp.message_handler(state=RekState.reklama, content_types=types.ContentType.ANY)
async def rek_state(msg: types.Message, state: FSMContext):
    await msg.answer(text="Reklama jo'natish boshlandi!")
    summa = 0
    query = 'SELECT * FROM users'  # noqa
    cur.execute(query)
    users = cur.fetchall()
    for i in users:
        query = 'SELECT * FROM admins'  # noqa
        cur.execute(query)
        admins = cur.fetchall()
        id_s = []
        for j in admins:
            id_s.append(int(j[1]))
        if int(i[1]) not in id_s:
            try:
                await msg.copy_to(int(i[1]), caption=msg.caption, caption_entities=msg.caption_entities,
                                  reply_markup=msg.reply_markup)
            except:  # noqa
                summa += 1
    await state.finish()


@dp.message_handler(Text("👤 Add admin"))
async def add_admin_handler(msg: types.Message):
    await AdminState.comment.set()
    await msg.answer(text='Admin ID kiriting: ')


@dp.message_handler(state=AdminState.comment)
async def admin_handler(msg: types.Message, state):
    try:
        if msg.text.isdigit():
            query = 'INSERT INTO admins(user_id) VALUES (%s)'  # noqa
            cur.execute(query, (msg.text,))
            con.commit()
        else:
            await msg.answer(text="ID Raqam bo'lishi kerak!")
    except:  # noqa
        await msg.answer(text='Nimadir xato ketdi!')
    else:
        await msg.answer('Admin Tayinlandi!')
    await state.finish()


@dp.message_handler(Text("❌ Delete admin"))
async def delete_admin_handler(msg: types.Message):
    await DeleteState.delete.set()
    await msg.answer(text='Admin ID kiriting: ')


@dp.message_handler(state=DeleteState.delete)
async def admin_delete(msg: types.Message, state):
    try:
        if msg.text.isdigit():
            query = 'DELETE FROM admins WHERE user_id = %s'  # noqa
            cur.execute(query, (msg.text,))
            con.commit()
        else:
            await msg.answer(text="ID Raqam bo'lishi kerak!")
    except:  # noqa
        await msg.answer(text="Nimadir xato ketdi!")
    else:
        await msg.answer(text='Admin muvaffaqiyatli o\'chirildi!')
    await state.finish()


@dp.message_handler(Text("Back ⬅️"))
async def back_menu(msg: types.Message):
    await msg.answer(text='Bosh menu 🛎', reply_markup=main_btn())


@dp.message_handler()
async def result_handler(msg: types.Message):
    if len(msg.text) > 4050:
        await msg.answer(text='Iltimos qisqaroq matn kiriting!')
    else:
        await msg.reply(data_edit(translator, msg.text))


async def on_startup(dp):
    create_table()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
