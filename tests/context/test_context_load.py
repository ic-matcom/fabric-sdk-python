import os
from pathlib import Path
from fabric_sdk.__env__ import FABRIC_PYTHON_SDK_NETWORK_CONFIG
import fabric_sdk as sdk


def test_load_msp():
    path = str(Path(__file__).resolve()).split('/')
    os.environ[FABRIC_PYTHON_SDK_NETWORK_CONFIG] = '/'.join(path[:-1])

    context = sdk.Context()

    assert len(context.ca_list) == 3
