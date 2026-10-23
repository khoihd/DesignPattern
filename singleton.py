import threading


class ServiceRegistry:
    # Shared reference to the Singleton instance
    _instance = None

    # Protects instance creation
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.services = {}

        return cls._instance

    def register(self, name, endpoint):
        with self._instance_lock:
            self.services[name] = endpoint

    def discover(self, name):
        with self._instance_lock:
            return self.services.get(name)


class AuthenticationService:
    def __init__(self):
        self.registry = ServiceRegistry()

    def start(self):
        self.registry.register("auth", "auth.internal:8080")


class PaymentService:
    def __init__(self):
        self.registry = ServiceRegistry()

    def start(self):
        endpoint = self.registry.discover("auth")
        print(f"Authentication endpoint: {endpoint}")


def main():
    auth = AuthenticationService()
    payment = PaymentService()

    auth.start()
    payment.start()

    print("Same registry:", auth.registry is payment.registry)

    registry1 = ServiceRegistry()
    registry2 = ServiceRegistry()

    print("Same instance:", registry1 is registry2)
    print("Registry contents:", registry2.services)


if __name__ == "__main__":
    main()
