# ==========================================
# 1. JOBS MODULE
# ==========================================
class JobsModule:
    def __init__(self):
        # Internal state owned by the Jobs module.
        self._jobs = {}

    def submit_job(self, job_id: str):
        self._jobs[job_id] = {
            "status": "queued",
            "worker_id": None,
        }

    def next_queued_job(self) -> str | None:
        for job_id, job in self._jobs.items():
            if job["status"] == "queued":
                return job_id
        return None

    def assign_job(self, job_id: str, worker_id: str):
        job = self._jobs[job_id]
        job["status"] = "running"
        job["worker_id"] = worker_id

    def get_job_info(self, job_id: str) -> tuple[str, str | None]:
        job = self._jobs[job_id]
        return job["status"], job["worker_id"]


# ==========================================
# 2. WORKERS MODULE
# ==========================================
class WorkersModule:
    def __init__(self):
        # Internal state owned by the Workers module.
        self._busy = {}

    def register_worker(self, worker_id: str):
        self._busy[worker_id] = False

    def reserve_available_worker(self) -> str | None:
        for worker_id, busy in self._busy.items():
            if not busy:
                self._busy[worker_id] = True
                return worker_id
        return None


# ==========================================
# 3. SCHEDULING MODULE
# ==========================================
class Scheduler:
    def __init__(self, jobs: JobsModule, workers: WorkersModule):
        self.jobs = jobs
        self.workers = workers

    def schedule_one(self):
        job_id = self.jobs.next_queued_job()
        if job_id is None:
            return

        worker_id = self.workers.reserve_available_worker()
        if worker_id is None:
            return

        self.jobs.assign_job(job_id, worker_id)

        print(f"Scheduled {job_id} on {worker_id}")


# ==========================================
# 4. APPLICATION / COMPOSITION ROOT
# ==========================================
def main():
    jobs = JobsModule()
    workers = WorkersModule()

    jobs.submit_job("job-1")
    jobs.submit_job("job-2")

    workers.register_worker("worker-a")

    scheduler = Scheduler(jobs, workers)
    scheduler.schedule_one()

    for job_id in ("job-1", "job-2"):
        status, worker_id = jobs.get_job_info(job_id)
        worker = worker_id or "unassigned"
        print(f"{job_id}: {status} ({worker})")


if __name__ == "__main__":
    main()
