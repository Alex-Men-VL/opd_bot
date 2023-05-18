import json
from pathlib import Path

from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from telegram.constants import MessageEntityType
from telegram.helpers import escape_markdown

from dto import (
    CategoryDTO,
    QuestionDTO,
)


def load_questions(path: Path):
    questions_per_category = []

    with path.open() as questions_file:
        data = json.load(questions_file)
    for category in data:
        questions = [
            QuestionDTO(text=escape_markdown(text, version=2), answer=answer) for text, answer in data[category].items()
        ]
        questions_per_category.append(
            CategoryDTO(
                title=category,
                questions=questions,
            )
        )
    return questions_per_category


def build_categories_menu(categories: list[str]) -> ReplyKeyboardMarkup:
    buttons = [[KeyboardButton(category)] for category in categories]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    return reply_markup


def build_questions_menu(questions: list[QuestionDTO]) -> ReplyKeyboardMarkup:
    button_list = [[KeyboardButton(question.question)] for question in questions]
    reply_markup = ReplyKeyboardMarkup(button_list, resize_keyboard=True)
    return reply_markup
