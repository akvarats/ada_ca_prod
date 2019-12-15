from typing import Optional
import uuid
import datetime
import os
import json
import logging
import shutil

from .datetime import datetime_now, datetime_to_iso, iso_to_datetime
from .docker import get_docker_env


STORAGE_PATH = get_docker_env("ADA_STORAGE") or "/storage"


class Job(object):

    STATUS_QUEUE = "queue"
    STATUS_IN_PROCESS = "in-process"
    STATUS_DONE = "done"
    STATUS_DEFERRED = "deffered"  # статус "задача отложена"

    STATUSES = [STATUS_QUEUE, STATUS_IN_PROCESS, STATUS_DONE, STATUS_DEFERRED]

    def __init__(self):
        self._type = None
        self._region = None
        self._uid = None
        self._data = None
        self._result = None
        self._status = None
        self._status_changed_at = None

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = value

    @property
    def region(self) -> str:
        return self._region

    @region.setter
    def region(self, value: str):
        self._region = value

    @property
    def uid(self) -> str:
        return self._uid

    @uid.setter
    def uid(self, value: str):
        self._uid = value

    @property
    def data(self) -> Optional[dict]:
        return self._data

    @data.setter
    def data(self, value: Optional[dict]):
        self._data = value

    @property
    def result(self) -> Optional[dict]:
        return self._result

    @result.setter
    def result(self, value: Optional[dict]):
        self._result = value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        if value not in Job.STATUSES:
            raise Exception("Статус {} не может быть установлен для задачи".format(value))
        self._status = value

    @property
    def status_changed_at(self) -> datetime.datetime:
        return self._status_changed_at

    @status_changed_at.setter
    def status_changed_at(self, value: datetime.datetime):
        self._status_changed_at = value

    @classmethod
    def new(cls, type: str, region: str):
        job = Job()
        job.type = type
        job.uid = new_job_uuid()
        job.region = region
        job.data = None
        job.result = None
        job.status_changed_at = datetime_now()

        return job

    def to_json(self):
        return dict(
            type=self.type,
            uid=self.uid,
            region=self.region,
            data=self.data,
            result=self.result,
            status=self.status,
            status_changed_at=datetime_to_iso(self.status_changed_at) if self.status_changed_at else None
        )

    def from_json(self, job_json):
        if not isinstance(job_json, dict):
            return

        self.type = job_json.get("type")
        self.uid = job_json.get("uid")
        self.region =job_json.get("region")
        self.data = job_json.get("data")
        self.result = job_json.get("result")
        self.status = job_json.get("status")
        self.status_changed_at = iso_to_datetime(job_json.get("status_changed_at")) if job_json.get("status_changed_at") \
            else None

        return self


def job_file_path(job_status, job_uid):

    if job_status in [Job.STATUS_QUEUE, Job.STATUS_IN_PROCESS, Job.STATUS_DEFERRED]:
        return os.path.join(STORAGE_PATH, job_status, job_uid)

    return os.path.join(STORAGE_PATH, job_status, job_uid[0:2], job_uid[2:4], job_uid)


def new_job_uuid():
    return str(uuid.uuid4()).replace("-", "")


def dump_job(job: Job):
    """ """
    if not job.status:
        job.status = Job.STATUS_QUEUE

    if not job.uid:
        job.uid = new_job_uuid()

    job.status_changed_at = datetime_now()

    # Создаем файл с заданием
    file_path = job_file_path(job_status=job.status, job_uid=job.uid)
    if os.path.exists(file_path):
        os.remove(file_path)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wt") as f:
        f.write(json.dumps(job.to_json(), ensure_ascii=False, indent=2))

    # удаляем файл с заданием из тех расположений по статусам, где его быть не должно
    for job_status in [s for s in Job.STATUSES if s != job.status]:
        job_path = job_file_path(job_status=job_status, job_uid=job.uid)
        if os.path.exists(job_path):
            os.remove(job_path)


def load_job(job_uid, job_status=None, storage_path=None) -> Job:
    """ """
    result = None

    file_path = None

    if job_status:
        file_path = job_file_path(job_status=job_status, job_uid=job_uid)
    else:
        for job_status in Job.STATUSES:
            probe_file_path = job_file_path(job_status=job_status, job_uid=job_uid)
            if os.path.exists(probe_file_path):
                file_path = probe_file_path
                break

    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, "rt") as f:
                result = Job().from_json(json.loads(f.read()))
        except Exception as e:
            logging.error("Не удалось загрузить задачу из файла {}".format(file_path))

    return result
