from app.core.database import Base

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql.expression import text




class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default="TRUE")
    email = Column(String, nullable=True, unique= True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("NOW()")
    )

    # ca correspond au filed contenu dans Post
    # "all": tout les type de modifs prit en compte
    # "delete-orphan": supprimer les post dont les User n'existe plus
    own_posts = relationship("Post", back_populates="owner", cascade="all, delete-orphan" )

    # pour les likes:
    likes = relationship("PostLike",
                        back_populates="like_owner",
                        cascade="all, delete-orphan")
