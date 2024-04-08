import os

SERVER_UBUNTU_VERSION = os.environ.get('RUN_LANG_UBUNTU')


def get_ubuntu():
    return SERVER_UBUNTU_VERSION


