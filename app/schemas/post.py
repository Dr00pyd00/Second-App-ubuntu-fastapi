from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.schemas.users import UserDataFromDbSchema


class PostAllDataSchema(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    published: bool = False


class PostDataToCreateSchema(BaseModel):
    title: str
    content: str
    published: Optional[bool] = False

class PostDataFromDbSchema(BaseModel):
    id: int
    title: str
    content: str
    published: Optional[bool] = False
    owner: UserDataFromDbSchema

    model_config = {"from_attributes":True}

