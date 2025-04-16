from typing import Optional

from pydantic import BaseModel, EmailStr


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    email: Optional[EmailStr] = None


class UserCreate(User):
    password: str


class UserInDB(User):
    hashed_password: str
