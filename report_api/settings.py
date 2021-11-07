import string
from typing import Optional
from functools import lru_cache

from pydantic import BaseSettings
from pydantic.networks import HttpUrl, PostgresDsn


class Settings(BaseSettings):
    ROOT: Optional[HttpUrl] = None
    DB_DSN: PostgresDsn = None

    EMAIL_PASS: str = None

    EMAIL_CONFIRM_SUCCSESS: HttpUrl = 'https://report.profcomff.com/email_confirmation_success'
    EMAIL_CONFIRM_RETRY: HttpUrl = 'https://report.profcomff.com/email_confirmation_retry'
    EMAIL_CONFIRM_ERROR: HttpUrl = 'https://report.profcomff.com/email_confirmation_error'

    PIN_SYMBOLS: str = string.ascii_uppercase + string.digits
    PIN_LENGTH: int = 6

    class Config:
        case_sensitive = True
        env_file = '.env'


@lru_cache()
def get_settings():
    return Settings()
