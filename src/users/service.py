from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.orm import Session

from . import models, schemas


def validate_user(db: Session, user: schemas.UserSchema):
    try:
        username = user.username
        stored_user = db.query(models.User).first()
        if username == stored_user.username:
            return JSONResponse(content={"is_user_valid": True})
    except:
        return JSONResponse(content={"is_user_valid": False})


def login(db: Session, user: schemas.UserSchema):
    try:
        stored_user = db.query(models.User).first()
        if stored_user.email != user.email:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Invalid credentials"},
            )
        if stored_user.password != user.password:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Invalid credentials"},
            )
        return JSONResponse(
            content={"email": stored_user.email, "username": stored_user.username}
        )
    except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Invalid credentials"},
        )
