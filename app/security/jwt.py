from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from app.errors_msg.jwt import ERROR_CREDENTIALS_JWT
from app.models.users import User
from app.services.users_service import get_user_by_id_or_404


SECRET_KEY = "patate2000"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Token creation with :
        # sub
        # exp
        # iat

def create_access_token(data:dict)->str:
    to_encode = data.copy()

    # expiration setup:
    now = datetime.now(timezone.utc)
    created_at = int(now.timestamp())
    expiration_time = int((now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
    # conversion en timestamp():float mais pour la gestion du token il faut du int donc ca supprime les micros secondes.

    to_encode.update({"iat":created_at,
                      "exp":expiration_time
                      })
    
    return jwt.encode(
        claims=to_encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )


# verify the token payload etc:
def verify_access_token(token:str)-> int | None:
    try:    
        payload = jwt.decode(
            token=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id: str | None = payload.get("sub")
        if not user_id:
            raise ERROR_CREDENTIALS_JWT
        
        return int(user_id)
    except JWTError:
        raise ERROR_CREDENTIALS_JWT

