from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class BrokerSettings(BaseSettings):
    """Настройки для RabbitMQ"""
    broker_username: str
    broker_password: str
    broker_host: str
    broker_port: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def broker_full_url(self) -> str:
        return (f"amqp://{self.broker_username}:{self.broker_password}@"
                f"{self.broker_host}:{self.broker_port}")


class SMTPSettings(BaseSettings):
    """Настройки для smtp"""
    smtp_service: str
    smtp_port: str
    smtp_email_sender: str
    smtp_email_secret: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Settings(BaseSettings):
    """Все настройки"""
    broker_settings: BrokerSettings
    smtp_settings: SMTPSettings


@lru_cache()
def init_settings():
    """Инициализация настроек"""
    all_settings = Settings(broker_settings=BrokerSettings(), smtp_settings=SMTPSettings())
    return all_settings


settings = init_settings()
