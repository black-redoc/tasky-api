from pydantic import BaseModel, ConfigDict


class TaskSchema(BaseModel):
    id: int | None = None
    title: str
    status: str
    project_id: int
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)
