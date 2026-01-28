from fastapi import HTTPException, status


ERROR_LIKE_ALREADY_EXIST = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail=f"This post is already liked..."
)

ERROR_LIKE_DOESNT_EXIST = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"This like doesnt exist..."
)