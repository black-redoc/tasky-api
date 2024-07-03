from typing import Annotated
from fastapi import APIRouter, Depends, status, Cookie
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


@router.get("/projects/", response_model=list[schemas.ProjectSchema])
async def read_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    session: Annotated[str | None, Cookie()] = None,
):
    projects = service.get_projects(db, skip=skip, limit=limit)
    return projects


@router.post(
    "/projects/",
    response_model=schemas.ProjectSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    project: schemas.ProjectSchema,
    db: Session = Depends(get_db),
):
    return service.create_project(db, project)


@router.put("/projects/", response_model=schemas.ProjectSchema)
async def update_project(project: schemas.ProjectSchema, db: Session = Depends(get_db)):
    return service.update_project(db, project)


@router.delete("/projects/{project_id}", status_code=status.HTTP_200_OK)
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    return service.delete_project(db, project_id)
