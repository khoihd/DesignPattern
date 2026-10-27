from dataclasses import dataclass


# =========================================================
# 1. Flyweight
# =========================================================
@dataclass(frozen=True, slots=True)
class TaskConfig:
    task_type: str
    cpu: int
    memory: int
    timeout: int
    retry_limit: int


# =========================================================
# 2. Flyweight Factory
# =========================================================
class TaskConfigFactory:
    def __init__(self):
        self._configs = {}

    def get_config(
        self,
        task_type,
        cpu,
        memory,
        timeout,
        retry_limit,
    ):
        key = (
            task_type,
            cpu,
            memory,
            timeout,
            retry_limit,
        )

        if key not in self._configs:
            print(f"[Factory] Creating config: {task_type}")

            self._configs[key] = TaskConfig(*key)

        else:
            print(f"[Factory] Reusing config: {task_type}")

        return self._configs[key]

    def config_count(self):
        return len(self._configs)


# =========================================================
# 3. Context
# =========================================================
class Task:
    def __init__(
        self,
        task_id,
        config: TaskConfig,
        status,
        assigned_worker,
    ):
        self.task_id = task_id
        self.config = config
        self.status = status
        self.assigned_worker = assigned_worker

    def execute(self):
        print(
            f"Task {self.task_id}: "
            f"type={self.config.task_type}, "
            f"cpu={self.config.cpu}, "
            f"worker={self.assigned_worker}, "
            f"status={self.status}"
        )


# =========================================================
# 4. Client
# =========================================================
def main():
    factory = TaskConfigFactory()

    # First configuration
    config_1 = factory.get_config("data_processing", 4, 8192, 300, 3)

    # Same configuration
    config_2 = factory.get_config("data_processing", 4, 8192, 300, 3)

    # Different configuration
    config_3 = factory.get_config("machine_learning", 8, 16384, 600, 2)

    task_1 = Task(101, config_1, "running", "worker-1")
    task_2 = Task(102, config_2, "pending", "worker-2")
    task_3 = Task(103, config_3, "completed", "worker-3")

    print("Executing tasks:")

    task_1.execute()
    task_2.execute()
    task_3.execute()

    print("Object sharing:")
    print("Task 1 and Task 2 share config:", task_1.config is task_2.config)
    print("Task 1 and Task 3 share config:", task_1.config is task_3.config)
    print("Number of unique configurations:", factory.config_count())


if __name__ == "__main__":
    main()
