#!/usr/bin/env python

from redis import Redis
from rq.job import Job
from rq.registry import FinishedJobRegistry
import json
from rq import Connection, Worker, Queue
import sys
import time
import os


redis = Redis(host=os.environ["REDIS_HOST"])


def worker_status():
    workers = Worker.all(connection=redis)
    for worker in workers:
        if worker.state == "busy":
            return False
    return True


def list_all_jobs():
    registry = FinishedJobRegistry(os.environ["RQ_QUEUE"], connection=redis)

    print(f"{len(registry.get_job_ids())} record(s) succesfully saved to './output/data.json'.")
    return Job.fetch_many(registry.get_job_ids(), connection=redis)


def write_to_json():
    json_data = []
    for job in list_all_jobs():
        json_data.append(job.return_value)

    with open('output/data.json', 'w') as outfile:
        json.dump(json_data, outfile)


def clear_registry():
    registry = FinishedJobRegistry(os.environ["RQ_QUEUE"], connection=redis)
    for job_id in registry.get_job_ids():
        registry.remove(job_id)


def listener():
    while True:
        print("Listening...")
        time.sleep(1)
        if worker_status():
            print("Writing to json file...")
            write_to_json()
            clear_registry()
            break



if __name__ == "__main__":
    listener()
    
