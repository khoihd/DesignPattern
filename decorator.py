from abc import ABC, abstractmethod
from collections import Counter
from time import perf_counter


# ============================================================
# 1. Component
# ============================================================
class Cache(ABC):
    @abstractmethod
    def get(self, key: str) -> str | None:
        pass

    @abstractmethod
    def set(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass


# ============================================================
# 2. Concrete Component
# ============================================================
class InMemoryCache(Cache):
    def __init__(self):
        self._data: dict[str, str] = {}

    def get(self, key: str) -> str | None:
        return self._data.get(key)

    def set(self, key: str, value: str) -> None:
        self._data[key] = value

    def delete(self, key: str) -> None:
        self._data.pop(key, None)


# ============================================================
# 3. Decorator: Logging
# ============================================================
class LoggingCache(Cache):
    def __init__(self, cache: Cache):
        self._cache = cache
    
    def get(self, key: str) -> str | None:
        print(f"[LOG] GET {key}")
        return self._cache.get(key)

    def set(self, key: str, value: str) -> None:
        print(f"[LOG] SET {key}")
        self._cache.set(key, value)

    def delete(self, key: str) -> None:
        print(f"[LOG] DELETE {key}")
        self._cache.delete(key)


# ============================================================
# 4. Decorator: Metrics
# ============================================================
class MetricsCache(Cache):
    def __init__(self, cache: Cache):
        self._cache = cache
        self.counts = Counter()
        self.durations = {}

    def _record(self, operation: str, duration: float):
        self.counts[operation] += 1

        if operation not in self.durations:
            self.durations[operation] = []

        self.durations[operation].append(duration)

    def get(self, key: str) -> str | None:
        start = perf_counter()

        try:
            return self._cache.get(key)
        finally:
            duration = perf_counter() - start
            self._record("GET", duration)

    def set(self, key: str, value: str) -> None:
        start = perf_counter()

        try:
            self._cache.set(key, value)
        finally:
            duration = perf_counter() - start
            self._record("SET", duration)

    def delete(self, key: str) -> None:
        start = perf_counter()

        try:
            self._cache.delete(key)
        finally:
            duration = perf_counter() - start
            self._record("DELETE", duration)

    def print_metrics(self):
        print("\n=== Cache Metrics ===")

        for operation in ("GET", "SET", "DELETE"):
            count = self.counts[operation]

            if count == 0:
                continue

            durations = self.durations[operation]

            average_ms = sum(durations) / len(durations) * 1000

            print(f"{operation}: count={count}, avg={average_ms:.3f} ms")


# ============================================================
# 6. Client
# ============================================================
class UserService:
    def __init__(self, cache: Cache):
        self._cache = cache

    def get_user(self, user_id: str) -> str | None:
        return self._cache.get(user_id)

    def save_user(self, user_id: str, name: str) -> None:
        self._cache.set(user_id, name)

    def delete_user(self, user_id: str) -> None:
        self._cache.delete(user_id)


# ============================================================
# 7. Application
# ============================================================
def main():
    # Original cache
    cache = InMemoryCache()

    # Add logging
    cache = LoggingCache(cache)

    # Add metrics
    cache = MetricsCache(cache)

    # Client
    service = UserService(cache)

    service.save_user("user-1", "Alice")
    print(service.get_user("user-1"))

    service.delete_user("user-1")
    print(service.get_user("user-1"))

    # MetricsCache is the outermost decorator
    cache.print_metrics()


if __name__ == "__main__":
    main()
