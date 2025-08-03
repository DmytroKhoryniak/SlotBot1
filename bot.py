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
    "uk": (
        "👋 Вітаю в сигнальному боті для слотів! 🎰🤖\n"
        "Тут працює ШТУЧНИЙ ІНТЕЛЕКТ з точністю 95% 🎯 — ловимо бонуси, зриваємо банки! 💣💰\n\n"
        "💸 Реальні гроші\n"
        "🔥 Мінімум ризику\n"
        "🚫 Робота? Забудь! Тут заробляють сидячи вдома 🛋️📱\n"
        "🌴 Хочеш свободу, як у мрії? Це твій шанс! 🏝️🕊️\n\n"
        "Тисни далі — і запускай грьобану машину бабла! 🚀💵💵💵"
    ),
    "ru": (
        "👋 Добро пожаловать в сигнального бота для слотов! 🎰🤖\n"
        "Здесь работает ИСКУССТВЕННЫЙ ИНТЕЛЛЕКТ с точностью 95% 🎯 — ловим бонусы, срываем банки! 💣💰\n\n"
        "💸 Реальные деньги\n"
        "🔥 Минимум риска\n"
        "🚫 Работа? Забудь! Здесь зарабатывают, сидя дома 🛋️📱\n"
        "🌴 Хочешь свободы, как в мечтах? Это твой шанс! 🏝️🕊️\n\n"
        "Жми дальше — запускай бабломашину! 🚀💵💵💵"
    ),
    "en": (
        "👋 Welcome to the slot signal bot! 🎰🤖\n"
        "Here, ARTIFICIAL INTELLIGENCE works with 95% accuracy 🎯 — we hunt bonuses and hit jackpots! 💣💰\n\n"
        "💸 Real money\n"
        "🔥 Minimum risk\n"
        "🚫 Work? Forget it! Earn while chilling at home 🛋️📱\n"
        "🌴 Want dream-like freedom? This is your shot! 🏝️🕊️\n\n"
        "Tap next — and launch the damn money machine! 🚀💵💵💵"
    )
},

    "after_register_text": {
    "uk": (
        "⚠️ УВАГА! Перш ніж почати — обов’язково зареєструйся в казино через кнопку вище 🔗🎰\n"
        "Це важливо! Без реєстрації бот НЕ зможе синхронізуватись з твоїм акаунтом 🚫🤖\n\n"
        "❌ Без цього сигнали не працюватимуть, будуть помилки і ти втратиш шанс на бабки 💸😤\n"
        "✅ Зроби 1 клік — і запускай гру без глюків! 🚀💥"
    ),
    "ru": (
        "⚠️ ВНИМАНИЕ! Перед началом — обязательно зарегистрируйся в казино через кнопку выше 🔗🎰\n"
        "Это важно! Без регистрации бот НЕ сможет синхронизироваться с твоим аккаунтом 🚫🤖\n\n"
        "❌ Без этого сигналы не будут работать, будут ошибки и ты упустишь шанс на деньги 💸😤\n"
        "✅ Сделай 1 клик — и запускай игру без сбоев! 🚀💥"
    ),
    "en": (
        "⚠️ ATTENTION! Before you start — make sure to register at the casino using the button above 🔗🎰\n"
        "It’s important! Without registration, the bot CANNOT sync with your account 🚫🤖\n\n"
        "❌ Without this, signals won’t work, errors will occur, and you’ll miss your chance at cash 💸😤\n"
        "✅ Just 1 click — and start the game with no glitches! 🚀💥"
    )
},
    "instruction_text": {
    "uk": (
        "📋 Інструкція, як зірвати куш: 💰💥\n\n"
        "1️⃣ Зареєструйся в казино через кнопку Реєстрація 🔗\n"
        "2️⃣ Поповни рахунок — мінімум $10 💳💵\n"
        "3️⃣ Зайди в слот, де хочеш отримати сигнал 🎰\n"
        "4️⃣ Зроби скріншот всередині гри 📸\n"
        "5️⃣ Запусти нашого бота 🤖\n"
        "6️⃣ Вибери свою мову 🌍\n"
        "7️⃣ Завантаж знімок екрана 🖼️\n"
        "8️⃣ Отримай сигнал та інфу, коли чекати бонус 🎯🎁\n\n"
        "🚀 Далі — просто лутай великі бабки! 💸💸💸"
    ),
    "ru": (
        "📋 Инструкция, как сорвать куш: 💰💥\n\n"
        "1️⃣ Зарегистрируйся в казино через кнопку Регистрация 🔗\n"
        "2️⃣ Пополни счёт — минимум $10 💳💵\n"
        "3️⃣ Зайди в слот, где хочешь получить сигнал 🎰\n"
        "4️⃣ Сделай скриншот внутри игры 📸\n"
        "5️⃣ Запусти нашего бота 🤖\n"
        "6️⃣ Выбери свой язык 🌍\n"
        "7️⃣ Загрузи скриншот 🖼️\n"
        "8️⃣ Получи сигнал и инфу, когда ждать бонус 🎯🎁\n\n"
        "🚀 А дальше — просто собирай большие бабки! 💸💸💸"
    ),
    "en": (
        "📋 Step-by-step to hit the jackpot: 💰💥\n\n"
        "1️⃣ Register at the casino using the Registration button 🔗\n"
        "2️⃣ Fund your account — minimum $10 💳💵\n"
        "3️⃣ Open the slot where you want the signal 🎰\n"
        "4️⃣ Take a screenshot inside the game 📸\n"
        "5️⃣ Launch our bot 🤖\n"
        "6️⃣ Choose your language 🌍\n"
        "7️⃣ Upload the screenshot 🖼️\n"
        "8️⃣ Get the signal and info on when to expect the bonus 🎯🎁\n\n"
        "🚀 Then — just loot those big bucks! 💸💸💸"
    )
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
