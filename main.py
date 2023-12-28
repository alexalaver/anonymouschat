from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data import Data
import buttons
import config as cfg
import logging

bot = Bot(token=cfg.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Data("localhost", "5432", "anonymouschat", "alex", "alexpass")
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Register(StatesGroup):
    reg_1 = State()
    reg_2 = State()


#function_search_all
async def search_all_button(message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        if(not db.check_user(user_id)):
            markup = buttons.RegisterGender(types)
            await message.answer(cfg.select_gender_1_text, reply_markup=markup)
            await Register.reg_1.set()
        else:
            if db.check_queue(user_id):
                await message.answer(cfg.search_two_text)
            else:
                if db.get_active_chat(user_id):
                    await message.answer(cfg.have_companion_error)
                else:
                    user_second = db.get_user_queue()
                    cancel_button = buttons.CancelButton(types)
                    if user_second == False:
                        id_queue = db.check_numbers_id_queue()
                        db.add_queue_all(id_queue, user_id)
                        await message.answer(cfg.queue_wait_text, reply_markup=cancel_button)
                    else:
                        db.delete_queue(user_second)
                        id_chats = db.check_numbers_id_chat()
                        db.create_chat_all(id_chats, user_id, user_second)
                        await dp.bot.send_message(chat_id=user_second, text=cfg.companion_right_text, reply_markup=None)
                        await message.answer(cfg.companion_right_text, reply_markup=None)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        await message.delete()
        user_id = message.from_user.id
        if(not db.check_user(user_id)):
            markup = buttons.RegisterGender(types)
            await message.answer(cfg.select_gender_1_text, reply_markup=markup)
            await Register.reg_1.set()
        else:
            markup = buttons.menu_buttons(types)
            await message.answer("TEST", reply_markup=markup)

@dp.callback_query_handler(state=Register.reg_1)
async def reg_1_callback(callback_query: types.CallbackQuery, state: FSMContext):
    markup = buttons.RegisterAge(types)
    if callback_query.data == "select_male_button":
        await state.update_data(gender="male")
        await callback_query.message.edit_text(cfg.select_gender_2_text, reply_markup=markup)
        await Register.reg_2.set()
    elif callback_query.data == "select_female_button":
        await state.update_data(gender="female")
        await callback_query.message.edit_text(cfg.select_gender_2_text, reply_markup=markup)
        await Register.reg_2.set()

@dp.message_handler(state=Register.reg_1)
async def reg_1_text(message: types.Message):
    await message.delete()
    markup = buttons.RegisterGender(types)
    await message.answer(cfg.select_gender_1_text, reply_markup=markup)

@dp.callback_query_handler(state=Register.reg_2)
async def reg_2_callback(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id = db.check_numbers_id()
    id += 1
    gender = data.get("gender")
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name
    username = callback_query.from_user.username
    age = None
    if callback_query.data == "age_12_17":
        age = "12-17"
    elif callback_query.data == "age_18_29":
        age = "18-29"
    elif callback_query.data == "age_30_49":
        age = "30-49"
    elif callback_query.data == "age_50_90":
        age = "50-90"
    db.add_user(id, user_id, first_name, username, gender, age)
    markup = buttons.menu_buttons(types)
    await callback_query.message.delete()
    await callback_query.message.answer(cfg.register_right, reply_markup=markup)
    await state.finish()

@dp.message_handler(state=Register.reg_2)
async def reg_2_text(message: types.Message):
    await message.delete()
    markup = buttons.RegisterAge(types)
    await message.answer(cfg.select_gender_2_text, reply_markup=markup)

@dp.callback_query_handler()
async def all_callback(callback_query: types.CallbackQuery):
    if callback_query.message.chat.type == types.ChatType.PRIVATE:
        if callback_query.data == "test":
            pass
        else:
            await callback_query.message.delete()
            await callback_query.answer(cfg.cannot_use_button, show_alert=True)

@dp.message_handler()
async def text_all(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        if message.text == cfg.search_all_button or message.text == "/search":
            await search_all_button(message)

if __name__ == "__main__":
    executor.start_polling(dp)