from yaml import load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from fabric_sdk.__env__ import FABRIC_PYTHON_SDK_NETWORK_CONFIG
import os
from .context import ContextClient, ConfigManager

import os


def Context(client_name=None, network_name=None) -> ContextClient:
    config_path = os.getenv(FABRIC_PYTHON_SDK_NETWORK_CONFIG)
    manager = ConfigManager()

    dir_list = os.listdir(config_path)
    dir_list = [file for file in dir_list if file.endswith('.yaml')]
    for file in dir_list:
        path = f'{config_path}/{file}'
        with open(path, 'r') as config_file:
            config = config_file.read()
            config = load(config, Loader=Loader)
            manager.add_new_config(path, config)
            config_file.close()

    return manager.client_compile(client_name, network_name)
