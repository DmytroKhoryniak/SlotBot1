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

languages = {
    "uk": "🇺🇦 Українська",
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English"
}

translations = {
    "start_text": {
        "uk": "👋 Вітаю в сигнальному боті слотів! Тут штучний інтелект дає 95% точних прогнозів — це твій шлях до великих грошей! 💸 З таким заробітком можна й на роботу забити — тільки виграші та свобода! 🚀 🔥 Готовий розбагатіти? Тоді поїхали! 🎰💰",
        "ru": "👋 Добро пожаловать в сигнального бота для слотов в казино! ...",
        "en": "👋 Welcome to the signal bot for casino slots! ..."
    },
    "after_register_text": {
        "uk": "‼️ Увага! Перед початком обов’язкові дії: ...",
        "ru": "‼️ Внимание! Перед началом обязательные действия: ...",
        "en": "‼️ Attention! Before you start, you must: ..."
    },
    "instruction_text": {
        "uk": "📘 Інструкція:\n1️⃣ Зареєструйся ...",
        "ru": "📘 Инструкция:\n1️⃣ Зарегистрируйся ...",
        "en": "📘 Instruction:\n1️⃣ Register ..."
    },
    "register_button": {
        "uk": "📝 Реєстрація",
        "ru": "📝 Регистрация",
        "en": "📝 Register"
    },
    "success_button": {
        "uk": "✅ Реєстрація успішна",
        "ru": "✅ Регистрация успешна",
        "en": "✅ Registered"
    },
    "instruction_button": {
        "uk": "📘 Інструкція",
        "ru": "📘 Инструкция",
        "en": "📘 Instruction"
    },
    "predict_button": {
        "uk": "🎯 Bonus Prediction",
        "ru": "🎯 Предсказание Бонуса",
        "en": "🎯 Bonus Prediction"
    },
    "restart_button": {
        "uk": "🔄 Restart bot",
        "ru": "🔄 Перезапуск бота",
        "en": "🔄 Restart bot"
    }
}

lang_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
for code, name in languages.items():
    lang_buttons.add(KeyboardButton(name))

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

    # Кнопки після вибору мови
    start_markup = InlineKeyboardMarkup(row_width=2)
    start_markup.add(
        InlineKeyboardButton(translations["register_button"][selected_lang], url="https://slot-bot-webapp.vercel.app/"),
        InlineKeyboardButton(translations["success_button"][selected_lang], callback_data="after_register")
    )

    await message.answer(translations["start_text"][selected_lang], reply_markup=start_markup)
    await Form.registered.set()

@dp.callback_query_handler(lambda c: c.data == 'after_register', state=Form.registered)
async def after_register(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    lang = user_data.get("language", "uk")

    # Кнопки основного меню
    main_markup = InlineKeyboardMarkup(row_width=2)
    main_markup.add(
        InlineKeyboardButton(translations["instruction_button"][lang], callback_data="instruction"),
        InlineKeyboardButton(
            text=translations["predict_button"][lang],
            web_app=WebAppInfo(url="https://slot-bot-webapp.vercel.app/")
        )
    )

    await callback_query.message.edit_text(translations["after_register_text"][lang], reply_markup=main_markup)

    restart_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    restart_markup.add(KeyboardButton(translations["restart_button"][lang]))
    await bot.send_message(callback_query.from_user.id, translations["restart_button"][lang], reply_markup=restart_markup)

@dp.callback_query_handler(lambda c: c.data == 'instruction', state='*')
async def send_instruction(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    lang = user_data.get("language", "uk")

    await callback_query.message.edit_text(
        translations["instruction_text"][lang],
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(translations["predict_button"][lang], web_app=WebAppInfo(url="https://slot-bot-webapp.vercel.app/"))
        )
    )

@dp.message_handler(lambda message: message.text.startswith("🔄"))
async def restart_bot(message: types.Message, state: FSMContext):
    await state.finish()  # Скидаємо FSM
    await cmd_start(message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
