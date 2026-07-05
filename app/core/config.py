from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LLM_PROVIDER: str = "ollama"
    LLM_MODEL: str = "ollama/llama3.2"
    LLM_ENDPOINT: str = "http://localhost:11434"

    EMBEDDING_PROVIDER: str = "ollama"
    EMBEDDING_MODEL: str = "ollama/llama3.2"
    EMBEDDING_ENDPOINT: str = "http://localhost:11434"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()