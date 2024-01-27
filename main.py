from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import BotBlocked
from data import Data
import buttons
import config as cfg
import logging

bot = Bot(token=cfg.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Data("192.168.2.140", "5432", "anonymouschat", "anon_user", "anon828282")
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Register(StatesGroup):
    reg_1 = State()
    reg_2 = State()


##################################### SEARCH ALL FUNCTION

async def search_all_button(message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        if(not db.check_user(user_id)):
            markup = buttons.RegisterGender()
            await message.answer(cfg.select_gender_1_text, reply_markup=markup)
            await Register.reg_1.set()
        else:
            if db.check_queue(user_id):
                await message.answer(cfg.search_two_text)
            else:
                if db.get_active_chat(user_id):
                    await message.answer(cfg.have_companion_error)
                else:
                    user_second = False
                    drop = None
                    gender_user = db.select_gender_users(user_id)
                    if gender_user == "male":
                        user_second = db.get_user_queue_male()
                        drop = 1
                    elif gender_user == "female":
                        user_second = db.get_user_queue_female()
                        drop = 2
                    if user_second == False:
                        user_second = db.get_user_queue()
                        drop = 3
                    cancel_button = buttons.CancelButton()
                    if user_second == False:
                        db.add_queue_all(user_id)
                        await message.answer(cfg.queue_wait_text, reply_markup=cancel_button)
                    else:
                        try:
                            search_gender_first = None
                            search_gender_second = None
                            if drop == 3:
                                db.delete_queue(user_second)
                            elif drop == 2:
                                db.delete_queue_female(user_second)
                                search_gender_second = "female"
                            elif drop == 1:
                                db.delete_queue_male(user_second)
                                search_gender_second = "male"
                            id_chats = db.check_numbers_id_chat()
                            id_chats += 1
                            db.create_chat_all(id_chats, user_id, user_second, search_gender_first, search_gender_second)
                            await dp.bot.send_message(chat_id=user_second, text=cfg.companion_right_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode=types.ParseMode.MARKDOWN)
                            await message.answer(cfg.companion_right_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode=types.ParseMode.MARKDOWN)
                        except BotBlocked:
                            db.delete_chats(user_id)
                            await message.answer(cfg.message_send_blocked_error)

##################################### SEARCH ALL FUNCTION

####################################### START COMMAND FUNC

async def start_command(message):
    if message.chat.type == types.ChatType.PRIVATE:
        await message.delete()
        user_id = message.from_user.id
        if db.check_queue(user_id):
            await message.answer(cfg.queue_error_commands)
        else:
            if db.get_active_chat(user_id):
                await message.answer(cfg.chats_error_commands)
            else:
                if(not db.check_user(user_id)):
                    markup = buttons.RegisterGender()
                    await message.answer(cfg.select_gender_1_text, reply_markup=markup)
                    await Register.reg_1.set()
                else:
                    markup = buttons.menu_buttons()
                    await message.answer("TEST", reply_markup=markup)

####################################### START COMMAND FUNC

####################################### STOP COMMAND FUNC

async def stop_command(message):
    if message.chat.type == types.ChatType.PRIVATE:
        await message.delete()
        user_id = message.from_user.id
        user_second = db.get_active_chat_second(user_id)
        if db.check_queue(user_id) or db.check_queue_male(user_id) or db.check_queue_female(user_id):
            markup = buttons.menu_buttons()
            await message.answer(cfg.stop_search_text, reply_markup=markup)
            db.delete_queue_all(user_id)
        elif user_second != False:
            markup = buttons.menu_buttons()
            await message.answer(cfg.stop_conversation_text, reply_markup=markup)
            await dp.bot.send_message(chat_id=user_second, text=cfg.stop_conversation_second_text, reply_markup=markup)
            db.delete_chats(user_id)
        else:
            await message.answer(cfg.error_commands)

####################################### STOP COMMAND FUNC

####################################### NEXT COMMAND FUNC

async def next_command_func(message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        if (not db.check_user(user_id)):
            markup = buttons.RegisterGender()
            await message.answer(cfg.select_gender_1_text, reply_markup=markup)
            await Register.reg_1.set()
        else:
            if db.check_queue(user_id):
                await message.answer(cfg.search_two_text)
            else:
                if db.get_active_chat(user_id):
                    user_second_right = db.get_active_chat_second(user_id)
                    markup = buttons.menu_buttons()
                    await dp.bot.send_message(chat_id=user_second_right, text=cfg.stop_conversation_second_text, reply_markup=markup)
                    db.delete_chats(user_id)
                    gender = db.select_serach_gender(user_id)
                    await message.answer(f"yeees {gender}")
                    user_second = False
                    drop = None
                    gender_second = None
                    user_first_gender = db.select_gender_users(user_id)
                    if gender == "male":
                        user_second = db.get_user_queue_male()
                        if user_second != False:
                            user_second_gender = db.select_gender_users(user_second)
                            if user_second_gender == gender and user_first_gender == "male":
                                drop = 1
                                gender_second = user_second_gender
                            else:
                                user_second = False
                    elif gender == "female":
                        user_second = db.get_user_queue_female()
                        if user_second != False:
                            user_second_gender = db.select_gender_users(user_second)
                            if user_second_gender == gender and user_first_gender == "male":
                                drop = 2
                                gender_second = user_second_gender
                            else:
                                user_second = False
                    if user_second == False:
                        user_second = db.get_user_queue()
                        if user_second == False:
                            pass
                        else:
                            user_second_gender = db.select_gender_users(user_second)
                            if user_second_gender == gender:
                                drop = 3
                                gender_second = None
                            else:
                                user_second = False
                    cancel_button = buttons.CancelButton()
                    if user_second == False:
                        if gender == "male":
                            db.add_queue_male(user_id)
                        elif gender == "female":
                            db.add_queue_female(user_id)
                        await message.answer(cfg.queue_wait_text, reply_markup=cancel_button)
                    else:
                        if drop == 3:
                            db.delete_queue(user_second)
                        elif drop == 2:
                            db.delete_queue_female(user_second)
                        elif drop == 1:
                            db.delete_queue_male(user_second)
                        id_chats = db.check_numbers_id_chat()
                        id_chats += 1
                        db.create_chat_all(id_chats, user_id, user_second, gender, gender_second)
                        await dp.bot.send_message(chat_id=user_second, text=cfg.companion_right_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode=types.ParseMode.MARKDOWN)
                        await message.answer(cfg.companion_right_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode=types.ParseMode.MARKDOWN)
                else:
                    user_second = False
                    drop = None
                    gender_user = db.select_gender_users(user_id)
                    if gender_user == "male":
                        user_second = db.get_user_queue_male()
                        drop = 1
                    elif gender_user == "female":
                        user_second = db.get_user_queue_female()
                        drop = 2
                    if user_second == False:
                        user_second = db.get_user_queue()
                        drop = 3
                    cancel_button = buttons.CancelButton()
                    if user_second == False:
                        db.add_queue_all(user_id)
                        await message.answer(cfg.queue_wait_text, reply_markup=cancel_button)
                    else:
                        try:
                            search_gender_first = None
                            search_gender_second = None
                            if drop == 3:
                                db.delete_queue(user_second)
                            elif drop == 2:
                                db.delete_queue_female(user_second)
                                search_gender_second = "female"
                            elif drop == 1:
                                db.delete_queue_male(user_second)
                                search_gender_second = "male"
                            id_chats = db.check_numbers_id_chat()
                            id_chats += 1
                            db.create_chat_all(id_chats, user_id, user_second, search_gender_first, search_gender_second)
                            await dp.bot.send_message(chat_id=user_second, text=cfg.companion_right_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode=types.ParseMode.MARKDOWN)
                            await message.answer(cfg.companion_right_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode=types.ParseMode.MARKDOWN)
                        except BotBlocked:
                            db.delete_chats(user_id)
                            await message.answer(cfg.message_send_blocked_error)


####################################### NEXT COMMAND FUNC

####################################### SEARCH GENDER FUNC

async def search_gender(message, gender):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        if (not db.check_user(user_id)):
            markup = buttons.RegisterGender()
            await message.answer(cfg.select_gender_1_text, reply_markup=markup)
            await Register.reg_1.set()
        else:
            if db.check_queue(user_id):
                await message.answer(cfg.search_two_text)
            else:
                if db.get_active_chat(user_id):
                    await message.answer(cfg.chats_error_commands)
                else:
                    user_second = False
                    drop = None
                    gender_second = None
                    user_first_gender = db.select_gender_users(user_id)
                    if gender == "male":
                        user_second = db.get_user_queue_male()
                        if user_second != False:
                            user_second_gender = db.select_gender_users(user_second)
                            if user_second_gender == gender and user_first_gender == "male":
                                drop = 1
                                gender_second = user_second_gender
                            else:
                                user_second = False
                    elif gender == "female":
                        user_second = db.get_user_queue_female()
                        if user_second != False:
                            user_second_gender = db.select_gender_users(user_second)
                            if user_second_gender == gender and user_first_gender == "female":
                                drop = 2
                                gender_second = user_second_gender
                            else:
                                user_second = False
                    if user_second == False:
                        user_second = db.get_user_queue()
                        if user_second == False:
                            pass
                        else:
                            user_second_gender = db.select_gender_users(user_second)
                            if user_second_gender == gender:
                                drop = 3
                                gender_second = None
                            else:
                                user_second = False
                    cancel_button = buttons.CancelButton()
                    if user_second == False:
                        if gender == "male":
                            db.add_queue_male(user_id)
                        elif gender == "female":
                            db.add_queue_female(user_id)
                        await message.answer(cfg.queue_wait_text, reply_markup=cancel_button)
                    else:
                        if drop == 3:
                            db.delete_queue(user_second)
                        elif drop == 2:
                            db.delete_queue_female(user_second)
                        elif drop == 1:
                            db.delete_queue_male(user_second)
                        id_chats = db.check_numbers_id_chat()
                        id_chats += 1
                        db.create_chat_all(id_chats, user_id, user_second, gender, gender_second)
                        await dp.bot.send_message(chat_id=user_second, text=cfg.companion_right_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode=types.ParseMode.MARKDOWN)
                        await message.answer(cfg.companion_right_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode=types.ParseMode.MARKDOWN)

####################################### SEARCH GENDER FUNC

########################## REGISTER IN THE BOT FUNC

@dp.callback_query_handler(state=Register.reg_1)
async def reg_1_callback(callback_query: types.CallbackQuery, state: FSMContext):
    markup = buttons.RegisterAge()
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
    markup = buttons.RegisterGender()
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
    markup = buttons.menu_buttons()
    await callback_query.message.delete()
    await callback_query.message.answer(cfg.register_right, reply_markup=markup)
    await state.finish()

@dp.message_handler(state=Register.reg_2)
async def reg_2_text(message: types.Message):
    await message.delete()
    markup = buttons.RegisterAge()
    await message.answer(cfg.select_gender_2_text, reply_markup=markup)

########################## REGISTER IN THE BOT FUNC

@dp.callback_query_handler()
async def all_callback(callback_query: types.CallbackQuery):
    if callback_query.message.chat.type == types.ChatType.PRIVATE:
        if callback_query.data == "test":
            pass
        else:
            await callback_query.message.delete()
            await callback_query.answer(cfg.cannot_use_button, show_alert=True)

@dp.message_handler(content_types=['text', 'photo', 'document', 'video'])
async def text_all(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        if (not db.check_user(user_id)):
            markup = buttons.RegisterGender()
            await message.answer(cfg.select_gender_1_text, reply_markup=markup)
            await Register.reg_1.set()
        else:
            user_second = db.get_active_chat_second(user_id)
            if user_second == False:
                if message.text == cfg.search_all_button or message.text == "/search":
                    await search_all_button(message)
                elif message.text == "/start":
                    await start_command(message)
                elif message.text == "/stop" or message.text == cfg.cancel_button:
                    await stop_command(message)
                elif message.text == "/next":
                    await next_command_func(message)
                elif message.text == cfg.female_button:
                    await search_gender(message, "female")
                elif message.text == cfg.male_button:
                    await search_gender(message, "male")
                elif message.text in cfg.have_not_command:
                    await message.answer(cfg.have_not_commands_text)
                else:
                    await message.answer(cfg.command_not_error)
            else:
                try:
                    if message.text:
                        if message.text in cfg.all_commands:
                            await message.answer(cfg.chats_error_commands)
                        elif message.text == "/stop":
                            await stop_command(message)
                        elif message.text == "/next":
                            await next_command_func(message)
                        elif message.text not in cfg.all_commands:
                            await dp.bot.send_message(chat_id=user_second, text=message.text)
                    elif message.photo:
                        if message.caption:
                            await dp.bot.send_photo(chat_id=user_second, photo=message.photo[-1].file_id, caption=message.caption)
                        else:
                            await dp.bot.send_photo(chat_id=user_second, photo=message.photo[-1].file_id)
                    elif message.video:
                        if message.caption:
                            await dp.bot.send_photo(chat_id=user_second, photo=message.video.file_id, caption=message.caption)
                        else:
                            await dp.bot.send_photo(chat_id=user_second, photo=message.video.file_id)
                    else:
                        await message.answer(cfg.message_send_second_error)
                except BotBlocked:
                    db.delete_chats(user_id)
                    markup = buttons.menu_buttons()
                    await message.answer(cfg.message_send_blocked_error, reply_markup=markup)
                except Exception as err:
                    print(f"[Ошибка при отправки сообщения] {err}")
                    await message.answer(cfg.message_send_error)

if __name__ == "__main__":
    executor.start_polling(dp)