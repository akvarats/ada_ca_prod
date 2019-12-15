from typing import Optional
import requests
from urllib.parse import urljoin

from redis import Redis
from rq import Queue

from .docker import get_docker_env
from .jobs import Job, dump_job


def enqueue_worker_job(job: Job):
    """ """

    job.status = Job.STATUS_QUEUE
    dump_job(job)

    redis_conn = Redis(host=get_docker_env("REDIS_HOST", "redis"), port=int(get_docker_env("REDIS_PORT", "6379")))

    queue_name = job.region
    if job.type in ["learn", "flash"]:
        queue_name = "{}.learn".format(queue_name)

    operation = "worker.classify"
    if job.type in ["learn"]:
        operation = "worker.learn"

    q = Queue(queue_name, connection=redis_conn)
    q.enqueue(operation, job_uid=job.uid)
