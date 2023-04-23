from app.api.config.models.main import AppConfig
from app.api.config.parser.api import load_auth_config, load_api_config
from app.common.config.models.paths import Paths
from app.common.config.parser.config_file_reader import read_config
from app.common.config.parser.main import load_config


def load_app_config(paths: Paths) -> AppConfig:
    config_dct = read_config(paths)
    return AppConfig.from_base(
        base=load_config(paths, config_dct),
        api=load_api_config(config_dct['api']),
        auth=load_auth_config(config_dct['auth'])
    )
