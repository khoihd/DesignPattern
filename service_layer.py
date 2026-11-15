class JobRepository:
    def __init__(self):
        self.jobs = {}

    def exists(self, job_id):
        return job_id in self.jobs

    def save(self, job_id, job):
        self.jobs[job_id] = job


class JobQueue:
    def __init__(self):
        self.pending = []

    def enqueue(self, job_id):
        self.pending.append(job_id)


class JobService:
    def __init__(self, repository, queue):
        self.repository = repository
        self.queue = queue

    def submit(self, job_id, job_type):
        if job_type not in {"backup", "report"}:
            raise ValueError(f"unsupported job type: {job_type}")

        if self.repository.exists(job_id):
            raise ValueError(f"duplicate job ID: {job_id}")

        job = {"type": job_type, "status": "queued"}
        self.repository.save(job_id, job)
        self.queue.enqueue(job_id)

        return job


class APIHandler:
    def __init__(self, service):
        self.service = service

    def submit(self, job_id, job_type):
        try:
            job = self.service.submit(job_id, job_type)
        except ValueError as error:
            return {"error": str(error)}

        return {"job_id": job_id, "status": job["status"]}


class CLICommand:
    def __init__(self, service):
        self.service = service

    def submit(self, job_id, job_type):
        try:
            self.service.submit(job_id, job_type)
        except ValueError as error:
            print(f"CLI: error ({error})")
        else:
            print(f"CLI: accepted {job_id}")


def main():
    repository = JobRepository()
    queue = JobQueue()
    service = JobService(repository, queue)

    api = APIHandler(service)
    cli = CLICommand(service)

    print("API:", api.submit("job-1", "backup"))
    cli.submit("job-2", "report")
    print("API:", api.submit("job-3", "cleanup"))
    cli.submit("job-1", "report")

    print("Jobs:", repository.jobs)
    print("Queue:", queue.pending)


if __name__ == "__main__":
    main()
