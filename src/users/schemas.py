from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    id: int | None = None
    username: str | None = None
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)
