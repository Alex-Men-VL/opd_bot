from pathlib import Path
from textwrap import dedent

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from constants import (
    CATEGORIES_MESSAGE,
    INCORRECT_CATEGORY_MESSAGE,
    QUESTION_CATEGORY,
    QUESTION_EMPTY_REQUEST_MESSAGE,
    QUESTION_NOT_FOUND,
    QUESTION_TEMPLATE,
    START_MESSAGE,
)
from dto import CategoryDTOStruct
from tg_lib import build_categories_menu


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.message.reply_text(text=dedent(START_MESSAGE))

    return 'CATEGORIES'


async def handle_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    categories = CategoryDTOStruct(context.bot_data.get('questions_per_category')).get_categories()
    reply_markup = build_categories_menu(categories)

    await update.message.reply_text(text=dedent(CATEGORIES_MESSAGE), reply_markup=reply_markup)
    return 'CURRENT_CATEGORY'


async def handle_current_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    category = update.message.text
    questions = CategoryDTOStruct(context.bot_data.get('questions_per_category')).get_questions_by_category(category)
    if category == 'Полезные ссылки':
        keyboard = [[InlineKeyboardButton(text=question.text, url=question.answer)] for question in questions]
    elif questions:
        keyboard = [[InlineKeyboardButton(text=question.text, callback_data=question.pk)] for question in questions]
    else:
        categories = CategoryDTOStruct(context.bot_data.get('questions_per_category')).get_categories()
        reply_markup = build_categories_menu(categories)

        await update.message.reply_markdown_v2(text=INCORRECT_CATEGORY_MESSAGE, reply_markup=reply_markup)

        return 'CURRENT_CATEGORY'

    if not keyboard:
        categories = CategoryDTOStruct(context.bot_data.get('questions_per_category')).get_categories()
        reply_markup = build_categories_menu(categories)

        await update.message.reply_markdown_v2(text=QUESTION_EMPTY_REQUEST_MESSAGE, reply_markup=reply_markup)

        return 'CURRENT_CATEGORY'

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_markdown_v2(
        text=dedent(QUESTION_CATEGORY.format(category=category)),
        reply_markup=reply_markup,
    )

    return 'CURRENT_CATEGORY' if category == 'Полезные ссылки' else 'CURRENT_QUESTION'


async def handle_current_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    try:
        question_pk = int(update.callback_query.data)
    except AttributeError:
        await context.bot.send_message(text=dedent(QUESTION_NOT_FOUND), chat_id=update.effective_chat.id)

        return 'CURRENT_QUESTION'

    question = CategoryDTOStruct(context.bot_data.get('questions_per_category')).get_question_by_pk(question_pk)

    if not question:
        await context.bot.send_message(text=dedent(QUESTION_NOT_FOUND), chat_id=update.effective_chat.id)

        return 'CURRENT_QUESTION'

    if (path := Path(question.answer)) and path.is_file() and path.exists():
        await context.bot.send_photo(
            photo=path.open(mode='rb'), chat_id=update.effective_chat.id, parse_mode=ParseMode.MARKDOWN_V2
        )
    else:
        await context.bot.send_message(
            text=dedent(QUESTION_TEMPLATE.format(question=question.text, answer=question.answer)),
            chat_id=update.effective_chat.id,
            parse_mode=ParseMode.MARKDOWN_V2,
        )

    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.id)

    return 'CURRENT_CATEGORY'
