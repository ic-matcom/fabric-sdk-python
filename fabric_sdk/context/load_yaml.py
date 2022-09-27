from yaml import load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from fabric_sdk.__env__ import FABRIC_PYTHON_SDK_NETWORK_CONFIG
import os
from .context import ContextClient, ConfigManager


def Context(client_name=None, network_name=None) -> ContextClient:
    config_path = os.getenv(FABRIC_PYTHON_SDK_NETWORK_CONFIG)
    manager = ConfigManager()

    with open(config_path, 'r') as config_file:
        config = config_file.read()
        config = load(config, Loader=Loader)

    return manager.client_compile(client_name, network_name)
