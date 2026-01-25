
from pydantic import BaseModel


# token data out from browser:
class TokenBearerCreatedSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


# for "sub"
class TokenSubDataSchema(BaseModel):
    sub: str