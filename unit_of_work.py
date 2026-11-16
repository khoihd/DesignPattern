import sqlite3


def setup_db():
    db = sqlite3.connect(":memory:")
    db.executescript("""
        CREATE TABLE jobs (
            id TEXT PRIMARY KEY,
            status TEXT NOT NULL
        );

        CREATE TABLE workers (
            id TEXT PRIMARY KEY,
            completed_jobs INTEGER NOT NULL
        );

        INSERT INTO jobs VALUES ('job-1', 'running');
        INSERT INTO workers VALUES ('worker-1', 0);
    """)
    return db


class JobRepository:
    def __init__(self, db):
        self.db = db

    def complete(self, job_id):
        self.db.execute("UPDATE jobs SET status = 'completed' WHERE id = ?", (job_id,))


class WorkerRepository:
    def __init__(self, db):
        self.db = db

    def record_completion(self, worker_id):
        self.db.execute(
            """UPDATE workers
               SET completed_jobs = completed_jobs + 1
               WHERE id = ?""",
            (worker_id,),
        )


class UnitOfWork:
    def __init__(self, db):
        self.db = db
        self.jobs = JobRepository(db)
        self.workers = WorkerRepository(db)
        self._committed = False

    def __enter__(self):
        self.db.execute("BEGIN")
        self._committed = False
        return self

    def commit(self):
        self.db.commit()
        self._committed = True

    def __exit__(self, exc_type, exc_value, traceback):
        if not self._committed:
            self.db.rollback()


def finish_job(db, fail=False):
    with UnitOfWork(db) as uow:
        uow.jobs.complete("job-1")

        if fail:
            raise RuntimeError("worker stats unavailable")

        uow.workers.record_completion("worker-1")

        uow.commit()


def show_state(db, label):
    status = db.execute("SELECT status FROM jobs WHERE id = 'job-1'").fetchone()[0]

    completed = db.execute(
        "SELECT completed_jobs FROM workers WHERE id = 'worker-1'"
    ).fetchone()[0]

    print(f"{label}: job={status}, worker_completed={completed}")


def main():
    for fail in (True, False):
        db = setup_db()

        try:
            finish_job(db, fail)
        except RuntimeError as error:
            print(f"Error: {error}")

        show_state(db, "After failure" if fail else "After success")
        db.close()


if __name__ == "__main__":
    main()
