import copy
from dataclasses import dataclass, field


@dataclass
class JobConfig:
    cpu: int
    memory: int
    timeout: int
    retries: int
    environment: dict = field(default_factory=dict)
    retry_policy: dict = field(default_factory=dict)


class Job:
    def __init__(self, name: str, config: JobConfig):
        self.name = name
        self.config = config

    def clone(self):
        return copy.deepcopy(self)


class JobScheduler:
    def __init__(self):
        self.jobs = []

    def submit(self, job: Job):
        self.jobs.append(job)

        print(
            f"Submitted {job.name}: "
            f"CPU={job.config.cpu}, "
            f"Memory={job.config.memory}, "
            f"Timeout={job.config.timeout}"
        )


def main():
    # 1. Create a prototype
    prototype = Job(
        name="standard-job",
        config=JobConfig(
            cpu=4,
            memory=8192,
            timeout=300,
            retries=3,
            environment={"LOG_LEVEL": "INFO", "REGION": "us-west-2"},
            retry_policy={
                "backoff": 2,
                "retryable_errors": ["TIMEOUT", "CONNECTION_ERROR"],
            },
        ),
    )

    # 2. Clone the prototype
    payment_job = prototype.clone()
    payment_job.name = "process-payments"

    report_job = prototype.clone()
    report_job.name = "generate-reports"

    # 3. Customize the clones
    payment_job.config.timeout = 120
    report_job.config.environment["REGION"] = "us-east-1"
    report_job.config.retry_policy["retryable_errors"].append("RATE_LIMIT")

    # 4. Submit jobs
    scheduler = JobScheduler()
    scheduler.submit(payment_job)
    scheduler.submit(report_job)

    # 5. Verify object independence
    print("\nObject identity:")
    print("Different jobs:", payment_job is not report_job)
    print("Different configs:", payment_job.config is not report_job.config)
    print(
        "Different environments:",
        payment_job.config.environment is not report_job.config.environment,
    )

    print(
        "Different retry lists:",
        payment_job.config.retry_policy["retryable_errors"]
        is not report_job.config.retry_policy["retryable_errors"],
    )

    # 6. Verify prototype is unchanged
    print("\nPrototype configuration:")
    print("Timeout:", prototype.config.timeout)
    print("Region:", prototype.config.environment["REGION"])
    print("Retryable errors:", prototype.config.retry_policy["retryable_errors"])


if __name__ == "__main__":
    main()
