from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.orm import Session

from . import models, schemas


def validate_user(db: Session, username: str):
    user = db.query(models.User).first()
    if username == user.username:
        return JSONResponse(content={"is_user_valid": True})
    return JSONResponse(content={"is_user_valid": False})


def login(db: Session, user: schemas.UserSchema):
    stored_user = db.query(models.User).first()
    if stored_user.email != user.email:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"erorr": "Invalid credentials"},
        )
    if stored_user.password != user.password:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"erorr": "Invalid credentials"},
        )
    return JSONResponse(content={"success": True})
