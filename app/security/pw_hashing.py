from passlib.context import CryptContext

"""
⚠️ Installation correcte de bcrypt / passlib (important)

bcrypt et passlib peuvent être incompatibles selon les versions
(Python 3.12 notamment). Si les versions ne sont pas alignées,
l'application peut crasher AVANT même le hashing des mots de passe.

Procédure recommandée :

1) Désinstaller les versions existantes :
   pip uninstall passlib bcrypt -y

2) Installer des versions compatibles et stables :
   pip install passlib==1.7.4 bcrypt==4.1.2

3) Figer les versions dans requirements.txt pour éviter
   les bugs futurs liés aux mises à jour automatiques.

Ces versions sont utilisées couramment en production
avec FastAPI + SQLAlchemy.
"""


pw_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# Hashing a password:
def hash_pw(password:str)->str:
    return pw_context.hash(password)

# Verification (true or false validation):
def verify_password(plain_pw:str, db_pw:str)->bool:
    return pw_context.verify(plain_pw, db_pw)

