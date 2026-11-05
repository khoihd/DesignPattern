from abc import ABC, abstractmethod


# Strategy contract
class RetryStrategy(ABC):
    @abstractmethod
    def delay(self, retry_number: int) -> int:
        pass


# Concrete strategy 1
class FixedDelay(RetryStrategy):
    def __init__(self, seconds: int):
        self.seconds = seconds

    def delay(self, retry_number: int) -> int:
        return self.seconds


# Concrete strategy 2
class ExponentialDelay(RetryStrategy):
    def __init__(self, base_seconds: int):
        self.base_seconds = base_seconds

    def delay(self, retry_number: int) -> int:
        return self.base_seconds * (2 ** (retry_number - 1))


# Context
class RetryPlanner:
    def __init__(self, strategy: RetryStrategy):
        self.strategy = strategy

    def next_delay(self, retry_number: int) -> int:
        if retry_number < 1:
            raise ValueError("retry_number must be >= 1")

        return self.strategy.delay(retry_number)


if __name__ == "__main__":
    planner = RetryPlanner(FixedDelay(2))

    print("Fixed delay:")
    for retry in range(1, 4):
        print(f"Retry {retry}: {planner.next_delay(retry)}s")

    # Replace the strategy at runtime
    planner.strategy = ExponentialDelay(2)

    print("Exponential backoff:")
    for retry in range(1, 4):
        print(f"Retry {retry}: {planner.next_delay(retry)}s")
