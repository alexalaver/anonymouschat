from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import logging

API_TOKEN = '6891045575:AAGk-IohsqKzTp0NDMR8EG9Yh9p24_KXFKg'
PAYMENTS_PROVIDER_TOKEN = '1877036958:TEST:c26344b9315b34d70d492f0968e3455564844eee'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start', 'buy'])
async def send_welcome(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("Премиум 1 месяц", callback_data="buy_1_month"),
               InlineKeyboardButton("Премиум 3 месяца", callback_data="buy_3_months"),
               InlineKeyboardButton("Премиум 6 месяцев", callback_data="buy_6_months"),
               InlineKeyboardButton("Премиум 1 год", callback_data="buy_1_year"))

    await message.reply("Выберите подписку, которую хотите приобрести:", reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data.startswith('buy_'))
async def process_callback(callback_query: types.CallbackQuery):
    prices = []
    title = ""
    description = ""

    if callback_query.data == "buy_1_month":
        prices = [LabeledPrice(label='Премиум подписка - 1 месяц', amount=500)]  # 500 units = 5.00 USD
        title = "Премиум подписка - 1 месяц"
        description = "1 месяц премиум подписки вашего бота"
    elif callback_query.data == "buy_3_months":
        prices = [LabeledPrice(label='Премиум подписка - 3 месяца', amount=1400)]  # 1400 units = 14.00 USD
        title = "Премиум подписка - 3 месяца"
        description = "3 месяца премиум подписки вашего бота"
    elif callback_query.data == "buy_6_months":
        prices = [LabeledPrice(label='Премиум подписка - 6 месяцев', amount=2700)]  # 2700 units = 27.00 USD
        title = "Премиум подписка - 6 месяцев"
        description = "6 месяцев премиум подписки вашего бота"
    elif callback_query.data == "buy_1_year":
        prices = [LabeledPrice(label='Премиум подписка - 1 год', amount=5000)]  # 5000 units = 50.00 USD
        title = "Премиум подписка - 1 год"
        description = "1 год премиум подписки вашего бота"

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=f"Вы выбрали {title}. Нажмите кнопку ниже для оплаты.",
        reply_markup=None
    )

    await bot.send_invoice(
        callback_query.from_user.id,
        title=title,
        description=description,
        provider_token=PAYMENTS_PROVIDER_TOKEN,
        currency="USD",
        prices=prices,
        start_parameter="premium-subscription",
        payload=callback_query.data
    )


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    await message.reply("Спасибо за покупку! Ваша премиум подписка активирована.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
