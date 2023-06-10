import urllib
from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.users.schemas import User, UserUpdate, UserOut, AuthOut
from app.database import get_db
from app.users import repositories
from app.utils.oauth2 import get_current_user
from app.utils.enums import RouteTags, RouteName

router = APIRouter(tags=[RouteTags.USERS.value], prefix=RouteName.USERS.value)


@router.post("/register", response_model=UserOut)
async def register_user(req: User, db_session: Annotated[Session, Depends(get_db)]):
    return await repositories.create(req, db_session)


@router.post("/login", response_model=AuthOut)
async def login(
    req: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: Annotated[Session, Depends(get_db)],
):
    return await repositories.login(req, db_session)


@router.get("/search", response_model=List[UserOut])
async def search_user(keyword: str, db_session: Annotated[Session, Depends(get_db)]):
    encoded_keyword = urllib.parse.urlsplit(keyword)
    print(encoded_keyword.path)
    return await repositories.search(encoded_keyword.path, db_session)


@router.get("/get/all", response_model=List[UserOut])
async def get_all_users(
    db_session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[  # pylint: disable=unused-argument
        AuthOut, Depends(get_current_user)
    ],
):
    return await repositories.get_all(db_session)


@router.get("/get/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db_session: Annotated[Session, Depends(get_db)]):
    return await repositories.get_by_id(user_id, db_session)


@router.patch("/update/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int,
    req_body: UserUpdate,
    db_session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[  # pylint: disable=unused-argument
        AuthOut, Depends(get_current_user)
    ],
):
    return await repositories.update(user_id, req_body, db_session)


@router.delete("/delete/{user_id}")
async def delete_user(
    user_id: int,
    db_session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[AuthOut, Depends(get_current_user)],
):
    if not current_user["is_admin"] | (current_user["id"] == user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    return await repositories.delete(user_id, db_session)
