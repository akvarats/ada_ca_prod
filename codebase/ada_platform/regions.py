import json
import logging

from ada_platform.docker import get_docker_secret


def get_available_reqions():
    """
    Возвращает список доступных регионов
    """
    result = None

    secret_tokens = get_docker_secret("region_tokens")
    tokens = None

    if secret_tokens:
        try:
            tokens = json.loads(secret_tokens)
        except Exception as e:
            logging.error("Не удалось прочитать значение region_tokens: {}".format(e))

    if tokens:
        try:
            result = list(set([t.get("region") for t in tokens.values() if t.get("region")]))
        except Exception as e:
            logging.error("Не удалось считать список кодов регионов: {}".format(e))

    return result
