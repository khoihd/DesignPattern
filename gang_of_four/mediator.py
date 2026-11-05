from collections import deque


# 1. Colleague: TaskScheduler
class TaskScheduler:
    def __init__(self):
        self.pending = deque()

    def enqueue(self, task: str):
        self.pending.append(task)
        print(f"Queued {task}")

    def requeue(self, task: str):
        self.pending.appendleft(task)
        print(f"Requeued {task}")

    def next_task(self) -> str | None:
        if not self.pending:
            return None

        return self.pending.popleft()


# 2. Colleague: WorkerManager
class WorkerManager:
    def __init__(self, workers: list[str]):
        self.running = {worker: None for worker in workers}
        self.failed = set()

    def assign(self, task: str) -> bool:
        for worker, current_task in self.running.items():
            if worker not in self.failed and current_task is None:
                self.running[worker] = task
                print(f"Assigned {task} to {worker}")
                return True

        return False

    def fail(self, worker: str) -> str | None:
        if worker not in self.running:
            raise ValueError(f"Unknown worker: {worker}")

        self.failed.add(worker)
        task = self.running[worker]
        self.running[worker] = None

        print(f"{worker} marked unhealthy")
        return task


# 3. Mediator
class TaskMediator:
    def __init__(self, scheduler: TaskScheduler, workers: WorkerManager):
        self.scheduler = scheduler
        self.workers = workers

    def submit(self, task: str):
        self.scheduler.enqueue(task)
        self.dispatch()

    def dispatch(self):
        while True:
            task = self.scheduler.next_task()

            if task is None:
                break

            if not self.workers.assign(task):
                self.scheduler.requeue(task)
                break

    def worker_failed(self, worker: str):
        task = self.workers.fail(worker)

        if task is not None:
            self.scheduler.requeue(task)

        self.dispatch()


# 4. Colleague: HealthMonitor
class HealthMonitor:
    def __init__(self, mediator: TaskMediator):
        self.mediator = mediator

    def report_failure(self, worker: str):
        print(f"Detected failure of {worker}")
        self.mediator.worker_failed(worker)


# 5. Client
if __name__ == "__main__":
    scheduler = TaskScheduler()
    workers = WorkerManager(["worker-1", "worker-2"])

    mediator = TaskMediator(scheduler, workers)
    monitor = HealthMonitor(mediator)

    mediator.submit("task-101")
    monitor.report_failure("worker-1")
