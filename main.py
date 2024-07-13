from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import BotBlocked, ChatNotFound
from data import Data
import buttons
import config as cfg
import logging
import datetime
import other_functions as fnc
import re

bot = Bot(token=cfg.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Data("localhost", "5432", "anonbas", "postgres", "alexman014")
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class FORMSTATE(StatesGroup):
    reg_1 = State()
    reg_2 = State()
    buy_tarife_1 = State()
    supports_1 = State()


##################################### SEARCH ALL FUNCTION

async def search_all_button(message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        if(not db.check_user(user_id)):
            markup = buttons.RegisterGender()
            await message.answer(cfg.select_gender_1_text, reply_markup=markup)
            await FORMSTATE.reg_1.set()
        else:
            if db.check_queue(user_id) or db.check_queue_male(user_id) or db.check_queue_female(user_id):
                await message.answer(cfg.search_two_text)
            else:
                if db.get_active_chat(user_id):
                    await message.answer(cfg.have_companion_error)
                else:
                    channels = db.select_channels()
                    new_channels = []
                    if channels is None:
                        pass
                    else:
                        for channel in channels:
                            if await get_chat_info_and_check_membership(channel, user_id) is True:
                                pass
                            elif await get_chat_info_and_check_membership(channel, user_id) is False:
                                new_channels.append(channel)
                    if new_channels == []:
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
                    else:
                        markup = buttons.MarkupsLink(new_channels)
                        await message.answer(cfg.not_subscribe_channels, reply_markup=markup)


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
                    await FORMSTATE.reg_1.set()
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
            await FORMSTATE.reg_1.set()
        else:
            if db.check_queue(user_id) or db.check_queue_male(user_id) or db.check_queue_female(user_id):
                await message.answer(cfg.search_two_text)
            else:
                channels = db.select_channels()
                new_channels = []
                if channels is None:
                    pass
                else:
                    for channel in channels:
                        if await get_chat_info_and_check_membership(channel, user_id) is True:
                            pass
                        elif await get_chat_info_and_check_membership(channel, user_id) is False:
                            new_channels.append(channel)
                if new_channels == []:
                    if db.get_active_chat(user_id):
                        user_second_right = db.get_active_chat_second(user_id)
                        markup = buttons.menu_buttons()
                        await dp.bot.send_message(chat_id=user_second_right, text=cfg.stop_conversation_second_text, reply_markup=markup)
                        gender = None
                        get_full_chats = db.get_full_chats_info(user_id)
                        if get_full_chats[1] == user_id:
                            gender = get_full_chats[3]
                        else:
                            gender = get_full_chats[4]
                        db.delete_chats(user_id)
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
                                if gender is None:
                                    pass
                                elif user_second_gender == gender:
                                    drop = 3
                                    gender_second = None
                                else:
                                    user_second = False
                        cancel_button = buttons.CancelButton()
                        if user_second == False:
                            if gender == "male":
                                db.add_queue_male(user_id)
                                await message.answer(cfg.queue_wait_man_text, reply_markup=cancel_button)
                            elif gender == "female":
                                db.add_queue_female(user_id)
                                await message.answer(cfg.queue_wait_girl_text, reply_markup=cancel_button)
                            else:
                                db.add_queue_all(user_id)
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
                                    print('right 1')
                                elif drop == 2:
                                    db.delete_queue_female(user_second)
                                    search_gender_second = "female"
                                    print('right 2')
                                elif drop == 1:
                                    db.delete_queue_male(user_second)
                                    search_gender_second = "male"
                                    print('right 3')
                                print('right 4')
                                id_chats = db.check_numbers_id_chat()
                                id_chats += 1
                                db.create_chat_all(id_chats, user_id, user_second, search_gender_first, search_gender_second)
                                await dp.bot.send_message(chat_id=user_second, text=cfg.companion_right_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode=types.ParseMode.MARKDOWN)
                                await message.answer(cfg.companion_right_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode=types.ParseMode.MARKDOWN)
                            except BotBlocked:
                                db.delete_chats(user_id)
                                await message.answer(cfg.message_send_blocked_error)
                else:
                    markup = buttons.MarkupsLink(new_channels)
                    markup_start = buttons.menu_buttons()
                    await message.answer(cfg.stop_conversation_text_error, reply_markup=markup_start)
                    await message.answer(cfg.not_subscribe_channels, reply_markup=markup)
                    if db.get_active_chat(user_id):
                        markup = buttons.menu_buttons()
                        user_second_right = db.get_active_chat_second(user_id)
                        db.delete_chats(user_id)
                        await dp.bot.send_message(chat_id=user_second_right, text=cfg.stop_conversation_second_text, reply_markup=markup)


####################################### NEXT COMMAND FUNC

####################################### SEARCH GENDER FUNC

async def search_gender(message, gender):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        if (not db.check_user(user_id)):
            markup = buttons.RegisterGender()
            await message.answer(cfg.select_gender_1_text, reply_markup=markup)
            await FORMSTATE.reg_1.set()
        else:
            if db.check_queue(user_id) or db.check_queue_male(user_id) or db.check_queue_female(user_id):
                await message.answer(cfg.search_two_text)
            else:
                tarife = db.select_tarife(user_id)
                current_time = datetime.datetime.now()
                if tarife is None:
                    markup = buttons.BuyTarifeButton()
                    await message.answer(cfg.tarife_not_text, reply_markup=markup)
                else:
                    tarife_formatted = datetime.datetime.strptime(tarife, "%Y-%m-%d %H:%M:%S")
                    if current_time >= tarife_formatted:
                        markup = buttons.BuyTarifeButton()
                        await message.answer(cfg.tarife_endend_text, reply_markup=markup)
                        db.update_tarife(user_id, None)
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

####################################### BUTTONS BUY TARIFE

async def buttons_buy_tarife_func(callback_query, state):
    user_id = callback_query.from_user.id
    tarife = db.select_tarife(user_id)
    current_time = datetime.datetime.now()
    markup = buttons.BackButton()
    if tarife is None:
        all_tarife = callback_query.data.split("/")
        sum_tarife = all_tarife[1][:-1]
        day_tarife = all_tarife[0]
        await state.update_data(sum_tarife=sum_tarife, day_tarife=day_tarife)
        await callback_query.message.delete()
        await callback_query.message.answer(cfg.tarife_but_text(sum_tarife, day_tarife), reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
        await FORMSTATE.buy_tarife_1.set()
    else:
        tarife_formatted = datetime.datetime.strptime(tarife, "%Y-%m-%d %H:%M:%S")
        if current_time >= tarife_formatted:
            all_tarife = callback_query.data.split("/")
            sum_tarife = all_tarife[1][:-1]
            day_tarife = all_tarife[0]
            await state.update_data(sum_tarife=sum_tarife, day_tarife=day_tarife)
            await callback_query.message.delete()
            await callback_query.message.answer(cfg.tarife_but_text(sum_tarife, day_tarife), reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            await FORMSTATE.buy_tarife_1.set()
        else:
            await callback_query.answer(cfg.tarife_have_error, show_alert=True)
            await callback_query.message.delete()

async def photo_get_buy_tarife_func(message, state):
    user_id = message.from_user.id
    markup_menu = buttons.menu_buttons()
    if message.text == cfg.back_button:
        await message.answer(cfg.back_text, reply_markup=markup_menu)
        await state.reset_state()
    else:
        if message.photo:
            photo_file_id = message.photo[0].file_id
            data = await state.get_data()
            sum_tarife = data.get("sum_tarife")
            day_tarife = data.get("day_tarife")
            markup = buttons.ConfirmOrderButtons(user_id, sum_tarife, day_tarife)
            await bot.send_photo(cfg.tarife_group_tag, caption=cfg.USER_SEND_PHOTO_TEXT(fnc.nick_with_link("Օգտագործողն", user_id), sum_tarife, day_tarife), photo=photo_file_id, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            await message.answer(cfg.check_screen_right_text, reply_markup=markup_menu)
            await state.finish()
        else:
            await message.answer(cfg.check_screen_error_text)

@dp.message_handler(state=FORMSTATE.buy_tarife_1, content_types=['text', 'photo'])
async def buy_tarife_state(message: types.Message, state: FSMContext):
    await photo_get_buy_tarife_func(message, state)

####################################### BUTTONS BUY TARIFE

async def buttons_accept_and_cancel_func(callback_query):
    buttons_select = callback_query.data.split(":")
    user_order_id = int(buttons_select[1])
    accept_or_cancel = buttons_select[0]
    message_id = callback_query.message.message_id
    if accept_or_cancel == "cancel":
        await bot.edit_message_caption(chat_id=cfg.tarife_group_tag, message_id=message_id, caption=cfg.CANCEL_USER_ORDER(fnc.nick_with_link("օգտագործողի", user_order_id)), reply_markup=None, parse_mode=types.ParseMode.MARKDOWN)
        await bot.send_message(chat_id=user_order_id, text=cfg.cancel_tarife_text)
    elif accept_or_cancel == "confirm":
        sum_tarife = buttons_select[2]
        day_tarife = buttons_select[3]
        tarife_day = None
        if day_tarife == cfg.one_day_tarife_button.split("/")[0]:
            tarife_day = 1
        elif day_tarife == cfg.one_week_tarife_button.split("/")[0]:
            tarife_day = 7
        elif day_tarife == cfg.one_month_tarife_button.split("/")[0]:
            tarife_day = 30
        elif day_tarife == cfg.one_year_tarife_button.split("/")[0]:
            tarife_day = 365
        elif day_tarife == cfg.forever_tarife_button.split("/")[0]:
            tarife_day = 3650
        current_time = datetime.datetime.now()
        time_plus_tarife_days = current_time + datetime.timedelta(days=tarife_day)
        formatted_time = time_plus_tarife_days.strftime("%Y-%m-%d %H:%M:%S")
        db.update_tarife(user_order_id, formatted_time)
        await bot.edit_message_caption(chat_id=cfg.tarife_group_tag, message_id=message_id, caption=cfg.CONFIRM_USER_ORDER(fnc.nick_with_link("օգտագործողի", user_order_id), day_tarife, sum_tarife), reply_markup=None, parse_mode=types.ParseMode.MARKDOWN)
        await bot.send_message(chat_id=user_order_id, text=cfg.CONFIRM_ORDERS_USER_TEXT(sum_tarife, day_tarife), parse_mode=types.ParseMode.MARKDOWN)

#################################### BUTTONS LOGIC ACCEPT AND CANCEL

#################################### SUPPORTS FUNCS

async def supports_button_func(message):
    markup = buttons.HelperButton()
    await message.answer(cfg.supports_button_text, reply_markup=markup)

async def supports_user_send_support_func(message, state):
    user_id = message.from_user.id
    markup = buttons.menu_buttons()
    if message.text == cfg.back_button:
        await message.answer(cfg.back_text, reply_markup=markup)
        await state.finish()
    else:
        if message.text:
            await bot.send_message(cfg.supports_group_tag, f"{cfg.USER_SEND_TASK_TEXT(user=fnc.nick_with_link('Օգտատերը', user_id), user_id=user_id)}\n\n{message.text}", parse_mode=types.ParseMode.MARKDOWN)
            await message.answer(cfg.support_user_send_sup_text, reply_markup=markup)
            await state.finish()
        elif message.photo:
            if message.caption:
                await bot.send_photo(cfg.supports_group_tag, caption=f"{cfg.USER_SEND_TASK_TEXT(user=fnc.nick_with_link('Օգտատերը', user_id), user_id=user_id)}\n\n{message.caption}", photo=message.photo[0].file_id, parse_mode=types.ParseMode.MARKDOWN)
                await message.answer(cfg.support_user_send_sup_text, reply_markup=markup)
                await state.finish()
            else:
                await bot.send_photo(cfg.supports_group_tag, caption=f"{cfg.USER_SEND_TASK_PHOTO_TEXT(user=fnc.nick_with_link('Օգտատերը', user_id), user_id=user_id)}", photo=message.photo[0].file_id, parse_mode=types.ParseMode.MARKDOWN)
                await message.answer(cfg.support_user_send_sup_text, reply_markup=markup)
                await state.finish()
        else:
            await message.answer(cfg.support_user_send_sup_error)

async def supports_send_user_func(message):
    match = None
    if message.reply_to_message.text:
        match = re.search(r'\((.*?)\)', message.reply_to_message.text)
    elif message.reply_to_message.caption:
        match = re.search(r'\((.*?)\)', message.reply_to_message.caption)
    if match:
        user_first_id = match.group(1)
    else:
        user_first_id = None
    if message.text:
        await bot.send_message(user_first_id, cfg.SUPPORT_RIGHT_TEXT(message.text))
        await message.answer(cfg.supports_send_right_text)
    elif message.photo:
        if message.caption:
            await bot.send_photo(user_first_id, caption=cfg.SUPPORT_RIGHT_TEXT_PHOTO(message.caption), photo=message.photo[0].file_id)
            await message.answer(cfg.supports_send_right_text)
        else:
            await bot.send_photo(user_first_id, caption=cfg.SUPPORT_RIGHT_PHOTO_SEND, photo=message.photo[0].file_id)
            await message.answer(cfg.supports_send_right_text)

async def send_command_admin(message):
    message_text = message.text.split(maxsplit=2)
    if len(message_text) > 2:
        if(not db.check_user(int(message_text[1]))):
            pass
        else:
            try:
                await bot.send_message(chat_id=int(message_text[1]), text=cfg.SEND_COMMAND_TEXT(message_text[2]))
                await message.answer(cfg.supports_send_right_text)
            except BotBlocked:
                await message.answer(cfg.send_message_user_support_error)
    else:
        await message.answer(cfg.shablon_send_command)

@dp.message_handler(state=FORMSTATE.supports_1, content_types=['text', 'photo'])
async def user_send_message_support_state(message: types.Message, state: FSMContext):
    await supports_user_send_support_func(message, state)

#################################### SUPPORTS FUNCS

#################################### LINK COMMAND FUNC

async def link_command_func(message):
    user_id = message.from_user.id
    user_second = db.get_active_chat_second(user_id)
    await message.answer(cfg.send_your_link_text_1)
    await bot.send_message(chat_id=user_second, text=cfg.send_your_link_text_2(fnc.nick_with_link("Օգտագործողը", user_id)), parse_mode=types.ParseMode.MARKDOWN)


#################################### LINK COMMAND FUNC

########################## REGISTER IN THE BOT FUNC

@dp.callback_query_handler(state=FORMSTATE.reg_1)
async def reg_1_callback(callback_query: types.CallbackQuery, state: FSMContext):
    markup = buttons.RegisterAge()
    if callback_query.data == "select_male_button":
        await state.update_data(gender="male")
        await callback_query.message.edit_text(cfg.select_gender_2_text, reply_markup=markup)
        await FORMSTATE.reg_2.set()
    elif callback_query.data == "select_female_button":
        await state.update_data(gender="female")
        await callback_query.message.edit_text(cfg.select_gender_2_text, reply_markup=markup)
        await FORMSTATE.reg_2.set()

@dp.message_handler(state=FORMSTATE.reg_1)
async def reg_1_text(message: types.Message):
    await message.delete()
    markup = buttons.RegisterGender()
    await message.answer(cfg.select_gender_1_text, reply_markup=markup)

@dp.callback_query_handler(state=FORMSTATE.reg_2)
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

@dp.message_handler(state=FORMSTATE.reg_2)
async def reg_2_text(message: types.Message):
    await message.delete()
    markup = buttons.RegisterAge()
    await message.answer(cfg.select_gender_2_text, reply_markup=markup)

########################## REGISTER IN THE BOT FUNC

######################### ADD CHANNELS FUNC


async def get_chat_info_and_check_membership(channel_link, user_id):
    try:
        new_link = channel_link.replace("https://t.me/", "").replace("@", "")

        member = await bot.get_chat_member(f"@{new_link}", user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False
    except ChatNotFound:
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

async def add_channels_command_func(message):
    message_text = message.text.split()
    message_id = message.from_user.id
    adminka = db.select_adminka(message_id)
    if adminka == 1:
        if len(message_text) == 2:
            channels = db.select_channels()
            if channels is None:
                channels = []
                channels.append(message_text[1])
                db.add_channels(channels)
                await message.answer(cfg.add_channels_correct_text)
            else:
                channels.append(message_text[1])
                db.update_channels(channels)
                await message.answer(cfg.add_channels_correct_text)
        else:
            await message.answer(cfg.add_channels_incorrect_text)

######################### ADD CHANNELS FUNC

@dp.callback_query_handler()
async def all_callback(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.message.chat.type == types.ChatType.PRIVATE:
        if callback_query.data in cfg.all_tarife_buttons:
            await buttons_buy_tarife_func(callback_query, state)
        else:
            await callback_query.message.delete()
            await callback_query.answer(cfg.cannot_use_button, show_alert=True)
    elif callback_query.message.chat.username == cfg.tarife_group_tag[1:]:
        await buttons_accept_and_cancel_func(callback_query)

@dp.message_handler(content_types=['text', 'photo', 'document', 'video'])
async def text_all(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        if (not db.check_user(user_id)):
            markup = buttons.RegisterGender()
            await message.answer(cfg.select_gender_1_text, reply_markup=markup)
            await FORMSTATE.reg_1.set()
        else:
            user_second = db.get_active_chat_second(user_id)
            if db.check_queue(user_id) or db.check_queue_male(user_id) or db.check_queue_female(user_id):
                if message.text == "/stop" or message.text == cfg.cancel_button:
                    await stop_command(message)
                else:
                    await message.answer(cfg.queue_error_commands)
            elif user_second == False:
                if message.text == cfg.search_all_button or message.text == "/search":
                    await search_all_button(message)
                elif message.text == "/start":
                    await start_command(message)
                elif message.text == "/next":
                    await next_command_func(message)
                elif message.text[:4] == "/add":
                    await add_channels_command_func(message)
                elif message.text == cfg.female_button:
                    await message.answer(cfg.in_job_text)
                    # await search_gender(message, "female")
                elif message.text == cfg.male_button:
                    await message.answer(cfg.in_job_text)
                    # await search_gender(message, "male")
                elif message.text == cfg.supports_button:
                    await supports_button_func(message)
                elif message.text in cfg.have_not_command:
                    await message.answer(cfg.have_not_commands_text)
                else:
                    await message.answer(cfg.command_not_error)
            else:
                try:
                    if message.text:
                        if message.text in cfg.commands_forbid_conversation:
                            await message.answer(cfg.chats_error_commands)
                        elif message.text == "/stop":
                            await stop_command(message)
                        elif message.text == "/next":
                            await next_command_func(message)
                        elif message.text == "/link":
                            await link_command_func(message)
                        elif message.text not in cfg.commands_forbid_conversation:
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
    elif message.chat.username == cfg.supports_group_tag[1:]:
        if message.reply_to_message:
            await supports_send_user_func(message)
        else:
            if message.text.split(maxsplit=2)[0] == "/send":
                await send_command_admin(message)


if __name__ == "__main__":
    executor.start_polling(dp)