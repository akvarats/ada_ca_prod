import os
import json
import numpy as np


class CorpusModel(object):

    def __init__(self):
        self._corpus = None
        self._distances = None
        self._meta = None

        self._meta_file_path = None
        self._corpus_file_path = None
        self._distance_file_path = None

    @property
    def corpus(self):
        return self._corpus

    @property
    def distances(self):
        return self._distances

    @distances.setter
    def distances(self, value):
        self._distances = value

    @property
    def meta(self):
        return self._meta

    @property
    def meta_file_path(self) -> str:
        return self._meta_file_path

    @property
    def corpus_file_path(self) -> str:
        return self._corpus_file_path

    @property
    def distance_file_path(self) -> str:
        return self._distance_file_path

    def load(self, model_folder):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self._meta_file_path = os.path.join(model_folder, "meta.json")
        self._corpus_file_path = os.path.join(model_folder, "corpus.json")
        self._distance_file_path = os.path.join(model_folder, "distances.npy")

        with open(self.meta_file_path, "rt") as f:
            self._meta = json.loads(f.read())

        with open(self.corpus_file_path, "rt") as f:
            self._corpus = json.loads(f.read())

        self._distances = np.load(self.distance_file_path)

        return self
