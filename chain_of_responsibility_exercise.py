# Let’s apply Chain of Responsibility to another distributed systems scenario.

# Imagine we’re building a distributed job scheduler.

# Before accepting a job, the scheduler must perform three checks:

# 1. Priority check: Reject jobs with invalid priorities.
# 2. Resource check: Reject jobs requesting too much CPU.
# 3. Scheduling: Assign accepted jobs to a worker.

# The desired processing flow is:

# Job Submission
#       |
#       v
# PriorityHandler
#       |
#       v
# ResourceHandler
#       |
#       v
# SchedulingHandler
#       |
#       v
# Job Result
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Job:
    job_id: int
    priority: int
    cpu_required: int


class JobHandler(ABC):
    @abstractmethod
    def handle(self, job: Job) -> str:
        pass


class SchedulingHandler(JobHandler):
    def handle(self, job):
        print("[Scheduling] Assigning worker")
        return f"Job {job.job_id} scheduled on worker-1"


class PriorityHanlder(JobHandler):
    def __init__(self, next_handler: JobHandler):
        self._next_handler = next_handler


    def handle(self, job: Job) -> str:
        print("[Priority] Checking priority")
        
        if not 1 <= job.priority <= 10:
            return "Rejected: Invalid priority"

        return self._next_handler.handle(job)


class ResourceHandler(JobHandler):
    def __init__(self, next_handler: JobHandler):
        self._next_handler = next_handler

    def handle(self, job: Job) -> str:
        print("[Resource] Checking CPU availability")
        
        if job.cpu_required > 8:
            return "Rejected: Insufficient CPU"

        return self._next_handler.handle(job)


def main():
    job = Job(1, 5, 0)
    # define the last scheduler first
    scheduling = SchedulingHandler()
    resource = ResourceHandler(scheduling)
    priority = PriorityHanlder(resource)
    
    result = priority.handle(job)
    print(result)

    # job: priority -> resource -> scheduling
    #       scheduling()
    #       resource(scheduling)
    #       priority(resource)
    #       priority.handle(job)
    

if __name__ == "__main__":
    main()