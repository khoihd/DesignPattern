import threading
import time
from dataclasses import dataclass
from queue import Queue


@dataclass(frozen=True)
class JobRequest:
    request_id: str
    job_id: str


@dataclass(frozen=True)
class JobReply:
    request_id: str
    job_id: str
    worker_id: str
    status: str


class JobService:
    def __init__(self, request_queue: Queue, reply_queue: Queue):
        self.request_queue = request_queue
        self.reply_queue = reply_queue
        self.next_request_number = 1

    def submit_job(self, job_id: str) -> str:
        request_id = f"req-{self.next_request_number}"
        self.next_request_number += 1

        request = JobRequest(request_id, job_id)
        self.request_queue.put(request)

        print(f"[JobService] Sent {request_id} for {job_id}")
        return request_id

    def receive_replies(self, count: int) -> dict:
        replies = {}

        for _ in range(count):
            reply = self.reply_queue.get()

            try:
                print(f"[JobService] Received reply for {reply.request_id}")
                replies[reply.request_id] = reply
            finally:
                self.reply_queue.task_done()

        return replies


class WorkerService:
    def __init__(self, worker_id: str, request_queue: Queue, reply_queue: Queue):
        self.worker_id = worker_id
        self.request_queue = request_queue
        self.reply_queue = reply_queue

    def run(self):
        while True:
            request = self.request_queue.get()

            try:
                if request is None:
                    break

                print(
                    f"[{self.worker_id}] Executing "
                    f"{request.job_id} ({request.request_id})"
                )

                # Simulate different execution durations.
                duration = 0.2 if request.job_id == "job-1" else 0.05
                time.sleep(duration)

                reply = JobReply(
                    request_id=request.request_id,
                    job_id=request.job_id,
                    worker_id=self.worker_id,
                    status="completed",
                )

                self.reply_queue.put(reply)
                print(f"[{self.worker_id}] Sent reply for {request.request_id}")
            finally:
                self.request_queue.task_done()


def main():
    request_queue = Queue()
    reply_queue = Queue()

    job_service = JobService(request_queue, reply_queue)

    workers = [
        WorkerService("worker-a", request_queue, reply_queue),
        WorkerService("worker-b", request_queue, reply_queue),
    ]

    threads = [threading.Thread(target=worker.run) for worker in workers]

    for thread in threads:
        thread.start()

    # Send both requests without waiting for either result.
    request_ids = [
        job_service.submit_job("job-1"),
        job_service.submit_job("job-2"),
    ]

    # Collect both replies, regardless of arrival order.
    replies = job_service.receive_replies(len(request_ids))

    print("\nMatched results:")
    for request_id in request_ids:
        reply = replies[request_id]
        print(f"{request_id} -> {reply.job_id}: {reply.status} by {reply.worker_id}")

    # Wait until workers finish processing.
    request_queue.join()

    # Stop the workers gracefully.
    for _ in workers:
        request_queue.put(None)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
