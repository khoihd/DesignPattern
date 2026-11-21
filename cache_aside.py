import time
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Job:
    job_id: str
    status: str


class JobRepository:
    def __init__(self):
        self.jobs = {
            "job-1": Job("job-1", "PENDING"),
            "job-2": Job("job-2", "RUNNING"),
        }

    def get_job(self, job_id: str) -> Job:
        print(f"[Database] Reading {job_id}")
        time.sleep(1)
        return self.jobs[job_id]

    def update_status(self, job_id: str, status: str) -> None:
        print(f"[Database] Updating {job_id} to {status}")
        self.jobs[job_id] = replace(
            self.jobs[job_id],
            status=status,
        )


class JobCache:
    def __init__(self):
        self.jobs: dict[str, Job] = {}

    def get(self, job_id: str) -> Job | None:
        return self.jobs.get(job_id)

    def set(self, job_id: str, job: Job) -> None:
        print(f"[Cache] Storing {job_id}")
        self.jobs[job_id] = job

    def delete(self, job_id: str) -> None:
        print(f"[Cache] Invalidating {job_id}")
        self.jobs.pop(job_id, None)


class JobService:
    def __init__(self, repository: JobRepository, cache: JobCache):
        self.repository = repository
        self.cache = cache

    def get_job(self, job_id: str) -> Job:
        job = self.cache.get(job_id)

        if job is not None:
            print(f"[Cache] Hit for {job_id}")
            return job

        print(f"[Cache] Miss for {job_id}")

        job = self.repository.get_job(job_id)
        self.cache.set(job_id, job)

        return job

    def update_status(self, job_id: str, status: str) -> None:
        self.repository.update_status(job_id, status)
        self.cache.delete(job_id)


def main():
    repository = JobRepository()
    cache = JobCache()

    job_service = JobService(repository, cache)

    start = time.perf_counter()

    for _ in range(3):
        job = job_service.get_job("job-1")
        print(job)

    elapsed = time.perf_counter() - start
    print(f"Elapsed time: {elapsed:.2f}s")

    print("--- Update job ---")

    job_service.update_status("job-1", "COMPLETED")
    print(job_service.get_job("job-1"))

    print("--- Read again ---")

    print(job_service.get_job("job-1"))


if __name__ == "__main__":
    main()
