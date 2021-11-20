import string
from typing import Optional
from functools import lru_cache
from datetime import datetime

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
    PIN_LENGTH: int = 70

    PASS_ALPHABET: str = string.ascii_letters + string.digits + string.punctuation

    class Config:
        case_sensitive = True
        env_file = '.env'


MAIL_CONFIRMATION_TEMPLATE = """
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
    <div class="content" style="width: 80%; max-width: 800px; padding: 10px; margin: 0 auto; font: 1.3rem sans-serif;">
        <h1>Регистрация успешно пройдена!</h1>
        <p>Привет! Это твой Профком студентов</p>
        <p>Благодарим тебя за регистрацию в качестве делегата. Теперь ты сможешь первым узнать об открытии нашего сайта
            и представить интересы своей группы на Конференции.</p>
        <p>Для продолжения пройди по ссылке: <a href={{url}}>{{url}}</a></p>
    </div>
</body>

</html>
"""

MAIL_PASSWORD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Профсоюзная конференция</title>
</head>

<body>
    <img class="header" style="width: 100%;" src="https://dyakov.space/wp-content/uploads/profcom-report-header.png"
        alt="62-я отчетно-выборная конференция профкома" />
    <div class="content" style="width: 80%; max-width: 800px; padding: 10px; margin: 0 auto; font: 1.3rem sans-serif;">
        <h1>Мы начали конференцию!</h1>
        <p>Привет, {{name}}! Это снова твой Профком студентов.</p>
        <p>Ты зарегистрировался на сайте, поэтому мы, как и обещали, пишем тебе: 62-я&nbsp;отчетно-выборная конференция
            профкома уже началась. На нашем сайте уже можно прочитать обо всем, что мы сделали за последний год, чего
            добились и сколько денег на это потратили.</p>
        <p>Главное, что отличает зарегистрированного делегата от обычного студента, который тоже может прочитать наш
            отчет, – ты можешь голосовать. Пожалуйста, воспользуйся этой возможностью и участвуй во всех голосованиях!
        </p>
        <p>Для входа в голосование тебе понадобятся следующие данные:</p>
        <p>Email: <b>{{email}}</b><br/>Пароль: <b>{{password}}</b></p>
        <h2>Что делать дальше?</h2>
        <ol>
            <li>Тебя ждут несколько вопросов, решение в которых мы не сможем принять без учета твоего мнения.</li>
            <li>Если тебе все понятно из нашего отчета, ты можешь проголосовать сразу.</li>
            <li>Если у тебя остались вопросы или замечания, ты сможешь задать все свои вопросы, на которые мы ответим в
                прямом эфире <a href="https://vk.com/profcomff" target="_blank" rel="noopener noreferrer">в нашей группе Вконтакте</a> в понедельник.</li>
            <li>Главное, успеть проголосовать до 22:00 23 ноября.</li>
            <li>Читай отчет, задавай вопросы, оставляй обратную связь и, конечно, голосуй.</li>
        </ol>
        <p>Ждем тебя на отчетно-выборной конференции Профкома студентов 2021!</p>
        <a href="https://report.profcomff.com/report" target="_blank" rel="noopener noreferrer"
            style="display: block; max-width: 80%; margin: 40px auto; padding: 20px; background-color: rgb(13, 110, 253); color: rgb(255, 255, 255); text-align: center; border-radius: 4px; text-decoration: none;">
            Читать отчет и голосовать
        </a>
    </div>
</body>

</html>
"""

TIME_START_VOTING = datetime(2021, 11, 21, 16, 0, 0, 0)
TIME_END_VOTING = datetime(2021, 11, 23, 20, 0, 0, 0)


@lru_cache()
def get_settings():
    return Settings()
