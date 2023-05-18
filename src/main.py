import logging
from pathlib import Path

from telegram import (
    BotCommand,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    MessageHandler,
)

from config import get_settings
from handlers import (
    handle_categories,
    handle_current_category,
    handle_current_question,
    handle_start,
)
from persistence import RedisPersistence
from tg_lib import load_questions


logger = logging.getLogger('bot')


async def handle_users_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if message := update.message:
        user_reply = message.text if message.text else message.location
    elif query := update.callback_query:
        user_reply = query.data
    else:
        return

    if user_reply == '/start':
        user_state = 'START'
    elif user_reply == '/categories':
        user_state = 'CATEGORIES'
    else:
        user_state = context.user_data['state'] or 'START'

    states_functions = {
        'START': handle_start,
        'CATEGORIES': handle_categories,
        'CURRENT_CATEGORY': handle_current_category,
        'CURRENT_QUESTION': handle_current_question,
    }
    state_handler = states_functions[user_state]

    try:
        next_state = await state_handler(update, context)
        context.user_data['state'] = next_state
    except Exception as err:
        print(err)


async def post_init(application: Application) -> None:
    common_commands = [
        BotCommand('/start', 'Старт бота'),
        BotCommand('/categories', 'Список категорий вопросов'),
    ]

    await application.bot.set_my_commands(
        language_code='ru',
        commands=common_commands,
    )


def main() -> None:
    settings = get_settings()

    questions_per_category = load_questions(path=Path('./questions.json'))
    initial_data = {
        'bot_data': {
            'questions_per_category': questions_per_category,
        }
    }
    persistence = RedisPersistence(url=settings.redis_url, initial_data=initial_data)
    application = Application.builder().token(settings.bot_token).persistence(persistence).post_init(post_init).build()

    application.add_handler(CallbackQueryHandler(handle_users_reply))
    application.add_handler(MessageHandler(filters.TEXT, handle_users_reply))

    logger.info('Бот запущен')

    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES, close_loop=False)
    except Exception as err:
        logger.error(err)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
