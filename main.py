from aiogram import Bot, Dispatcher, types, executor
import buttons
import config as cfg
import logging

bot = Bot(token=cfg.BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        markup = buttons.menu_buttons(types)
        await message.answer("TEST", reply_markup=markup)



if __name__ == "__main__":
    executor.start_polling(dp)