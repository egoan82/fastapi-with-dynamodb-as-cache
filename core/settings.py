import logging
import os
from enum import Enum
from functools import lru_cache
from typing import List, Optional, Tuple

from dotenv import load_dotenv

load_dotenv()


class EnvironmentEnum(str, Enum):
    production = "production"
    local = "local"
    devel = "devel"
    staging = "staging"


class GlobalConfig():
    title: str = "Fastapi with Dynamodb"
    description: str = "Fastapi with Dynamodb"
    root_path: str ="/api/v1"
    docs_url: str = "/docs"
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    version: str = "1.0.0"
    max_connection_count: int = 10
    min_connection_count: int = 10
    api_prefix: str = "/api"
    allowed_hosts: List[str] = ["*"]
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")
    debug: bool = False
    testing: bool = False
    timezone: str = "UTC"
    environment: EnvironmentEnum

    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region_name: str = os.getenv("AWS_REGION_NAME")

    base_url_localstack: str = os.getenv("BASE_URL_LOCALSTACK")


class LocalConfig(GlobalConfig):
    """Local configurations."""

    debug: bool = True
    environment: EnvironmentEnum = EnvironmentEnum.local


class DevelConfig(GlobalConfig):
    """Devel configurations."""

    debug: bool = True
    environment: EnvironmentEnum = EnvironmentEnum.devel


class StagingConfig(GlobalConfig):
    """Staging configurations."""

    debug: bool = True
    environment: EnvironmentEnum = EnvironmentEnum.staging


class ProdConfig(GlobalConfig):
    """Production configurations."""

    debug: bool = False
    environment: EnvironmentEnum = EnvironmentEnum.production


class FactoryConfig:
    def __init__(self, environment: Optional[str]):
        self.environment = environment
        self.configurations_maps = {
            EnvironmentEnum.local.value: LocalConfig,
            EnvironmentEnum.devel.value: DevelConfig,
            EnvironmentEnum.staging.value: StagingConfig,
            EnvironmentEnum.production.value: ProdConfig,
        }

    def __call__(self) -> GlobalConfig:
        return self.configurations_maps[self.environment]()


@lru_cache()
def get_configuration() -> GlobalConfig:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s"
    )
    return FactoryConfig(os.environ.get("ENVIRONMENT"))()


settings = get_configuration()

if settings.environment != EnvironmentEnum.production.value:
    logging.info(f"Loaded config {settings.environment} !!")
