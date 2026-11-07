import json
from dataclasses import dataclass


# MODEL
@dataclass
class Task:
    id: str
    status: str = "pending"


class TaskModel:
    def __init__(self):
        self.tasks: dict[str, Task] = {}

    def submit(self, task_id: str) -> Task:
        task = Task(task_id)
        self.tasks[task_id] = task
        return task

    def get(self, task_id: str) -> Task | None:
        return self.tasks.get(task_id)

    def complete(self, task_id: str) -> bool:
        task = self.get(task_id)

        if task is None or task.status != "pending":
            return False

        task.status = "completed"
        return True


# VIEW
class TaskView:
    def render_task(self, task: Task | None) -> str:
        if task is None:
            return json.dumps({"error": "task not found"}, sort_keys=True)

        return json.dumps({"id": task.id, "status": task.status}, sort_keys=True)

    def render_completion(self, task_id: str, completed: bool) -> str:
        return json.dumps({"id": task_id, "completed": completed}, sort_keys=True)


# CONTROLLER
class TaskController:
    def __init__(self, model: TaskModel, view: TaskView):
        self.model = model
        self.view = view

    def submit(self, task_id: str) -> str:
        task = self.model.submit(task_id)
        return self.view.render_task(task)

    def get_status(self, task_id: str) -> str:
        task = self.model.get(task_id)
        return self.view.render_task(task)

    def complete(self, task_id: str) -> str:
        completed = self.model.complete(task_id)
        return self.view.render_completion(task_id, completed)


def main():
    model = TaskModel()
    view = TaskView()
    controller = TaskController(model, view)

    print(controller.submit("task-1"))
    print(controller.get_status("task-1"))
    print(controller.complete("task-1"))
    print(controller.get_status("task-1"))
    print(controller.complete("task-1"))


if __name__ == "__main__":
    main()
