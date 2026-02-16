from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings


# SQLALCHEMY_URL = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_port}/{settings.postgres_database_name}"

engine = create_engine(settings.db_url)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()

# generator::w

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()