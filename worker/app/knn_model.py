from collections import OrderedDict

from sklearn.neighbors import KNeighborsClassifier

from tools import get_clean_rusvectores_words, normalized_executor


class KNNPrediction(object):
    def __init__(self, labels):
        self._labels = labels
        self._predicted = {}

    @property
    def labels(self):
        return self._labels

    def set_predicted_for_label(self, label, predicted):
        self._predicted[label] = sorted(predicted, key=lambda x: x[1], reverse=True)

    def prediction_for_label(self, label):
        return self._predicted[label][0]

    def top3_for_label(self, label):
        return self._predicted[label][0:3]


class KNNPrediction1(object):

    def __init__(self):
        self._all_predicted_categories = []
        self._predicted_category = None

        self._all_predicted_themes = []
        self._predicted_theme = None

        self._all_predicted_executors = []
        self._predicted_executor = []

    # --------------------------------------------------------------------------------------------
    # Предсказания по категориям
    # --------------------------------------------------------------------------------------------
    @property
    def all_predicted_categories(self):
        return self._all_predicted_categories

    @all_predicted_categories.setter
    def all_predicted_categories(self, value):
        self._all_predicted_categories = value

    @property
    def predicted_category(self):
        return self._predicted_category

    @predicted_category.setter
    def predicted_category(self, value):
        self._predicted_category = value

    @property
    def top3_predicted_categories(self):
        return self.all_predicted_categories[0:3] if self.all_predicted_categories else []

    # --------------------------------------------------------------------------------------------
    # Предсказания по исполнителям
    # --------------------------------------------------------------------------------------------
    @property
    def all_predicted_executors(self):
        return self._all_predicted_executors

    @all_predicted_executors.setter
    def all_predicted_executors(self, value):
        self._all_predicted_executors = value

    @property
    def predicted_executor(self):
        return self._predicted_executor

    @predicted_executor.setter
    def predicted_executor(self, value):
        self._predicted_executor = value

    @property
    def top3_predicted_executors(self):
        return self.all_predicted_executors[0:3] if self.all_predicted_executors else []

    # --------------------------------------------------------------------------------------------
    # Предсказания по темам
    # --------------------------------------------------------------------------------------------
    @property
    def all_predicted_themes(self):
        return self._all_predicted_themes

    @all_predicted_themes.setter
    def all_predicted_themes(self, value):
        self._all_predicted_themes = value

    @property
    def predicted_theme(self):
        return self._predicted_theme

    @predicted_theme.setter
    def predicted_theme(self, value):
        self._predicted_theme = value

    @property
    def top3_predicted_themes(self):
        return self.all_predicted_themes[0:3] if self.all_predicted_themes else []


class KNNModel(object):
    """ Основная модель классификации """

    def __init__(self, predictor, word2vec, labels):

        self._predictor = predictor
        self._word2vec = word2vec
        self._labels = labels

        self._knn_categories = None
        self._knn_themes = None
        self._knn_executors = None

        self._corpus_model = None

        self._categories = None
        self._targets_category = None

        self._themes = None
        self._targets_theme = None

        self._executors = None
        self._targets_executors = None

        self._label_targets = {}
        self._label_values = {}
        self._label_knn = {}

        # количество раз, сколько было сделано предсказаний
        self._predictioned_count = 0

    @property
    def corpus_model(self):
        return self._corpus_model

    @property
    def corpus(self):
        return self.corpus_model.corpus if self.corpus_model else None

    @property
    def distances(self):
        return self.corpus_model.distances if self.corpus_model else None

    @property
    def labels(self) -> list:
        return self._labels

    @property
    def predictioned_count(self):
        return self._predictioned_count

    @property
    def word2vec(self):
        return self._word2vec

    @property
    def predictor(self):
        return self._predictor

    def fit(self, corpus_model):
        """

        :param corpus_model:C
        :return:
        """
        self._corpus_model = corpus_model

        self._prepare_labels()

        for label in self.labels:
            self._label_knn[label] = KNeighborsClassifier(n_neighbors=10, metric="precomputed")
            self._label_knn[label].fit(self.distances, self._label_targets[label])

    def predict(self, text):
        """
        Предсказывает категорию, тему и проч.
        """
        self._predictioned_count += 1

        text_vectors = get_clean_rusvectores_words(text, self._predictor, self._word2vec)

        text_distances = [self._word2vec.wmdistance(text_vectors, c["cleaned_rusvectores_words"]) for c in self.corpus]

        prediction = KNNPrediction(labels=self.labels)

        for label in self.labels:
            proba = self._label_knn[label].predict_proba([text_distances])
            predicted = []
            for i in range(0, len(proba[0])):
                if proba[0][i] >= 0.01:
                    predicted.append((
                        self._label_name_by_index(label, i),
                        proba[0][i]
                    ))
            prediction.set_predicted_for_label(label, predicted)


        return prediction

    # ----------------------------------------------------------------------------------------------
    # всякие функции
    # ----------------------------------------------------------------------------------------------
    def _prepare_labels(self):
        """ """

        for label in self.labels:
            self._label_values[label] = OrderedDict()
            self._label_targets[label] = []

            for row in self.corpus:
                if row[label] not in self._label_values[label]:
                    value_index = len(self._label_values[label])
                    self._label_values[label][row[label]] = value_index
                self._label_targets[label].append(self._label_values[label][row[label]])

    def _label_name_by_index(self, label, index):
        result = None
        for cname, cindex in self._label_values[label].items():
            if cindex == index:
                result = cname
                break
        return result
