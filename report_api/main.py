import random
from os import name
from typing import Optional
import secrets
import asyncio
from datetime import datetime

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_sqlalchemy import DBSessionMiddleware, db
from pydantic import BaseModel
from pydantic.networks import EmailStr
from sqlalchemy import func
from starlette.responses import RedirectResponse
from report_api.mail import send_confirmation_email, send_password_email

from report_api.models import Answer, Question, Status, UnionMember, ResponseOption
from report_api.settings import TIME_END_VOTING, TIME_START_VOTING, get_settings

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
    if answer == "skip":
        return ResponseOption.skip


@app.post("/register")
async def register_user(registration_details: RegistrationDetails):
    """
    Регистрация
    """
    if datetime.utcnow() > TIME_START_VOTING:
        raise HTTPException(401, "voiting already started")

    user = (
        db.session.query(UnionMember)
        .filter(
            func.upper(UnionMember.email) == registration_details.email.upper()
        )
        .one_or_none()
    )
    if user:
        raise HTTPException(409, 'user already exists')

    new_user = UnionMember(
        last_name=registration_details.last_name,
        first_name=registration_details.first_name,
        patronymic=registration_details.patronymic,
        academic_group_number=registration_details.academic_group_number,
        email=registration_details.email
    )

    db.session.add(new_user)
    db.session.commit()

    send_confirmation_email('Профсоюзная конференция - Подтверждение электронной почты',
                            registration_details.email,
                            f'https://app.profcomff.com/report/api/register/{new_user.email_uuid}')

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

    if datetime.utcnow() > TIME_START_VOTING:
        generate_pass(user)

    return RedirectResponse(settings.EMAIL_CONFIRM_SUCCSESS)


@app.post("/login")
async def login(login_details: LoginDetails):
    """
    Вход пользователя по логину и паролю
    """
    if datetime.utcnow() > TIME_END_VOTING:
        raise HTTPException(401, "voiting already finished")

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

    user_answered_question_id = db.session.query(
        Answer.question_id).filter(Answer.union_member == user)
    questions = db.session.query(Question.text, Question.id).filter(
        Question.id.not_in(user_answered_question_id)).order_by(Question.index).all()

    return {"status": "ok", "token": token, "questions": questions}


@app.post("/question/{id}")
async def answer(id: int, answer_details: AnswerDetails):
    """
    Ответ на вопрос
    """
    if datetime.utcnow() > TIME_END_VOTING:
        raise HTTPException(401, "voiting already finished")

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
        if answer.question.id == id:
            raise HTTPException(409, 'answer already exists')

    question = (
        db.session.query(Question)
        .filter(
            Question.id == id
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

    all_question_ids = set(db.session.query(Question.id).all())
    user_answered_question_id = set(db.session.query(
        Answer.question_id).filter(Answer.union_member == user).all())
    if all_question_ids == user_answered_question_id:
        user.status = Status.finished

    db.session.commit()
    return {"status": "ok"}


@app.get("/passes")
async def generate_passes():
    """
    Генерация и отправка паролей для подтвержденных пользователей
    """
    users = (
        db.session.query(UnionMember)
        .filter(
            UnionMember.password == None,
            UnionMember.status == Status.confirmed
        ).all()
    )
    if len(users) <= 0:
        raise HTTPException(400, "users not found")

    for user in users:
        generate_pass(user)
        await asyncio.sleep(2)

    return {"status": "ok"}


def generate_pass(user: UnionMember):
    password = ''.join(secrets.choice(settings.PASS_ALPHABET)
                       for i in range(12))
    user.password = password
    db.session.commit()
    send_password_email('Профсоюзная конференция уже началась',
                        user.email,
                        user.first_name,
                        password)

# Посмотреть результаты
# @app.get("/stats?token=<Что-то страшное>")
