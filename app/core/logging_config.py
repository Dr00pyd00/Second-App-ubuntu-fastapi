import logging
import sys 
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logging() -> None:
    """Config for PARENT logger.

    - Run it ONE time in main.py
    """

    # cree le dossier logs a la racine du projet
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True) # => si le dossier existe deja ne leve pas d'erreur et continue.

    # Format des logs:
    log_format = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console Handler ======================
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    console_handler.setLevel(logging.INFO)

    # File (GENERAL) "app.log" Handler =================
    file_general_handler = RotatingFileHandler(
        filename= log_dir / "app.log",
        maxBytes=1024*1024*10, # 10mo
        backupCount=5,
        encoding="utf-8", # permet char speciaux, emoticones etc
    )
    file_general_handler.setFormatter(log_format)
    file_general_handler.setLevel(logging.INFO)

    # File (ERRORS) "errors.log" Handler ===============
    file_errors_handler = RotatingFileHandler(
        filename= log_dir / "errors.log",
        maxBytes=1024*1024*10, # 10mo
        backupCount=5,
        encoding="utf-8", # permet char speciaux, emoticones etc
    )
    file_errors_handler.setFormatter(log_format)
    file_errors_handler.setLevel(logging.ERROR)


    # ICI  je creer un logger ROOT : je donne pas de nom ca en fait le PARENT
    # chaque logger nommé sera un enfant de celui ci.

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

        # j'ajoute tout les handler a ce root donc les enfants aurant les meme handlers
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_general_handler)
    root_logger.addHandler(file_errors_handler)
    

    ### Reduction des bruits: 
    # des package ont leurs propres logger : uvicorn / sqlalchemy par exemple
    # le logger root va les recuperer automatiquement donc je dois reduire leurs level sinon je vais voir chaque log uvicorn..

        # uvicorn:
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

        # sqlalchemy
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)




def get_logger(name:str) -> logging.Logger:
    """Return a logger for a specific module.

    Args:
        name (str): name of the project module ( __name___)

    Returns:
        logging.Logger: logger with root_logger config
    """

    return logging.getLogger(name)


        