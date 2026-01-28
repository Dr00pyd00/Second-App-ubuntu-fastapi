"""
post_service.py

Ce module contient la logique métier pour les posts.

Principe :
- Toutes les fonctions sont indépendantes de FastAPI.
- Elles reçoivent les données et la session SQLAlchemy.
- Elles gèrent les opérations sur la base (CRUD) et les erreurs métier (ex: post non trouvé).

Objectif :
- Centraliser la logique métier pour éviter les duplications.
- Faciliter les tests unitaires sans serveur HTTP.
- Rendre le code réutilisable par plusieurs routes ou scripts.

Résumé :
Service = métier et base de données. 
Le router se contente de décrire l'API et d'invoquer le service.
"""


from sqlalchemy.orm import Session

from app.models.post import Post
from app.errors_msg.post import error_post_not_found_by_id
from app.schemas.post import PostDataToCreateSchema, PostDataFromDbSchema


# Service: Gestion CRUD for database = retrieve, select, modify.


# Chercher un post sinon renvoyer un 404:
def get_post_by_id_or_404(post_id:int, db:Session)->Post | None:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        error_post_not_found_by_id(id=post_id)
    return post


# Create post:
def create_post_service(
        data: PostDataToCreateSchema,
        db: Session,
        user_id: int
)->Post:
    post = Post(**data.model_dump(), user_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

# Update post:
def update_post_service(
    post_id: int,
    data: PostDataToCreateSchema,
    db: Session,
)->Post:
    post = get_post_by_id_or_404(post_id=post_id, db=db)
    for k,v in data.model_dump().items():
        setattr(post,k,v)
    db.commit()
    db.refresh(post)
    return post

# Delete post:
def delete_post_service(
    post_id: int,
    db: Session
)->None:
    post = get_post_by_id_or_404(post_id=post_id, db=db)
    db.delete(post)
    db.commit()
