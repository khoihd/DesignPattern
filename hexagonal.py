import sqlite3
from dataclasses import dataclass
from typing import Protocol


# ==================================================
# CORE: Domain model
# ==================================================
@dataclass(frozen=True)
class Job:
    job_id: str
    status: str = "queued"

    def __post_init__(self):
        if not self.job_id.strip():
            raise ValueError("Job ID cannot be empty")


# ==================================================
# CORE: Ports
# ==================================================
# Inbound port
class SubmitJob(Protocol):
    def submit(self, job_id: str) -> Job: ...


# Outbound ports
class JobRepository(Protocol):
    def save(self, job: Job) -> None: ...


class JobQueue(Protocol):
    def publish(self, job_id: str) -> None: ...


# ==================================================
# CORE: Application service
# ==================================================
class JobService:
    def __init__(self, repository: JobRepository, queue: JobQueue):
        self.repository = repository
        self.queue = queue

    def submit(self, job_id: str) -> Job:
        job = Job(job_id)

        self.repository.save(job)
        self.queue.publish(job.job_id)

        return job


# ==================================================
# OUTBOUND ADAPTERS: Infrastructure
# ==================================================
class SqliteJobRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.connection.execute(
            "CREATE TABLE jobs (id TEXT PRIMARY KEY, status TEXT NOT NULL)"
        )

    def save(self, job: Job) -> None:
        self.connection.execute(
            "INSERT INTO jobs VALUES (?, ?)",
            (job.job_id, job.status),
        )
        self.connection.commit()

        print(f"Database: saved {job.job_id}")


class InMemoryJobQueue:
    def __init__(self):
        self.messages: list[str] = []

    def publish(self, job_id: str) -> None:
        self.messages.append(job_id)

        print(f"Queue: published {job_id}")


# ==================================================
# INBOUND ADAPTER: Command-line interface
# ==================================================
class CliAdapter:
    def __init__(self, submit_job: SubmitJob):
        self.submit_job = submit_job

    def run(self, job_id: str) -> Job:
        print(f"CLI: submitting {job_id}")

        return self.submit_job.submit(job_id)


# ==================================================
# COMPOSITION ROOT: Dependency wiring
# ==================================================

# Caller → Inbound Adapter → Inbound Port → Core → Outbound Port → Outbound Adapter → External System
def main():
    db = sqlite3.connect(":memory:")

    try:
        repository = SqliteJobRepository(db)
        queue = InMemoryJobQueue()

        service = JobService(repository, queue)

        cli = CliAdapter(service)

        job = cli.run("job-1")
        print(f"Result: {job.job_id} ({job.status})")
    finally:
        db.close()


if __name__ == "__main__":
    main()
