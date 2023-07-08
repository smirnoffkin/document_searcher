from pydantic import BaseSettings, PostgresDsn


class DefaultSettings(BaseSettings):
    POSTGRES_DEALECT_DRIVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    @property
    def database_url(self):
        return PostgresDsn.build(
            scheme=self.POSTGRES_DEALECT_DRIVER,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=f"/{self.POSTGRES_DB}",
        )

    @property
    def async_database_url(self):
        return PostgresDsn.build(
            scheme=f"{self.POSTGRES_DEALECT_DRIVER}+asyncpg",
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=f"/{self.POSTGRES_DB}",
        )

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def broker_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    ELASTICSEARCH_URL: str

    class Config:
        env_file = ".env"


settings = DefaultSettings()
