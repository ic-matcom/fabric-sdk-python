import os
from pathlib import Path
from fabric_sdk.__env__ import FABRIC_PYTHON_SDK_NETWORK_CONFIG
import fabric_sdk as sdk


def test_load_msp():
    path = str(Path(__file__).resolve()).split('/')
    path[-1] = 'msp.yaml'
    os.environ[FABRIC_PYTHON_SDK_NETWORK_CONFIG] = '/'.join(path)

    context = sdk.context.init()

    assert len(context.certificateAuthorities) == 3
