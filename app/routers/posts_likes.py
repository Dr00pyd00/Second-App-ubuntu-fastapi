from typing import Annotated

from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.posts_likes_service import create_post_like_service, delete_post_like_service
from app.models.users import User
from app.dependencies.jwt import get_current_user
from app.schemas.posts_likes import PostLikeFromDbSchema




router = APIRouter(
    prefix="/posts",
    tags=["posts_likes"]
)



# CREATE LIKE :
@router.post("/{post_id}/like", status_code=status.HTTP_201_CREATED, response_model=PostLikeFromDbSchema)
def create_post_like(
    post_id: Annotated[int, Path(..., description="the post ID to like")],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
)->PostLikeFromDbSchema:
    
    return create_post_like_service(
        user_id=current_user.id,
        post_id=post_id,
        db=db,
    )


# DELETE LIKE:
@router.delete("/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_like(
    current_user: Annotated[User, Depends(get_current_user)],
    post_id: Annotated[int, Path(..., description="the post ID to like")],
    db: Annotated[Session, Depends(get_db)],
)-> None:
    
    return delete_post_like_service(
        user_id=current_user.id,
        post_id=post_id,
        db=db,
    )