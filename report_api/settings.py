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


MAIL_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body>
    <img class="header" style="width: 100%;" src="https://dyakov.space/wp-content/uploads/profcom-report-header.png"
        alt="62-я отчетно-выборная конференция профкома" />
    <div class="content" style="width: 80%; max-width: 300px; padding: 10px; margin: 0 auto; font: 1em sans-serif;">
        <h1>Регистрация успешно пройдена!</h1>
        <p>Привет! Это твой Профком студентов</p>
        <p>Благодарим тебя за регистрацию в качестве делегата. Теперь ты сможешь первым узнать об открытии нашего сайта
            и представить интересы своей группы на Конференции.</p>
        <p>Для продолжения пройди по ссылке: <a href={{url}}>{{url}}</a></p>
    </div>
    <div class="footer" style="width: 90%; text-align: center; padding: 5%; background-color: #8ba8bf; color: white;">
        <sup>Профком студентов физфака &copy; 2021</sup></div>
</body>

</html>
"""


@lru_cache()
def get_settings():
    return Settings()
