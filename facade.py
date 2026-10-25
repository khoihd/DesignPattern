from dataclasses import dataclass


# ==================================================
# Data Model
# ==================================================
@dataclass
class Job:
    job_id: str
    cpu: int
    task: str


# ==================================================
# Subsystem Components
# ==================================================
class JobValidator:
    def validate(self, job: Job):
        print(f"[Validator] Validating {job.job_id}")

        if job.cpu <= 0:
            raise ValueError("CPU must be positive")

        if not job.task:
            raise ValueError("Task cannot be empty")


class ResourceManager:
    def allocate(self, job: Job) -> str:
        print(f"[ResourceManager] Allocating {job.cpu} CPUs")

        return f"allocation-{job.job_id}"


class Scheduler:
    def schedule(self, job: Job, allocation_id: str) -> str:
        print(f"[Scheduler] Scheduling {job.job_id} using {allocation_id}")

        return f"schedule-{job.job_id}"


class JobRepository:
    def __init__(self):
        self._jobs = {}

    def save(self, job: Job, schedule_id: str):
        print(f"[Repository] Saving {job.job_id}")

        self._jobs[job.job_id] = {"job": job, "schedule_id": schedule_id}

    def get(self, job_id: str):
        return self._jobs.get(job_id)


class WorkerDispatcher:
    def dispatch(self, job: Job, schedule_id: str):
        print(f"[Dispatcher] Dispatching {job.job_id} with {schedule_id}")


# ==================================================
# Facade
# ==================================================
class JobService:
    def __init__(
        self,
        validator: JobValidator,
        resource_manager: ResourceManager,
        scheduler: Scheduler,
        repository: JobRepository,
        dispatcher: WorkerDispatcher,
    ):
        self._validator = validator
        self._resource_manager = resource_manager
        self._scheduler = scheduler
        self._repository = repository
        self._dispatcher = dispatcher

    def submit_job(self, job: Job) -> str:
        print(f"\n[JobService] Submitting {job.job_id}")

        self._validator.validate(job)
        allocation_id = self._resource_manager.allocate(job)
        schedule_id = self._scheduler.schedule(job, allocation_id)
        self._repository.save(job, schedule_id)
        self._dispatcher.dispatch(job, schedule_id)
        print("[JobService] Submission completed")

        return schedule_id


# ==================================================
# Client
# ==================================================
def main():
    job_service = JobService(
        validator=JobValidator(),
        resource_manager=ResourceManager(),
        scheduler=Scheduler(),
        repository=JobRepository(),
        dispatcher=WorkerDispatcher(),
    )

    job = Job(job_id="job-123", cpu=4, task="process_dataset")
    schedule_id = job_service.submit_job(job)
    print(f"\nClient received: {schedule_id}")


if __name__ == "__main__":
    main()
