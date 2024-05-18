from pydantic import BaseModel, ConfigDict

from src.tasks.schemas import TaskSchema


class ProjectSchema(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None
    tasks: list[TaskSchema] | None = []

    model_config = ConfigDict(from_attributes=True)
