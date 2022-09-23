from distutils.command.config import config
from fabric_sdk.context.load_yaml import load_network_config


config = load_network_config()
print(config)
