import time
from collections import deque
from threading import Lock


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: float):
        if max_requests <= 0 or window_seconds <= 0:
            raise ValueError("Rate limit must be positive")

        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.timestamps = deque()
        self.lock = Lock()

    def allow_request(self) -> bool:
        with self.lock:
            now = time.monotonic()

            # Remove expired timestamps.
            while self.timestamps and now - self.timestamps[0] >= self.window_seconds:
                self.timestamps.popleft()

            # Reject if the rate limit is reached.
            if len(self.timestamps) >= self.max_requests:
                return False

            # Accept and record the request.
            self.timestamps.append(now)
            return True


class JobRepository:
    def __init__(self):
        self.jobs = {}

    def save(self, job_id: str):
        self.jobs[job_id] = {"job_id": job_id, "status": "PENDING"}


class JobService:
    def __init__(self, repository: JobRepository, rate_limiter: RateLimiter):
        self.repository = repository
        self.rate_limiter = rate_limiter

    def submit_job(self, job_id: str) -> bool:
        if not self.rate_limiter.allow_request():
            print(f"[JobService] Rejected {job_id}: rate limit exceeded")
            return False

        self.repository.save(job_id)
        print(f"[JobService] Accepted {job_id}")
        return True


def main():
    repository = JobRepository()

    rate_limiter = RateLimiter(max_requests=3, window_seconds=1.0)

    job_service = JobService(repository, rate_limiter)

    print("--- First batch ---")

    for i in range(1, 7):
        job_service.submit_job(f"job-{i}")

    print("Waiting for 1.1 seconds...")
    time.sleep(1.1)

    print("--- Second batch ---")

    for i in range(7, 11):
        job_service.submit_job(f"job-{i}")

    print("Total stored jobs: {len(repository.jobs)}")


if __name__ == "__main__":
    main()
