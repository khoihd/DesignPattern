from functools import wraps


def logging_decorator(func):
    @wraps(func)
    def log_wrapper(*args, **kargs):
        print("LOGGING BEFORE")
        func(*args, **kargs)
        print("LOGGING AFTER")

    return log_wrapper


def debugging_decorator(func):
    @wraps(func)
    def debug_wrapper(*args, **kargs):
        print("DEBUGGING BEFORE")
        func(*args, **kargs)
        print("DEBUGGING AFTER")

    return debug_wrapper


@logging_decorator
@debugging_decorator
def get_user(user_id):
    print(f"Database: Fetching user {user_id}")
    return {"id": user_id, "name": "Alice"}


def main():
    # decorate_get_user = logging_decorator(get_user)
    # decorate_get_user("user-1")
    get_user("user-1")
    print(get_user.__name__)


if __name__ == "__main__":
    main()
