from collections import Counter
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class StatusChanged:
    job_id: str
    old_status: str
    new_status: str


class StatusObserver(Protocol):
    def on_status_changed(self, event: StatusChanged) -> None: ...


class Job:
    def __init__(self, job_id: str):
        self._job_id = job_id
        self._status = "queued"
        self._observers: list[StatusObserver] = []

    @property
    def status(self) -> str:
        return self._status

    def subscribe(self, observer: StatusObserver) -> None:
        if not any(item is observer for item in self._observers):
            self._observers.append(observer)

    def unsubscribe(self, observer: StatusObserver) -> None:
        self._observers = [item for item in self._observers if item is not observer]

    def set_status(self, new_status: str) -> None:
        if new_status not in {"queued", "running", "succeeded", "failed"}:
            raise ValueError(f"unknown status: {new_status}")
        if new_status == self._status:
            return

        old_status = self._status
        self._status = new_status
        event = StatusChanged(self._job_id, old_status, new_status)

        for observer in tuple(self._observers):
            observer.on_status_changed(event)


class MetricsCollector:
    def __init__(self):
        self.counts: Counter[str] = Counter()

    def on_status_changed(self, event: StatusChanged) -> None:
        self.counts[event.new_status] += 1


class AuditLogger:
    def on_status_changed(self, event: StatusChanged) -> None:
        print(f"audit: {event.job_id} {event.old_status} -> {event.new_status}")


if __name__ == "__main__":
    metrics = MetricsCollector()
    audit = AuditLogger()
    job = Job("job-42")
    job.subscribe(metrics)
    job.subscribe(audit)

    job.set_status("running")
    job.set_status("succeeded")

    print("Status:", job.status)
    print("Metrics:", dict(metrics.counts))
