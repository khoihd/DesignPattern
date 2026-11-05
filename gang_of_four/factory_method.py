import sqlite3
from abc import ABC, abstractmethod


# ============================================================
# 1. Product Interface
# ============================================================
class Database(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute(self, query: str):
        pass

    @abstractmethod
    def close(self):
        pass


# ============================================================
# 2. Concrete Products
# ============================================================
class SQLiteDatabase(Database):
    def __init__(self):
        self.connection = None

    def connect(self):
        print("[SQLite] Connecting...")

        # Real SQLite database, stored in memory
        self.connection = sqlite3.connect(":memory:")

        # Initialize sample data
        self.connection.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        """)

        self.connection.executemany(
            "INSERT INTO users (name) VALUES (?)",
            [
                ("Alice",),
                ("Bob",),
                ("Charlie",),
            ],
        )

        self.connection.commit()

    def execute(self, query: str):
        if self.connection is None:
            raise RuntimeError("Database is not connected")

        print(f"[SQLite] Executing: {query}")

        cursor = self.connection.execute(query)
        return cursor.fetchall()

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            print("[SQLite] Connection closed")


class MySQLDatabase(Database):
    """
    Simulated MySQL adapter.
    Does not connect to an actual MySQL server.
    """

    def connect(self):
        print("[MySQL] Simulated connection established")

    def execute(self, query: str):
        print(f"[MySQL] Simulated execution: {query}")

        return [
            (1, "Alice"),
            (2, "Bob"),
        ]

    def close(self):
        print("[MySQL] Simulated connection closed")


class PostgreSQLDatabase(Database):
    """
    Simulated PostgreSQL adapter.
    Does not connect to an actual PostgreSQL server.
    """

    def connect(self):
        print("[PostgreSQL] Simulated connection established")

    def execute(self, query: str):
        print(f"[PostgreSQL] Simulated execution: {query}")

        return [
            (1, "Alice"),
            (3, "Charlie"),
        ]

    def close(self):
        print("[PostgreSQL] Simulated connection closed")


class OracleDatabase(Database):
    def connect(self):
        print("[Oracle] Simulated connection established")

    def execute(self, query: str):
        print(f"[Oracle] Simulated execution: {query}")
        return [
            (1, "Alice"),
            (4, "David"),
        ]

    def close(self):
        print("[Oracle] Simulated connection closed")


# ============================================================
# 3. Creator
# ============================================================
class Application(ABC):
    @abstractmethod
    def create_database(self) -> Database:
        """
        Factory Method.

        Subclasses decide which Database implementation
        should be instantiated.
        """

    def run(self):
        database = self.create_database()

        try:
            database.connect()
            users = database.execute("SELECT * FROM users")

            print("Users:")
            for user in users:
                print(f"  {user}")
        finally:
            database.close()


# ============================================================
# 4. Concrete Creators
# ============================================================
class SQLiteApplication(Application):
    def create_database(self) -> Database:
        return SQLiteDatabase()


class MySQLApplication(Application):
    def create_database(self) -> Database:
        return MySQLDatabase()


class PostgreSQLApplication(Application):
    def create_database(self) -> Database:
        return PostgreSQLDatabase()

class OracleApplication(Application):
    def create_database(self) -> Database:
        return OracleDatabase()


# ============================================================
# 5. Client
# ============================================================
def main():
    applications = [
        SQLiteApplication(),
        MySQLApplication(),
        PostgreSQLApplication(),
        OracleApplication()
    ]

    for app in applications:
        print()
        print("=" * 40)
        print(f"Running {type(app).__name__}")
        print("=" * 40)
        app.run()


if __name__ == "__main__":
    main()
