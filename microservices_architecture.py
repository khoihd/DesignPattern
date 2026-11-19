from multiprocessing import get_context


# ==========================================
# 1. JOB SERVICE
# ==========================================
class JobService:
    def __init__(self):
        self._jobs = {}

    def submit_job(self, job_id):
        self._jobs[job_id] = {
            "status": "queued",
            "worker_id": None,
        }

    def next_queued_job(self):
        for job_id, job in self._jobs.items():
            if job["status"] == "queued":
                return job_id
        
        return None

    def assign_job(self, job_id, worker_id):
        self._jobs[job_id]["status"] = "running"
        self._jobs[job_id]["worker_id"] = worker_id

    def get_job_info(self, job_id):
        job = self._jobs[job_id]
        return job["status"], job["worker_id"]


# ==========================================
# 2. WORKER SERVICE
# ==========================================
class WorkerService:
    def __init__(self):
        self._busy = {}

    def register_worker(self, worker_id):
        self._busy[worker_id] = False

    def reserve_available_worker(self):
        for worker_id, busy in self._busy.items():
            if not busy:
                self._busy[worker_id] = True
                return worker_id
        
        return None


# ==========================================
# 3. SERVICE PROCESS / MESSAGE HANDLER
# ==========================================
def serve(conn, service_type):
    # Service state is created inside its own process.
    service = service_type()

    while True:
        method, args = conn.recv()

        if method == "stop":
            conn.send(None)
            break

        # Trusted local demo: invoke the requested method.
        result = getattr(service, method)(*args)
        conn.send(result)

    conn.close()


# ==========================================
# 4. INTER-PROCESS REQUEST-REPLY
# ==========================================
def rpc(conn, method, *args):
    conn.send((method, args))
    return conn.recv()


# ==========================================
# 5. SERVICE CLIENTS
# ==========================================
class JobClient:
    def __init__(self, conn):
        self.conn = conn

    def submit_job(self, job_id):
        return rpc(self.conn, "submit_job", job_id)

    def next_queued_job(self):
        return rpc(self.conn, "next_queued_job")

    def assign_job(self, job_id, worker_id):
        return rpc(self.conn, "assign_job", job_id, worker_id)

    def get_job_info(self, job_id):
        return rpc(self.conn, "get_job_info", job_id)


class WorkerClient:
    def __init__(self, conn):
        self.conn = conn

    def register_worker(self, worker_id):
        return rpc(self.conn, "register_worker", worker_id)

    def reserve_available_worker(self):
        return rpc(self.conn, "reserve_available_worker")


# ==========================================
# 6. SCHEDULER
# ==========================================
class Scheduler:
    def __init__(self, job_client, worker_client):
        self.job_client = job_client
        self.worker_client = worker_client

    def schedule_one(self):
        job_id = self.job_client.next_queued_job()
        if job_id is None:
            return

        worker_id = self.worker_client.reserve_available_worker()
        if worker_id is None:
            return

        self.job_client.assign_job(job_id, worker_id)
        print(f"Scheduled {job_id} on {worker_id}")


# ==========================================
# 7. APPLICATION
# ==========================================
def main():
    ctx = get_context("spawn")

    # Create communication channels.
    job_client_conn, job_server_conn = ctx.Pipe()
    worker_client_conn, worker_server_conn = ctx.Pipe()

    # Create separate service processes.
    jobs_process = ctx.Process(
        target=serve,
        args=(job_server_conn, JobService),
    )

    workers_process = ctx.Process(
        target=serve,
        args=(worker_server_conn, WorkerService),
    )

    jobs_process.start()
    workers_process.start()

    # Parent no longer needs the server ends.
    job_server_conn.close()
    worker_server_conn.close()

    # Construct clients and scheduler.
    job_client = JobClient(job_client_conn)
    worker_client = WorkerClient(worker_client_conn)
    scheduler = Scheduler(job_client, worker_client)

    job_client.submit_job("job-1")
    job_client.submit_job("job-2")
    worker_client.register_worker("worker-a")

    scheduler.schedule_one()

    for job_id in ("job-1", "job-2"):
        status, worker_id = job_client.get_job_info(job_id)
        print(f"{job_id}: {status} ({worker_id or 'unassigned'})")

    # Graceful shutdown for this demonstration.
    rpc(job_client_conn, "stop")
    rpc(worker_client_conn, "stop")

    job_client_conn.close()
    worker_client_conn.close()

    jobs_process.join()
    workers_process.join()


if __name__ == "__main__":
    main()
