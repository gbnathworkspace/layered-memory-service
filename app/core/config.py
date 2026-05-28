from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_uri: str
    mongodb_db_name: str = "layered_memory"
    voyage_api_key: str
    memory_service_api_key: str
    log_level: str = "INFO"

    model_config = {"env_file": ".env"}


settings = Settings()
