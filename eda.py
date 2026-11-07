from dataclasses import dataclass


# Event
@dataclass(frozen=True)
class TaskCompleted:
    task_id: str


# Event Bus
class EventBus:
    def __init__(self):
        self.handlers: dict[type, list] = {}

    def subscribe(self, event_type: type, handler) -> None:
        self.handlers.setdefault(event_type, []).append(handler)

    def publish(self, event: object) -> None:
        for handler in self.handlers.get(type(event), []):
            handler(event)


# Event Handlers
class AuditLog:
    def on_task_completed(self, event: TaskCompleted) -> None:
        print(f"AUDIT: {event.task_id} completed")


class NotificationService:
    def on_task_completed(self, event: TaskCompleted) -> None:
        print(f"NOTIFY: {event.task_id} completed")


# Publisher
class TaskService:
    def __init__(self, event_bus: EventBus):
        self.tasks: dict[str, str] = {}
        self.event_bus = event_bus

    def submit(self, task_id: str) -> None:
        self.tasks[task_id] = "pending"

    def get_status(self, task_id: str) -> str | None:
        return self.tasks.get(task_id)

    def complete(self, task_id: str) -> bool:
        if self.tasks.get(task_id) != "pending":
            return False

        self.tasks[task_id] = "completed"

        self.event_bus.publish(TaskCompleted(task_id))

        return True


def main():
    event_bus = EventBus()

    audit_log = AuditLog()
    notifier = NotificationService()

    # Register event handlers
    event_bus.subscribe(TaskCompleted, audit_log.on_task_completed)
    event_bus.subscribe(TaskCompleted, notifier.on_task_completed)

    # Create task service
    service = TaskService(event_bus)

    service.submit("task-1")

    print(f"Status before: {service.get_status('task-1')}")
    print(f"First completion: {service.complete('task-1')}")
    print(f"Second completion: {service.complete('task-1')}")
    print(f"Status after: {service.get_status('task-1')}")


if __name__ == "__main__":
    main()
