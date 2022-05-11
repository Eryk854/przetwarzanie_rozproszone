from typing import Any

import yaml


def read_config_value(key: str) -> Any:
    with open("config.yaml", "r") as file:
        value = yaml.load(file, Loader=yaml.FullLoader)
        value = value[key]
        return value
