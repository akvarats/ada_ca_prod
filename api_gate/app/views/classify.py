import logging

from flask import request, jsonify
from flask_jwt_extended import decode_token

from run import app

from ada_platform.auth import get_auth_token, check_auth_token
from ada_platform.workers import enqueue_worker_job
from ada_platform.jobs import Job


@app.route("/classify", methods=["POST"])
def classify():
    """
    Операция классификации текста на гейте
    """

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
    if not request.is_json:
        return "Указан некорректный Content-Type (должно быть application/json)", 400

    if not request.json or not "text" in request.json:
        return "Не указан параметр text", 400

    text = (request.json or {}).get("text")

    job = Job.new(type="classify", region=decoded_token["identity"]["region"])
    job.data = dict(text=text)

    enqueue_worker_job(job)

    return jsonify(dict(uid=job.uid))
