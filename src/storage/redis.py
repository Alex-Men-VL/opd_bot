from dataclasses import asdict

import aioredis
from pydantic import RedisDsn

from dto import QuestionDTO
from storage.base import AbstractStorage


class RedisStorage(AbstractStorage):
    def __init__(self, redis_url: RedisDsn) -> None:
        self.redis_url = redis_url

    async def save_question(self, dto: QuestionDTO):
        async with aioredis.from_url(self.redis_url, decode_responses=True) as redis_conn:
            question_id = await redis_conn.incr('questions:id')
            key = f'questions:{question_id}'
            mapping = asdict(dto)
            await redis_conn.hmset(key, mapping)
            return question_id

    async def get_questions(self) -> list[QuestionDTO]:
        async with aioredis.from_url(self.redis_url, decode_responses=True) as redis_conn:
            keys = await redis_conn.keys('questions:*')
            if 'questions:id' in keys:
                keys.remove('questions:id')
            questions = []
            for key in keys:
                question = await redis_conn.hgetall(key)
                questions.append(
                    QuestionDTO(**question),
                )
            return questions

    async def get_by_id(self, question_id) -> QuestionDTO | None:
        async with aioredis.from_url(self.redis_url, decode_responses=True) as redis_conn:
            key = f'questions:{question_id}'
            question = await redis_conn.hgetall(key)
            if not question:
                return None
            return QuestionDTO(**question)

    async def get_answer_by_question(self, question_text: str) -> str | None:
        async with aioredis.from_url(self.redis_url, decode_responses=True) as redis_conn:
            keys = await redis_conn.keys('questions:*')
            if 'questions:id' in keys:
                keys.remove('questions:id')
            for key in keys:
                question = await redis_conn.hget(key, 'question')
                if question == question_text:
                    answer = await redis_conn.hget(key, 'answer')
                    return answer
            return None
