import logging

from telegram import (
    BotCommand,
    Update,
)
from telegram.ext import (
    Application,
    ContextTypes,
    filters,
    MessageHandler,
)

from config import get_settings
from handlers import (
    handle_current_question,
    handle_load,
    handle_load_answer,
    handle_load_question,
    handle_questions,
    handle_start,
)
from persistence import RedisPersistence
from storage.redis import RedisStorage


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
    elif user_reply == '/load':
        user_state = 'LOAD'
    elif user_reply == '/questions':
        user_state = 'QUESTIONS'
    else:
        user_state = context.user_data['state'] or 'START'

    states_functions = {
        'START': handle_start,
        'QUESTIONS': handle_questions,
        'CURRENT_QUESTION': handle_current_question,
        'LOAD': handle_load,
        'LOAD_QUESTION': handle_load_question,
        'LOAD_ANSWER': handle_load_answer,
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
        BotCommand('/questions', 'Список вопросов'),
        BotCommand('/load', 'Загрузить вопросы (доступно только администратору)'),
    ]

    await application.bot.set_my_commands(
        language_code='ru',
        commands=common_commands,
    )


def main() -> None:
    settings = get_settings()

    persistence = RedisPersistence(url=settings.redis_url)
    application = Application.builder().token(settings.bot_token).persistence(persistence).post_init(post_init).build()

    application.add_handler(MessageHandler(filters.TEXT, handle_users_reply))
    application.storage = RedisStorage(redis_url=settings.redis_storage_url)

    logger.info('Бот запущен')

    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES, close_loop=False)
    except Exception as err:
        logger.error(err)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
