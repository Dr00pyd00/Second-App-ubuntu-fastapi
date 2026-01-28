from sqlalchemy.orm import Session

from app.models.users import User
from app.schemas.users import UserCreateSchema, UserDataFromDbSchema
from app.schemas.users import UserOauth2PwUsernameSchema
from app.security.pw_hashing import hash_pw 
from app.errors_msg.users import error_username_taken, error_user_not_found_by_id, ERROR_USER_INVALID_CREDENTIALS
from app.security.pw_hashing import verify_password
from app.security.jwt import create_access_token
from app.schemas.token import TokenBearerCreatedSchema, TokenSubDataSchema



# Service for Users in db:

# get user or send a 404 HTTPException:
def get_user_by_id_or_404(id:int, db:Session)->User | None:
    user = db.query(User).filter(User.id == id).first()
    if not user:
        error_user_not_found_by_id(id=id)
    return user

# Create user:
def create_user_service(
        data: UserCreateSchema,
        db: Session,
)->User:
    
    # check if username alreaady exist:
    existing_user = db.query(User).filter(User.username == data.username).first()
    if existing_user:
        error_username_taken(username=data.username)
    # hash the password:
    user_dict = data.model_dump()
    user_dict["password"] = hash_pw(user_dict["password"])
    new_user = User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# authentication of a user:
def auth_user_service(
        user_creds:UserOauth2PwUsernameSchema,
        db:Session,
)->TokenBearerCreatedSchema:
    user = db.query(User).filter(User.username == user_creds.username).first()
    if not user:
        raise ERROR_USER_INVALID_CREDENTIALS
    if not verify_password(user_creds.password, user.password):
        raise ERROR_USER_INVALID_CREDENTIALS
    
    # si tout est ok:
    token = create_access_token(TokenSubDataSchema(sub=str(user.id))) 

    return {"access_token":token,
            "token_type":"bearer"}