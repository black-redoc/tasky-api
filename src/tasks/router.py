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


@router.get("/tasks/", response_model=list[schemas.TaskSchema])
async def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = service.get_tasks(db, skip=skip, limit=limit)
    return users


@router.post(
    "/tasks/",
    response_model=schemas.TaskSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_tasks(
    task: schemas.TaskSchema,
    db: Session = Depends(get_db),
):
    return service.create_task(db, task)


@router.put("/tasks/", response_model=schemas.TaskSchema)
async def update_project(task: schemas.TaskSchema, db: Session = Depends(get_db)):
    return service.update_task(db, task)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def delete_project(task_id: int, db: Session = Depends(get_db)):
    return service.delete_task(db, task_id)
