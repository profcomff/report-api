from functools import lru_cache

from pydantic import BaseSettings
from pydantic.networks import AnyHttpUrl, PostgresDsn


class Settings(BaseSettings):
    DB_DSN: PostgresDsn = None

    EMAIL_CONFIRM_OK: AnyHttpUrl = 'https://www.profcomff.com/service/email_confirmed'
    EMAIL_CONFIRM_FAIL: AnyHttpUrl = 'https://www.profcomff.com/service/email_fail'

    class Config:
        case_sensitive = True
        env_file = '.env'

@lru_cache()
def get_settings():
    return Settings()
