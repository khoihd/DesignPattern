from abc import ABC, abstractmethod


# ==========================================
# 1. Implementor
# ==========================================
class Storage(ABC):
    @abstractmethod
    def save(self, key: str, value: object) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> object | None:
        pass


# ==========================================
# 2. Concrete Implementors
# ==========================================
class PostgreSQLStorage(Storage):
    def __init__(self):
        self._data = {}

    def save(self, key, value):
        print(f"[PostgreSQL] Saving {key}: {value}")
        self._data[key] = value

    def get(self, key):
        print(f"[PostgreSQL] Getting {key}")
        return self._data.get(key)


class RedisStorage(Storage):
    def __init__(self):
        self._data = {}

    def save(self, key, value):
        print(f"[Redis] Saving {key}: {value}")
        self._data[key] = value

    def get(self, key):
        print(f"[Redis] Getting {key}")
        return self._data.get(key)


# ==========================================
# 3. Abstraction
# ==========================================
class Service(ABC):
    def __init__(self, storage: Storage):
        self._storage = storage


# ==========================================
# 4. Refined Abstractions
# ==========================================
class UserService(Service):
    def save_user(self, user_id: int, name: str):
        key = f"user:{user_id}"
        self._storage.save(key, name)

    def get_user(self, user_id: int):
        key = f"user:{user_id}"
        return self._storage.get(key)


class OrderService(Service):
    def save_order(self, order_id: int, amount: float):
        key = f"order:{order_id}"
        self._storage.save(key, amount)

    def get_order(self, order_id: int):
        key = f"order:{order_id}"
        return self._storage.get(key)


# ==========================================
# 5. Client
# ==========================================


def main():

    postgres = PostgreSQLStorage()
    redis = RedisStorage()

    # UserService with PostgreSQL
    user_service = UserService(postgres)
    user_service.save_user(101, "Alice")
    print("Retrieved user:", user_service.get_user(101))
    print()

    # OrderService with Redis
    order_service = OrderService(redis)
    order_service.save_order(501, 99.99)
    print("Retrieved order:", order_service.get_order(501))
    print()

    # Switch UserService to Redis
    redis_user_service = UserService(redis)
    redis_user_service.save_user(102, "Bob")
    print("Retrieved user:", redis_user_service.get_user(102))


if __name__ == "__main__":
    main()
