import sqlite3 as sql
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import CallbackQuery, MediaGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import os

bot = Bot("8429333528:AAFvdMZ9H45Oo2W7ln7sezTu2xt14Yta2HI")
Storage = MemoryStorage()
dp = Dispatcher(bot, storage=Storage)


db_dir = '/app/data'
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

db_path = os.path.join(db_dir, 'bot.db')
conn = sql.connect(db_path)
db.isolation_level = None
cur = db.cursor()

class AddDZ(StatesGroup):
    waiting_for_subject = State()
    waiting_for_task = State()
    waiting_for_photo = State()
    waiting_for_date = State()

class AddVidhuk(StatesGroup):
    waiting_for_vidhuk = State()

dzpbutton = types.KeyboardButton('ДЗ по предметам')
dztmbutton = types.KeyboardButton('ДЗ на завтра')
infobutton = types.KeyboardButton('Додаткова Інформація')

add_dzbutton = types.KeyboardButton('Додати ДЗ')
top_usersbutton = types.KeyboardButton('Топ юзерів')

studentmarkup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
adminmarkup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
superadminmarkup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

studentmarkup.add(dzpbutton, dztmbutton, infobutton)
adminmarkup.add(dzpbutton, dztmbutton, infobutton, add_dzbutton, top_usersbutton)
superadminmarkup.add(dzpbutton, dztmbutton, infobutton, add_dzbutton, top_usersbutton)


@dp.message_handler(commands=['start'])
async def start(message: types.Message, state = FSMContext):
    username = message.from_user.username
    user_tag = "@" + str(username)

    cur.execute("SELECT name, user_status, join_date FROM users WHERE user_id = ?", (user_tag,))
    result = cur.fetchone()

    if result is not None:
        name, status, join_date = result

        # Перевіряємо, чи дата вже була записана раніше
        if join_date is None:
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur.execute("UPDATE users SET join_date = ? WHERE user_id = ?", (current_date, user_tag))
            db.commit()

        await state.update_data(user_status=status)
        if status == 'student':
            await message.answer(f"👋 Привіт, {name} 😊! Тут ти зможеш переглянути домашнє завдання! Для цього користуйся меню нижче⬇️", reply_markup=studentmarkup)
        elif status == 'admin':
            await message.answer(f"👋 Привіт, {name} 😊! Тут ти зможеш переглянути, або записати домашнє завдання! Для цього користуйся меню нижче⬇️", reply_markup=adminmarkup)
        elif status == 'superadmin':
            await message.answer(f"👋 Привіт, {name} 😊! Тут ти зможеш переглянути, або записати домашнє завдання! Також ти маєш деякі особливі права суперадміна! Для користування всіма переліченими функціями, користуйся меню нижче⬇️", reply_markup=superadminmarkup)
    else:
        await message.answer(f"👋 Привіт! Якщо ти наш, то напиши цьому додіку, щоби він тебе додав до вайтлисту: @DJAST_GTH")

@dp.message_handler(lambda message: message.text == 'ДЗ по предметам')
async def dzpredmet(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    infabutton = types.InlineKeyboardButton('🖥 Інформатика', callback_data='buttoninfa_pressed')
    matembutton = types.InlineKeyboardButton('📐 Математика', callback_data='buttonmatem_pressed')
    fizikabutton = types.InlineKeyboardButton('⚛️ Фізика', callback_data='buttonfizika_pressed')
    himiabutton = types.InlineKeyboardButton('🧪 Хімія', callback_data='buttonhimia_pressed')
    ukrmovabutton = types.InlineKeyboardButton('📝 Українська мова', callback_data='buttonukrmova_pressed')
    engmovabutton = types.InlineKeyboardButton('📝 Англійська мова', callback_data='buttonengmova_pressed')
    ukrlitbutton = types.InlineKeyboardButton('📝 Українська література', callback_data='buttonukrlit_pressed')
    zarlitbutton = types.InlineKeyboardButton('📝 Зарубіжна література', callback_data='buttonzarlit_pressed')
    ukristbutton = types.InlineKeyboardButton('📜 Історія України', callback_data='buttonukrist_pressed')
    vsesvistbutton = types.InlineKeyboardButton('📜 Всесвітня історія', callback_data='buttonvsesvist_pressed')
    zubutton = types.InlineKeyboardButton('🔱 Захист України', callback_data='buttonzu_pressed')
    biologiabutton = types.InlineKeyboardButton('🌱 Біологія', callback_data='buttonbiologia_pressed')
    gromosvbutton = types.InlineKeyboardButton('⚖️ Громадянська освіта', callback_data='buttongromosv_pressed')
    ekobutton = types.InlineKeyboardButton('⚖️ Економічна теорія', callback_data='buttoneko_pressed')
    pravobutton = types.InlineKeyboardButton('🏛️ Основи правознавства', callback_data='buttonpravo_pressed')
    fizkulbutton = types.InlineKeyboardButton('💪 Фізична культура', callback_data='buttonfizkul_pressed')

    markup.add(infabutton, matembutton, fizikabutton, himiabutton, ukrmovabutton, engmovabutton, ukrlitbutton, zarlitbutton, ukristbutton, vsesvistbutton,
               zubutton, biologiabutton, gromosvbutton, ekobutton, pravobutton, fizkulbutton)

    await message.answer("👌 Чудово! Ось список предметів. Вибери потрібний, а я відправлю список 10 останніх ДЗ по ньому", reply_markup=markup)


subjects = {
    "buttoninfa_pressed": "Інформатика",
    "buttonmatem_pressed": "Математика",
    "buttonfizika_pressed": "Фізика",
    "buttonhimia_pressed": "Хімія",
    "buttonukrmova_pressed": "Українська мова",
    "buttonengmova_pressed": "Англійська мова",
    "buttonukrlit_pressed": "Українська література",
    "buttonzarlit_pressed": "Зарубіжна література",
    "buttonukrist_pressed": "Історія України",
    "buttonvsesvist_pressed": "Всесвітня історія",
    "buttonzu_pressed": "Захист України",
    "buttonbiologia_pressed": "Біологія",
    "buttongromosv_pressed": "Громадянська освіта",
    "buttoneko_pressed": "Економічна теорія",
    "buttonpravo_pressed": "Основи правознавства",
    "buttonfizkul_pressed": "Фізична культура"
}

@dp.callback_query_handler(lambda c: c.data in subjects.keys())
async def universal_subject_handler(callback: types.CallbackQuery):
    subject_name = subjects[callback.data]
    cur.execute("SELECT Завдання, Строк, file_id FROM ДЗ WHERE Предмет = ? ORDER BY rowid DESC LIMIT 10", (subject_name,))
    results = cur.fetchall()
    await callback.answer()
    if not results:
        await callback.message.answer(f"📭 По предмету <b>{subject_name}</b> завдань не знайдено.", parse_mode="HTML")
    else:
        text_header = f"📚 10 останніх завдань: <b>{subject_name}</b>\n\n"
        await callback.message.answer(text_header, parse_mode="HTML")

        for i, row in enumerate(results, 1):
            msg_text = f"{i}. 📅 {row[1]}\n📝 {row[0]}\n\n"
            if row[2]:
                file_ids = row[2].split(",")
                if len(file_ids) > 1:
                    media = MediaGroup()
                    for idx, f_id in enumerate(file_ids):
                        media.attach_photo(f_id, caption=msg_text if idx == 0 else "")
                    await callback.message.answer_media_group(media)
                else:
                    await callback.message.answer_photo(file_ids[0], caption=msg_text)
            else:
                await callback.message.answer(msg_text)


months = {
    1: "січня", 2: "лютого", 3: "березня", 4: "квітня",
    5: "травня", 6: "червня", 7: "липня", 8: "серпня",
    9: "вересня", 10: "жовтня", 11: "листопада", 12: "грудня"
}

week = {
    0: "Понеділок",
    1: "Вівторок",
    2: "Середа",
    3: "Четвер",
    4: "П’ятниця",
    5: "Субота",
    6: "Неділя"
}


@dp.message_handler(lambda message: message.text == 'ДЗ на завтра')
async def dztomorrow(message: types.Message):
    today = datetime.now()
    tomorrow_date = today + timedelta(days=1)
    tomorrow = f"{tomorrow_date.day} {months[tomorrow_date.month]}"

    cur.execute("SELECT Предмет, Завдання, file_id FROM ДЗ WHERE Строк = ?", (tomorrow,))
    result = cur.fetchall()

    header = f"👌 Ось домашнє завдання на завтра ({week[tomorrow_date.weekday()]}, {tomorrow}):"

    if not result:
        await message.answer("🎉 Завдань не знайдено! Можна відпочивати... Або дехто забув додати..")
    else:
        await message.answer(header)
        for i, row in enumerate(result, 1):
            msg_text = f"{i}. <b>{row[0]}</b>: {row[1]}\n\n"
            if row[2]:
                file_ids = row[2].split(",")
                if len(file_ids) > 1:
                    media = MediaGroup()
                    for idx, f_id in enumerate(file_ids):
                        media.attach_photo(f_id, caption=msg_text if idx == 0 else "")
                    await message.answer_media_group(media)
                else:
                    await message.answer_photo(file_ids[0], caption=msg_text, parse_mode="HTML")
            else:
                await message.answer(msg_text, parse_mode="HTML")


@dp.message_handler(lambda message: message.text == 'Додаткова Інформація')
async def info_handler(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    probotabutton = types.InlineKeyboardButton('ℹ️ Про бота', callback_data='probotabutton_pressed')
    otzivbutton = types.InlineKeyboardButton('✍️ Написати відгук', callback_data='otzivbutton_pressed')

    markup.add(probotabutton, otzivbutton)

    await message.answer("👌 Чудово! вибирай потрібну тобі інформацію нижче", reply_markup=markup)

@dp.callback_query_handler(text="probotabutton_pressed")
async def process_callback_button(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Це бот-асистент, що помагатиме Вам із пошуком потрібного ДЗ по предмету чи дню тижня. \n\nТворець: @DJAST_GTH")

@dp.callback_query_handler(text="otzivbutton_pressed")
async def process_callback_button(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    username = callback_query.from_user.username
    cur.execute("SELECT user_status FROM users WHERE user_id = ?", ("@" + str(username),))
    result = cur.fetchone()
    await state.update_data(user_status=result[0])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    menubutton = types.KeyboardButton('⬅️ Назад до меню')

    markup.add(menubutton)

    await callback_query.message.answer("Добре! Напишіть свій відгук:", reply_markup=markup)
    await AddVidhuk.waiting_for_vidhuk.set()

@dp.message_handler(state=AddVidhuk.waiting_for_vidhuk)
async def vidhuk_written(message: types.Message, state: FSMContext):
    data = await state.get_data()
    status = data.get('user_status')
    markup = studentmarkup
    if status == 'admin':
        markup = adminmarkup
    elif status == 'superadmin':
        markup = superadminmarkup

    if message.text == '⬅️ Назад до меню':
        await state.finish()
        await message.answer("Повертаємося...", reply_markup=markup)
        return

    username = message.from_user.username
    vidhuk = message.text
    date = datetime.now().isoformat()

    try:
        cur.execute("INSERT INTO Відгуки (Юзер, Відгук, Дата) VALUES (?, ?, ?)",
                    (username, vidhuk, date))
        db.commit()
        await message.answer(f"✅ Ваш відгук збережено", reply_markup=markup)
    except Exception as e:
        print(f"Помилка БД: {e}")
        await message.answer("❌ Сталася помилка при записі відгуку. Спробуйте пізніше.", reply_markup=markup)
    finally:
        await state.finish()


@dp.message_handler(lambda message: message.text == 'Додати ДЗ')
async def add_dz(message: types.Message, state: FSMContext):
    username = message.from_user.username
    cur.execute("SELECT user_status FROM users WHERE user_id = ?", ("@" + str(username),))
    result = cur.fetchone()
    await state.update_data(user_status=result[0] if result else 'student', photo_ids=[])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    menubutton = types.KeyboardButton('⬅️ Назад до меню')
    infabutton = types.KeyboardButton('Інформатика')
    matembutton = types.KeyboardButton('Математика')
    fizikabutton = types.KeyboardButton('Фізика')
    himiabutton = types.KeyboardButton('Хімія')
    ukrmovabutton = types.KeyboardButton('Українська мова')
    engmovabutton = types.KeyboardButton('Англійська мова')
    ukrlitbutton = types.KeyboardButton('Українська література')
    zarlitbutton = types.KeyboardButton('Зарубіжна література')
    ukristbutton = types.KeyboardButton('Історія України')
    vsesvistbutton = types.KeyboardButton('Всесвітня історія')
    zubutton = types.KeyboardButton('Захист України')
    biologiabutton = types.KeyboardButton('Біологія')
    gromosvbutton = types.KeyboardButton('Громадянська освіта')
    ekobutton = types.KeyboardButton('Економічна теорія')
    pravobutton = types.KeyboardButton('Основи правознавства')
    fizkulbutton = types.KeyboardButton('Фізична культура')

    markup.add(menubutton, infabutton, matembutton, fizikabutton, himiabutton, ukrmovabutton, engmovabutton, ukrlitbutton, zarlitbutton, ukristbutton, vsesvistbutton,
                zubutton, biologiabutton, gromosvbutton, ekobutton, pravobutton, fizkulbutton)

    await message.answer("Добре! Давайте додамо ДЗ. Виберіть предмет:", reply_markup=markup)
    await AddDZ.waiting_for_subject.set()

@dp.message_handler(state=AddDZ.waiting_for_subject)
async def subject_chosen(message: types.Message, state: FSMContext):
    if message.text == '⬅️ Назад до меню':
        data = await state.get_data()
        status = data.get('user_status')
        markup = studentmarkup
        if status == 'admin':
            markup = adminmarkup
        elif status == 'superadmin':
            markup = superadminmarkup
        await state.finish()
        await message.answer("Повертаємося...", reply_markup=markup)
        return

    await state.update_data(chosen_subject=message.text)
    await message.answer(f"Чудово! Предмет: {message.text}. Тепер напиши завдання:",
                         reply_markup=types.ReplyKeyboardRemove())
    await AddDZ.waiting_for_task.set()

@dp.message_handler(state=AddDZ.waiting_for_task)
async def task_entered(message: types.Message, state: FSMContext):
    await state.update_data(dz_text=message.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("Без фото ❌"), types.KeyboardButton("Готово ✅"))
    await message.answer(f"Надішліть фото до завдання або натисніть кнопку:", reply_markup=markup)
    await AddDZ.waiting_for_photo.set()

@dp.message_handler(state=AddDZ.waiting_for_photo, content_types=['photo', 'text'])
async def photo_entered(message: types.Message, state: FSMContext):
    data = await state.get_data()
    photo_ids = data.get('photo_ids', [])

    if message.text == "Без фото ❌":
        await state.update_data(file_id=None)
    elif message.text == "Готово ✅":
        await state.update_data(file_id=",".join(photo_ids) if photo_ids else None)
    elif message.photo:
        photo_ids.append(message.photo[-1].file_id)
        await state.update_data(photo_ids=photo_ids)
        return await message.answer(f"Фото отримано! Можете надіслати ще або натисніть «Готово ✅»")
    else:
        return await message.answer("Надішліть фото або натисніть кнопку.")

    await message.answer(f"Зрозумів. Тепер напиши дату здачі (наприклад: 5 січня):",
                         reply_markup=types.ReplyKeyboardRemove())
    await AddDZ.waiting_for_date.set()

@dp.message_handler(state=AddDZ.waiting_for_date)
async def date_entered(message: types.Message, state: FSMContext):
    data = await state.get_data()
    subject = data.get('chosen_subject')
    dz_text = data.get('dz_text')
    file_id = data.get('file_id')
    date = message.text
    status = data.get('user_status')

    markup = studentmarkup
    if status == 'admin':
        markup = adminmarkup
    elif status == 'superadmin':
        markup = superadminmarkup

    try:
        cur.execute("INSERT INTO ДЗ (Предмет, Завдання, Строк, file_id) VALUES (?, ?, ?, ?)",
                    (subject, dz_text, date, file_id))
        db.commit()
        await message.answer(f"✅ Збережено", reply_markup=markup)
    except Exception as e:
        print(f"Помилка БД: {e}")
        await message.answer("❌ Сталася помилка при записі. Спробуйте пізніше.", reply_markup=markup)
    finally:
        await state.finish()

@dp.message_handler(lambda message: message.text == 'Топ юзерів')
async def show_top_users(message: types.Message):
    username_accessor = "@" + str(message.from_user.username)
    cur.execute("SELECT user_status FROM users WHERE user_id = ?", (username_accessor,))
    res = cur.fetchone()

    if res and res[0] in ['admin', 'superadmin']:
        # Вибираємо юзернейм (user_id) та дату, сортуємо від найдавніших
        cur.execute("""
            SELECT user_id, join_date FROM users
            WHERE join_date IS NOT NULL
            ORDER BY join_date ASC
            LIMIT 10
        """)
        users = cur.fetchall()

        if not users:
            await message.answer("📭 Список порожній або ніхто ще не запускав бот.")
            return

        text = "🏆 <b>Топ 10 перших користувачів:</b>\n\n"
        for i, (u_id, date) in enumerate(users, 1):
            text += f"{i}. {u_id} — 📅 <code>{date}</code>\n"

        await message.answer(text, parse_mode="HTML")
    else:
        await message.answer("❌ У вас немає прав для перегляду цієї інформації.")


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    finally:
        db.close()
