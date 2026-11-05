from abc import ABC, abstractmethod


# 1. Visitor interface
class ResourceVisitor(ABC):
    @abstractmethod
    def visit_compute_node(self, node):
        pass

    @abstractmethod
    def visit_database(self, database):
        pass


# 2. Resource interface
class Resource(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


# 3. Concrete resources
class ComputeNode(Resource):
    def __init__(self, name, vcpus, patched):
        self.name = name
        self.vcpus = vcpus
        self.patched = patched

    def accept(self, visitor):
        return visitor.visit_compute_node(self)


class DatabaseInstance(Resource):
    def __init__(self, name, storage_gb, encrypted):
        self.name = name
        self.storage_gb = storage_gb
        self.encrypted = encrypted

    def accept(self, visitor):
        return visitor.visit_database(self)


# 4. Concrete visitors
class InventoryVisitor(ResourceVisitor):
    def visit_compute_node(self, node):
        return f"Compute {node.name}: {node.vcpus} vCPU"

    def visit_database(self, database):
        return f"Database {database.name}: {database.storage_gb} GB"


class MonthlyCostVisitor(ResourceVisitor):
    def visit_compute_node(self, node):
        return node.vcpus * 20

    def visit_database(self, database):
        return database.storage_gb * 0.15


# 5. Client
if __name__ == "__main__":
    resources = [
        ComputeNode("worker-1", 4, patched=True),
        DatabaseInstance("users-db", 200, encrypted=False),
    ]

    inventory_visitor = InventoryVisitor()
    cost_visitor = MonthlyCostVisitor()

    for resource in resources:
        print(resource.accept(inventory_visitor))

    total = sum(resource.accept(cost_visitor) for resource in resources)

    print(f"Estimated monthly cost: ${total:.2f}")
