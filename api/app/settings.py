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


class ProductionSettings(Settings):
    pass


class DevelopmentSettings(Settings):
    fastapi_debug: bool = True


class TestingSettings(Settings):
    pass


settings: Settings = globals()[os.environ.get("ENVIRONMENT", "Testing") + "Settings"]()
