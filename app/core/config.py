from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):

    # database:
    postgres_user : str = Field(..., env="POSTGRES_USER")
    postgres_password : str = Field(..., env="POSTGRES_PASSWORD")
    postgres_host : str = Field(default="localhost", env="POSTGRES_HOST")
    postgres_port : int = Field(default=5432, env="POSTGRES_PORT")
    postgres_database_name : str = Field(..., env="POSTGRES_DATABASE_NAME")

    # security:
    secret_key : str = Field(..., env="SECRET_KEY")
    algorithm : str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes : int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # je met l'url pour la db ici 
    @property
    def db_url(self):
        return (
            f"postgresql://{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_database_name}"
        )


    # config sert a gerer la config de la class:
    class Config:
        env_file = ".env"  # dit ou chercher.
        case_sensitive = False

# crée une instance a utiliser pour mon app:
settings = Settings() 
