from __future__ import annotations

import re

from pydantic import BaseModel, validator

from app.core.models import dto


class UserRegister(BaseModel):
    username: str
    password: str
    email: str

    @validator('username')
    def username_validation(cls, v):
        pattern_username = re.compile(r'[A-Za-z][A-Za-z1-9_]+')
        if v == "":
            raise ValueError('Username is empty')
        if not pattern_username.match(v):
            raise ValueError('Wrong username format')
        if len(v) > 32:
            raise ValueError('Too long username')
        return v

    @validator('password')
    def password_validation(cls, v):
        pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$')
        if not pattern_password.match(v):
            raise ValueError('Wrong password format')
        return v

    @validator('email')
    def email_validation(cls, v):
        pattern_email = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not pattern_email.match(v):
            raise ValueError('Wrong email format')
        return v

    def to_dto(self) -> dto.User:
        return dto.User(
            username=self.username,
            email=self.email
        )
