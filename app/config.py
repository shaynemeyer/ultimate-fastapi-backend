from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
    env_file="../.env",
    env_ignore_empty=True,
    extra="ignore",
)


class AppSettings(BaseSettings):
    APP_NAME: str = "FastShip"
    APP_DOMAIN: str = "localhost:8000"


class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: str

    model_config = _base_config

    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class SecuritySettings(BaseSettings):

    JWT_SECRET: str
    JWT_ALGORITHM: str
    SECURITY_SALT: str 

    model_config = _base_config


class NotificationSettings(BaseSettings):

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    model_config = _base_config


app_settings = AppSettings()
db_settings = DatabaseSettings()
security_settings = SecuritySettings()
notification_settings = NotificationSettings()
