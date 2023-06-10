from pydantic import BaseModel


class NewData(BaseModel):
    content: str


class Question(BaseModel):
    content: str


class QuestionOut(BaseModel):
    status: str
    message: str

    class Config:
        orm_mode = True
