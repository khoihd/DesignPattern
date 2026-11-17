import sqlite3
from dataclasses import dataclass
from typing import Protocol


# ==========================================
# 1. ENTITIES / DOMAIN
# ==========================================
@dataclass(frozen=True)
class Job:
    job_id: str
    status: str = "queued"


# ==========================================
# 2. USE CASES / APPLICATION
# ==========================================
@dataclass(frozen=True)
class SubmitJobRequest:
    job_id: str


@dataclass(frozen=True)
class SubmitJobResponse:
    job_id: str
    status: str


# Application-owned interfaces
class JobRepository(Protocol):
    def save(self, job: Job) -> None: ...


class JobQueue(Protocol):
    def publish(self, job_id: str) -> None: ...


class SubmitJobInput(Protocol):
    def execute(self, request: SubmitJobRequest) -> SubmitJobResponse: ...


# Application use case
class SubmitJobUseCase:
    def __init__(self, repository: JobRepository, queue: JobQueue):
        self.repository = repository
        self.queue = queue

    def execute(self, request: SubmitJobRequest) -> SubmitJobResponse:
        job = Job(request.job_id)

        self.repository.save(job)
        self.queue.publish(job.job_id)

        return SubmitJobResponse(
            job_id=job.job_id,
            status=job.status,
        )


# ==========================================
# 3. INTERFACE ADAPTERS
# ==========================================

# ------------------------------------------
# INBOUND ADAPTER 1: CLI
# ------------------------------------------
class CliPresenter:
    def present(self, response: SubmitJobResponse):
        print(f"Result: {response.job_id} ({response.status})")


class CliController:
    def __init__(self, use_case: SubmitJobInput, presenter: CliPresenter):
        self.use_case = use_case
        self.presenter = presenter

    def run(self, command: str):
        job_id = command.split()[1]
        print(f"CLI: submitting {job_id}")

        request = SubmitJobRequest(job_id)
        response = self.use_case.execute(request)

        self.presenter.present(response)


# ------------------------------------------
# INBOUND ADAPTER 2: MESSAGE CONSUMER
# ------------------------------------------
class MessageConsumer:
    def __init__(self, use_case: SubmitJobInput):
        self.use_case = use_case

    def on_message(self, message: dict):
        job_id = message["job_id"]
        print(f"Message: submitting {job_id}")

        request = SubmitJobRequest(job_id)
        return self.use_case.execute(request)


# ------------------------------------------
# OUTBOUND ADAPTER 1: DATABASE
# ------------------------------------------
class SqliteJobRepository:
    def __init__(self, db: sqlite3.Connection):
        self.db = db
        self.db.execute("CREATE TABLE jobs (job_id TEXT PRIMARY KEY, status TEXT)")

    def save(self, job: Job):
        self.db.execute(
            "INSERT INTO jobs VALUES (?, ?)",
            (job.job_id, job.status),
        )
        self.db.commit()
        print(f"Database: saved {job.job_id}")


# ------------------------------------------
# OUTBOUND ADAPTER 2: MESSAGE QUEUE
# ------------------------------------------
class InMemoryJobQueue:
    def __init__(self):
        self.messages: list[str] = []

    def publish(self, job_id: str):
        self.messages.append(job_id)
        print(f"Queue: published {job_id}")


# ==========================================
# 4. FRAMEWORKS / DRIVERS & COMPOSITION ROOT
# ==========================================
def main():
    db = sqlite3.connect(":memory:")

    try:
        # Outbound adapters
        repository = SqliteJobRepository(db)
        queue = InMemoryJobQueue()

        # Shared application use case
        use_case = SubmitJobUseCase(repository, queue)

        # Inbound adapter 1: CLI
        cli = CliController(use_case, CliPresenter())
        cli.run("submit job-1")

        # Inbound adapter 2: Message Consumer
        consumer = MessageConsumer(use_case)
        response = consumer.on_message({"job_id": "job-2"})
        print(f"Message result: {response.job_id} ({response.status})")

    finally:
        db.close()


if __name__ == "__main__":
    main()
