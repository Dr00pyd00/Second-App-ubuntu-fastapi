from fastapi import HTTPException, status



# Error when create with username already taken:
def error_username_taken(username:str)->HTTPException:
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Username \"{username}\" already taken..."
    )

# Error when user no found with ID:
def error_user_not_found_by_id(id:int)-> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user with ID:{id} NOT FOUND..."
    )

# Error for Invalids Credentials login:
ERROR_USER_INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials: Password or Username INVALID"
)