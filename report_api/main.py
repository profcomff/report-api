from typing import Optional
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_sqlalchemy import DBSessionMiddleware, db
from pydantic.networks import EmailStr
from sqlalchemy import func

from models import Status, UnionMember

app = FastAPI()


class RegistrationDetails(BaseModel):
    last_name: str
    first_name: str
    patronymic: Optional[str] = None
    academic_group_number: str
    email: EmailStr


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

    db.session.add(registration_details)
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
            func.upper(UnionMember.email_uuid) == uuid4
        )
        .one_or_none()
    )
    if not user:
        return {"status": "fail"}
    user.status = Status.confirmed
    db.session.commit()
    return {"message": "ok"}

# Вход пользователя по логину и паролю


# @app.post("/login")
# Ответ на вопрос
# @app.post("/question/{num}")
# Посмотреть результаты
# @app.get("/stats?token=<Что-то страшное>")
