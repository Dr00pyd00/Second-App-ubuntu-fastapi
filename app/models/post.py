from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean,nullable=False, server_default=text("TRUE"))
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("NOW()"),
    )

    # pour les user_owner:

    # FK: on met  "table.colonne" que l'on veut associer.
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable= False,
    )    
    # pythonic: effet miroire back pop doit correspondre a l'autre table
    # on associe le CLASS voulu "" pour eviter circulaire.
    owner = relationship("User", back_populates="own_posts")

    # pour les likes:

    likes = relationship("PostLike", 
                        back_populates="post_liked",
                        cascade="all, delete-orphan")
