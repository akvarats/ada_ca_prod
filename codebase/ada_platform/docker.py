import os
from typing import Optional


def get_docker_env(name: str, default: Optional[str] = None):
    return os.getenv(name, default)


def get_docker_secret(secrete_name: str, default: Optional[str] = None):
    """ Возвращает значение, переданное в контейнер через docker secret """
    secrete = default

    secrete_path = "/run/secrets/{}".format(secrete_name)

    if secrete_path and os.path.isfile(secrete_path):
        with open(secrete_path, 'r') as f:
            secrete = f.read().strip()

    return secrete
