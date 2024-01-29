import config as cfg
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

def menu_buttons():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(cfg.search_all_button)
    markup.row(cfg.male_button, cfg.female_button)
    markup.add(cfg.supports_button)
    return markup

def RegisterGender():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text=cfg.select_male_button, callback_data="select_male_button"),
        InlineKeyboardButton(text=cfg.select_female_button, callback_data="select_female_button")
    )
    return markup

def RegisterAge():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text=cfg.age_12_17, callback_data="age_12_17"),
        InlineKeyboardButton(text=cfg.age_18_29, callback_data="age_18_29"),
        InlineKeyboardButton(text=cfg.age_30_49, callback_data="age_30_49"),
        InlineKeyboardButton(text=cfg.age_50_90, callback_data="age_50_90")
    )
    return markup

def CancelButton():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(
        cfg.cancel_button
    )
    return markup

def BuyTarifeButton():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text=cfg.one_day_tarife_button, callback_data=cfg.one_day_tarife_button),
        InlineKeyboardButton(text=cfg.one_week_tarife_button, callback_data=cfg.one_week_tarife_button),
        InlineKeyboardButton(text=cfg.one_month_tarife_button, callback_data=cfg.one_month_tarife_button),
        InlineKeyboardButton(text=cfg.one_year_tarife_button, callback_data=cfg.one_year_tarife_button),
        InlineKeyboardButton(text=cfg.forever_tarife_button,callback_data=cfg.forever_tarife_button)
    )
    return markup

def ConfirmOrderButtons(callback_data, sum, day):
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text="Հաստատել", callback_data=f"confirm:{callback_data}:{sum}:{day}")
    btn2 = InlineKeyboardButton(text="Չեղարկել", callback_data=f"cancel:{callback_data}")
    markup.add(btn1, btn2)
    return markup