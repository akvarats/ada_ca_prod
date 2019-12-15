import os
import gensim
from rnnmorph.predictor import RNNMorphPredictor

from ada_platform.docker import get_docker_env
from ada_platform.models import get_corpus_model_conf

from corpus_model import CorpusModel
from knn_model import KNNModel


MODELS_PATH = get_docker_env("ADA_MODELS") or "/models"

MORPH_PREDICTOR = RNNMorphPredictor(language="ru")

WORD2VEC_MODEL = gensim.models.KeyedVectors.load_word2vec_format(os.path.join(MODELS_PATH, "180/model.bin"), binary=True)

CORPUS_MODELS = {}

KNN_MODELS = {}


def get_corpus_model(region) -> CorpusModel:
    """ """
    if region not in CORPUS_MODELS:
        corpus_model_conf = get_corpus_model_conf(models_path=MODELS_PATH, region=region)
        CORPUS_MODELS["region"] = CorpusModel().load(corpus_model_conf.corpus_model_path)

    return CORPUS_MODELS["region"]


def get_knn_model(region) -> KNNModel:
    """
    Возвращает knn модель для указанного региона
    """
    if region in KNN_MODELS:
        if KNN_MODELS[region].predictioned_count > 100:
            # убираем модель их кеша, чтобы она перечиталась
            del KNN_MODELS[region]

    if region not in KNN_MODELS:
        corpus_model_conf = get_corpus_model_conf(models_path=MODELS_PATH, region=region)
        knn_model = KNNModel(predictor=MORPH_PREDICTOR, word2vec=WORD2VEC_MODEL, labels=corpus_model_conf.labels)
        knn_model.fit(get_corpus_model(region))

        KNN_MODELS[region] = knn_model

    return KNN_MODELS[region]
