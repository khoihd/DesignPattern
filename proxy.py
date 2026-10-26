from abc import ABC, abstractmethod


# =========================================================
# 1. Subject Interface
# =========================================================
class DatabaseService(ABC):
    @abstractmethod
    def delete_record(self, record_id: int) -> None:
        pass


# =========================================================
# 2. Real Subject
# =========================================================
class RealDatabaseService(DatabaseService):
    def delete_record(self, record_id: int) -> None:
        print(f"[Database] Deleting record {record_id}")


# =========================================================
# 3. Protection Proxy
# =========================================================
class ProtectedDatabaseProxy(DatabaseService):
    def __init__(self, service: DatabaseService, role: str):
        self._service = service
        self._role = role

    def delete_record(self, record_id: int) -> None:

        if self._role != "admin":
            raise PermissionError("Access denied")

        self._service.delete_record(record_id)


# =========================================================
# 4. Main
# =========================================================
if __name__ == "__main__":
    database = RealDatabaseService()
    
    admin_proxy = ProtectedDatabaseProxy(database, role="admin")
    user_proxy = ProtectedDatabaseProxy(database, role="user")

    print("Admin request:")
    admin_proxy.delete_record(101)

    print("\nRegular user request:")
    try:
        user_proxy.delete_record(102)
    except PermissionError as e:
        print(f"PermissionError: {e}")
