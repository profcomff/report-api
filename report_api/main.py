from os import name
from typing import Optional

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_sqlalchemy import DBSessionMiddleware, db
from pydantic import BaseModel
from pydantic.networks import EmailStr
from sqlalchemy import func
from starlette.responses import RedirectResponse

from report_api.models import Status, UnionMember
from report_api.settings import get_settings

settings = get_settings()
app = FastAPI()
app.add_middleware(DBSessionMiddleware,
                   db_url=settings.DB_DSN)


class RegistrationDetails(BaseModel):
    last_name: str
    first_name: str
    patronymic: Optional[str] = None
    academic_group_number: str
    email: EmailStr

    class Config:
        orm_mode = True


@app.post("/register")
async def register_user(registration_details: RegistrationDetails):
    """
    Регистрация
    """
    user = (
        db.session.query(UnionMember)
        .filter(
            func.upper(UnionMember.email) == registration_details.email.upper()
        )
        .one_or_none()
    )
    if user:
        return {"status": "fail"}

    new_user = UnionMember(
        last_name=registration_details.last_name,
        first_name=registration_details.first_name,
        patronymic=registration_details.patronymic,
        academic_group_number=registration_details.academic_group_number,
        email=registration_details.email
    )

    db.session.add(new_user)
    db.session.commit()

    # TODO отправить письмо для подтверждения электронной почты

    return {"status": "ok"}


@app.get("/register/{uuid4}")
async def confirm_email(uuid4: str):
    """
    Для подтверждения электронной почты
    """
    user = (
        db.session.query(UnionMember)
        .filter(
            UnionMember.email_uuid == uuid4
        )
        .one_or_none()
    )
    if not user:
        return RedirectResponse(settings.EMAIL_CONFIRM_FAIL)
    user.status = Status.confirmed
    db.session.commit()
    return RedirectResponse(settings.EMAIL_CONFIRM_OK)

# Вход пользователя по логину и паролю


# @app.post("/login")
# Ответ на вопрос
# @app.post("/question/{num}")
# Посмотреть результаты
# @app.get("/stats?token=<Что-то страшное>")
