from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.core.database import get_db
from app.security.jwt import verify_access_token
from app.services.users_service import get_user_by_id_or_404
from app.models.users import User


# Comment la dependance sait ou aller chercher le token:
    # va automatiquement dans le header chercher le bearer.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # precise la page de login pour la doc

# Avoir le User courant:
def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[Session , Depends(get_db)],
)-> User:
    user_id = verify_access_token(token=token)
    user = get_user_by_id_or_404(id=user_id, db=db)
    return user