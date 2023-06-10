# pylint: disable=invalid-name
from uuid import UUID
from pydantic import BaseModel, EmailStr
from app.utils.hash import Hashing


class UserBase(BaseModel):
    def __init__(self, **data):
        super().__init__(**data)
        self.is_admin = False

    uuid: UUID | None
    name: str
    username: str
    email: EmailStr
    is_admin: bool | None = None


class User(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: str | None = None
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    uuid: UUID
    name: str
    username: str
    email: EmailStr
    is_admin: bool | None = None

    class Config:
        orm_mode = True


class UserAdminIn(User):
    def __init__(self, **data):
        super().__init__(**data)
        self.is_admin = True

    class Config:
        orm_mode = True


class UserInDB(User):
    is_admin: bool

    def __init__(self, **data):
        super().__init__(**data)
        self.is_admin = data["is_admin"] | False
        self.password = Hashing.hash(data["password"])


class AuthIn(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class AuthToken(BaseModel):
    access_token: str
    token_type: str


class AuthOut(BaseModel):
    token: AuthToken
    user: UserOut | None = None

    class Config:
        orm_mode = True
