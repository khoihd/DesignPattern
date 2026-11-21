import time
from concurrent.futures import ThreadPoolExecutor


class JobRepository:
    def __init__(self):
        self.shards = {
            "shard-1": (120, 1),
            "shard-2": (80, 2),
            "shard-3": (150, 3),
        }

    def count_completed_jobs(self, shard_id: str) -> int:
        job_count, delay = self.shards[shard_id]

        print(f"Querying {shard_id}...")
        time.sleep(delay)
        print(f"{shard_id} returned {job_count}")

        return job_count


class JobService:
    def __init__(self, repository: JobRepository, executor: ThreadPoolExecutor):
        self.repository = repository
        self.executor = executor

    def count_completed_jobs(self, shard_ids: list[str]) -> int:
        # Fan-Out: dispatch independent subtasks.
        futures = [
            self.executor.submit(
                self.repository.count_completed_jobs,
                shard_id,
            )
            for shard_id in shard_ids
        ]

        # Fan-In: collect results.
        counts = [future.result() for future in futures]

        # Fan-In: aggregate results.
        return sum(counts)


def main():
    repository = JobRepository()

    with ThreadPoolExecutor(max_workers=3) as executor:
        job_service = JobService(repository, executor)

        shard_ids = ["shard-1", "shard-2", "shard-3"]

        start = time.perf_counter()

        total = job_service.count_completed_jobs(shard_ids)

        elapsed = time.perf_counter() - start

        print(f"Total completed jobs: {total}")
        print(f"Execution time: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
