import asyncio
import time


class Deadline:
    def __init__(self, timeout: float):
        self.expires_at = time.monotonic() + timeout

    def remaining(self) -> float:
        return max(0.0, self.expires_at - time.monotonic())

    def timeout_for(self, operation_timeout: float) -> float:
        remaining = self.remaining()

        if remaining <= 0:
            raise TimeoutError("Deadline exceeded")

        return min(operation_timeout, remaining)


class JobRepository:
    def __init__(self, delay: float):
        self.delay = delay

    async def get_job(self, job_id: str) -> dict:
        print(f"[JobRepository] Retrieving {job_id}")

        await asyncio.sleep(self.delay)

        return {"job_id": job_id, "status": "RUNNING", "worker_id": "worker-1"}


class WorkerService:
    def __init__(self, delay: float):
        self.delay = delay

    async def get_worker(self, worker_id: str) -> dict:
        print(f"[WorkerService] Retrieving {worker_id}")

        await asyncio.sleep(self.delay)

        return {"worker_id": worker_id, "hostname": "worker-server-01"}


class JobService:
    def __init__(self, repository: JobRepository, worker_service: WorkerService, operation_timeout: float):
        self.repository = repository
        self.worker_service = worker_service
        self.operation_timeout = operation_timeout

    async def get_job_details(self, job_id: str, deadline: Deadline) -> dict:
        # Operation 1: Retrieve the job.
        timeout = deadline.timeout_for(self.operation_timeout)

        print(f"[JobService] Job timeout: {timeout:.2f}s")

        job = await asyncio.wait_for(self.repository.get_job(job_id), timeout=timeout)

        # Operation 2: Retrieve the assigned worker.
        timeout = deadline.timeout_for(self.operation_timeout)

        print(f"[JobService] Worker timeout: {timeout:.2f}s")

        worker = await asyncio.wait_for(
            self.worker_service.get_worker(job["worker_id"]), timeout=timeout
        )

        return {"job": job, "worker": worker}


async def run_case(name: str, repository_delay: float, worker_delay: float):
    print(f"--- {name} ---")

    repository = JobRepository(repository_delay)
    worker_service = WorkerService(worker_delay)

    job_service = JobService(repository, worker_service, operation_timeout=2.0)

    start = time.monotonic()
    deadline = Deadline(timeout=3.0)

    try:
        result = await job_service.get_job_details("job-1", deadline)
        print(f"Result: {result}")
    except TimeoutError:
        print("Request failed: operation timed out")

    print(f"Elapsed time: {time.monotonic() - start:.2f}s")


async def run_demo():
    await run_case("Case 1: Successful request", repository_delay=0.5, worker_delay=0.5)

    await run_case("Case 2: Individual operation timeout", repository_delay=2.5, worker_delay=0.5)

    await run_case("Case 3: Overall deadline exceeded", repository_delay=1.8, worker_delay=1.8)


def main():
    asyncio.run(run_demo())


if __name__ == "__main__":
    main()
