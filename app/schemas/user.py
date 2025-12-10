from pydantic import BaseModel, EmailStr


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: str


class User(BaseModel):
    username: str
    email: EmailStr | None = None


class UserCreate(User):
    password: str


class UserInDB(User):
    hashed_password: str
