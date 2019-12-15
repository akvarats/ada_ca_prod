import logging

from flask import request, jsonify
from flask_jwt_extended import decode_token

from ada_platform.regions import get_available_reqions
from run import app

from ada_platform.auth import get_auth_token, check_auth_token
from ada_platform.workers import enqueue_worker_job
from ada_platform.jobs import load_job, dump_job, Job

@app.route("/flash", methods=["POST"])
def flash():
    """ """
    if not request.is_json:
        return "Указан некорректный Content-Type (должно быть application/json)", 400

    if not request.json or not "region" in request.json:
        return "Не указан параметр region", 400

    region = request.json["region"]
    if not region:
        return "Указано пустое значение параметра region", 403

    # читаем список доступных регионов
    available_regions = get_available_reqions()
    if not available_regions:
        return "Список доступных регионов пуст", 500

    if region not in available_regions:
        return "Указан некорректный регион {}".format(region), 403

    # Формируем задачу на сброс кеша модели
    job = Job.new(type="flash", region=region)
    enqueue_worker_job(job)

    return {"job_uid": job.uid}