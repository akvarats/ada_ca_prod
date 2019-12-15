import os
import gensim
import string
import nltk
import csv

from rnnmorph.predictor import RNNMorphPredictor
from sklearn.metrics import pairwise_distances


def get_morph_predictor():
    """ """
    return RNNMorphPredictor(language="ru")


def get_word2vec_model(model_filepath):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    return gensim.models.KeyedVectors.load_word2vec_format(model_filepath, binary=True)


def morph_words(words, predictor):
    """
    Постановка слова в начальную форму и вычисление части речи

    @param predictor: предиктор (RNNMorphPredictor)
    @param word: список строк со словами из предложения
    """
    morphs = predictor.predict(words)

    result = []
    for m in morphs:
        result.append((m.normal_form, m.pos))

    return result


def get_clean_rusvectores_words(text: str, predictor: RNNMorphPredictor, word2vec_model):
    """ """
    result = []

    for punct in string.punctuation:
        text = text.replace(punct, " ")

    morphs = morph_words(nltk.word_tokenize(text, language="russian"), predictor)

    for morph in morphs:
        rv_word = "{0}_{1}".format(morph[0], morph[1])
        if rv_word in word2vec_model.wv:
            result.append(rv_word)

    return result


def read_corpus(corpus_filepath, predictor, model):
    """ Читает корпус начального текста """
    result = []

    with open(corpus_filepath) as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # skip header
        for row in csv_reader:
            orig_text = row[1]
            cleaned_rusvectores_words = get_clean_rusvectores_words(orig_text, predictor, model)
            if cleaned_rusvectores_words:
                result.append(
                    dict(
                        id=row[0],
                        orig_text=orig_text,
                        category=row[2],
                        theme=row[3],
                        executor=row[4],
                        cleaned_rusvectores_words=cleaned_rusvectores_words
                    )
                )

    return result


def get_distance_matrix_for_corpus(corpus, word2vec_model):
    """ """
    X = [[i] for i in range(0, len(corpus))]

    distance = lambda x, y: word2vec_model.wmdistance(
        corpus[int(x[0])]["cleaned_rusvectores_words"],
        corpus[int(y[0])]["cleaned_rusvectores_words"]
    )

    return pairwise_distances(X, metric=distance, n_jobs=-1)


def get_chunks(N, chunk_size):
    """ 
    Возвращает список кортежей (index_from, index_to) для заданного массива [0, 1, ..., N]
    """
    return [(i, min(i + chunk_size, N)) for i in range(0, N, chunk_size)]


def normalized_executor(executor_name):
    """ """
    result = executor_name

    if ";" in executor_name:
        result = executor_name.split(";")[0]

    lower_name = result.lower()

    if "администрация" in lower_name or "префектура" in lower_name:
        result = "Администрация/префектура района/города/округа"

    return result