# pylint: disable=redefined-builtin, invalid-name
from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from app.kajian.models import KajianModel, KajianCategoryModel
from app.kajian.schemas import Kajian, KajianUpdate, KajianCategory


async def post(new_kajian: Kajian, db_session: Session, current_user: dict):
    try:
        kajian = KajianModel(**new_kajian.dict(), author_id=current_user["id"])
        db_session.add(kajian)
        db_session.commit()
        db_session.refresh(kajian)
        return kajian
    except Exception as exc:
        raise exc


async def get_all(db_session: Session):
    try:
        kajian_list = db_session.query(KajianModel).all()
        if len(kajian_list) == 0:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="Tidak ada data",
                headers={"X-Error": "No Content"},
            )
        return kajian_list
    except Exception as exc:
        raise exc


async def get(id: int, db_session: Session):
    try:
        kajian = db_session.query(KajianModel).filter(KajianModel.id == id).first()
        if not kajian:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"kajian dengan id {id} tidak ditemukan",
            )
        return kajian
    except Exception as exc:
        raise exc


async def update(id: int, kajian_to_update: KajianUpdate, db_session: Session):
    try:
        kajian = db_session.query(KajianModel).filter(KajianModel.id == id)
        if not kajian.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"kajian dengan id {id} tidak ditemukan",
            )
        kajian.update(kajian_to_update.dict(exclude_none=True))
        db_session.commit()
        db_session.flush()
        db_session.refresh(kajian.first())
        return {
            "status": "success",
            "message": f"kajian dengan id {id} berhasil diupdate",
        }
    except Exception as exc:
        raise exc


async def delete(id: int, db_session: Session, current_user: dict):
    try:
        kajian = db_session.query(KajianModel).filter(KajianModel.id == id)
        filtered_kajian = kajian.first()

        if not filtered_kajian:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"kajian dengan id {id} tidak ditemukan",
            )
        if not current_user["id"] == filtered_kajian.user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Forbidden",
            )
        kajian.delete(synchronize_session=False)
        db_session.commit()
        return {
            "status": "success",
            "message": f"kajian dengan id {id} berhasil dihapus",
        }
    except Exception as exc:
        raise exc


async def create_category(new_category: KajianCategory, db_session: Session):
    try:
        category = KajianCategoryModel(**new_category.dict())
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)
        return category
    except Exception as exc:
        raise exc
