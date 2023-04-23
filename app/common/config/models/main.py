from dataclasses import dataclass

from app.common.config.models.paths import Paths
from app.infrastructure.db.config.models.db import DBConfig


@dataclass
class Config:
    paths: Paths
    db: DBConfig
