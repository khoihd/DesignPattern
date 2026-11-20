class LegacyJobApplication:
    def __init__(self):
        self.jobs = {
            "job-1": {
                "job_id": "job-1",
                "status": "running",
                "worker_id": "worker-a",
            }
        }

        self.workers = {
            "worker-a": {
                "worker_id": "worker-a",
                "name": "Alice",
            }
        }

    def get_job(self, job_id):
        print("[Legacy] get_job")
        return self.jobs[job_id].copy()

    def get_worker(self, worker_id):
        print("[Legacy] get_worker")
        return self.workers[worker_id].copy()

    # Simplified data export for migration.
    def export_jobs(self):
        return {k: v.copy() for k, v in self.jobs.items()}

    def export_workers(self):
        return {k: v.copy() for k, v in self.workers.items()}


class JobService:
    def __init__(self, jobs):
        # Independent copy of migrated records.
        self.jobs = {k: v.copy() for k, v in jobs.items()}

    def get_job(self, job_id):
        print("[JobService] get_job")
        return self.jobs[job_id].copy()


class WorkerDirectoryService:
    def __init__(self, workers):
        # Independent copy of migrated records.
        self.workers = {k: v.copy() for k, v in workers.items()}

    def get_worker(self, worker_id):
        print("[WorkerDirectoryService] get_worker")
        return self.workers[worker_id].copy()


class StranglerRouter:
    def __init__(self, legacy):
        # Initially, every request goes to the legacy system.
        self.handlers = {
            "jobs": legacy.get_job,
            "workers": legacy.get_worker,
        }

    def get(self, path):
        resource, record_id = path.strip("/").split("/")

        handler = self.handlers.get(resource)
        if handler is None:
            raise ValueError(f"Unknown resource: {resource}")

        return handler(record_id)

    def migrate(self, resource, new_handler):
        if resource not in self.handlers:
            raise ValueError(f"Unknown resource: {resource}")

        self.handlers[resource] = new_handler


class JobDashboard:
    def __init__(self, api):
        self.api = api

    def display(self):
        print(self.api.get("/jobs/job-1"))
        print(self.api.get("/workers/worker-a"))


def main():
    legacy = LegacyJobApplication()
    router = StranglerRouter(legacy)
    dashboard_client = JobDashboard(router)

    # Phase 0: Everything is still handled by legacy.
    print("=== Phase 0: Legacy ===")
    dashboard_client.display()

    # Phase 1: Migrate worker management.
    new_worker_directory = WorkerDirectoryService(legacy.export_workers())

    router.migrate(
        "workers",
        new_worker_directory.get_worker,
    )

    print("\n=== Phase 1: Workers migrated ===")
    dashboard_client.display()

    # Phase 2: Migrate job management.
    new_job_service = JobService(legacy.export_jobs())

    router.migrate(
        "jobs",
        new_job_service.get_job,
    )

    print("\n=== Phase 2: Jobs migrated ===")
    dashboard_client.display()


if __name__ == "__main__":
    main()
