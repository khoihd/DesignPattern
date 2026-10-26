from abc import ABC, abstractmethod


# ==========================================
# Component
# ==========================================
class JobComponent(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def get_cost(self) -> int:
        pass


# ==========================================
# Leaf
# ==========================================
class Task(JobComponent):
    def __init__(self, name: str, cost: int):
        self.name = name
        self.cost = cost

    def execute(self) -> None:
        print(f"[Task] Executing {self.name}")

    def get_cost(self) -> int:
        return self.cost


# ==========================================
# Composite
# ==========================================
class TaskGroup(JobComponent):
    def __init__(self, name: str):
        self.name = name
        self.children: list[JobComponent] = []

    def add(self, component: JobComponent) -> None:
        self.children.append(component)

    def execute(self) -> None:
        print(f"[TaskGroup] Starting {self.name}")

        for child in self.children:
            child.execute()

        print(f"[TaskGroup] Completed {self.name}")

    def get_cost(self) -> int:
        return sum(child.get_cost() for child in self.children)


# ==========================================
# Client
# ==========================================
def main():
    # Individual tasks
    download = Task("DownloadData", 10)
    clean = Task("CleanData", 15)
    transform = Task("TransformData", 20)
    upload = Task("UploadResults", 5)

    # Nested group
    processing = TaskGroup("Processing")
    processing.add(clean)
    processing.add(transform)

    # Root group
    job = TaskGroup("DataProcessing")
    job.add(download)
    job.add(processing)
    job.add(upload)

    # Execute entire hierarchy
    job.execute()

    # Aggregate computational cost
    print(f"\nTotal computational cost: {job.get_cost()}")


if __name__ == "__main__":
    main()
