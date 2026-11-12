class Worker:
    def __init__(self, worker_id, failing_tasks=()):
        self.worker_id = worker_id
        self.failing_tasks = set(failing_tasks)

    def execute(self, task_id):
        return task_id not in self.failing_tasks


class Orchestrator:
    def __init__(self, workers, max_attempts=2):
        if not workers:
            raise ValueError("At least one worker is required")
        if max_attempts < 1:
            raise ValueError("max_attempts must be positive")

        self.workers = workers
        self.max_attempts = max_attempts
        self.statuses = {}

    def run(self, tasks):
        self.statuses = {}

        for index, task_id in enumerate(tasks):
            self.statuses[task_id] = "failed"

            attempts = min(self.max_attempts, len(self.workers))

            for attempt in range(attempts):
                worker_index = (index + attempt) % len(self.workers)
                worker = self.workers[worker_index]

                success = worker.execute(task_id)

                print(
                    f"{task_id} -> {worker.worker_id}: "
                    f"{'success' if success else 'failed'}"
                )

                if success:
                    self.statuses[task_id] = "completed"
                    break

        return self.statuses.copy()


def main():
    workers = [
        Worker("worker-1", failing_tasks={"task-1", "task-3"}),
        Worker("worker-2", failing_tasks={"task-3"}),
    ]

    orchestrator = Orchestrator(workers, max_attempts=2)

    tasks = ["task-1", "task-2", "task-3"]
    statuses = orchestrator.run(tasks)

    print(f"Final statuses: {statuses}")


if __name__ == "__main__":
    main()
