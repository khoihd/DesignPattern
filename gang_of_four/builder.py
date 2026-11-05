from dataclasses import dataclass


# ==========================================
# 1. Product Configuration
# ==========================================
@dataclass(frozen=True)
class ClientConfig:
    endpoint: str
    backup_endpoint: str | None
    timeout: float
    retries: int
    backoff: float
    pool_size: int
    use_tls: bool
    failure_threshold: int
    recovery_timeout: float


# ==========================================
# 2. Product
# ==========================================
class ServiceClient:
    def __init__(self, config: ClientConfig):
        self.config = config

    def connect(self):
        protocol = "https" if self.config.use_tls else "http"
        print(f"Connecting to {protocol}://{self.config.endpoint}")
        print(f"Timeout: {self.config.timeout}s")
        print(f"Retries: {self.config.retries}")
        print(f"Pool size: {self.config.pool_size}")

    def execute(self, request: str):
        print(f"\nExecuting request: {request}")
        # Simulated deterministic failure.
        primary_available = False
        for attempt in range(self.config.retries + 1):
            print(f"Attempt {attempt + 1}: {self.config.endpoint}")

            if primary_available:
                return "Success"

            if attempt < self.config.retries:
                print(f"Retrying after {self.config.backoff}s...")

        if self.config.backup_endpoint:
            print(f"Failing over to {self.config.backup_endpoint}")

            # Simulated successful backup request.

            return "Success via backup"

        raise ConnectionError("All attempts failed")


# ==========================================
# 3. Builder
# ==========================================


class ServiceClientBuilder:
    def __init__(self):
        self._endpoint = None
        self._backup_endpoint = None
        self._timeout = 5.0
        self._retries = 3
        self._backoff = 1.0
        self._pool_size = 10
        self._use_tls = True
        self._circuit_breaker_threshold = 5
        self._circuit_breaker_timeout = 30.0

    def with_endpoint(self, endpoint: str):
        self._endpoint = endpoint
        return self

    def with_backup_endpoint(self, endpoint: str):
        self._backup_endpoint = endpoint
        return self

    def with_timeout(self, timeout: float):
        self._timeout = timeout
        return self

    def with_retries(self, retries: int):
        self._retries = retries
        return self

    def with_backoff(self, backoff: float):
        self._backoff = backoff
        return self

    def with_connection_pool(self, size: int):
        self._pool_size = size
        return self

    def with_tls(self, enabled: bool):
        self._use_tls = enabled
        return self

    def with_circuit_breaker(self, failure_threshold: int, recovery_timeout: float):
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        return self


    def build(self) -> ServiceClient:
        # Validate configuration.
        if not self._endpoint:
            raise ValueError("Endpoint is required")

        if self._timeout <= 0:
            raise ValueError("Timeout must be positive")

        if self._retries < 0:
            raise ValueError("Retries cannot be negative")

        if self._backoff < 0:
            raise ValueError("Backoff cannot be negative")

        if self._pool_size <= 0:
            raise ValueError("Connection pool size must be positive")

        if self._failure_threshold < 0:
            raise ValueError("Failure threshold cannot be negative")
        
        if self._recovery_timeout < 0:
            raise ValueError("Recovery timeout cannot be negative")
    
        config = ClientConfig(
            endpoint=self._endpoint,
            backup_endpoint=self._backup_endpoint,
            timeout=self._timeout,
            retries=self._retries,
            backoff=self._backoff,
            pool_size=self._pool_size,
            use_tls=self._use_tls,
            failure_threshold=self._failure_threshold,
            recovery_timeout=self._recovery_timeout
        )

        return ServiceClient(config)


# ==========================================
# 4. Application
# ==========================================
def main():
    clientbuilder = (
        ServiceClientBuilder()
        .with_endpoint("server1.example.com")
        .with_backup_endpoint("server2.example.com")
        .with_timeout(3)
        .with_retries(2)
        .with_backoff(0.5)
        .with_connection_pool(20)
        .with_tls(True)
        .with_circuit_breaker(failure_threshold=5,
            recovery_timeout=30
        )
    )
    
    client = clientbuilder.build()

    client.connect()
    result = client.execute("GET user:123")
    print(f"\nResult: {result}")


if __name__ == "__main__":
    main()
