import json
import logging

from ada_platform.docker import get_docker_secret


def get_region_identity_for_token(token_value):
    """

    :param token_value:
    :return:
    """
    result = None

    tokens = None
    secret_tokens = get_docker_secret("region_tokens")

    if secret_tokens:
        try:
            tokens = json.loads(secret_tokens)
        except Exception as e:
            logging.error("Не удалось прочитать значение region_tokens: {}".format(e))

    if tokens:
        result = tokens.get(token_value)

    return result
