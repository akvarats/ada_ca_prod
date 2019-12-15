import os
import json

from .docker import get_docker_env


class RegionModelsConf(object):
    """ Настройка моделей для региона """
    def __init__(self):
        self.region = None
        self.corpus_model_path = None
        self.labels = []


def get_corpus_model_conf(models_path: str, region: str) -> RegionModelsConf:
    """
    """
    model_conf_path = os.path.join(models_path, "conf/{}.json".format(region))

    if not os.path.exists(model_conf_path):
        raise Exception("Не найдена настройка моделей для региона {} по пути {}".format(region, model_conf_path))

    with open(model_conf_path, "rt") as f:
        model_conf_json = json.loads(f.read())

    result = RegionModelsConf()
    result.region = region
    result.corpus_model_path = os.path.join(models_path, model_conf_json["corpus_model"])
    result.labels = model_conf_json["labels"]

    return result
