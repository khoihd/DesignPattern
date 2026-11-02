from __future__ import annotations


class JobState:
    name: str

    def start(self, job: Job) -> None:
        raise ValueError(f"cannot start a {self.name} job")

    def succeed(self, job: Job) -> None:
        raise ValueError(f"cannot succeed a {self.name} job")

    def fail(self, job: Job) -> None:
        raise ValueError(f"cannot fail a {self.name} job")


class Queued(JobState):
    name = "queued"

    def start(self, job: Job) -> None:
        job._state = Running()


class Running(JobState):
    name = "running"

    def succeed(self, job: Job) -> None:
        job._state = Succeeded()

    def fail(self, job: Job) -> None:
        job._state = Failed()


class Failed(JobState):
    name = "failed"

    def start(self, job: Job) -> None:
        job._state = Running()


class Succeeded(JobState):
    name = "succeeded"


class Job:
    def __init__(self, job_id: str):
        self.job_id = job_id
        self._state: JobState = Queued()

    @property
    def status(self) -> str:
        return self._state.name

    def start(self) -> None:
        self._state.start(self)

    def succeed(self) -> None:
        self._state.succeed(self)

    def fail(self) -> None:
        self._state.fail(self)


if __name__ == "__main__":
    job = Job("job-42")
    print("Initial:", job.status)

    job.start()
    print("Started:", job.status)

    job.fail()
    print("Failed:", job.status)

    job.start()
    print("Retried:", job.status)

    job.succeed()
    print("Finished:", job.status)

    try:
        job.start()
    except ValueError as error:
        print("Rejected:", error)
