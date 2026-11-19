class WorkerDirectoryService:
    def __init__(self):
        self._profiles = {}

    def register_worker(self, worker_id, name):
        self._profiles[worker_id] = {"name": name}

    def list_worker_ids(self):
        return list(self._profiles)

    def get_worker_name(self, worker_id):
        return self._profiles[worker_id]["name"]


class DispatchService:
    def __init__(self):
        self._jobs = {}
        self._worker_busy = {}

    def add_worker(self, worker_id):
        self._worker_busy[worker_id] = False

    def submit_job(self, job_id):
        self._jobs[job_id] = {
            "status": "queued",
            "worker_id": None,
        }

    def schedule_one(self):
        # Find a queued job.
        job_id = None
        for candidate, job in self._jobs.items():
            if job["status"] == "queued":
                job_id = candidate
                break

        if job_id is None:
            return

        # Find an available worker.
        worker_id = None
        for candidate, busy in self._worker_busy.items():
            if not busy:
                worker_id = candidate
                break

        if worker_id is None:
            return

        # Both updates belong to DispatchService.
        self._worker_busy[worker_id] = True
        self._jobs[job_id]["status"] = "running"
        self._jobs[job_id]["worker_id"] = worker_id

        print(f"Scheduled {job_id} on {worker_id}")

    def get_job_info(self, job_id):
        return self._jobs[job_id]


def main():
    directory = WorkerDirectoryService()
    dispatch = DispatchService()

    directory.register_worker("worker-a", "Alice")

    # Synchronize eligible workers during initial setup.
    for worker_id in directory.list_worker_ids():
        dispatch.add_worker(worker_id)

    dispatch.submit_job("job-1")
    dispatch.submit_job("job-2")

    dispatch.schedule_one()

    for job_id in ("job-1", "job-2"):
        job = dispatch.get_job_info(job_id)
        worker_id = job["worker_id"] or "unassigned"
        print(f"{job_id}: {job['status']} ({worker_id})")


if __name__ == "__main__":
    main()
