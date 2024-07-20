try:
    user_id = message.from_user.id
    await message.answer(cfg.USER_LOGS_COM(fnc.nick_with_link("Օգտագործողը", user_id), "/start"))
except Exception as err:
    error_message = f"An error occurred: {err}\n" + traceback.format_exc()
    await bot.send_message(chat_id=cfg.logs_group, text=f"An unexpected error occurred:\n{error_message}")