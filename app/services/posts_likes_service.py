from sqlalchemy.orm import Session

from app.services.users_service import get_user_by_id_or_404
from app.services.post_service import get_post_by_id_or_404
from app.models.posts_likes import PostLike
from app.errors_msg.posts_likes import ERROR_LIKE_ALREADY_EXIST, ERROR_LIKE_DOESNT_EXIST
from app.core.logging_config import get_logger

logger = get_logger(__name__)



# pour creation: 
    # etre connecter current : fait par le router
    # user exist? : get or 404
    # posts exist : get or 404
    # creation du like
    # return un schema ?

def create_post_like_service(
        user_id: int,
        post_id: int,
        db: Session,
)->PostLike:
    # checks rapide
    post = get_post_by_id_or_404(post_id=post_id, db=db)
    user = get_user_by_id_or_404(id=user_id, db=db)

    # gestion doublons :
    existing_like = db.query(PostLike).filter(
        PostLike.user_id == user_id,
        PostLike.post_id == post_id
        ).first()

    if existing_like:
        logger.warning(f"Attempt by User ID:{user_id} to Like Post ID:{post_id} but already liked.")
        raise ERROR_LIKE_ALREADY_EXIST

    like = PostLike(
        user_id=user_id,
        post_id=post_id
    )
    db.add(like)
    db.commit()
    db.refresh(like)
    logger.info(f"Post ID:{post_id} liked by User ID:{user_id}.")

    return like



def delete_post_like_service(
        user_id: int, 
        post_id: int,
        db: Session
)->None:
     # checks rapide
    post = get_post_by_id_or_404(post_id=post_id, db=db)
    user = get_user_by_id_or_404(id=user_id, db=db)
    
    # verification si le like existe vraiment: 
    existing_like = db.query(PostLike).filter(
        PostLike.user_id == user_id,
        PostLike.post_id == post_id
        ).first()

    if not existing_like:
        logger.warning(f"Attempt by User ID:{user_id} to UnLike Post ID:{post_id} Post NOT liked.")
        raise ERROR_LIKE_DOESNT_EXIST

    db.delete(existing_like)
    db.commit()
    logger.info(f"Post ID:{post_id} unliked by User ID:{user_id}.") 
    return
   
    
