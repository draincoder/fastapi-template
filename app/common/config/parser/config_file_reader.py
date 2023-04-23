import os

import yaml

from app.common.config.models.paths import Paths


def read_config(paths: Paths) -> dict:
    if not (file := os.getenv("CONFIG_FILE")):
        file = "config.yml"
    with (paths.config_path / file).open("r") as f:
        return yaml.safe_load(f)
