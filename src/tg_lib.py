from functools import wraps

from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from config import get_settings
from dto import QuestionDTO


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i : i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def build_questions_menu(questions: list[QuestionDTO]) -> ReplyKeyboardMarkup:
    button_list = [[KeyboardButton(question.question)] for question in questions]
    reply_markup = ReplyKeyboardMarkup(button_list, resize_keyboard=True)
    return reply_markup


def check_permissions(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        settings = get_settings()
        if user_id not in settings.bot_admin_ids and not settings.debug:
            await update.message.reply_text('Доступ запрещен')
            return
        return await func(update, context, *args, **kwargs)

    return wrapped
