import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.core.database import Base, get_db


# creation d'une fausse db pour les tests:

SQLALCHEMY_URL_TEST = "sqlite:///./test.db"

# on utilise sqlite un fichier local pas un server!
engine = create_engine(
    url=SQLALCHEMY_URL_TEST,
    connect_args={"check_same_thread":False} # required by sqlite!
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine   # cette fois relié a sqlite local
)

# creer une session de db pour chaque fonction testé:
@pytest.fixture(scope="function")
def db_session():
    """db creation for each test functions"""
    # creation de toutes les tables:
    Base.metadata.create_all(bind=engine)
    # on créé la session:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        # on supprime toute les tables creers pour le test.
        Base.metadata.drop_all(bind=engine) # toujours avant de close!
        db.close()

    
# Maintenant on créé un client ( navigateur viruel ou postman perso):

@pytest.fixture(scope="function")
def client(db_session: Session):
    """
    Creation d'un client de test qui utilisera la db test plus haut.

    1. Override get_db pour utiliser db_session qu'on a créé plus haut en slqlite
    2. Crée un TestClient
    3. aprés le test resttore le get_db ( del l'override)
    """

    # OVERRIDE : remmplace get_db dans tout le code:
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    # Dit à FastAPI : "Quand tu vois Depends(get_db), utilise override_get_db"
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()