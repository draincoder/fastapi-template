from app.common.config.models.main import Config
from app.common.config.models.paths import Paths
from app.infrastructure.db.config.parser.db import load_db_config


def load_config(paths: Paths, config_dct: dict) -> Config:
    return Config(
        paths=paths,
        db=load_db_config(config_dct["db"])
    )
