import sqlite3
from abc import ABC, abstractmethod

# ============================================================
# 1. ABSTRACT PRODUCTS
# ============================================================


class Connection(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute(self, query):
        pass

    @abstractmethod
    def begin(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def close(self):
        pass


class SQLDialect(ABC):
    @abstractmethod
    def select_users(self, limit):
        pass


class Transaction(ABC):
    @abstractmethod
    def begin(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass


# ============================================================
# 2. SQLITE PRODUCT FAMILY
# ============================================================
class SQLiteConnection(Connection):
    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(":memory:")

        self.connection.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        """)

        self.connection.executemany(
            "INSERT INTO users (name) VALUES (?)", [("Alice",), ("Bob",), ("Charlie",)]
        )

        self.connection.commit()

        print("Connected to SQLite")

    def execute(self, query):
        cursor = self.connection.execute(query)
        return cursor.fetchall()

    def begin(self):
        self.connection.execute("BEGIN")

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            print("Closed SQLite connection")


class SQLiteDialect(SQLDialect):
    def select_users(self, limit):
        return f"SELECT * FROM users LIMIT {int(limit)}"


class SQLiteTransaction(Transaction):
    def __init__(self, connection: SQLiteConnection):
        self.connection = connection

    def begin(self):
        print("SQLite transaction started")
        self.connection.begin()

    def commit(self):
        self.connection.commit()
        print("SQLite transaction committed")

    def rollback(self):
        self.connection.rollback()
        print("SQLite transaction rolled back")


# ============================================================
# 3. MYSQL PRODUCT FAMILY (SIMULATED)
# ============================================================
class MySQLConnection(Connection):
    def connect(self):
        print("Connected to MySQL (simulated)")

    def execute(self, query):
        print(f"MySQL executing: {query}")
        return [(1, "Alice"), (2, "Bob")]

    def begin(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        print("Closed MySQL connection")


class MySQLDialect(SQLDialect):
    def select_users(self, limit):
        return f"SELECT * FROM users LIMIT {int(limit)}"


class MySQLTransaction(Transaction):
    def __init__(self, connection: MySQLConnection):
        self.connection = connection

    def begin(self):
        self.connection.begin()
        print("MySQL transaction started")

    def commit(self):
        self.connection.commit()
        print("MySQL transaction committed")

    def rollback(self):
        self.connection.rollback()
        print("MySQL transaction rolled back")


# ============================================================
# 4. POSTGRESQL PRODUCT FAMILY (SIMULATED)
# ============================================================
class PostgreSQLConnection(Connection):
    def connect(self):
        print("Connected to PostgreSQL (simulated)")

    def execute(self, query):
        print(f"PostgreSQL executing: {query}")
        return [(1, "Alice"), (2, "Bob")]

    def begin(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        print("Closed PostgreSQL connection")


class PostgreSQLDialect(SQLDialect):
    def select_users(self, limit):
        return f"SELECT * FROM users FETCH FIRST {int(limit)} ROWS ONLY"


class PostgreSQLTransaction(Transaction):
    def __init__(self, connection: PostgreSQLConnection):
        self.connection = connection

    def begin(self):
        self.connection.begin()
        print("PostgreSQL transaction started")

    def commit(self):
        self.connection.commit()
        print("PostgreSQL transaction committed")

    def rollback(self):
        self.connection.rollback()
        print("PostgreSQL transaction rolled back")


# ============================================================
# 5. ABSTRACT FACTORY
# ============================================================
class DatabaseFactory(ABC):
    @abstractmethod
    def create_connection(self) -> Connection:
        pass

    @abstractmethod
    def create_dialect(self) -> SQLDialect:
        pass

    @abstractmethod
    def create_transaction(self, connection: Connection) -> Transaction:
        pass


# ============================================================
# 6. CONCRETE FACTORIES
# ============================================================
class SQLiteFactory(DatabaseFactory):
    def create_connection(self):
        return SQLiteConnection()

    def create_dialect(self):
        return SQLiteDialect()

    def create_transaction(self, connection):
        if not isinstance(connection, SQLiteConnection):
            raise TypeError("SQLite connection required")

        return SQLiteTransaction(connection)


class MySQLFactory(DatabaseFactory):
    def create_connection(self):
        return MySQLConnection()

    def create_dialect(self):
        return MySQLDialect()

    def create_transaction(self, connection):
        if not isinstance(connection, MySQLConnection):
            raise TypeError("MySQL connection required")

        return MySQLTransaction(connection)


class PostgreSQLFactory(DatabaseFactory):
    def create_connection(self):
        return PostgreSQLConnection()

    def create_dialect(self):
        return PostgreSQLDialect()

    def create_transaction(self, connection):
        if not isinstance(connection, PostgreSQLConnection):
            raise TypeError("PostgreSQL connection required")

        return PostgreSQLTransaction(connection)


# ============================================================
# 7. APPLICATION
# ============================================================


class Application:
    def __init__(self, factory: DatabaseFactory):
        self.factory = factory

    def run(self):

        connection = self.factory.create_connection()
        dialect = self.factory.create_dialect()
        transaction = self.factory.create_transaction(connection)

        try:
            connection.connect()

            transaction.begin()

            try:
                query = dialect.select_users(limit=2)

                users = connection.execute(query)

                print("Users:", users)

                transaction.commit()

            except Exception:
                transaction.rollback()
                raise

        finally:
            connection.close()


# ============================================================
# 8. MAIN
# ============================================================

if __name__ == "__main__":
    factories = [SQLiteFactory(), MySQLFactory(), PostgreSQLFactory()]

    for factory in factories:
        print(f"\nRunning with {factory.__class__.__name__}")

        app = Application(factory)
        app.run()
