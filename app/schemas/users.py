from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import re


# Create a user:
class UserCreateSchema(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username: 3 to 50 characters."
    )
    password: str = Field(
        ...,
        min_length=5,
        max_length=80,
        description="user password: 5 to 80 characters"
    )
    is_active : bool = True

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, name:str)->str:
        if re.match(r'^[a-zA-Z0-9_]+$', name) is None:
            raise ValueError("<username> must be alphanumeric only (can contain '_').")
        return name

    @field_validator("password")
    @classmethod
    def password_complexity(cls, user_password:str)->str:

        if not any(char.isdigit() for char in user_password):
            raise ValueError("password must have at least ONE digit.")
        if not any(char.isalpha() for char in user_password):
            raise ValueError("password must have at least ONE alphabetic symbol.")

        return user_password


#  Data client can see:
class UserDataFromDbSchema(BaseModel):
    id: int
    username: str
    is_active : bool
    created_at : datetime

    model_config = {"from_attributes":True}

# what the Oauth2PasswordRequest have to give:
class UserOauth2PwUsernameSchema(BaseModel):
    username: str
    password: str
