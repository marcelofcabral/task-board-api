from typing import Annotated

from database import get_db
from fastapi import Depends, HTTPException, status
from models import UserModel
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_user_or_404(id: int, db: Annotated[Session, Depends(get_db)]) -> UserModel:
    user = db.get(UserModel, id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


def get_all_users(db: Annotated[Session, Depends(get_db)]) -> list[UserModel]:
    users = db.execute(select(UserModel)).all()

    return users
