import csv
import io
import json
from abc import ABC, abstractmethod


class UserImporter(ABC):
    def __init__(self, storage):
        self.storage = storage

    # Template Method
    def import_users(self, source):
        print("Starting import")

        # Step 1: Format-specific parsing
        rows = self.parse_rows(source)

        # Step 2: Shared normalization and validation
        users = []
        for row in rows:
            user = {
                "id": int(row["id"]),
                "email": row["email"].strip().lower(),
            }

            if user["id"] <= 0 or not user["email"]:
                raise ValueError("Invalid user")

            users.append(user)

        # Step 3: Shared storage
        self.storage.extend(users)

        print(f"Saved {len(users)} users")

        # Step 4: Optional customization
        self.after_import(len(users))

        return len(users)

    @abstractmethod
    def parse_rows(self, source):
        pass

    def after_import(self, count):
        pass


class CSVUserImporter(UserImporter):
    def parse_rows(self, source):
        return list(csv.DictReader(io.StringIO(source)))

    def after_import(self, count):
        print(f"CSV audit: {count} users imported")


class JSONLUserImporter(UserImporter):
    def parse_rows(self, source):
        return [json.loads(line) for line in source.splitlines() if line.strip()]


if __name__ == "__main__":
    storage = []

    csv_data = """id,email
1, Alice@Example.com
2,BOB@example.com
"""

    jsonl_data = """{"id": 3, "email": " Carol@Example.com "}
{"id": 4, "email": "dave@example.com"}"""

    csv_importer = CSVUserImporter(storage)
    jsonl_importer = JSONLUserImporter(storage)

    csv_importer.import_users(csv_data)
    jsonl_importer.import_users(jsonl_data)

    print(storage)
