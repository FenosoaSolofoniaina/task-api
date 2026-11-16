from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path



_PROJECT_DIR = Path(__file__).resolve().parent.parent
_DATA_DIR = _PROJECT_DIR / "data"
_DATA_DIR.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings) :

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    #
    @property
    def PROJECT_JSON_DIR(self) :
        return _PROJECT_DIR / "jsons"
    
    # TOKEN CONFIGURATION
    JWT_SECRET_KEY: str = Field(validation_alias='JWT_SECRET_KEY')
    JWT_ALGORITHM: str = Field(validation_alias='JWT_ALGORITHM')
    ACCESS_TOKEN_TTL: int = Field(validation_alias='ACCESS_TOKEN_TTL_MINUTES')
    
    # DATABASE CONFIGURATION
    DB_NAME: str = Field(validation_alias='SQLITE_DBNAME')
    
    @property
    def DB_PATH(self) -> str :
        return f"sqlite:///{_DATA_DIR}/{self.DB_NAME}"

    # SECURITY ATTEMPT
    MAX_ATTEMPTS: int = Field(validation_alias='MAX_ATTEMPTS')
    DURATION_ATTEMPTS_SECONDS: int = Field(validation_alias='DURATION_ATTEMPTS_SECONDS')

    # Allow Origins
    FRONTEND_URL:str = Field(validation_alias='FRONTEND_URL')

    ROUT_PREFIX: str = "/api/v1"

    

settings = Settings()