import logging
import os
import sys

from pydantic_settings import BaseSettings


__all__ = ["settings"]


LOG = logging.getLogger("app")
if "pytest" not in sys.modules:
    LOGGING = {
        "version": 1,
        "formatters": {"simple": {"format": "{levelname} {message}", "style": "{"}},
        "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "simple"}},
        "loggers": {"fm": {"handlers": ["console"]}},
    }


class Settings(BaseSettings):
    fastapi_debug: bool = False
    elastic_url: str = None
    elastic_user: str = "elastic"
    elastic_password: str = None
    elastic_index: str = "geophotoradar"
    api_import_token: str = None


class ProductionSettings(Settings):
    pass


class DevelopmentSettings(Settings):
    fastapi_debug: bool = True
    elastic_url: str = "http://es01:9200"
    elastic_password: str = "geophotoradar"
    api_import_token: str = "dataimporttoken"


class TestingSettings(Settings):
    elastic_url: str = "http://localhost:9201"
    elastic_password: str = "geophotoradar"
    elastic_index: str = "testing"
    api_import_token: str = "testtoken"


class TestingDockerSettings(Settings):
    elastic_url: str = "http://elasticsearch:9200"
    elastic_password: str = "geophotoradar"
    elastic_index: str = "testing"
    api_import_token: str = "testtoken"


settings: Settings = globals()[os.environ.get("ENVIRONMENT", "Testing") + "Settings"]()
