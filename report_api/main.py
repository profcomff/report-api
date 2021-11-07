import random
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
from report_api.mail import send_email

from report_api.models import Answer, Question, Status, UnionMember, ResponseOption
from report_api.settings import get_settings

settings = get_settings()
app = FastAPI(root_path=settings.ROOT)
app.add_middleware(DBSessionMiddleware,
                   db_url=settings.DB_DSN)
origins = [
    "https://app.profcomff.com",
    "http://app.profcomff.com",
    "https://www.profcomff.com",
    "http://www.profcomff.com",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RegistrationDetails(BaseModel):
    last_name: str
    first_name: str
    patronymic: Optional[str] = None
    academic_group_number: str
    email: EmailStr

    class Config:
        orm_mode = True


class LoginDetails(BaseModel):
    email: EmailStr
    password: str


class AnswerDetails(BaseModel):
    token: str
    answer: str


def answer_to_enum(answer: str):
    if answer == "yes":
        return ResponseOption.yes
    if answer == "no":
        return ResponseOption.no


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
        raise HTTPException(409,'user already exists')

    new_user = UnionMember(
        last_name=registration_details.last_name,
        first_name=registration_details.first_name,
        patronymic=registration_details.patronymic,
        academic_group_number=registration_details.academic_group_number,
        email=registration_details.email
    )

    db.session.add(new_user)
    db.session.commit()

    send_email('Профсоюзная конференция - Подтверждение электронной почты',
               registration_details.email,
               f'https://app.profcomff.com/report/api/register/{new_user.email_uuid}')
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
        return RedirectResponse(settings.EMAIL_CONFIRM_ERROR)
    if(user.status != Status.unconfirmed):
        return RedirectResponse(settings.EMAIL_CONFIRM_RETRY)
    user.status = Status.confirmed
    db.session.commit()
    return RedirectResponse(settings.EMAIL_CONFIRM_SUCCSESS)


@app.post("/login")
async def login(login_details: LoginDetails):
    """
    Вход пользователя по логину и паролю
    """
    user = (
        db.session.query(UnionMember)
        .filter(
            UnionMember.email == login_details.email,
            UnionMember.password == login_details.password,
            UnionMember.status == Status.confirmed
        )
        .one_or_none()
    )
    if not user:
        raise HTTPException(401)

    token = ''
    for _ in range(settings.PIN_LENGTH):
        token += random.choice(settings.PIN_SYMBOLS)

    user.token = token
    db.session.commit()

    questions = (db.session.query(
        Question.text).order_by(Question.index).all())

    return {"status": "ok", "quesions": questions}


@app.post("/question/{index}")
async def answer(index: int, answer_details: AnswerDetails):
    """
    Ответ на вопрос
    """
    user = (
        db.session.query(UnionMember)
        .filter(
            UnionMember.token == answer_details.token
        )
        .one_or_none()
    )
    if not user:
        raise HTTPException(401)

    for answer in user.answers:
        if answer.question.index == index:
            raise HTTPException(409,'answer already exists')

    question = (
        db.session.query(Question)
        .filter(
            Question.index == index
        )
        .one_or_none()
    )

    if not question:
        raise HTTPException(404)

    new_answer = Answer(
        union_member_id=user.id,
        question_id=question.id,
        answer=answer_to_enum(answer_details.answer)
    )
    db.session.add(new_answer)

    question_max_index = (
        db.session.query(func.max(Question.index)).scalar()
    )

    if index == question_max_index:
        user.status = Status.finished

    db.session.commit()
    return {"status": "ok"}

# Посмотреть результаты
# @app.get("/stats?token=<Что-то страшное>")
