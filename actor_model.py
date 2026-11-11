from dataclasses import dataclass
from queue import Queue
from threading import Barrier, Thread, current_thread


@dataclass(frozen=True)
class ProcessTask:
    task_id: str


@dataclass(frozen=True)
class GetCount:
    reply_to: Queue


@dataclass(frozen=True)
class Stop:
    pass


class WorkerActor:
    def __init__(self, worker_id: str):
        self.worker_id = worker_id
        self.mailbox = Queue()

        # The actor's message-processing thread.
        self.thread = Thread(
            target=self._run,
            name=f"actor-{worker_id}",
        )

    def start(self) -> None:
        self.thread.start()

    def send(self, message) -> None:
        self.mailbox.put(message)

    def _run(self) -> None:
        # Private state owned by the actor thread.
        completed_count = 0

        while True:
            message = self.mailbox.get()

            if isinstance(message, ProcessTask):
                completed_count += 1

            elif isinstance(message, GetCount):
                message.reply_to.put((completed_count, current_thread().name))

            elif isinstance(message, Stop):
                break

    def get_count(self):
        reply = Queue()
        self.send(GetCount(reply))
        return reply.get()

    def stop(self) -> None:
        self.send(Stop())
        self.thread.join()


def producer(worker: WorkerActor, barrier: Barrier) -> None:
    # Synchronize the start of both producers.
    barrier.wait()

    # Each producer sends two messages.
    for index in range(2):
        task_id = f"{current_thread().name}-task-{index + 1}"
        worker.send(ProcessTask(task_id))


def main():
    worker = WorkerActor("worker-1")
    worker.start()

    barrier = Barrier(2)

    # Two producer threads share the same actor.
    producer_1 = Thread(
        target=producer,
        args=(worker, barrier),
        name="producer-1",
    )

    producer_2 = Thread(
        target=producer,
        args=(worker, barrier),
        name="producer-2",
    )

    producer_1.start()
    producer_2.start()

    producer_1.join()
    producer_2.join()

    # Query the actor after both producers finish.
    count, actor_thread = worker.get_count()

    print("Producer threads: producer-1, producer-2")
    print(f"Actor thread: {actor_thread}")
    print(f"Completed tasks: {count}")

    worker.stop()


if __name__ == "__main__":
    main()
