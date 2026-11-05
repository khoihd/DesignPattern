
class TaskQueue:
    def __init__(self):
        self.tasks = []

    def enqueue(self, task_id):
        self.tasks.append(task_id)

    def get_tasks(self):
        return self.tasks


class TaskScheduler:
    def __init__(self, queue):
        self.queue = queue

    def submit(self, task_id):
        self.queue.enqueue(task_id)


if __name__ == "__main__":
    # Create a shared dependency
    queue = TaskQueue()

    # Inject the same queue into two schedulers
    scheduler1 = TaskScheduler(queue)
    scheduler2 = TaskScheduler(queue)

    scheduler1.submit("task-1")
    scheduler2.submit("task-2")

    print("Scheduler 1:", scheduler1.queue.get_tasks())
    print("Scheduler 2:", scheduler2.queue.get_tasks())
    print("Same queue:", scheduler1.queue is scheduler2.queue)
