import string
from functools import lru_cache

from pydantic import BaseSettings
from pydantic.networks import AnyHttpUrl, PostgresDsn


class Settings(BaseSettings):
    DB_DSN: PostgresDsn = None

    EMAIL_CONFIRM_SUCCSESS: AnyHttpUrl = 'https://report.profcomff.com/email_confirmation_success'
    EMAIL_CONFIRM_RETRY: AnyHttpUrl = 'https://report.profcomff.com/email_confirmation_retry'
    EMAIL_CONFIRM_ERROR: AnyHttpUrl = 'https://report.profcomff.com/email_confirmation_error'

    PIN_SYMBOLS: str = string.ascii_uppercase + string.digits
    PIN_LENGTH: int = 6

    class Config:
        case_sensitive = True
        env_file = '.env'


@lru_cache()
def get_settings():
    return Settings()
