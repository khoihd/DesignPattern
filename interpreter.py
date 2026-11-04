from abc import ABC, abstractmethod
from collections.abc import Mapping


# 1. Common expression interface
class Expression(ABC):
    @abstractmethod
    def interpret(self, context: Mapping[str, float]) -> bool:
        pass


# 2. Terminal expression
class GreaterThan(Expression):
    def __init__(self, metric: str, threshold: float):
        self.metric = metric
        self.threshold = threshold

    def interpret(self, context: Mapping[str, float]) -> bool:
        return context[self.metric] > self.threshold


# 3. Nonterminal expressions
class And(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def interpret(self, context: Mapping[str, float]) -> bool:
        return self.left.interpret(context) and self.right.interpret(context)


class Or(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def interpret(self, context: Mapping[str, float]) -> bool:
        return self.left.interpret(context) or self.right.interpret(context)


class Not(Expression):
    def __init__(self, expression: Expression):
        self.expression = expression

    def interpret(self, context: Mapping[str, float]) -> bool:
        return not self.expression.interpret(context)


# 4. Client code
if __name__ == "__main__":
    workers = {
        "worker-1": {
            "cpu_percent": 91,
            "queue_depth": 140,
            "free_memory_mb": 600,
        },
        "worker-2": {
            "cpu_percent": 43,
            "queue_depth": 20,
            "free_memory_mb": 600,
        },
        "worker-3": {
            "cpu_percent": 92,
            "queue_depth": 80,
            "free_memory_mb": 2048,
        },
    }

    high_cpu = GreaterThan("cpu_percent", 85)
    large_queue = GreaterThan("queue_depth", 100)
    memory_above_800 = GreaterThan("free_memory_mb", 800)

    # (high_cpu OR large_queue)
    # AND NOT (memory_above_800)
    alert_rule = And(
        Or(high_cpu, large_queue),
        Not(memory_above_800),
    )

    for name, metrics in workers.items():
        alert = alert_rule.interpret(metrics)
        print(f"{name}: alert={alert}")
