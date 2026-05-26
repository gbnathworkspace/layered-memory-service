from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_uri: str
    mongodb_db: str = "layered_memory"
    api_key: str
    openai_api_key: str

    model_config = {"env_file": ".env"}


settings = Settings()
