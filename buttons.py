import config as cfg

def menu_buttons(types):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(cfg.search_all_button)
    markup.row(cfg.male_button, cfg.female_button)
    markup.add(cfg.settings_button)
    return markup