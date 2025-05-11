from pydantic import BaseModel, ConfigDict


class UserRead(BaseModel):
    username: str
    model_config = ConfigDict(from_attributes=True)
