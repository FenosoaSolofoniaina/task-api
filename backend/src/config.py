from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings) :

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # TOKEN CONFIGURATION
    TOKEN_TTL: int = Field(validation_alias='TOKEN_TTL_HOURS')
    JWT_SECRET_KEY: str = Field(validation_alias='JWT_SECRET_KEY')
    JWT_ALGORITHM: str = Field(validation_alias='JWT_ALGORITHM')
    
    # DATABASE CONFIGURATION
    DB_NAME: str = Field(validation_alias='SQLITE_DBNAME')

    # SECURITY ATTEMPT
    MAX_ATTEMPTS: int = Field(validation_alias='MAX_ATTEMPTS')
    DURATION_ATTEMPTS_SECONDS: int = Field(validation_alias='DURATION_ATTEMPTS_SECONDS')

    

settings = Settings()