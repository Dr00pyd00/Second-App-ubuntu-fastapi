"""
posts.py (router)

Ce module expose les endpoints HTTP pour gérer les posts.

Principe :
- Décrit les routes, méthodes HTTP, status codes et schémas Pydantic.
- Injecte la session DB et les données via Depends() et Body().
- Ne contient pas de logique métier : toutes les opérations sont déléguées à post_service.py.

Objectif :
- Séparer clairement le transport HTTP de la logique métier.
- Améliorer la lisibilité, la testabilité et la maintenance.
- Permettre aux développeurs et recruteurs de comprendre immédiatement la structure.

Résumé :
Router = interface HTTP
Service = logique métier
Cette séparation rend le projet professionnel et évolutif.
"""


from app.core.database import get_db
from app.schemas.post import PostDataFromDbSchema, PostDataToCreateSchema
from app.models.post import Post
from app.models.users import User
from app.services.post_service import get_post_by_id_or_404, create_post_service, update_post_service, delete_post_service
from app.dependencies.jwt import get_current_user

from fastapi import APIRouter, Depends,status, Body, Path
from sqlalchemy.orm import Session
from typing import List, Annotated


# Endpoints for FASTAPI / posts:


router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

#===============================#
#====== CRUD ===================#
#===============================#


# ALL:
@router.get("/", status_code=status.HTTP_200_OK, response_model= List[PostDataFromDbSchema])
async def get_all_posts(db:Session=Depends(get_db)):
    posts = db.query(Post).all()
    return posts


# DETAIL by ID:
@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostDataFromDbSchema)
async def post_detail_by_id(
    post_id:int,
    db:Session=Depends(get_db)
):
    return get_post_by_id_or_404(post_id=post_id, db=db)    


# CREATE:
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostDataFromDbSchema)
async def create_post(
    post_fields: Annotated[PostDataToCreateSchema, Body()],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):

    return create_post_service(data=post_fields, db=db, user_id=current_user.id)


# UPDATE by ID:
@router.put("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostDataFromDbSchema)
async def update_post_by_id(
    post_id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
    post_new_fields: Annotated[PostDataToCreateSchema, Body()],
):
    return update_post_service(post_id=post_id, data=post_new_fields, db=db)


# DELETE by ID:
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_by_id(
    post_id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
)->None:
    delete_post_service(post_id=post_id, db=db)

    