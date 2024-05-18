from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.orm import Session

from . import models, schemas


def get_projects(db: Session, skip: int, limit: int):
    return db.query(models.Project).offset(skip).limit(limit).all()


def get_project_by_title(db: Session, title: str):
    try:
        project = db.query(models.Project).filter(models.Project.title == title).first()
        if not project:
            raise Exception(f"Project {title} not found")
        return project
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": e.args[0] if e.args else str(e)},
        )


def create_project(db: Session, project: schemas.ProjectSchema):
    try:
        model = models.Project(**project.model_dump())
        db.add(model)
        db.commit()
        db.refresh(model)
        return model
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": e.args[0] if e.args else str(e)},
        )


def delete_project(db: Session, project_id: int):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Project not found"},
        )

    db.delete(project)
    db.commit()
    return JSONResponse(
        status_code=200, content={"message": "Project deleted successfully"}
    )


def update_project(db: Session, project: schemas.ProjectSchema):
    try:
        update_project = (
            db.query(models.Project).filter(models.Project.id == project.id).first()
        )

        if not update_project:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": "Project not found"},
            )

        for key, value in project.model_dump().items():
            setattr(update_project, key, value) if value else None
        db.commit()
        db.refresh(update_project)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": e.args[0] if e.args else str(e)},
        )
    return update_project
