# pylint: disable=redefined-builtin, invalid-name
from typing import Annotated, List
from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.kajian import repositories
from app.kajian.schemas import Kajian, KajianOut, KajianUpdate, KajianCategory
from app.users.schemas import AuthOut
from app.utils.oauth2 import get_current_user
from app.utils.enums import RouteName, RouteTags

router = APIRouter(
    tags=[RouteTags.KAJIAN.value],
    prefix=RouteName.KAJIAN.value,
)


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=KajianOut)
async def post_kajian(
    req_body: Kajian,
    db_session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[  # pylint: disable=unused-argument
        AuthOut, Depends(get_current_user)
    ],
):
    return await repositories.post(req_body, db_session, current_user)


@router.get("/get/all", response_model=List[KajianOut])
async def get_all_kajian(db_session: Annotated[Session, Depends(get_db)]):
    return await repositories.get_all(db_session)


@router.get("/get/{id}")
async def get_kajian(
    id: int,
    db_session: Annotated[Session, Depends(get_db)],
):
    return await repositories.get(id, db_session)


@router.patch("/{id}/update", status_code=status.HTTP_202_ACCEPTED)
async def update_kajian(
    id: int,
    req_body: KajianUpdate,
    db_session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[  # pylint: disable=unused-argument
        AuthOut, Depends(get_current_user)
    ],
):
    return await repositories.update(id, req_body, db_session)


@router.delete("/{id}/delete", status_code=status.HTTP_200_OK)
async def delete_kajian(
    id: int,
    db_session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[AuthOut, Depends(get_current_user)],
):
    if not current_user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    return await repositories.delete(id, db_session, current_user)


@router.post(
    "/add/category",
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    req_body: KajianCategory,
    db_session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[  # pylint: disable=unused-argument
        AuthOut, Depends(get_current_user)
    ],
):
    if not current_user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    return await repositories.create_category(req_body, db_session)
