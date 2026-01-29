
# Second app with fastapi.

Upgrape the precision of my code.

-Annotated


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
