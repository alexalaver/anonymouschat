import config as cfg

def menu_buttons(types):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(cfg.search_all_button)
    markup.row(cfg.male_button, cfg.female_button)
    markup.add(cfg.settings_button)
    return markup

def RegisterGender(types):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text=cfg.select_male_button, callback_data="select_male_button"),
        types.InlineKeyboardButton(text=cfg.select_female_button, callback_data="select_female_button")
    )
    return markup

def RegisterAge(types):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text=cfg.age_12_17, callback_data="age_12_17"),
        types.InlineKeyboardButton(text=cfg.age_18_29, callback_data="age_18_29"),
        types.InlineKeyboardButton(text=cfg.age_30_49, callback_data="age_30_49"),
        types.InlineKeyboardButton(text=cfg.age_50_90, callback_data="age_50_90")
    )
    return markup

def CancelButton(types):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(
        cfg.cancel_button
    )
    return markup