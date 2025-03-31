from pydantic import BaseModel


class UserAuthInfo(BaseModel):
    sub_id: str
