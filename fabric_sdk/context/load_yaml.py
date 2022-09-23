from yaml import load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from fabric_sdk.__env__ import FABRIC_PYTHON_SDK_NETWORK_CONFIG
import os
from .context import Context


def load_network_config() -> Context:
    config_path = os.getenv(FABRIC_PYTHON_SDK_NETWORK_CONFIG)

    with open(config_path, 'r') as config_file:
        config = config_file.read()
        config = load(config, Loader=Loader)

    return Context(config)
