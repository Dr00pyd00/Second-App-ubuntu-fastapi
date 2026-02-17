from fastapi import HTTPException, status


# si un post n'est pas trouvé 
def error_post_not_found_by_id(id:int)-> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with ID:{id} NOT FOUND..."
    )


#====== Soft Delete =========================

ERROR_NOT_CURRENT_USER_POST  = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Current user is not Post owner"
)

# si le post a deja ete delete et que je veux delete par dessus:
ERROR_ALREADY_SOFT_DELETED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Post already soft-deleted."
)


# si on essai de restore un post pas soft deleted:
ERROR_TRY_RESTORE_UNDELETED_POST = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Post you try to restore, is not deleted."
)