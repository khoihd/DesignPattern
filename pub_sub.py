from dataclasses import dataclass


@dataclass(frozen=True)
class JobCompleted:
    job_id: str
    worker_id: str


class EventBus:
    def __init__(self):
        # topic -> list of subscriber callbacks
        self._subscribers = {}

    def subscribe(self, topic: str, handler):
        self._subscribers.setdefault(topic, []).append(handler)

    def publish(self, topic: str, event):
        for handler in self._subscribers.get(topic, []):
            handler(event)


class MonitoringService:
    def on_job_completed(self, event: JobCompleted):
        print(f"[MonitoringService] Recorded {event.job_id}")


class NotificationService:
    def on_job_completed(self, event: JobCompleted):
        print(f"[NotificationService] Notified {event.job_id}")


class AuditService:
    def on_job_completed(self, event: JobCompleted):
        print(f"[AuditService] Audited {event.job_id}")


class JobService:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def complete_job(self, job_id: str, worker_id: str):
        event = JobCompleted(job_id, worker_id)

        print(f"[JobService] Completed {job_id}")

        # Publish once, without knowing the subscribers.
        self.event_bus.publish("job.completed", event)


def main():
    event_bus = EventBus()

    monitoring = MonitoringService()
    notification = NotificationService()
    audit = AuditService()

    # Register subscribers.
    event_bus.subscribe("job.completed", monitoring.on_job_completed)
    event_bus.subscribe("job.completed", notification.on_job_completed)
    event_bus.subscribe("job.completed", audit.on_job_completed)

    job_service = JobService(event_bus)

    job_service.complete_job("job-42", "worker-a")


if __name__ == "__main__":
    main()
