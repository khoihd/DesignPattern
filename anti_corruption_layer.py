# acl_with.py

from dataclasses import dataclass


# ========================================
# Modern domain model
# ========================================
@dataclass(frozen=True)
class Worker:
    worker_id: str
    accepting_jobs: bool
    available_slots: int

    def can_accept_job(self):
        return self.accepting_jobs and self.available_slots > 0


# ========================================
# Legacy external system
# ========================================
class LegacyWorkerSystem:
    def __init__(self):
        self.nodes = [
            {
                "node_ref": "worker-a",
                "mode": "A",
                "max_jobs": "3",
                "active_jobs": "1",
            },
            {
                "node_ref": "worker-b",
                "mode": "D",
                "max_jobs": "4",
                "active_jobs": "0",
            },
            {
                "node_ref": "worker-c",
                "mode": "A",
                "max_jobs": "2",
                "active_jobs": "2",
            },
        ]

    def list_nodes(self):
        print("[LegacyWorkerSystem] list_nodes()")
        return [node.copy() for node in self.nodes]


# ========================================
# Anti-Corruption Layer
# ========================================
# Translate from the legacy worker information format to new worker information format
# ACL takes the legacy as dependent injection, but implements methods with modern API and access the legacy
class WorkerDirectoryACL:
    def __init__(self, legacy_system):
        self.legacy_system = legacy_system

    def list_workers(self):
        nodes = self.legacy_system.list_nodes()

        print("[WorkerDirectoryACL] Translating legacy records")

        return [self._to_worker(node) for node in nodes]

    def _to_worker(self, node):
        mode = node["mode"]

        if mode not in {"A", "D"}:
            raise ValueError(f"Unknown legacy worker mode: {mode}")

        max_jobs = int(node["max_jobs"])
        active_jobs = int(node["active_jobs"])

        if max_jobs < 0 or not 0 <= active_jobs <= max_jobs:
            raise ValueError("Invalid legacy worker capacity")

        return Worker(
            worker_id=node["node_ref"],
            accepting_jobs=(mode == "A"),
            available_slots=max_jobs - active_jobs,
        )


# ========================================
# Modern application service
# ========================================
class JobService:
    def __init__(self, worker_directory):
        self.worker_directory = worker_directory

    # Implement the modern select_worker method
    #   using ACL as an adapter to the legacy system
    def select_worker(self, job_id):
        workers = self.worker_directory.list_workers()

        for worker in workers:
            if worker.can_accept_job():
                print(f"[JobService] {job_id} selected {worker.worker_id}")
                return worker.worker_id

        raise RuntimeError("No available worker")


# ========================================
# Composition root
# ========================================
def main():
    legacy = LegacyWorkerSystem()

    worker_directory = WorkerDirectoryACL(legacy)

    job_service = JobService(worker_directory)

    job_service.select_worker("job-42")


if __name__ == "__main__":
    main()
