from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.orm import Session

from . import models, schemas
from src.projects.models import Project


def get_tasks(db: Session, skip: int, limit: int):
    return db.query(models.Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: schemas.TaskSchema):
    try:
        project = db.query(Project).filter(Project.id == task.project_id).first()
        task_title = f"{project.title}:{task.title}"
        model = models.Task(
            title=task_title,
            description=task.description,
            status=task.status,
            project_id=task.project_id,
        )
        db.add(model)
        db.commit()
        db.refresh(model)
        return model
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": e.args[0] if e.args else str(e)},
        )


def update_task(db: Session, task: schemas.TaskSchema):
    try:
        update_task = db.query(models.Task).filter(models.Task.id == task.id).first()

        if not update_task:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": "Task not found"},
            )

        for key, value in task.model_dump().items():
            setattr(update_task, key, value) if value else None
        db.commit()
        db.refresh(update_task)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": e.args[0] if e.args else str(e)},
        )
    return update_task


def delete_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Task not found"},
        )

    db.delete(task)
    db.commit()
    return JSONResponse(
        status_code=200, content={"message": "Task deleted successfully"}
    )
