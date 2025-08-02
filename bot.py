from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo
)
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging

API_TOKEN = '7978588767:AAFn6S40YOG470r0hzJoDR90nv9ggJ3wGf0'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class Form(StatesGroup):
    language = State()
    registered = State()

# Словник мов
languages = {
    "uk": "🇺🇦 Українська",
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English"
}

# Кнопки вибору мови
lang_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
for code, name in languages.items():
    lang_buttons.add(KeyboardButton(name))

# Кнопка рестарту
restart_button = ReplyKeyboardMarkup(resize_keyboard=True)
restart_button.add(KeyboardButton("🔄 Restart bot"))

# Кнопки після реєстрації
start_markup = InlineKeyboardMarkup(row_width=2)
start_markup.add(
    InlineKeyboardButton("📝 Реєстрація", url="https://slot-bot-webapp.vercel.app/"),
    InlineKeyboardButton("✅ Реєстрація успішна", callback_data="after_register")
)

# Кнопки основного меню
main_markup = InlineKeyboardMarkup(row_width=2)
main_markup.add(
    InlineKeyboardButton("📘 Інструкція", callback_data="instruction"),
    InlineKeyboardButton(
        text="🎯 Bonus Prediction",
        web_app=WebAppInfo(url="https://slot-bot-webapp.vercel.app/")
    )
)

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer("Оберіть мову / Выберите язык / Choose language:", reply_markup=lang_buttons)
    await Form.language.set()

@dp.message_handler(state=Form.language)
async def set_language(message: types.Message, state: FSMContext):
    selected_lang = None
    for code, name in languages.items():
        if name in message.text:
            selected_lang = code
            break

    if not selected_lang:
        await message.reply("Будь ласка, оберіть мову з клавіатури.")
        return

    await state.update_data(language=selected_lang)

    await message.answer(
        "\U0001F44B Вітаю тебе в сигнальному боті для слотів у казино!\n"
        "\n\U0001F3B0 Тут працює штучний інтелект нового покоління, який аналізує тисячі ігор в реальному часі.\n"
        "\n\U0001F50D Бот виявляє моменти підвищеної віддачі у слотах та надсилає сигнали з точністю до 80%."
        "\n\U0001F4CA Алгоритм навчений на реальних даних гравців і постійно самонавчається для кращої ефективності.\n"
        "\n\u26A1\uFE0F Тільки актуальні та перевірені сигнали\n"
        "\U0001F4C8 Мінімум ризику — максимум результату\n"
        "\U0001F4B8 Працюєш — заробляєш\n"
        "\n\U0001F514 Увімкни сповіщення, щоб не пропустити “гарячий” слот.\n"
        "\nГотовий почати? Натисни нижче ⬇️",
        reply_markup=start_markup
    )
    await Form.registered.set()

@dp.callback_query_handler(lambda c: c.data == 'after_register', state=Form.registered)
async def after_register(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "‼️ Увага! Перед початком обов’язкові дії:\n"
        "1️⃣ Зареєструйся за посиланням у кнопці «Реєстрація» зверху.\n"
        "🔒 Реєстрація обов’язкова, адже бот синхронізується з твоїм профілем та зчитує інформацію для правильного підбору сигналу.\n"
        "\n2️⃣ Після успішної реєстрації — прочитай покрокову інструкцію.\n"
        "3️⃣ Далі натискай «Обрати гру», і бот надішле тобі сигнал.\n"
        "\n\U0001F4B8 Ти всього в двох кроках від прибутку.\nВперед до грошей! 🚀",
        reply_markup=main_markup
    )
    # Показуємо кнопку рестарту
    await bot.send_message(callback_query.from_user.id, "🔄 Якщо потрібно, натисни «Restart bot»", reply_markup=restart_button)

@dp.callback_query_handler(lambda c: c.data == 'instruction', state='*')
async def send_instruction(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "📘 Інструкція:\n"
        "1️⃣ Зареєструйся по посиланню зверху\n"
        "2️⃣ Запусти Bonus Predictor\n"
        "3️⃣ Завантаж скрін з гри та вибери слот\n"
        "4️⃣ Отримай сигнал з шансами на бонус\n"
        "\nНатисни нижче, щоб перейти до аналізу",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("🎯 Bonus Prediction", url="https://slot-bot-webapp.vercel.app/")
        )
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
