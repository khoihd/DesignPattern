import sqlite3


# Domain Model
class Job:
    def __init__(self, job_id, status):
        self.id = job_id
        self.status = status

    def complete(self):
        if self.status != "running":
            raise ValueError("Only running jobs can be completed")

        self.status = "completed"


# Data Mapper
class JobMapper:
    def __init__(self, db):
        self.db = db

    def find_by_id(self, job_id):
        row = self.db.execute(
            "SELECT job_id, state FROM jobs WHERE job_id = ?",
            (job_id,),
        ).fetchone()

        if row is None:
            raise ValueError("Job not found")

        # Database row -> Domain object
        return Job(
            job_id=row[0],
            status=row[1],
        )

    def save(self, job):
        # Domain object -> Database row
        self.db.execute(
            "UPDATE jobs SET state = ? WHERE job_id = ?",
            (job.status, job.id),
        )


def setup_db():
    db = sqlite3.connect(":memory:")

    db.execute("""
        CREATE TABLE jobs (
            job_id TEXT PRIMARY KEY,
            state TEXT NOT NULL
        )
    """)

    db.execute(
        "INSERT INTO jobs VALUES (?, ?)",
        ("job-1", "running"),
    )
    db.commit()

    return db


def main():
    db = setup_db()

    mapper = JobMapper(db)

    job = mapper.find_by_id("job-1")
    print(f"Loaded: {job.id} ({job.status})")

    job.complete()
    mapper.save(job)
    db.commit()

    print(f"Domain: {job.id} ({job.status})")

    row = db.execute(
        "SELECT state FROM jobs WHERE job_id = ?",
        ("job-1",),
    ).fetchone()
    print(f"Database: {row[0]}")

    db.close()


if __name__ == "__main__":
    main()
