from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.settings.database import SessionLocal
from . import schemas, service


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.post("/users/")
async def valid_user(user: schemas.UserSchema, db: Session = Depends(get_db)):
    return service.validate_user(db, user)


@router.post(
    "/login/",
)
async def login(
    user: schemas.UserSchema,
    db: Session = Depends(get_db),
):
    return service.login(db, user)
