from pydantic import BaseModel


class RequestModel(BaseModel):
    pass


class PageInfoRequestModel(BaseModel):
    page_num: int
    page_size: int
