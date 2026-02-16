from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field


class Settings(BaseSettings):

    model_config = ConfigDict(env_file=".env")

    # database:
    postgres_user : str  
    postgres_password : str 
    postgres_host : str = "localhost"
    postgres_port : int = 5432
    postgres_database_name : str 

    # security:
    secret_key : str 
    algorithm : str  = "HS256"
    access_token_expire_minutes : int = 30

    # je met l'url pour la db ici 
    @property
    def db_url(self):
        """ Build complete url for sql"""
        return (
            f"postgresql://{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_database_name}"
        )


    # config sert a gerer la config de la class: DEPRECATED
    # class Config:
    #     env_file = ".env"  # dit ou chercher.
    #     case_sensitive = False

# crée une instance a utiliser pour mon app:
settings = Settings() 
