
# Second app with fastapi.

Upgrape the precision of my code.

-Annotated
## 🚀 Installation

1. Clone le repo
```bash
   git clone https://github.com/ton-username/ton-projet.git
   cd ton-projet
```

2. Crée ton fichier .env depuis le template
```bash
   cp .env.example .env
```

3. Édite .env avec tes vraies valeurs
```bash
   nano .env
   # Remplace les valeurs "your_*_here"
```

4. Génère une vraie SECRET_KEY
```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   # Copie le résultat dans .env
```

----------------------------------------------------

## Alembic:

### 1. Installation:
```python
pip install alembic
alembic --version
```

### 2. Initialisation:

```python
alembic init alembic
```

=> ca crée:
```java
alembic/
 ├─ versions/        ← TES MIGRATIONS (sacré)
 ├─ env.py           ← cerveau d’Alembic
 └─ script.py.mako
alembic.ini          ← config globale
```


 ==> Puis aller dans alembic/env.py et modifier target_metada = None.
 
 ==> IMPORTER TOUT LES MODELS!!


 ```python

# models que alembic prend en compte:
from app.models.users import User
from app.models.posts import Post
from app.models.posts_likes import PostLike

# tables :
from app.core.database import Base

 #target_metadata = None
  target_metadata = Base.metadata

```

== > Impoter l'url de SQL puis ajouter au context:

```python 

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", SQLALCHEMY_URL)
```

## Ici de cas:

-Setup au debut ( recommandé ):

Alembic crée tout
    1. init alembic 
    2. ecrires models
    3. generer migration initail
    4. appliquer migration

```bash
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```



-Setup en cours de projet avec un DB deja un peu rempli:

    1. generer une revision (vide ducoup)
    2. dire a alembic que c'est l'etat officiel
    3. continuer normalement

```bash
# veut dire qu'on prend ce point pour reference meme vide
alembic stamp head
```


ATTENTION quand on:


```bash
alembic revision --autogenerate -m "initial schema"
```

=> creer une table "alembic_version" dans la db.


-------------------------

# Ajout d'un Enum dans Postres avec Alembic

Exemple d'un enum pour un mixin:

### -Creation d'un ENUM

```python
from enum import Enum as PyEnum

class StatusEnum(PyEnum):
    ACTIVE = "active"
    DELETED = "deleted"
    ARCHIVED = "archived"
    SIGNALED = "signaled"
```

### -Creation pour Postgres

==> on lance la revision:
```bash 
alembic revision --autogenerate -m'ajout de "status"'
```

==> NE PAS UPGRADE

### Modification explicite de la version alembic generée:

-creer le type (enum)
-ajouter la colonne pour que les anciens rows soient remplis

```python
from alembic import op
from sqlalchemy.dialects import postgresql

def upgrade():
    # Création du type PostgreSQL
    status_enum = postgresql.ENUM("ACTIVE", "DELETED", "ARCHIVED", "SIGNALED", name="status_enum")
    status_enum.create(op.get_bind(), checkfirst=True)  # check_first: ecrase pas le type si deja present

    # Ajout des colonnes
    op.add_column(
        'users',
        sa.Column(
            'status',
            postgresql.ENUM("ACTIVE","DELETED","ARCHIVED","SIGNALED", name="status_enum"),
            nullable=False,
            server_default='ACTIVE'    # ca va remplir les rows deja existantes
        )
    )
```

Et pour le downgrade:

```python
def downgrade():
    op.drop_column('users', 'status')
    status_enum = postgresql.ENUM("ACTIVE", "DELETED", "ARCHIVED", "SIGNALED", name="status_enum")
    status_enum.drop(op.get_bind(), checkfirst=True)

```


==> Ici, tout est pret pour le coté db , mais pas en sqlalchemy.

### -Mixin dans SQLAlchemy

```python
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ENUM as PGEnum

class StatusMixin:
    status = Column(
        PGEnum("ACTIVE", "DELETED", "ARCHIVED", "SIGNALED", name="status_enum"),
        nullable=False,
        server_default='ACTIVE'
    )
```

### Final

```bash 
alembic upgrade head
```


--- 

# .env et dotenv :

Sert a isolé des variables importantes:  

### Creer un fichier .env a la racine:
Dedans on met les trucs importants:

```bash
PASSWD="truc"
```
Puis on les retrouves:

```python
import os 
from dotenv import load_dotenv

# on charge les variables du fichier .env
load_dotenv()

print(os.getenv("PASSWD")) # existe donc renvoi la valeur 
print(os.getenv("YASSWD")) # inexistant return None

print(os.environ["PASSWD"]) # existe ou ERROR 
print(os.environ.get("YASSWD", "truc")) # safer: valeur default
```

### Attention : en .env **Tout est STRING** .


---

## Comment acceder aux variables ? 

> Avec Pydantic-settings

```bash
pip install pydantic-setting
```

On creer une class Settings on l'on setup les variables voulu.

```python
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # les '...' signifie OBLIGATOIRE:
    postgres_user : str = Field(..., env="POSTGRES_USER")
    # on peut mettre une valeur par defaut:
    postgres_port : str = Field(default="localhost", env="POSTGRES_PORT")

    # config sert a gerer la config de la class:
    class Config:
        env_file = ".env"  # dit ou chercher.
        case_sensitive = False

# crée une instance a utiliser pour mon app:
settings = Settings() 
```


---

# Gestion et Validations pydantic avancé:

On met un Field pour etre encore plus precis , puis des foncitons de validations.

```python
from pydantic import Field, field_validator
```

Exemple de field:
```python
class UserSchema(Basemodel):
    username: str = Field(
        ...,  # rend OBLIGATOIRE
        min_length=1,
        max_length=56,
        description="name for user: 1 to 56 char."
    )
```

Ensuite on utilise **field_validatoir** pour cibler un champ:
```python
import re # sert pour regex

@filed_validator('username')
@classmethod # subtil mais: c'est une verification AVANT la creation de l'instance donc on utilise un classmethod car l'instance est pas encore créé.
def username_alphanumeric(cls, name)->str:
    if re.match(r'^[a-zA-Z0-9_]+$', name) is None:
        # re.match compare le regex et la valeur de la func:
            # si ca marche : renvoi un objet regex
            # si marche PAS : renvoi None
        raise ValueError("Username need to be alphanumeric")
    return name
```


--- 

# TESTS 

Dans un dossier tests/ :
- Tout les fichiers commencent par test_
- Il y a un fichier de config : **conftest** -> nom IMPORTANT pour pytest !

```bash
app/tests/
├── conftest.py
├── __init__.py
├── test_auth.py
└── test_users.py
```

Dans **conftest** on creer des objets speciaux pour le test:
- une DB
- un client 

---

On install pytest 
```python
pip install pytest
```

## Conftest.py :

### Creation d'un db test:

```python 
import pytest
from fastapi.testclient import TestClient # feature de test 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.core.database import Base, get_db

SQLITE_URL_TEST = "sqlite:///./test.db"
# url:
# sqlite://  # protocole
# / : root 
# ./ dossier courant

test_engine = create_engine(
    url=SQLITE_URL_TEST,
    connect_args={"check_same_thread":False} # OBLIGATOIRE pour sqlite.
)

# Moyen de communication : generateur de session
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
) 
```

On va creer des **fixtures pytest**.  
Ce sont des functions qui se lancent avant chaque function test pour creer un semblant de setup propre au test (pour ne pas toucher la vrai db par exemple)

```python

# on appel le decorator
# par default le scode est function:
@pytest.fixture(scope="function)
def db_session():
    # on creer toute les table a l'ancienne sans alemnic:
    Base.metadata.create_all(bind=test_engine)
    # on creer une session:
    db = TestgSessionLocal()
    # on fait un gen de session:
    try:
        yield db
    finally:
        # on supprime aussi les tables pour TOUT cleaner:
        Base.metadata.drop_all(bind=test_engine)
        # on close APRES !!
        db.close()
```

Ensuite on creer un **client** (postaman virtuel de test):

```python
@pytest.fixture(scope="function")
# On va utiliser justement la fixture db_session faire juste avant:
def client(db_session: Session):
    # 1. On cree un client qui utilise la db de test cree plus haut.
    # 2. On OVERRIDE le get_db pour utiliser la db de test ( les foncitons dans routers/ ont la dependance get_db donc il faut modifier ca pour que le test soit isole...)
    # 3. Apres le test le get_db doit etre restaure : del l'override

    # Ici on creer la fonction qui va REMPLACER get_db:
    def override_get_db():
        try:
            yield db_session # on apelle la db test!
        finally:
            pass # le reste est gerer dans db_session qui est lui meme un gen

    # Ici on precise bien de remplacer la gonction get_db:
    # "Quand tu vois Depends(get_db) remplace get_db par db_session:
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    # on donne "app" comme on le donnerai a uvicorn
    #  Simule un serveur HTTP EN MÉMOIRE
    #  Pas de port, pas de réseau
    #  Utilise la DB SQLite de test

    # A la fin on enleve l'override:
    app.dependency_overrides.clear()
```

A **chaque** appel d'une fonction test, est charger avant les fixtures.  
Ce qu'il se passe:  
- Une DB est creer pour le test , avec les tables de l'app
- Un client est creer avec un override pour get_db donc les routes du code sont utilisables sans problemes
- Tout est **clean** a la fin car ce sont des generateur qui reset tout apres leurs appels

