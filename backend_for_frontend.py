class DispatchService:
    def __init__(self):
        self._jobs = {
            "job-1": {
                "job_id": "job-1",
                "status": "running",
                "priority": "high",
                "worker_id": "worker-a",
            }
        }

    def get_job(self, job_id):
        return self._jobs[job_id].copy()


class WorkerDirectoryService:
    def __init__(self):
        self._workers = {
            "worker-a": {
                "name": "Alice",
                "team": "Compute",
            }
        }

    def get_worker(self, worker_id):
        return self._workers[worker_id].copy()


# Backend specifically for the web application.
class WebBFF:
    def __init__(self, dispatch, directory):
        self.dispatch = dispatch
        self.directory = directory

    def get_job_view(self, job_id):
        job = self.dispatch.get_job(job_id)
        worker = self.directory.get_worker(job["worker_id"])

        return {
            "job_id": job["job_id"],
            "status": job["status"],
            "priority": job["priority"],
            "worker": {
                "name": worker["name"],
                "team": worker["team"],
            },
        }


# Backend specifically for the mobile application.
class MobileBFF:
    def __init__(self, dispatch):
        self.dispatch = dispatch

    def get_job_view(self, job_id):
        job = self.dispatch.get_job(job_id)

        return {
            "job_id": job["job_id"],
            "status": job["status"],
        }


class APIGateway:
    def __init__(self, routes):
        self.routes = routes

    def get(self, path):
        prefix, _, resource_id = path.rpartition("/")
        handler = self.routes.get(prefix)

        if handler is None or not resource_id:
            raise ValueError(f"Unknown path: {path}")

        return handler(resource_id)


class WebClient:
    def __init__(self, gateway):
        self.gateway = gateway

    def display_job(self, job_id):
        return self.gateway.get(f"/web/jobs/{job_id}")


class MobileClient:
    def __init__(self, gateway):
        self.gateway = gateway

    def display_job(self, job_id):
        return self.gateway.get(f"/mobile/jobs/{job_id}")


def main():
    dispatch = DispatchService()
    directory = WorkerDirectoryService()

    web_bff = WebBFF(dispatch, directory)
    mobile_bff = MobileBFF(dispatch)

    gateway = APIGateway(
        {
            "/web/jobs": web_bff.get_job_view,
            "/mobile/jobs": mobile_bff.get_job_view,
        }
    )

    web = WebClient(gateway)
    mobile = MobileClient(gateway)

    print("Web:", web.display_job("job-1"))
    print("Mobile:", mobile.display_job("job-1"))


if __name__ == "__main__":
    main()
