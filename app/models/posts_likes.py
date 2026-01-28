from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from app.core.database import Base



class PostLike(Base):
    __tablename__ = "postlikes"
    # pas de id on s'en fou
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True )
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

    post_liked = relationship("Post", back_populates="likes")
    like_owner = relationship("User", back_populates="likes")