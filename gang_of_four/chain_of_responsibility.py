from abc import ABC, abstractmethod
from dataclasses import dataclass


# ============================================================
# Request and Response
# ============================================================
@dataclass
class Request:
    user_id: str | None
    request_count: int
    payload: dict


@dataclass
class Response:
    status_code: int
    message: str


# ============================================================
# Handler Interface
# ============================================================
class Handler(ABC):
    @abstractmethod
    def handle(self, request: Request) -> Response:
        pass


# ============================================================
# Authentication Handler
# ============================================================
class AuthenticationHandler(Handler):
    def __init__(self, next_handler: Handler):
        self.next_handler = next_handler

    def handle(self, request: Request) -> Response:
        print("[Authentication] Checking user")

        if request.user_id is None:
            return Response(401, "Unauthorized")

        return self.next_handler.handle(request)


# ============================================================
# Rate Limit Handler
# ============================================================
class RateLimitHandler(Handler):
    def __init__(self, next_handler: Handler, max_requests: int = 100):
        self.next_handler = next_handler
        self.max_requests = max_requests

    def handle(self, request: Request) -> Response:
        print("[RateLimit] Checking request quota")

        if request.request_count > self.max_requests:
            return Response(429, "Too Many Requests")

        return self.next_handler.handle(request)


# ============================================================
# Validation Handler
# ============================================================
class ValidationHandler(Handler):
    def __init__(self, next_handler: Handler):
        self.next_handler = next_handler

    def handle(self, request: Request) -> Response:
        print("[Validation] Checking payload")

        if "task" not in request.payload:
            return Response(400, "Bad Request")

        return self.next_handler.handle(request)


# ============================================================
# Execution Handler
# ============================================================
class ExecutionHandler(Handler):
    def handle(self, request: Request) -> Response:
        print("[Execution] Processing request")
        task = request.payload["task"]

        return Response(200, f"Task '{task}' submitted")


# ============================================================
# Main
# ============================================================
def main():
    # Construct the chain from the last handler backward.
    execution = ExecutionHandler()
    validation = ValidationHandler(execution)
    rate_limit = RateLimitHandler(validation, max_requests=100)
    authentication = AuthenticationHandler(rate_limit)

    # Entry point
    server = authentication

    requests = [
        Request(None, 10, {"task": "backup"}),
        Request("user-1", 150, {"task": "backup"}),
        Request("user-2", 20, {}),
        Request("user-3", 20, {"task": "backup"}),
    ]

    for i, request in enumerate(requests, start=1):
        print(f"--- Request {i} ---")
        response = server.handle(request)
        print(f"Response: {response}")


if __name__ == "__main__":
    main()
