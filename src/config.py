from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SESSION_MIDDLEWARE_KEY: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    
    model_config = SettingsConfigDict(
        env_file=".env"
    )
    
config = Settings() # type: ignore
