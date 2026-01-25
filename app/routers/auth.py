from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm   # va chercher "username" et "password" dans header
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.token import TokenBearerCreatedSchema
from app.services.users_service import auth_user_service

router = APIRouter(
    tags=["authentication"]
)


# Login : 
@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenBearerCreatedSchema)
async def login(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
)->TokenBearerCreatedSchema:

    return auth_user_service(user_creds=user_credentials, db=db)