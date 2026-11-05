from abc import ABC, abstractmethod


# ==================================================
# 1. Target Interface
# ==================================================
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


# ==================================================
# 2. Application-Level Exception
# ==================================================
class CacheError(Exception):
    pass


# ==================================================
# 3. Compatible Cache Implementation
# ==================================================
class InMemoryCache(Cache):
    def __init__(self):
        self.data: dict[str, str] = {}

    def get(self, key: str) -> str | None:
        return self.data.get(key)

    def set(self, key: str, value: str) -> None:
        self.data[key] = value

    def delete(self, key: str) -> None:
        self.data.pop(key, None)


# ==================================================
# 4. External Cache (Adaptee)
# ==================================================
class ExternalCacheException(Exception):
    pass


class ExternalCache:
    def __init__(self):
        self.storage: dict[bytes, bytes] = {}

    def fetch(self, key: bytes) -> bytes | None:
        if key == b"error":
            raise ExternalCacheException("Connection failed")

        return self.storage.get(key)

    def store(self, key: bytes, value: bytes) -> None:
        self.storage[key] = value

    def remove(self, key: bytes) -> None:
        self.storage.pop(key, None)


# ==================================================
# 5. Adapter
# ==================================================
class ExternalCacheAdapter(Cache):
    def __init__(self, cache: ExternalCache):
        self.cache = cache

    def get(self, key: str) -> str | None:
        return self.cache.fetch(key)

    def set(self, key: str, value: str) -> None:
        return self.cache.store(key, value)

    def delete(self, key: str) -> None:
        self.cache.remove(key)


# ==================================================
# 6. Client
# ==================================================
class UserService:
    def __init__(self, cache: Cache):
        self.cache = cache

    def save_user(self, user_id: str, name: str):
        self.cache.set(user_id, name)

    def get_user(self, user_id: str):
        return self.cache.get(user_id)

    def delete_user(self, user_id: str):
        self.cache.delete(user_id)


# ==================================================
# 7. Demonstration
# ==================================================
def main():
    print("=== In-Memory Cache ===")
    memory_cache = InMemoryCache()

    # inject InMemoryCache directly to UserService
    service = UserService(memory_cache)
    service.save_user("user-1", "Alice")
    print(service.get_user("user-1"))

    service.delete_user("user-1")
    print(service.get_user("user-1"))
    print("\n=== External Cache ===")

    external_cache = ExternalCache()
    adapter = ExternalCacheAdapter(external_cache)

    # inject the adapter, which implements Cache, to UserService
    # adapter is ExternalCacheAdapter, which injects ExternalCache, and pass the method calls to ExternalCache
    service = UserService(adapter)
    service.save_user("user-2", "Bob")
    print(service.get_user("user-2"))

    service.delete_user("user-2")
    print(service.get_user("user-2"))
    print("\n=== Exception Translation ===")

    try:
        service.get_user("error")

    except CacheError as exc:
        print(type(exc).__name__)
        print(exc)


if __name__ == "__main__":
    main()
