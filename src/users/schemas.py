from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    id: int | None = None
    username: str | None = None
    email: str | None = None
    password: str | None = None

    model_config = ConfigDict(from_attributes=True)
