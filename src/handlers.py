from textwrap import dedent

from telegram import (
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import ContextTypes

from constants import (
    LOAD_ANSWER_MESSAGE,
    LOAD_CREATED_MESSAGE,
    LOAD_QUESTION_MESSAGE,
    QUESTION_EMPTY_REQUEST_MESSAGE,
    QUESTION_NOT_FOUND,
    QUESTION_REQUEST_MESSAGE,
    START_MESSAGE,
)
from dto import QuestionDTO
from tg_lib import (
    build_questions_menu,
    check_permissions,
)


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.message.reply_text(text=dedent(START_MESSAGE))

    return 'QUESTIONS'


async def handle_questions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    questions = await context.application.storage.get_questions()
    reply_markup = build_questions_menu(questions)

    await update.message.reply_text(
        text=dedent(QUESTION_REQUEST_MESSAGE) if questions else dedent(QUESTION_EMPTY_REQUEST_MESSAGE),
        reply_markup=reply_markup,
    )

    return 'CURRENT_QUESTION'


async def handle_current_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    questions = await context.application.storage.get_questions()
    reply_markup = build_questions_menu(questions)

    answer = await context.application.storage.get_answer_by_question(update.message.text)

    await update.message.reply_markdown_v2(
        text=answer if answer else dedent(QUESTION_NOT_FOUND),
        reply_markup=reply_markup,
    )

    return 'CURRENT_QUESTION'


@check_permissions
async def handle_load(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.message.reply_text(text=dedent(LOAD_QUESTION_MESSAGE), reply_markup=ReplyKeyboardRemove())
    return 'LOAD_QUESTION'


async def handle_load_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    message = update.message.text
    context.user_data.setdefault('question', message)

    await update.message.reply_text(text=dedent(LOAD_ANSWER_MESSAGE))

    return 'LOAD_ANSWER'


async def handle_load_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    message = update.message.text_markdown_v2_urled
    question = context.user_data.get('question')
    await context.application.storage.save_question(
        QuestionDTO(
            question=question,
            answer=message,
        ),
    )
    del context.user_data['question']

    await update.message.reply_text(text=dedent(LOAD_CREATED_MESSAGE))

    return 'START'
