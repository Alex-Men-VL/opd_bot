from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

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
