import json
from dataclasses import asdict, dataclass


@dataclass
class Job:
    job_id: str
    job_type: str
    status: str
    retries: int
    internal_notes: str


@dataclass(frozen=True)
class JobResponseDTO:
    job_id: str
    job_type: str
    status: str


class JobRepository:
    def __init__(self):
        self.jobs = {}

    def save(self, job):
        self.jobs[job.job_id] = job

    def get(self, job_id):
        return self.jobs.get(job_id)


class JobService:
    def __init__(self, repository):
        self.repository = repository

    def get_job(self, job_id):
        job = self.repository.get(job_id)

        if job is None:
            raise ValueError(f"unknown job ID: {job_id}")

        return job


class APIHandler:
    def __init__(self, service):
        self.service = service

    def get_job(self, job_id):
        job = self.service.get_job(job_id)

        dto = JobResponseDTO(
            job_id=job.job_id,
            job_type=job.job_type,
            status=job.status,
        )

        return asdict(dto)


def main():
    repository = JobRepository()

    repository.save(
        Job(
            job_id="job-1",
            job_type="backup",
            status="queued",
            retries=2,
            internal_notes="Internal scheduling details",
        )
    )

    service = JobService(repository)
    api = APIHandler(service)

    response = api.get_job("job-1")

    print("API response:", json.dumps(response, sort_keys=True))


if __name__ == "__main__":
    main()
