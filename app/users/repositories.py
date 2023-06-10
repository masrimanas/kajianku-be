from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.users.schemas import User, UserInDB, UserUpdate, AuthOut, AuthToken
from app.users.models import UserModel
from app.utils.token import create_access_token
from app.utils.hash import Hashing
from app.utils.email_validator import check


async def create(user: User, db_session: Session):
    try:
        new_user = UserModel(**UserInDB(**user.dict()).dict())
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)
        return new_user
    except Exception as exc:
        raise exc


async def login(user: OAuth2PasswordRequestForm, db_session: Session):
    try:
        filter_user = (
            UserModel.email == user.username
            if check(user.username)
            else UserModel.username == user.username
        )
        user_db = db_session.query(UserModel).filter(filter_user).first()

        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User dengan email {user.username} tidak ditemukan",
            )
        if not Hashing.verify(user.password, user_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Periksa kembali password anda",
            )
        access_token = create_access_token(
            data={
                "uuid": str(user_db.uuid),
                "name": user_db.name,
                "sub": user_db.email,
                "is_admin": user_db.is_admin,
                "id": user_db.id,
            }
        )
        return AuthOut(
            token=AuthToken(access_token=access_token, token_type="bearer"),
            user=user_db,
        )
    except Exception as exc:
        raise exc


async def update(user_id: int, user: UserUpdate, db_session: Session):
    try:
        user_db = db_session.query(UserModel).filter(UserModel.id == user_id)
        if not user_db.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user dengan id {user_id} tidak ditemukan",
            )
        user_db.update(user.dict(exclude_none=True))
        db_session.commit()
        db_session.flush()
        db_session.refresh(user_db.first())
        return user_db.first()
    except Exception as exc:
        raise exc


async def create_admin(user: UserInDB, db_session: Session):
    try:
        new_user = UserModel(**user.dict(exclude={"is_admin"}), is_admin=True)
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)
        return new_user
    except Exception as exc:
        raise exc


async def get_all(db_session: Session):
    try:
        users = db_session.query(UserModel).all()
        return users
    except Exception as exc:
        raise exc


async def get_by_id(user_id: int, db_session: Session):
    try:
        user = db_session.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user dengan id {user_id} tidak ditemukan",
            )
        return user
    except Exception as exc:
        raise exc


async def search(keyword: str, db_session: Session):
    try:
        user = db_session.query(UserModel).filter(
            UserModel.email.like(f"%{keyword}%")
            | UserModel.username.like(f"%{keyword}%")
            | UserModel.name.like(f"%{keyword}%")
        )
        if len(user.all()) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Hasil pencarian untuk kata kunci {keyword} tidak ditemukan",
            )
        return user.all()
    except Exception as exc:
        raise exc


async def delete(user_id: int, db_session: Session):
    try:
        user = db_session.query(UserModel).filter(UserModel.id == user_id)
        if not user.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user dengan id {user_id} tidak ditemukan",
            )
        user.delete(synchronize_session=False)
        db_session.commit()
        return {"message": f"user dengan id {user_id} berhasil dihapus"}
    except Exception as exc:
        raise exc
