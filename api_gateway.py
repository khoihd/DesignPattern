class DispatchService:
    def __init__(self):
        self._jobs = {}

    def submit_job(self, job_id):
        self._jobs[job_id] = {"status": "queued"}

    def get_job(self, job_id):
        return self._jobs[job_id]


class WorkerDirectoryService:
    def __init__(self):
        self._workers = {}

    def register_worker(self, worker_id, name):
        self._workers[worker_id] = name

    def list_workers(self):
        return self._workers.copy()


class APIGateway:
    def __init__(self, dispatch, directory):
        self.dispatch = dispatch
        self.directory = directory

    def handle(self, method, path, token, body=None):
        # 1. Shared authentication
        if token != "demo-token":
            return {
                "status": 401,
                "body": {"error": "Unauthorized"},
            }

        # 2. Route to WorkerDirectoryService
        if method == "GET" and path == "/workers":
            return {
                "status": 200,
                "body": self.directory.list_workers(),
            }

        # 3. Route to DispatchService
        if method == "POST" and path == "/jobs":
            job_id = body["job_id"]
            self.dispatch.submit_job(job_id)

            return {
                "status": 201,
                "body": {"job_id": job_id},
            }

        if method == "GET" and path.startswith("/jobs/"):
            job_id = path.removeprefix("/jobs/")

            return {
                "status": 200,
                "body": self.dispatch.get_job(job_id),
            }

        return {
            "status": 404,
            "body": {"error": "Not found"},
        }


def main():
    dispatch = DispatchService()
    directory = WorkerDirectoryService()

    directory.register_worker("worker-a", "Alice")

    # Create the API Gateway.
    gateway = APIGateway(dispatch, directory)

    # Client only communicates with the gateway.
    token = "demo-token"

    response = gateway.handle("GET", "/workers", token)
    print("Workers:", response["body"])

    gateway.handle(
        "POST",
        "/jobs",
        token,
        {"job_id": "job-1"},
    )

    response = gateway.handle("GET", "/jobs/job-1", token)
    print("Job:", response["body"])

    # Authentication is handled by the gateway.
    response = gateway.handle("GET", "/workers", "invalid-token")
    print("Unauthorized request:", response["status"])


if __name__ == "__main__":
    main()
