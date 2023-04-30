from functools import lru_cache

from pydantic import (
    BaseSettings,
    Field,
    RedisDsn,
)


class Config(BaseSettings):
    bot_token: str = Field(
        env='BOT_TOKEN',
    )
    redis_url: RedisDsn = Field(
        env='REDIS_URL',
    )

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> Config:
    return Config()
