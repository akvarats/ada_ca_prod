import logging
import datetime
import json

import numpy as np

from tools import get_clean_rusvectores_words

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

from ada_platform.jobs import load_job, Job, dump_job


def classify(job_uid):
    """ """

    logging.info("/classify: начинаем обработку задачи {}".format(job_uid))

    job = load_job(job_uid=job_uid, job_status=Job.STATUS_QUEUE)

    if not job:
        logging.error("Задача {} не найдена".format(job_uid))
        return

    job.status = Job.STATUS_IN_PROCESS
    dump_job(job)

    t1 = datetime.datetime.now()

    from worker_globals import get_knn_model
    knn = get_knn_model(job.region)
    prediction = knn.predict(job.data["text"])

    job.result = dict(
        time=int((datetime.datetime.now() - t1).total_seconds() * 1000),
    )

    for label in prediction.labels:
        job.result[label] = dict(
            predicted=prediction.prediction_for_label(label)[0],
            top3=[dict(
                value=c[0],
                prob=c[1]
            ) for c in prediction.top3_for_label(label)]
        )

    job.status = Job.STATUS_DONE
    dump_job(job)

    logging.info("/classify: обработка задачи {} завершена".format(job_uid))


# -------------------------------------------------------------------------------------------------
# Метод для обучения
# -------------------------------------------------------------------------------------------------
def learn(job_uid):
    """
    """
    logging.info("/learn: начинаем обработку задачи {}".format(job_uid))
    job = load_job(job_uid=job_uid, job_status=Job.STATUS_QUEUE)

    if not job:
        logging.error("Задача {} не найдена".format(job_uid))
        return

    job.status = Job.STATUS_IN_PROCESS
    dump_job(job)

    from worker_globals import get_knn_model
    knn = get_knn_model(job.region)

    # проверяем наличие всех меток
    for label in knn.labels:
        if not job.data.get(label):
            job.status = Job.STATUS_DONE
            job.result = {
                "success": False,
                "error_msg": "Не указано значение метки {}".format(label)
            }
            dump_job(job)
            logging.info("/learn: ошибка при обработке задачи {}:".format(job_uid, job.result["error_msg"]))
            return

    # пересчитываем дистанции от нового текста до каждого ищ

    text = job.data["text"]
    text_vectors = get_clean_rusvectores_words(text, knn.predictor, knn.word2vec)

    # добавляем элемент в корпус
    corp_item = {
        "orig_text": text,
        "cleaned_rusvectores_words": text_vectors
    }

    for label in knn.labels:
        corp_item[label] = job.data[label]

    # вычисляем расстояния до каждой из моделей
    text_distances = [knn.word2vec.wmdistance(text_vectors, c["cleaned_rusvectores_words"]) for c in knn.corpus]

    X = np.vstack((knn.distances, [text_distances]))

    y_distances = [[d] for d in text_distances]
    y_distances.append([0])  # чтобы матрица осталась прямоугольной, мы вставляем 0
    Y = np.hstack((X, y_distances))

    knn.corpus_model.corpus.append(corp_item)

    # сохраняем новую матрицу расстояний и модель корпуса
    np.save(knn.corpus_model.distance_file_path, Y)
    with open(knn.corpus_model.corpus_file_path, "wt") as f:
        f.write(json.dumps(knn.corpus_model.corpus, ensure_ascii=False, indent=2))

    job.status = Job.STATUS_DONE
    dump_job(job)

    logging.info("/learn: обработка задачи {} завершена".format(job_uid))


# -------------------------------------------------------------------------------------------------
# Метод для сброса состояния воркеров
# -------------------------------------------------------------------------------------------------
def flash(job_uid):
    """
    """
    logging.info("/flash: начинаем обработку задачи {}".format(job_uid))
    job = load_job(job_uid=job_uid, job_status=Job.STATUS_QUEUE)

    if not job:
        logging.error("Задача {} не найдена".format(job_uid))
        return

    job.status = Job.STATUS_IN_PROCESS
    dump_job(job)

    from worker_globals import get_knn_model
    knn = get_knn_model(job.region)

    job.status = Job.STATUS_DONE
    dump_job(job)

    logging.info("/flash: обработка задачи {} завершена".format(job_uid))