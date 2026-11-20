import threading
import time
from queue import Queue


class JobService:
    def __init__(self, job_queue: Queue):
        self.job_queue = job_queue

    def submit_job(self, job_id: str):
        self.job_queue.put(job_id)
        print(f"[JobService] Submitted {job_id}")


class WorkerService:
    def __init__(self, worker_id: str, job_queue: Queue):
        self.worker_id = worker_id
        self.job_queue = job_queue

    def run(self):
        while True:
            # Wait until a job becomes available.
            job_id = self.job_queue.get()

            if job_id is None:
                self.job_queue.task_done()
                break

            try:
                print(f"[{self.worker_id}] Started {job_id}")
                time.sleep(0.5)  # Simulate slow work
                print(f"[{self.worker_id}] Finished {job_id}")
            finally:
                self.job_queue.task_done()


def main():
    job_queue = Queue()
    job_service = JobService(job_queue)

    workers = [
        WorkerService("worker-a", job_queue),
        WorkerService("worker-b", job_queue),
        WorkerService("worker-c", job_queue),
    ]

    threads = [threading.Thread(target=worker.run) for worker in workers]

    for thread in threads:
        thread.start()

    # Producer submits jobs while workers run.
    for i in range(1, 7):
        job_service.submit_job(f"job-{i}")

    # Wait until all submitted jobs finish.
    job_queue.join()

    # Shut down workers cleanly.
    for _ in workers:
        job_queue.put(None)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
