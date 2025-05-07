from pydantic import BaseModel, ConfigDict


class UserRead(BaseModel):
    username: str
