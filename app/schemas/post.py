from pydantic import BaseModel, Field
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
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="title for post: 1 to 200 characters."
    )
    content: str = Field(
        ...,
        min_length=1,
        max_length=100000,
        description="content of the post: 1 to 100000 characters."
    )
    published: Optional[bool] = True

class PostDataFromDbSchema(BaseModel):
    id: int
    title: str
    content: str
    published: Optional[bool] = False
    owner: UserDataFromDbSchema
    status: str
    deleted_at: datetime | None

    model_config = {"from_attributes":True}

