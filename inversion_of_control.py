class BackupWorker:
    def backup(self, job_id):
        if job_id == "backup-2":
            raise RuntimeError("storage unavailable")

        print(f"{job_id}: backup saved")


class ReportWorker:
    def generate(self, job_id):
        print(f"{job_id}: report generated")


class JobRuntime:
    def __init__(self):
        self.handlers = {}

    def register(self, job_type, handler):
        if job_type in self.handlers:
            raise ValueError(f"Duplicate handler: {job_type}")

        self.handlers[job_type] = handler

    def run(self, jobs):
        statuses = {}

        for job_type, job_id in jobs:
            handler = self.handlers.get(job_type)

            if handler is None:
                print(f"{job_id}: failed (no handler for {job_type})")
                statuses[job_id] = "failed"
                continue

            try:
                handler(job_id)
            except RuntimeError as error:
                print(f"{job_id}: failed ({error})")
                statuses[job_id] = "failed"
            else:
                print(f"{job_id}: completed")
                statuses[job_id] = "completed"

        return statuses


def main():
    backup_worker = BackupWorker()
    report_worker = ReportWorker()

    runtime = JobRuntime()

    runtime.register("backup", backup_worker.backup)
    runtime.register("report", report_worker.generate)

    jobs = [
        ("backup", "backup-1"),
        ("backup", "backup-2"),
        ("report", "report-1"),
    ]

    statuses = runtime.run(jobs)
    print(f"Final statuses: {statuses}")


if __name__ == "__main__":
    main()
