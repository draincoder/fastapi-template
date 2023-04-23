import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class DBConfig:
    type: str | None = None
    connector: str | None = None
    host: str = "localhost"
    port: int = 5432
    login: str = ""
    password: str = ""
    name: str = "test"
    path: str | None = None
    echo: bool = False

    @property
    def uri(self):
        if self.type in ("mysql", "postgresql"):
            url = (
                f"{self.type}+{self.connector}://"
                f"{self.login}:{self.password}"
                f"@{self.host}:{self.port}/{self.name}"
            )
        elif self.type == "sqlite":
            url = f"{self.type}://{self.path}"
        else:
            raise ValueError("DB_TYPE not mysql, sqlite or postgres")
        logger.debug(url)
        return url
