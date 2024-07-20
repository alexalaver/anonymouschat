import asyncio
from aiogram import Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import StateFilter, Command, CommandStart
import config as cfg
import app.functions as fnc
from app.functions import FORMSTATE
from bots import bot
import logging

dp = Dispatcher(storage=MemoryStorage())

async def start():
    dp.message.register(fnc.photo_get_buy_tarife_func, StateFilter(FORMSTATE.buy_tarife_1))
    dp.callback_query.register(fnc.reg_1_callback, StateFilter(FORMSTATE.reg_1))
    dp.message.register(fnc.reg_1_text, StateFilter(FORMSTATE.reg_1))
    dp.callback_query.register(fnc.reg_2_callback, StateFilter(FORMSTATE.reg_2))
    dp.callback_query.register(fnc.reg_2_text, StateFilter(FORMSTATE.reg_2))
    dp.message.register(fnc.command_send_all_2, StateFilter(FORMSTATE.command_send_1))
    dp.message.register(fnc.start_command_func, CommandStart())
    dp.message.register(fnc.next_command_func, Command("search", "next"))
    dp.message.register(fnc.next_command_func, F.text == cfg.search_all_button_1)
    dp.message.register(fnc.add_channels_command_func, Command("add"))
    dp.message.register(fnc.get_link_command, Command("get_link"))
    dp.message.register(fnc.command_send_all_1, Command("send"))
    dp.message.register(fnc.search_gender_func, Command("male", "female"))
    dp.message.register(fnc.search_gender_func, F.text.in_([cfg.male_button, cfg.female_button]))
    dp.message.register(fnc.supports_button_func, F.text == cfg.supports_button)
    dp.message.register(fnc.link_command_func, Command("link"))
    # dp.message.register(fnc.send_invoice_handler, Command("donate"))
    dp.pre_checkout_query.register(fnc.pre_checkout_handler)
    dp.message.register(fnc.success_payment_handler, F.successful_payment)
    dp.callback_query.register(fnc.all_callback)
    dp.message.register(fnc.stop_command, Command("stop"))
    dp.message.register(fnc.channels_command, Command("channels"))
    dp.message.register(fnc.stop_command, F.text == cfg.cancel_button)
    dp.message.register(fnc.delete_command, Command("delete"))
    dp.message.register(fnc.text_all)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        logger.exception("Error while running the bot")
