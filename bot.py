from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
import asyncio
import time

TOKEN = "8977454092:AAHH7fvoXTHJn4_-RAfTswtM3X17gtWblrc"
ADMIN_ID = 8043686910  # Вставь сюда свой Telegram ID

bot = Bot(TOKEN)
dp = Dispatcher()

cooldown = {}

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Вставить текст")]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Здесь ты можешь отправить сообщение.\n"
        "Нажми кнопку ниже.",
        reply_markup=keyboard
    )

@dp.message(F.text == "📝 Вставить текст")
async def button(message: Message):
    await message.answer("✍️ Отправьте сообщение.")

@dp.message()
async def receive(message: Message):
    user_id = message.from_user.id

    if message.text == "📝 Вставить текст":
        return

    now = time.time()

    if user_id in cooldown:
        left = int(cooldown[user_id] - now)
        if left > 0:
            minutes = left // 60
            seconds = left % 60
            await message.answer(
                f"⏳ Подождите ещё {minutes} мин. {seconds} сек."
            )
            return

    cooldown[user_id] = now + 600  # 10 минут

    await bot.send_message(
        ADMIN_ID,
        f"📩 Новое сообщение\n\n"
        f"👤 @{message.from_user.username}\n"
        f"🆔 {user_id}\n\n"
        f"💬 {message.text}"
    )

    await message.answer(
        "✅ Спасибо! Сообщение успешно отправлено.\n\n"
        "⏳ Теперь ожидайте 10 минут."
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())