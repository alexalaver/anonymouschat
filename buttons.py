import config as cfg
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton

def menu_buttons():
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=cfg.search_all_button_1)],
        [KeyboardButton(text=cfg.male_button), KeyboardButton(text=cfg.female_button)],
        [KeyboardButton(text=cfg.supports_button)]
    ],
            resize_keyboard=True)
    return markup

def RegisterGender():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=cfg.select_male_button, callback_data="select_male_button"),
         InlineKeyboardButton(text=cfg.select_female_button, callback_data="select_female_button")]
    ])
    return markup

def RegisterAge():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=cfg.age_12_17, callback_data="age_12_17"),
        InlineKeyboardButton(text=cfg.age_18_29, callback_data="age_18_29")],
        [InlineKeyboardButton(text=cfg.age_30_49, callback_data="age_30_49"),
        InlineKeyboardButton(text=cfg.age_50_90, callback_data="age_50_90")]
    ])
    return markup

def CancelButton():
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=cfg.cancel_button)]
    ],
            resize_keyboard=True)
    return markup

def BackButton():
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=cfg.back_button)]
    ],
                resize_keyboard=True)
    return markup

def BuyTarifeButton():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=cfg.one_day_tarife_button, callback_data=cfg.one_day_tarife_button),
        InlineKeyboardButton(text=cfg.one_week_tarife_button, callback_data=cfg.one_week_tarife_button)],
        [InlineKeyboardButton(text=cfg.one_month_tarife_button, callback_data=cfg.one_month_tarife_button),
        InlineKeyboardButton(text=cfg.one_year_tarife_button, callback_data=cfg.one_year_tarife_button)],
        [InlineKeyboardButton(text=cfg.forever_tarife_button,callback_data=cfg.forever_tarife_button)]
    ])
    return markup

def ConfirmOrderButtons(callback_data, sum, day):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Հաստատել", callback_data=f"confirm:{callback_data}:{sum}:{day}"),
         InlineKeyboardButton(text="Չեղարկել", callback_data=f"cancel:{callback_data}")]
    ])
    return markup

def HelperButton():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Սեղմեք", url=cfg.helper_link)]
    ])
    return markup

def MarkupsLink(channels):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{num} {cfg.channel_range}", url=channel)]
        for num, channel in enumerate(channels, start=1)
    ])
    return markup

def VIPDonateButton(dram, dollar, tarife_count):

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Оплатить {dram}֏ / {dollar}$ / {tarife_count} ⭐️", pay=True)],
        [InlineKeyboardButton(text=f"Вернутся назад", callback_data="back_from_vip")]
    ])
    return markup
