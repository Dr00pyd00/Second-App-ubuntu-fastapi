from enum import Enum as PyEnum
from sqlalchemy import Column, Enum as sqlEnum
from sqlalchemy.orm import Session

# Mon enum python:
# pas DELTE dedans car on fait un mixin expres pour
class StatusEnum(PyEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    SIGNALED = "signaled"


# Mixins que je peux ajouter ( Parent ) dans mes objets tables
class StatusMixin:

    status = Column(
                    sqlEnum(StatusEnum, name="status_enum", create_type=False), 
                    default=StatusEnum.ACTIVE, 
                    nullable=False,
                    server_default="ACTIVE"

                    )

    @classmethod
    def query_visible(cls, session:Session):
        """return que les objets actifs"""
        return session.query(cls).filter(
            cls.status == StatusEnum.ACTIVE,
            cls.deleted_at.is_(None),
            )