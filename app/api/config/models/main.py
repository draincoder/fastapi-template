from dataclasses import dataclass

from .api import AuthConfig, ApiConfig
from app.common.config.models.main import Config


@dataclass
class AppConfig(Config):
    auth: AuthConfig
    api: ApiConfig

    @classmethod
    def from_base(cls, base: Config, auth: AuthConfig, api: ApiConfig):
        return cls(
            paths=base.paths,
            db=base.db,
            api=api,
            auth=auth
        )
