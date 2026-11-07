import sqlite3
from dataclasses import dataclass


@dataclass
class Task:
    id: str
    status: str


class TaskRepository:
    def __init__(self, db):
        self.db = db

    def add(self, task):
        self.db.execute(
            "INSERT INTO tasks (id, status) VALUES (?, ?)", (task.id, task.status)
        )
        self.db.commit()

    def get(self, task_id):
        row = self.db.execute(
            "SELECT id, status FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()

        if row is None:
            return None

        return Task(id=row[0], status=row[1])

    def save(self, task):
        self.db.execute(
            "UPDATE tasks SET status = ? WHERE id = ?", (task.status, task.id)
        )
        self.db.commit()


class TaskService:
    def __init__(self, tasks):
        self.tasks = tasks

    def submit(self, task_id):
        task = Task(task_id, "pending")
        self.tasks.add(task)

    def get_status(self, task_id):
        task = self.tasks.get(task_id)
        return task.status if task else None

    def complete(self, task_id):
        task = self.tasks.get(task_id)

        if task is None or task.status != "pending":
            return False

        task.status = "completed"
        self.tasks.save(task)
        return True


def main():
    db = sqlite3.connect(":memory:")

    try:
        db.execute("""
            CREATE TABLE tasks (
                id TEXT PRIMARY KEY,
                status TEXT NOT NULL
            )
        """)

        repository = TaskRepository(db)
        service = TaskService(repository)

        service.submit("task-1")

        print("Before:", service.get_status("task-1"))
        print("Completed:", service.complete("task-1"))
        print("After:", service.get_status("task-1"))
        print("Completed again:", service.complete("task-1"))
    finally:
        db.close()


if __name__ == "__main__":
    main()
