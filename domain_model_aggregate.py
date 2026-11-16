from dataclasses import dataclass


@dataclass(frozen=True)
class Attempt:
    number: int
    outcome: str


# The aggregate root, which contains Attempt objects and serves as the gatekeeper to the Attempt objects
class Job:
    def __init__(self, job_id: str, max_retries: int = 1):
        if max_retries < 0:
            raise ValueError("max_retries must be nonnegative")

        self.job_id = job_id
        self._max_retries = max_retries
        self._status = "queued"
        self._retries_used = 0
        self._attempts: list[Attempt] = []

    @property
    def status(self) -> str:
        return self._status

    @property
    def retries_used(self) -> int:
        return self._retries_used

    @property
    def attempts(self) -> tuple[Attempt, ...]:
        return tuple(self._attempts)

    def start(self) -> None:
        if self._status != "queued":
            raise ValueError(f"cannot start a {self._status} job")

        self._status = "running"

    def finish_attempt(self, succeeded: bool) -> None:
        if self._status != "running":
            raise ValueError("job must be running to finish an attempt")

        self._attempts.append(
            Attempt(
                number=len(self._attempts) + 1,
                outcome="succeeded" if succeeded else "failed",
            )
        )

        if succeeded:
            self._status = "completed"
        elif self._retries_used < self._max_retries:
            self._retries_used += 1
            self._status = "queued"
        else:
            self._status = "failed"

    def cancel(self) -> None:
        if self._status not in ("queued", "running"):
            raise ValueError(f"cannot cancel a {self._status} job")

        self._status = "cancelled"


class Scheduler:
    def start(self, job: Job) -> None:
        job.start()


class Worker:
    def finish(self, job: Job, succeeded: bool) -> None:
        job.finish_attempt(succeeded)


class APIHandler:
    def cancel(self, job: Job) -> None:
        job.cancel()


def main():
    job = Job("job-1", max_retries=1)

    scheduler = Scheduler()
    worker = Worker()
    api = APIHandler()

    # First attempt fails.
    scheduler.start(job)
    worker.finish(job, succeeded=False)

    print(
        f"After attempt 1: status={job.status}, "
        f"retries={job.retries_used}, attempts={len(job.attempts)}"
    )

    # Retry succeeds.
    scheduler.start(job)
    worker.finish(job, succeeded=True)

    print(
        f"After attempt 2: status={job.status}, "
        f"retries={job.retries_used}, attempts={len(job.attempts)}"
    )

    # Invalid cancellation is rejected.
    try:
        api.cancel(job)
    except ValueError as exc:
        print(f"Cancel rejected: {exc}")

    print(f"Final status: {job.status}")


if __name__ == "__main__":
    main()
