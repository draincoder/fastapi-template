from app.infrastructure.db.config.models.db import DBConfig


def load_db_config(db_dict: dict) -> DBConfig:
    return DBConfig(
        type=db_dict.get("type"),
        connector=db_dict.get("connector"),
        host=db_dict.get("host"),
        port=db_dict.get("port"),
        login=db_dict.get("login"),
        password=db_dict.get("password"),
        name=db_dict.get("name"),
        path=db_dict.get("path"),
        echo=db_dict.get("echo"),
    )
