from fastapi import FastAPI
from app.chatbot.routers import router as chatbot_router
from app.kajian.routers import router as kajian_router
from app.users.routers import router as users_router
from app.database import engine, Base

app = FastAPI(
    title="Kajianku API",
    description="API untuk aplikasi mobile dan Web Kajianku",
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Hello World"}


app.include_router(chatbot_router)
app.include_router(kajian_router)
app.include_router(users_router)
