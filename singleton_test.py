import threading
import time


class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance == None:
                time.sleep(0.01)
                cls._instance = super().__new__(cls)
                cls._instance.registry = {}

        return cls._instance

    def register(self, service: str, location: str):
        with self._lock:
            self.registry[service] = location

    def discover(self, service: str):
        with self._lock:
            return self.registry.get(service)


class ChildSingleton(Singleton):
    _instance = None


def worker():
    obj = Singleton()
    print(f"Object ID: {hex(id(obj))}")

def main():
    threads = []
    for _ in range(20):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
    

