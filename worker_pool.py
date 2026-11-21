import threading
import time
from queue import Queue


class WorkerService:
    def execute(self, job_id: str):
        worker_id = threading.current_thread().name

        print(f"[{worker_id}] Started {job_id}")
        time.sleep(1)
        print(f"[{worker_id}] Finished {job_id}")


class WorkerPool:
    def __init__(self, worker_service: WorkerService, num_workers: int):
        if num_workers < 1:
            raise ValueError("At least one worker is required")

        self.worker_service = worker_service
        self.task_queue = Queue()
        self.closed = False

        self.threads = [
            threading.Thread(
                target=self._worker_loop,
                name=f"worker-{i + 1}",
            )
            for i in range(num_workers)
        ]

        for thread in self.threads:
            thread.start()

    def _worker_loop(self):
        while True:
            job_id = self.task_queue.get()

            try:
                if job_id is None:
                    break

                self.worker_service.execute(job_id)

            finally:
                self.task_queue.task_done()

    def submit(self, job_id: str):
        if self.closed:
            raise RuntimeError("Worker pool is closed")

        self.task_queue.put(job_id)

    def wait_for_completion(self):
        self.task_queue.join()

    def shutdown(self):
        if self.closed:
            return

        self.closed = True

        # Wait for all submitted jobs to finish.
        self.wait_for_completion()

        # Send one shutdown signal per worker.
        for _ in self.threads:
            self.task_queue.put(None)

        # Wait for all worker threads to terminate.
        for thread in self.threads:
            thread.join()


class JobService:
    def __init__(self, worker_pool: WorkerPool):
        self.worker_pool = worker_pool

    def submit_job(self, job_id: str):
        print(f"[JobService] Submitting {job_id}")
        self.worker_pool.submit(job_id)


def main():
    worker_service = WorkerService()

    worker_pool = WorkerPool(
        worker_service=worker_service,
        num_workers=3,
    )

    job_service = JobService(worker_pool)

    start = time.perf_counter()

    try:
        for i in range(1, 7):
            job_service.submit_job(f"job-{i}")

        worker_pool.wait_for_completion()

    finally:
        worker_pool.shutdown()

    elapsed = time.perf_counter() - start
    print(f"Total execution time: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
