from fastapi import status, APIRouter
from app.chatbot.schemas import NewData, Question, QuestionOut
from app.chatbot.repositories import insert, ask
from app.utils.enums import RouteName, RouteTags


router = APIRouter(
    tags=[RouteTags.CHATBOT.value],
    prefix=RouteName.CHATBOT.value,
)


@router.post("/ask", status_code=status.HTTP_201_CREATED, response_model=QuestionOut)
async def ask_question(req_body: Question):
    return await ask(req_body)


@router.post("/insert", status_code=status.HTTP_201_CREATED)
async def insert_new_data(req_body: NewData):
    return await insert(req_body)
