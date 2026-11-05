from collections.abc import Iterator


# This is an iterator
# iter(iterator) -> return itself
# next(iterator) -> maintains self._idx
class TaskIterator(Iterator):
    # initialization is done here
    def __init__(self, collections):        
        self._collections = collections
        self._idx = 0

    # next(iterator) is processed here
    def __next__(self):
        if self._idx >= len(self._collections):
            raise StopIteration

        item = self._collections[self._idx]
        self._idx += 1
        return item

    # iter(iterator) -> return the same object
    def __iter__(self):
        return self


# This is an iterable
# iter(obj) -> return a new iterator
# next(obj) -> does not work
class TaskCollection:
    def __init__(self, collections):
        self._collections = collections

    def __iter__(self):
        return TaskIterator(self._collections)


def main():
    tasks = TaskCollection([
        "task-101",
        "task-102",
        "task-103"
    ])

    iter_task = iter(tasks)
    print(next(iter_task))
    print(next(iter_task))
    print(iter(iter_task) is iter_task)

    tasks2 = iter(tasks)
    print(next(tasks2))
    
    for task in tasks:
        print(f"Processing {task}")

    # run another loop
    for task in tasks:
        print(f"Processing {task}")


if __name__ == "__main__":
    main()