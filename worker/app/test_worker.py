import sys

sys.path.insert(0, "../../codebase")

from worker import classify

from ada_platform.jobs import Job, dump_job, load_job


if __name__ == "__main__":

    # 1. Создаем задачу на классификацию
    job = Job().new(type="classify", region="ryazyan")
    job.data = dict(text="Не работает светофор на пересечении улиц")
    job.status = Job.STATUS_QUEUE
    dump_job(job)

    # 2. Выполняем задачу
    classify(job_uid=job.uid)

    # 3. Печатаем результат
    job = load_job(job_uid=job.uid)
    print(job.result)