from dataclasses import dataclass


@dataclass(frozen=True)
class ConfigSnapshot:
    _concurrency: int
    _queues: tuple[str, ...]


class WorkerConfig:
    def __init__(self, concurrency: int, queues: list[str]):
        self.set_concurrency(concurrency)
        self._queues = list(queues)

    def set_concurrency(self, value: int) -> None:
        if value < 1:
            raise ValueError("concurrency must be at least 1")
        self._concurrency = value

    def add_queue(self, name: str) -> None:
        if name not in self._queues:
            self._queues.append(name)

    def save(self) -> ConfigSnapshot:
        return ConfigSnapshot(self._concurrency, tuple(self._queues))

    def restore(self, snapshot: ConfigSnapshot) -> None:
        self._concurrency = snapshot._concurrency
        self._queues = list(snapshot._queues)

    def __str__(self) -> str:
        return f"concurrency={self._concurrency}, queues={self._queues}"


class ConfigHistory:
    def __init__(self, config: WorkerConfig):
        self._config = config
        self._undo: list[ConfigSnapshot] = []

    def checkpoint(self) -> None:
        self._undo.append(self._config.save())

    def undo(self) -> bool:
        if not self._undo:
            return False
        self._config.restore(self._undo.pop())
        return True


if __name__ == "__main__":
    config = WorkerConfig(2, ["emails"])
    history = ConfigHistory(config)
    print("Initial:", config)

    history.checkpoint()
    config.set_concurrency(8)
    config.add_queue("reports")
    print("Edited:", config)

    history.undo()
    print("Restored:", config)
    print("Undo available:", history.undo())
