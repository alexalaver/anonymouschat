from aiogram import types, enums, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
import asyncio
from data import Data
from bots import bot
import buttons
import config as cfg
import datetime
import other_functions as fnc
import random
import string

router = Router()

class FORMSTATE(StatesGroup):
    reg_1 = State()
    reg_2 = State()
    buy_tarife_1 = State()
    supports_1 = State()
    command_send_1 = State()

db = Data("localhost", "5432", "anonbas", "postgres", "alexman014")


##################################### SEARCH ALL FUNCTION

# async def search_all_button(message, state):
#     if message.chat.type == enums.ChatType.PRIVATE:
#         user_id = message.from_user.id
#         if(not db.check_user(user_id)):
#             markup = buttons.RegisterGender()
#             await message.answer(cfg.select_gender_1_text, reply_markup=markup)
#             await state.set_state(FORMSTATE.reg_1)
#         else:
#             if db.check_queue(user_id) or db.check_queue_male(user_id) or db.check_queue_female(user_id):
#                 await message.answer(cfg.search_two_text)
#             else:
#                 if db.get_active_chat(user_id):
#                     await message.answer(cfg.have_companion_error)
#                 else:
#                     channels = db.select_channels()
#                     new_channels = []
#                     if channels is None:
#                         pass
#                     else:
#                         for channel in channels:
#                             if await get_chat_info_and_check_membership(channel, user_id) is True:
#                                 pass
#                             elif await get_chat_info_and_check_membership(channel, user_id) is False:
#                                 new_channels.append(channel)
#                     if new_channels == []:
#                         user_second = False
#                         drop = None
#                         gender_user = db.select_gender_users(user_id)
#                         if gender_user == "male":
#                             user_second = db.get_user_queue_male()
#                             drop = 1
#                         elif gender_user == "female":
#                             user_second = db.get_user_queue_female()
#                             drop = 2
#                         if user_second == False:
#                             user_second = db.get_user_queue()
#                             drop = 3
#                         cancel_button = buttons.CancelButton()
#                         if user_second == False:
#                             db.add_queue_all(user_id)
#                             await message.answer(cfg.queue_wait_text, reply_markup=cancel_button)
#                         else:
#                             try:
#                                 search_gender_first = None
#                                 search_gender_second = None
#                                 if drop == 3:
#                                     db.delete_queue(user_second)
#                                 elif drop == 2:
#                                     db.delete_queue_female(user_second)
#                                     search_gender_second = "female"
#                                 elif drop == 1:
#                                     db.delete_queue_male(user_second)
#                                     search_gender_second = "male"
#                                 id_chats = db.check_numbers_id_chat()
#                                 id_chats += 1
#                                 characters = string.ascii_letters + string.digits
#                                 random_id = ''.join(random.choice(characters) for _ in range(16))
#                                 db.create_chat_all(id_chats, user_id, user_second, search_gender_first, search_gender_second, random_id)
#                                 await bot.send_message(chat_id=user_second, text=cfg.companion_right_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode=enums.ParseMode.MARKDOWN)
#                                 await message.answer(cfg.companion_right_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode=enums.ParseMode.MARKDOWN)
#                             except TelegramForbiddenError:
#                                 db.delete_chats(user_id)
#                                 await message.answer(cfg.message_send_blocked_error)
#                     else:
#                         markup = buttons.MarkupsLink(new_channels)
#                         await message.answer(cfg.not_subscribe_channels, reply_markup=markup)


##################################### SEARCH ALL FUNCTION

####################################### START COMMAND FUNC

async def start_command_func(message: types.Message, state: types.Message):
    if message.chat.type == enums.ChatType.PRIVATE:
        await message.delete()
        user_id = message.from_user.id
        if db.get_active_chat(user_id):
            await message.answer(cfg.chats_error_commands)
        elif db.check_queue(user_id) or db.check_queue_male(user_id) or db.check_queue_female(user_id):
            await message.answer(cfg.search_two_text)
        else:
            if(not db.check_user(user_id)):
                markup = buttons.RegisterGender()
                await message.answer(cfg.select_gender_1_text, reply_markup=markup)
                await state.set_state(FORMSTATE.reg_1)
            else:
                markup = buttons.menu_buttons()
                await message.answer(cfg.start_text, reply_markup=markup)

####################################### START COMMAND FUNC

####################################### REGISTER BUTTON

async def reg_1_callback(callback_query: types.CallbackQuery, state: FSMContext):
    markup = buttons.RegisterAge()
    if callback_query.data == "select_male_button":
        await state.update_data(gender="male")
        await callback_query.message.edit_text(cfg.select_gender_2_text, reply_markup=markup)
        await state.set_state(FORMSTATE.reg_2)
    elif callback_query.data == "select_female_button":
        await state.update_data(gender="female")
        await callback_query.message.edit_text(cfg.select_gender_2_text, reply_markup=markup)
        await state.set_state(FORMSTATE.reg_2)

async def reg_1_text(message: types.Message):
    await message.delete()
    markup = buttons.RegisterGender()
    await message.answer(cfg.select_gender_1_text, reply_markup=markup)

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
    db.add_user(id, user_id, first_name.encode('utf-8'), username.encode('utf-8'), gender, age)
    markup = buttons.menu_buttons()
    await callback_query.message.delete()
    await callback_query.message.answer(cfg.register_right, reply_markup=markup)
    await state.clear()

async def reg_2_text(message: types.Message):
    await message.delete()
    markup = buttons.RegisterAge()
    await message.answer(cfg.select_gender_2_text, reply_markup=markup)

####################################### REGISTER BUTTON




####################################### STOP COMMAND FUNC

async def stop_command(message: types.Message):
    if message.chat.type == enums.ChatType.PRIVATE:
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
            await bot.send_message(chat_id=user_second, text=cfg.stop_conversation_second_text, reply_markup=markup)
            db.delete_chats(user_id)
        else:
            await message.answer(cfg.error_commands)

####################################### STOP COMMAND FUNC

####################################### NEXT COMMAND FUNC

async def next_command_func(message: types.Message, state: FSMContext):
    if message.chat.type == enums.ChatType.PRIVATE:
        user_id = message.from_user.id
        if (not db.check_user(user_id)):
            markup = buttons.RegisterGender()
            await message.answer(cfg.select_gender_1_text, reply_markup=markup)
            await state.set_state(FORMSTATE.reg_1)
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
                        await bot.send_message(chat_id=user_second_right, text=cfg.stop_conversation_second_text, reply_markup=markup)
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
                            db.delete_queue_all(user_second)
                            id_chats = db.check_numbers_id_chat()
                            id_chats += 1
                            characters = string.ascii_letters + string.digits
                            random_id = ''.join(random.choice(characters) for _ in range(16))
                            db.create_chat_all(id_chats, user_id, user_second, gender, gender_second, random_id)
                            await bot.send_message(chat_id=user_second, text=cfg.companion_right_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode=enums.ParseMode.MARKDOWN)
                            await message.answer(cfg.companion_right_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode=enums.ParseMode.MARKDOWN)
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
                                characters = string.ascii_letters + string.digits
                                random_id = ''.join(random.choice(characters) for _ in range(16))
                                db.create_chat_all(id_chats, user_id, user_second, search_gender_first, search_gender_second, random_id)
                                await bot.send_message(chat_id=user_second, text=cfg.companion_right_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode=enums.ParseMode.MARKDOWN)
                                await message.answer(cfg.companion_right_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode=enums.ParseMode.MARKDOWN)
                            except TelegramForbiddenError:
                                db.delete_chats(user_id)
                                await message.answer(cfg.message_send_blocked_error)
                else:
                    markup = buttons.MarkupsLink(new_channels)
                    markup_start = buttons.menu_buttons()
                    if db.get_active_chat(user_id):
                        markup = buttons.menu_buttons()
                        user_second_right = db.get_active_chat_second(user_id)
                        db.delete_chats(user_id)
                        await message.answer(cfg.stop_conversation_text_error, reply_markup=markup_start)
                        await bot.send_message(chat_id=user_second_right, text=cfg.stop_conversation_second_text, reply_markup=markup)
                    await message.answer(cfg.not_subscribe_channels, reply_markup=markup)



####################################### NEXT COMMAND FUNC

####################################### SEARCH GENDER FUNC

async def search_gender_func(message: types.Message, state: FSMContext):
    if message.chat.type == enums.ChatType.PRIVATE:
        gender = None
        if message.text == "male" or message.text == cfg.male_button:
            gender = "male"
        elif message.text == "female" or message.text == cfg.female_button:
            gender = "female"
        user_id = message.from_user.id
        await bot.send_message(chat_id=cfg.logs_group, text=f"{fnc.nick_with_link('USER', user_id)} ENTER {gender} BUTTON", parse_mode=enums.ParseMode.MARKDOWN)
        if (not db.check_user(user_id)):
            markup = buttons.RegisterGender()
            await message.answer(cfg.select_gender_1_text, reply_markup=markup)
            await state.set_state(FORMSTATE.reg_1)
        else:
            if db.get_active_chat(user_id):
                await message.answer(cfg.chats_error_commands)
            elif db.check_queue(user_id) or db.check_queue_male(user_id) or db.check_queue_female(user_id):
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
                                characters = string.ascii_letters + string.digits
                                random_id = ''.join(random.choice(characters) for _ in range(16))
                                db.create_chat_all(id_chats, user_id, user_second, gender, gender_second, random_id)
                                await bot.send_message(chat_id=user_second, text=cfg.companion_right_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode=enums.ParseMode.MARKDOWN)
                                await message.answer(cfg.companion_right_text, reply_markup=types.ReplyKeyboardRemove(), parse_mode=enums.ParseMode.MARKDOWN)

####################################### SEARCH GENDER FUNC

####################################### BUTTONS BUY TARIFE

# async def buttons_buy_tarife_func(callback_query: types.CallbackQuery):
#     user_id = callback_query.from_user.id
#     tarife = db.select_tarife(user_id)
#     current_time = datetime.datetime.now()
#     markup = buttons.BackButton()
#     if tarife is None:
#         all_tarife = callback_query.data.split("/")
#         sum_tarife = all_tarife[1][:-1]
#         day_tarife = all_tarife[0]
#         await state.update_data(sum_tarife=sum_tarife, day_tarife=day_tarife)
#         await callback_query.message.delete()
#         await callback_query.message.answer(cfg.tarife_but_text(sum_tarife, day_tarife), reply_markup=markup, parse_mode=enums.ParseMode.MARKDOWN)
#         await state.set_state(FORMSTATE.buy_tarife_1)
#     else:
#         tarife_formatted = datetime.datetime.strptime(tarife, "%Y-%m-%d %H:%M:%S")
#         if current_time >= tarife_formatted:
#             all_tarife = callback_query.data.split("/")
#             sum_tarife = all_tarife[1][:-1]
#             day_tarife = all_tarife[0]
#             await state.update_data(sum_tarife=sum_tarife, day_tarife=day_tarife)
#             await callback_query.message.delete()
#             await callback_query.message.answer(cfg.tarife_but_text(sum_tarife, day_tarife), reply_markup=markup, parse_mode=enums.ParseMode.MARKDOWN)
#             await state.set_state(FORMSTATE.buy_tarife_1)
#         else:
#             await callback_query.answer(cfg.tarife_have_error, show_alert=True)
#             await callback_query.message.delete()

async def photo_get_buy_tarife_func(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    markup_menu = buttons.menu_buttons()
    if message.text == cfg.back_button:
        await message.answer(cfg.back_text, reply_markup=markup_menu)
        await state.clear()
    else:
        if message.photo:
            photo_file_id = message.photo[0].file_id
            data = await state.get_data()
            sum_tarife = data.get("sum_tarife")
            day_tarife = data.get("day_tarife")
            markup = buttons.ConfirmOrderButtons(user_id, sum_tarife, day_tarife)
            await bot.send_photo(cfg.tarife_group_tag, caption=cfg.USER_SEND_PHOTO_TEXT(fnc.nick_with_link("Օգտագործողն", user_id), sum_tarife, day_tarife), photo=photo_file_id, reply_markup=markup, parse_mode=enums.ParseMode.MARKDOWN)
            await message.answer(cfg.check_screen_right_text, reply_markup=markup_menu)
            await state.clear()
        else:
            await message.answer(cfg.check_screen_error_text)


async def buttons_accept_and_cancel_func(callback_query):
    buttons_select = callback_query.data.split(":")
    user_order_id = int(buttons_select[1])
    accept_or_cancel = buttons_select[0]
    message_id = callback_query.message.message_id
    if accept_or_cancel == "cancel":
        await bot.edit_message_caption(chat_id=cfg.tarife_group_tag, message_id=message_id, caption=cfg.CANCEL_USER_ORDER(fnc.nick_with_link("օգտագործողի", user_order_id)), reply_markup=None, parse_mode=enums.ParseMode.MARKDOWN)
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
        await bot.edit_message_caption(chat_id=cfg.tarife_group_tag, message_id=message_id, caption=cfg.CONFIRM_USER_ORDER(fnc.nick_with_link("օգտագործողի", user_order_id), day_tarife, sum_tarife), reply_markup=None, parse_mode=enums.ParseMode.MARKDOWN)
        await bot.send_message(chat_id=user_order_id, text=cfg.CONFIRM_ORDERS_USER_TEXT(sum_tarife, day_tarife), parse_mode=enums.ParseMode.MARKDOWN)

async def all_callback(callback_query: types.CallbackQuery):
    if callback_query.message.chat.type == enums.ChatType.PRIVATE:
        if callback_query.data in cfg.all_tarife_buttons:
            await callback_query.message.delete()
            tarife_count = None
            dram = None
            dollar = None
            if callback_query.data == cfg.one_day_tarife_button:
                tarife_count = 75
                dram = 750
                dollar = 1.89
            elif callback_query.data == cfg.one_week_tarife_button:
                tarife_count = 100
                dram = 2400
                dollar = 2.39
            elif callback_query.data == cfg.one_month_tarife_button:
                tarife_count = 350
                dram = 3400
                dollar = 8.49
            elif callback_query.data == cfg.one_year_tarife_button:
                tarife_count = 1000
                dram = 9300
                dollar = 23.99
            elif callback_query.data == cfg.forever_tarife_button:
                tarife_count = 2500
                dram = 24000
                dollar = 60.99
            prices = [types.LabeledPrice(label="XTR", amount=tarife_count)]
            await callback_query.message.answer_invoice(
                title="💎 VIP статус",
                description=cfg.vip_descreption(),
                prices=prices,
                provider_token="",
                payload="channel_support",
                currency="XTR",
                reply_markup=buttons.VIPDonateButton(dram, dollar, tarife_count),
            )
        elif callback_query.data == "back_from_vip":
            markup = buttons.BuyTarifeButton()
            await callback_query.message.delete()
            await callback_query.message.answer(cfg.tarife_not_text, reply_markup=markup)
        else:
            await callback_query.message.delete()
            await callback_query.answer(cfg.cannot_use_button, show_alert=True)
    elif callback_query.message.chat.username == cfg.tarife_group_tag[1:]:
        await buttons_accept_and_cancel_func(callback_query)

#################################### BUTTONS LOGIC ACCEPT AND CANCEL

#################################### SUPPORTS FUNCS

async def supports_button_func(message: types.Message):
    if message.chat.type == enums.ChatType.PRIVATE:
        markup = buttons.HelperButton()
        user_id = message.from_user.id
        if db.get_active_chat(user_id):
            await message.answer(cfg.chats_error_commands)
        elif db.check_queue(user_id) or db.check_queue_male(user_id) or db.check_queue_female(user_id):
            await message.answer(cfg.error_search)
        else:
            await message.answer(cfg.supports_button_text, reply_markup=markup)


#################################### SUPPORTS FUNCS

#################################### LINK COMMAND FUNC

async def link_command_func(message: types.Message):
    if message.chat.type == enums.ChatType.PRIVATE:
        user_id = message.from_user.id
        if db.get_active_chat(user_id):
            user_second = db.get_active_chat_second(user_id)
            await message.answer(cfg.send_your_link_text_1)
            await bot.send_message(chat_id=user_second, text=cfg.send_your_link_text_2(fnc.nick_with_link("Օգտագործողը", user_id)), parse_mode=enums.ParseMode.MARKDOWN)
        elif db.check_queue(user_id) or db.check_queue_male(user_id) or db.check_queue_female(user_id):
            await message.answer(cfg.error_search)
        else:
            await message.answer(cfg.link_in_search)


#################################### LINK COMMAND FUNC

######################### ADD CHANNELS FUNC


async def get_chat_info_and_check_membership(channel_link, user_id):
    try:
        new_link = channel_link.replace("https://t.me/", "").replace("@", "")

        member = await bot.get_chat_member(f"@{new_link}", user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False
    except TelegramBadRequest:
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

async def add_channels_command_func(message: types.Message):
    if message.chat.type == enums.ChatType.PRIVATE:
        message_text = message.text.split()
        message_id = message.from_user.id
        adminka = db.select_adminka(message_id)
        if db.get_active_chat(message_id):
            await message.answer(cfg.chats_error_commands)
        elif db.check_queue(message_id) or db.check_queue_male(message_id) or db.check_queue_female(message_id):
            await message.answer(cfg.search_two_text)
        else:
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

########################## COMMAND SEND

async def command_send_all_1(message: types.Message, state: FSMContext):
    if message.chat.type == enums.ChatType.PRIVATE:
        user_id = message.from_user.id
        if db.get_active_chat(user_id):
            await message.answer(cfg.chats_error_commands)
        elif db.check_queue(user_id) or db.check_queue_male(user_id) or db.check_queue_female(user_id):
            await message.answer(cfg.search_two_text)
        else:
            if db.select_adminka(user_id) == 1:
                await state.set_state(FORMSTATE.command_send_1)
                markup = buttons.BackButton()
                await message.answer(cfg.command_send_1_text, reply_markup=markup)

async def command_send_all_2(message: types.Message, state: FSMContext):
    if message.text == cfg.back_button:
        markup = buttons.menu_buttons()
        await message.answer(cfg.back_text, reply_markup=markup)
        await state.clear()
    else:
        markup = buttons.menu_buttons()
        await state.clear()
        users = db.select_all_id()
        user_send = 0
        for user in users:
            try:
                await bot.send_message(chat_id=user, text=f"{message.text}")
                user_send += 1
            except Exception as err:
                pass
            await asyncio.sleep(1)

        await message.answer(cfg.command_send_2_text(user_send), reply_markup=markup)


########################## COMMAND SEND

############################# GET LINK COMMAND

async def get_link_command(message: types.Message):
    if message.chat.type == enums.ChatType.PRIVATE:
        user_id = message.from_user.id
        adminka = db.select_adminka(user_id)
        if db.get_active_chat(user_id):
            await message.answer(cfg.chats_error_commands)
        elif db.check_queue(user_id) or db.check_queue_male(user_id) or db.check_queue_female(user_id):
            await message.answer(cfg.search_two_text)
        else:
            if adminka == 1:
                message_text = message.text.split()
                if len(message_text) == 2:
                    await message.answer(text=f"{cfg.link_user_text} - {fnc.nick_with_link('LINK', message_text[1])}", parse_mode=enums.ParseMode.MARKDOWN)

############################# GET LINK COMMAND


############################## CHANNELS COMMAND

async def channels_command(message: types.Message):
    if message.chat.type == enums.ChatType.PRIVATE:
        user_id = message.from_user.id
        adminka = db.select_adminka(user_id)
        if db.get_active_chat(user_id):
            await message.answer(cfg.chats_error_commands)
        elif db.check_queue(user_id) or db.check_queue_male(user_id) or db.check_queue_female(user_id):
            await message.answer(cfg.search_two_text)
        else:
            if adminka == 1:
                channels = db.select_channels()
                if channels is None or channels == []:
                    await message.answer(cfg.channels_not_Text)
                else:
                    num = 1
                    channels_text = cfg.channels_text
                    for channel in channels:
                        channels_text = channels_text + f"\n{num}. {channel}"
                        num += 1
                    await message.answer(channels_text)

############################## CHANNELS COMMAND

############################## DELETE COMMAND

async def delete_command(message: types.Message):
    if message.chat.type == enums.ChatType.PRIVATE:
        user_id = message.from_user.id
        adminka = db.select_adminka(user_id)
        if db.get_active_chat(user_id):
            await message.answer(cfg.chats_error_commands)
        elif db.check_queue(user_id) or db.check_queue_male(user_id) or db.check_queue_female(user_id):
            await message.answer(cfg.search_two_text)
        else:
            if adminka == 1:
                try:
                    message_text = message.text.split()
                    message_num = int(message_text[1])
                    channels = db.select_channels()
                    if channels is None:
                        await message.answer(cfg.channels_not_Text)
                    else:
                        try:
                            chan_delete = channels[message_num - 1]
                            new_channels = [item for item in channels if item != chan_delete]
                            db.update_channels(new_channels)
                            await message.answer(cfg.correct_delete_text)
                        except (IndexError, TypeError):
                            await message.answer(cfg.error_delete_text)
                except ValueError:
                    await message.answer(cfg.error_delete_text)


############################## DELETE COMMAND


######################## DONATE FUNC

async def pre_checkout_handler(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

async def success_payment_handler(message: types.Message):
    successful_payment = message.successful_payment
    total_amount = successful_payment.total_amount
    tarife_day = None
    dram = None
    if total_amount == 75:
        tarife_day = 1
        dram = 750
    elif total_amount == 100:
        tarife_day = 7
        dram = 2400
    elif total_amount == 350:
        tarife_day = 30
        dram = 3400
    elif total_amount == 1000:
        tarife_day = 365
        dram = 9300
    elif total_amount == 2500:
        tarife_day = 3650
        dram = 24000
    current_time = datetime.datetime.now()
    time_plus_tarife_days = current_time + datetime.timedelta(days=tarife_day)
    formatted_time = time_plus_tarife_days.strftime("%Y-%m-%d %H:%M:%S")
    db.update_tarife(message.from_user.id, formatted_time)
    await bot.send_message(chat_id=message.from_user.id, text=cfg.CONFIRM_ORDERS_USER_TEXT(dram, tarife_day), parse_mode=enums.ParseMode.MARKDOWN)
    await bot.send_message(chat_id=cfg.logs_group, text=f"{fnc.nick_with_link('USER', message.from_user.id)} CORRECT BUY VIP", parse_mode=enums.ParseMode.MARKDOWN)

######################## DONATE FUNC

################### TEXT ALL

async def text_all(message: types.Message, state: FSMContext):
    if message.chat.type == enums.ChatType.PRIVATE:
        user_id = message.from_user.id
        if (not db.check_user(user_id)):
            markup = buttons.RegisterGender()
            await message.answer(cfg.select_gender_1_text, reply_markup=markup)
            await state.set_state(FORMSTATE.reg_1)
        else:
            user_second = db.get_active_chat_second(user_id)
            if db.check_queue(user_id) or db.check_queue_male(user_id) or db.check_queue_female(user_id):
                await message.answer(cfg.queue_error_commands)
            elif user_second == False:
                await message.answer(cfg.command_not_error)
            else:
                try:
                    if message.text:
                        if message.text not in cfg.commands_forbid_conversation:
                            if "https" in message.text or "http" in message.text or message.text[:4] == "t.me":
                                pass
                            elif message.text[0] == "@":
                                await message.answer(cfg.error_tag_text)
                            else:
                                await bot.send_message(chat_id=user_second, text=message.text)
                                channel_message_text = db.get_active_chat_all(user_id)
                                channel_mes_text = f"ID чата: {channel_message_text[0]}\nИдентификатор чата: {channel_message_text[5]}\nПользователь 1: {channel_message_text[1]}\nПользователь 2: {channel_message_text[2]}\nОтправил сообщение: {user_id}\n\n{message.text}"
                                await bot.send_message(chat_id=cfg.channel_messages, text=channel_mes_text)
                    elif message.photo:
                        if message.caption:
                            if "https" in message.caption or "http" in message.caption or message.caption[:4] == "t.me":
                                pass
                            elif message.caption[0] == "@":
                                await message.answer(cfg.error_tag_text)
                            else:
                                await bot.send_photo(chat_id=user_second, photo=message.photo[-1].file_id, caption=message.caption)
                                channel_message_text = db.get_active_chat_all(user_id)
                                channel_mes_text = f"ID чата: {channel_message_text[0]}\nИдентификатор чата: {channel_message_text[5]}\nПользователь 1: {channel_message_text[1]}\nПользователь 2: {channel_message_text[2]}\nОтправил сообщение: {user_id}\n\n{message.caption}"
                                await bot.send_photo(chat_id=cfg.channel_messages, photo=message.photo[-1].file_id, caption=channel_mes_text)
                        else:
                            await bot.send_photo(chat_id=user_second, photo=message.photo[-1].file_id)
                            channel_message_text = db.get_active_chat_all(user_id)
                            channel_mes_text = f"ID чата: {channel_message_text[0]}\nИдентификатор чата: {channel_message_text[5]}\nПользователь 1: {channel_message_text[1]}\nПользователь 2: {channel_message_text[2]}\nОтправил сообщение: {user_id}"
                            await bot.send_photo(chat_id=cfg.channel_messages, photo=message.photo[-1].file_id, caption=channel_mes_text)
                    elif message.video:
                        if message.caption:
                            if message.caption:
                                if "https" in message.caption or "http" in message.caption or message.caption[:4] == "t.me":
                                    pass
                                elif message.caption[0] == "@":
                                    await message.answer(cfg.error_tag_text)
                                else:
                                    await bot.send_photo(chat_id=user_second, photo=message.video.file_id, caption=message.caption)
                        else:
                            await bot.send_photo(chat_id=user_second, photo=message.video.file_id)
                            channel_message_text = db.get_active_chat_all(user_id)
                            channel_mes_text = f"ID чата: {channel_message_text[0]}\nИдентификатор чата: {channel_message_text[5]}\nПользователь 1: {channel_message_text[1]}\nПользователь 2: {channel_message_text[2]}\nОтправил сообщение: {user_id}\n\n"
                            await bot.send_photo(chat_id=cfg.channel_messages, photo=message.video.file_id, caption=channel_mes_text)
                    elif message.sticker:
                        await bot.send_sticker(chat_id=user_second, sticker=message.sticker.file_id)
                    else:
                        await message.answer(cfg.message_send_second_error)
                except TelegramForbiddenError:
                    db.delete_chats(user_id)
                    markup = buttons.menu_buttons()
                    await message.answer(cfg.message_send_blocked_error, reply_markup=markup)
                except Exception as err:
                    print(f"[Ошибка при отправки сообщения] {err}")
                    await message.answer(cfg.message_send_error)

################### TEXT ALL
