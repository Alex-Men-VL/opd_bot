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

    bot_admin_ids: list[int] = Field(
        env='BOT_ADMIN_IDS',
        default_factory=list,
    )
    debug: bool = Field(
        env='DEBUG',
        default=False,
    )

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> Config:
    return Config()
