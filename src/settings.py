from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    postgres_host: str
    postgres_database_name: str
    postgres_password: str
    postgres_port: int
    postgres_username: str

    kafka_brokers: str = "localhost:9092"
    kafka_topic_ads: str = "ads"
    kafka_consumer_group: str = "search-service"

    ad_service_url: str = "http://localhost:8000"

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_username}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_database_name}"
