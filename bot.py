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

API_TOKEN = '7978588767:AAFn6S40YOG470r0hzJoDR90nv9ggJ3wGf0'  # 🔐 Заміни на свій токен

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

texts = {
    "choose_language": {
        "uk": "Оберіть мову / Выберите язык / Choose language:",
        "ru": "Оберіть мову / Выберите язык / Choose language:",
        "en": "Оберіть мову / Выберите язык / Choose language:"
    },
    "welcome": {
        "uk": (
            "\U0001F44B Вітаю тебе в сигнальному боті для слотів у казино!\n\n"
            "\U0001F3B0 Тут працює штучний інтелект нового покоління, який аналізує тисячі ігор в реальному часі.\n\n"
            "\U0001F50D Бот виявляє моменти підвищеної віддачі у слотах та надсилає сигнали з точністю до 80%.\n"
            "\U0001F4CA Алгоритм навчений на реальних даних гравців і постійно самонавчається для кращої ефективності.\n\n"
            "\u26A1\uFE0F Тільки актуальні та перевірені сигнали\n"
            "\U0001F4C8 Мінімум ризику — максимум результату\n"
            "\U0001F4B8 Працюєш — заробляєш\n\n"
            "\U0001F514 Увімкни сповіщення, щоб не пропустити “гарячий” слот.\n\n"
            "Готовий почати? Натисни нижче ⬇️"
        ),
        "ru": (
            "\U0001F44B Привет! Это сигнальный бот для игровых автоматов в казино!\n\n"
            "\U0001F3B0 Искусственный интеллект анализирует тысячи игр в реальном времени.\n\n"
            "\U0001F50D Бот определяет моменты с высокой отдачей и отправляет сигналы с точностью до 80%.\n"
            "\U0001F4CA Алгоритм обучен на реальных данных и постоянно самообучается.\n\n"
            "\u26A1\uFE0F Только проверенные сигналы\n"
            "\U0001F4C8 Минимум риска — максимум результата\n"
            "\U0001F4B8 Играешь — зарабатываешь\n\n"
            "\U0001F514 Включи уведомления, чтобы не пропустить “горячий” слот.\n\n"
            "Готов начать? Нажимай кнопку ниже ⬇️"
        ),
        "en": (
            "\U0001F44B Welcome to the signal bot for casino slots!\n\n"
            "\U0001F3B0 AI analyzes thousands of games in real time.\n\n"
            "\U0001F50D The bot detects high payout moments and sends signals with up to 80% accuracy.\n"
            "\U0001F4CA The algorithm is trained on real player data and constantly improves.\n\n"
            "\u26A1\uFE0F Only verified signals\n"
            "\U0001F4C8 Minimum risk — maximum result\n"
            "\U0001F4B8 Play smart — earn more\n\n"
            "\U0001F514 Turn on notifications to catch the “hot” slot.\n\n"
            "Ready to start? Tap the button below ⬇️"
        )
    },
    "after_register": {
        "uk": (
            "‼️ Увага! Перед початком обов’язкові дії:\n"
            "1️⃣ Зареєструйся за посиланням у кнопці «Реєстрація» зверху.\n"
            "🔒 Реєстрація обов’язкова, адже бот синхронізується з твоїм профілем та зчитує інформацію для правильного підбору сигналу.\n\n"
            "2️⃣ Після успішної реєстрації — прочитай покрокову інструкцію.\n"
            "3️⃣ Далі натискай «Обрати гру», і бот надішле тобі сигнал.\n\n"
            "\U0001F4B8 Ти всього в двох кроках від прибутку.\nВперед до грошей! 🚀"
        ),
        "ru": (
            "‼️ Внимание! Перед началом обязательные шаги:\n"
            "1️⃣ Зарегистрируйся по ссылке в кнопке «Регистрация» выше.\n"
            "🔒 Регистрация обязательна, бот синхронизируется с твоим профилем.\n\n"
            "2️⃣ После успешной регистрации — прочитай инструкцию.\n"
            "3️⃣ Затем нажми «Выбрать игру», и бот отправит сигнал.\n\n"
            "\U0001F4B8 Ты в двух шагах от прибыли.\nВперёд к деньгам! 🚀"
        ),
        "en": (
            "‼️ Attention! Follow these steps:\n"
            "1️⃣ Register using the link in the «Register» button above.\n"
            "🔒 Registration is required to sync your profile for accurate signal detection.\n\n"
            "2️⃣ After registering, read the step-by-step guide.\n"
            "3️⃣ Then tap «Pick a game» to get a signal.\n\n"
            "\U0001F4B8 You’re two steps away from profit.\nLet’s go! 🚀"
        )
    },
    "instruction": {
        "uk": "📘 Інструкція:\n1️⃣ Зареєструйся\n2️⃣ Запусти Bonus Predictor\n3️⃣ Завантаж скрін\n4️⃣ Отримай сигнал",
        "ru": "📘 Инструкция:\n1️⃣ Зарегистрируйся\n2️⃣ Запусти Bonus Predictor\n3️⃣ Загрузить скрин\n4️⃣ Получи сигнал",
        "en": "📘 Instructions:\n1️⃣ Register\n2️⃣ Run Bonus Predictor\n3️⃣ Upload a screenshot\n4️⃣ Get the signal"
    },
    "restart": {
        "uk": "🔄 Якщо потрібно, натисни «Restart bot»",
        "ru": "🔄 При необходимости нажми «Restart bot»",
        "en": "🔄 If needed, tap «Restart bot»"
    }
}

lang_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
for code, name in languages.items():
    lang_buttons.add(KeyboardButton(name))

restart_button = ReplyKeyboardMarkup(resize_keyboard=True)
restart_button.add(KeyboardButton("🔄 Restart bot"))

start_markup = InlineKeyboardMarkup(row_width=2)
start_markup.add(
    InlineKeyboardButton("📝 Реєстрація", url="https://slot-bot-webapp.vercel.app/"),
    InlineKeyboardButton("✅ Реєстрація успішна", callback_data="after_register")
)

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer(texts["choose_language"]["uk"], reply_markup=lang_buttons)
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

    await message.answer(texts["welcome"][selected_lang], reply_markup=start_markup)
    await Form.registered.set()

@dp.callback_query_handler(lambda c: c.data == 'after_register', state=Form.registered)
async def after_register(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "uk")

    await callback_query.message.edit_text(texts["after_register"][lang], reply_markup=main_markup)
    await bot.send_message(callback_query.from_user.id, texts["restart"][lang], reply_markup=restart_button)

main_markup = InlineKeyboardMarkup(row_width=2)
main_markup.add(
    InlineKeyboardButton("📘 Інструкція", callback_data="instruction"),
    InlineKeyboardButton("🎯 Bonus Prediction", web_app=WebAppInfo(url="https://slot-bot-webapp.vercel.app/"))
)

@dp.callback_query_handler(lambda c: c.data == 'instruction', state='*')
async def send_instruction(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "uk")
    await callback_query.message.edit_text(
        texts["instruction"][lang],
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("🎯 Bonus Prediction", url="https://slot-bot-webapp.vercel.app/")
        )
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
