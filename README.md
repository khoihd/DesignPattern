# Software Design Patterns in Python

A practical, example-driven tutorial on software design patterns using
**Python**, with an emphasis on backend engineering, distributed
systems, networking, concurrency, and fault tolerance.

The goal is not just to memorize pattern definitions, but to understand
**what problems they solve, how they work, and when they are worth
using**.

## Learning approach

Each lesson starts with a realistic engineering problem and develops a
solution step by step. Examples favor the Python standard library and
minimal setup.

Lessons follow a consistent structure:

1.  **Introduction** — Definition, intent, and purpose of the pattern.
2.  **Real-world problem** — A runnable initial implementation.
3.  **Why it is a problem** — Design limitations, coupling,
    maintainability, and relevant OOP/SOLID principles.
4.  **Solution** — Design reasoning and architecture.
5.  **Implementation** — Complete executable Python code, run commands,
    and expected output.
6.  **Walkthrough** — Class responsibilities, relationships, and
    execution flow.
7.  **Related concepts** — Relevant Python features and software
    engineering ideas.
8.  **Trade-offs and alternatives** — Production use cases, costs, and
    when *not* to use the pattern.
9.  **Optional exercise** — A practice problem with a reference
    solution.

## Curriculum

### Creational patterns

Patterns concerned with object creation.

| Pattern                   | Core idea                                                                          |
| ------------------------- | ---------------------------------------------------------------------------------- |
| Factory Method            | Let subclasses customize object creation within a shared workflow.                 |
| Abstract Factory          | Create families of related, compatible objects.                                    |
| Builder                   | Construct complex objects step by step.                                            |
| Singleton                 | Provide a single shared instance within a defined scope.                           |
| Prototype                 | Create objects by copying existing instances.                                      |

### Structural patterns

Patterns concerned with composing classes and objects.

| Pattern                   | Core idea                                                                          |
| ------------------------- | ---------------------------------------------------------------------------------- |
| Adapter                   | Make incompatible interfaces work together.                                        |
| Decorator                 | Add behavior to an object without changing its class.                              |
| Facade                    | Provide a simplified interface to a complex subsystem.                             |
| Composite                 | Treat individual objects and object groups uniformly.                              |
| Proxy                     | Control access to another object.                                                  |
| Bridge                    | Separate an abstraction from its implementation.                                   |
| Flyweight                 | Share common state to reduce memory usage.                                         |

### Behavioral patterns

Patterns concerned with responsibilities, communication, and algorithms.

| Pattern                   | Core idea                                                                          |
| ------------------------- | ---------------------------------------------------------------------------------- |
| Strategy                  | Encapsulate interchangeable algorithms.                                            |
| Observer                  | Notify dependents when an object’s state changes.                                  |
| Command                   | Represent a request as an object.                                                  |
| State                     | Change behavior according to an object’s current state.                            |
| Template Method           | Define an algorithm skeleton while allowing selected steps to vary.                |
| Chain of Responsibility   | Pass requests through a sequence of handlers.                                      |
| Mediator                  | Centralize communication between collaborating objects.                            |
| Iterator                  | Traverse a collection without exposing its internals.                              |
| Memento                   | Capture and restore state without exposing implementation details.                 |
| Visitor                   | Define operations separately from the object structures they operate on.           |
| Interpreter               | Represent and evaluate expressions in a small language or grammar.                 |

## Engineering focus

Examples and discussions emphasize:

- Database interfaces, connections, and transactions
- Distributed job scheduling and service configuration
- Network clients, retries, timeouts, and failover
- Concurrency, shared state, and thread safety
- Fault tolerance and backend infrastructure
- Testability, dependency injection, and maintainable APIs

Patterns are presented as **tools rather than rules**. Each lesson
considers simpler Python alternatives, including functions, composition,
dataclasses, and standard-library features.

## Requirements

- Python 3.10+ recommended
- A terminal and a code editor
- No third-party packages unless a particular example explicitly
  requires them

## Running examples

Run a lesson’s Python example from the repository root or its lesson
directory:

``` bash
python3 path/to/example.py
```

Replace `path/to/example.py` with the actual script path. Individual
lessons provide their own run instructions and expected output.

## How to use this repository

Read the problem statement before examining the solution. Try to
identify the design limitation, then compare your approach with the
pattern implementation. Run the example, modify it, and attempt the
optional exercise before consulting its solution.

The most useful question to ask for every pattern is:

> **What concrete problem does this solve, and would a simpler design be
> sufficient?**

## References

- *Design Patterns: Elements of Reusable Object-Oriented Software* —
  Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides (Gang of
  Four)
- [Python documentation](https://docs.python.org/3/)
- [Refactoring.Guru — Design
  Patterns](https://refactoring.guru/design-patterns)

## License

See the repository’s license file, if provided.
