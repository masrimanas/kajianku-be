from uuid import UUID
from datetime import datetime
from typing import List
from pydantic import BaseModel
from app.users.schemas import User


class KajianCategory(BaseModel):
    name: str


class KajianCategoryOut(KajianCategory):
    id: int

    class Config:
        orm_mode = True


class Kajian(BaseModel):
    title: str
    images: List[str] | None = None
    content: str
    location: str
    longlat: List[float] | None = None
    date: datetime
    category_id: int
    tags: List[str]
    organizers: List[str]
    speakers: List[str]


class KajianUpdate(BaseModel):
    title: str | None = None
    images: List[str] | None = None
    content: str | None = None
    location: str | None = None
    longlat: List[float] | None = None
    date: datetime | None = None
    category_id: int | None = None
    tags: List[str] | None = None
    organizers: List[str] | None = None
    speakers: List[str] | None = None


class KajianOut(BaseModel):
    title: str
    uuid: UUID
    images: List[str] | None = None
    content: str
    location: str
    longlat: List[float] | None = None
    date: datetime
    category: KajianCategoryOut = None
    tags: List[str] | None
    organizers: List[str]
    speakers: List[str]
    author: User

    class Config:
        orm_mode = True
