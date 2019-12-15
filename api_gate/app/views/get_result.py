import logging

from flask import request, jsonify
from flask_jwt_extended import decode_token

from run import app

from ada_platform.auth import get_auth_token, check_auth_token
from ada_platform.workers import enqueue_worker_job
from ada_platform.jobs import load_job, Job


@app.route("/get-result", methods=["GET"])
def get_result():

    # Проверяем права на выполнение запроса
    # ------------------------------------------------------------------------------------------------------------------
    auth_token = get_auth_token(request)
    if not auth_token:
        return "Не указан токен доступа", 401

    auth_result = check_auth_token(auth_token)
    if not auth_result:
        return "Неверный токен доступа", 403

    jwt_token = auth_result.get("jwt_token")

    if not jwt_token:
        return "Не удалось получить jwt_token", 403

    decoded_token = None
    try:
        decoded_token = decode_token(jwt_token)
    except Exception as e:
        logging.error("Ошибка декодирования jwt-токена: {}".format(e))

    if not decoded_token:
        return "Не удалось декодировать jwt_token", 403

    # Проверяем входные параметры
    # ------------------------------------------------------------------------------------------------------------------
    if not "uid" in request.args:
        return "Не указан параметр uid", 400

    job_uid = (request.args or {}).get("uid")

    job = load_job(job_uid=job_uid)

    if not job or job.region != decoded_token["identity"]["region"]:
        return "Задача {} не найдена".format(job_uid), 404

    result = dict(
        status=job.status,
        result=job.result if job.status == Job.STATUS_DONE else None
    )

    return result