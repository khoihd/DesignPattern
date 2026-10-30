import random
from abc import ABC, abstractmethod
from collections import deque


# Receiver
class Worker:
    def __init__(self, worker_id: str):
        self._worker_id = worker_id
    
    def execute_task(self, task_id: str):
        print(f"Worker {self._worker_id} is executing task {task_id}")

    def cancel_task(self, task_id: str):
        print(f"Worker {self._worker_id} is canceling task {task_id}")

    def restart_service(self, task_id: str):
        print(f"Worker {self._worker_id} is restarting service {task_id}")


class Command(ABC):
    def __init__(self, task_id: str):
        self._worker = None
        self._task_id = task_id

    def set_worker(self, worker):
        self._worker = worker

    @abstractmethod
    def execute(self) -> None:
        pass


class ExecuteTaskCommand(Command):
    def execute(self) -> None:
        if self._worker is None:
            raise RuntimeError("Worker is not set or not available")
        
        self._worker.execute_task(self._task_id)


class CancelTaskCommand(Command):
    def execute(self) -> None:
        if self._worker is None:
            print("Worker is not set or not available")
            return
        
        self._worker.cancel_task(self._task_id)


class RestartServiceCommand(Command):
    def execute(self) -> None:
        if self._worker is None:
            print("Worker is not set or not available")
            return
        
        self._worker.restart_service(self._task_id)


# Invoker
class TaskScheduler:
    def __init__(self, workers: list[Worker]):
        self._workers = workers
        self._queue: deque[Command] = deque()

    def select_worker(self):
        return random.choice(self._workers)

    def submit(self, command: Command):
        self._queue.append(command)
        
    def run(self):
        while self._queue:
            command = self._queue.popleft()
            worker = self.select_worker()
            command.set_worker(worker)
            command.execute()


# ==========================================
# 5. Client
# ==========================================
if __name__ == "__main__":
    workers = [Worker(i) for i in range(10)]
    scheduler = TaskScheduler(workers)
    command1 = ExecuteTaskCommand(
        "task-101"
    )

    command2 = CancelTaskCommand(
        "task-102"
    )

    command3 = RestartServiceCommand(
        "database-service"
    )

    scheduler.submit(command1)
    scheduler.submit(command2)
    scheduler.submit(command3)
    print("All commands submitted.")
    scheduler.run()
