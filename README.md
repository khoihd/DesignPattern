# Software Design Patterns in Python

A practical, example-driven tutorial on software design patterns and
software architecture using **Python**, with an emphasis on backend
engineering, distributed systems, networking, concurrency, and fault tolerance.

The goal is not to memorize pattern definitions, but to understand
**why a pattern exists, how it works, and when its complexity is justified**.

## Learning approach

Each lesson starts with a **complete, runnable design without the pattern**,
explains its limitations, and then refactors it step by step. Examples favor
the Python standard library, small working programs, and clear object relationships.

Lessons follow a consistent nine-part structure:

1. **Introduction** — Definition, intent, and purpose.
2. **Real-world problem** — Complete executable code without the pattern.
3. **Why it is a problem** — Limitations of the initial design, when relevant.
4. **Solution** — Architectural reasoning and step-by-step refactoring.
5. **Implementation** — Complete executable Python code, run command, and exact output.
6. **Walkthrough** — Responsibilities, object relationships, and execution flow.
7. **Related concepts** — Relevant OOP, Python, and software engineering ideas.
8. **Trade-offs and alternatives** — Benefits, costs, and when *not* to use the pattern.
9. **Optional exercise** — One practice problem with a complete working solution.

Unit tests and mocks are **not included by default**; they are introduced only
when needed to explain a concept. Unnecessary interfaces, registries, factories,
and frameworks are avoided.

## Curriculum

Lessons use **Level.Topic** numbering, with topic numbering restarting at
`1` in each level. Level 0 contains the original 23 Gang of Four (GoF)
lessons; Levels 1–3 extend the curriculum to broader modern architecture and
distributed-systems topics.

| Level | Focus | Topics | Lesson range |
| --- | --- | ---: | --- |
| 0 | Original Gang of Four (GoF) design patterns | 23 | 0.1–0.23 |
| 1 | Core application and system design | 33 | 1.1–1.33 |
| 2 | Essential distributed-systems patterns | 42 | 2.1–2.42 |
| 3 | Advanced architecture and operations | 12 | 3.1–3.12 |
| **Total** | | **110** | |

The roadmap is a proposed learning sequence, not an exhaustive or official
classification. It mixes design patterns, architectural styles, concurrency
models, and operational techniques; these are not all the same kind of pattern.

## Level 0 — Gang of Four design patterns (0.1–0.23)

The original object-oriented design pattern lessons, in the order taught.

### Creational patterns

Patterns concerned with object creation.

| Lesson | Topic | Core idea |
| --- | --- | --- |
| 0.1 | Factory Method | Let subclasses customize object creation within a shared workflow. |
| 0.2 | Abstract Factory | Create families of related, compatible objects. |
| 0.3 | Builder | Construct complex objects step by step. |
| 0.4 | Singleton | Provide a single shared instance within a defined scope. |
| 0.5 | Prototype | Create objects by copying existing instances. |

### Structural patterns

Patterns concerned with composing classes and objects.

| Lesson | Topic | Core idea |
| --- | --- | --- |
| 0.6 | Adapter | Make incompatible interfaces work together. |
| 0.7 | Decorator | Add behavior to an object without changing its class. |
| 0.8 | Facade | Provide a simplified interface to a complex subsystem. |
| 0.9 | Composite | Treat individual objects and object groups uniformly. |
| 0.10 | Proxy | Control access to another object. |
| 0.11 | Bridge | Separate an abstraction from its implementation. |
| 0.12 | Flyweight | Share common state to reduce memory usage. |

### Behavioral patterns

Patterns concerned with responsibilities, communication, and algorithms.

| Lesson | Topic | Core idea |
| --- | --- | --- |
| 0.13 | Chain of Responsibility | Pass requests through a sequence of handlers. |
| 0.14 | Command | Represent a request as an object. |
| 0.15 | Iterator | Traverse a collection without exposing its internals. |
| 0.16 | Mediator | Centralize communication between collaborating objects. |
| 0.17 | Memento | Capture and restore state without exposing implementation details. |
| 0.18 | Observer | Notify dependents when an object’s state changes. |
| 0.19 | State | Change behavior according to an object’s current state. |
| 0.20 | Strategy | Encapsulate interchangeable algorithms. |
| 0.21 | Template Method | Define an algorithm skeleton while allowing selected steps to vary. |
| 0.22 | Visitor | Define operations separately from the object structures they operate on. |
| 0.23 | Interpreter | Represent and evaluate expressions in a small language or grammar. |

## Level 1 — Core application and system design (1.1–1.33)

Application components, boundaries, and common backend architectures.

### Foundational patterns

| Lesson | Topic | Core idea |
| --- | --- | --- |
| 1.1 | Dependency Injection | Supply dependencies from outside a component to reduce coupling and improve tests. |
| 1.2 | Repository | Provide a persistence abstraction between domain logic and storage. |
| 1.3 | Model-View-Controller (MVC) | Separate data/application behavior, presentation, and input coordination. |
| 1.4 | Event-Driven Architecture (EDA) | Decouple components through the publication and handling of events. |
| 1.5 | Actor Model | Represent independent stateful actors that communicate through messages. |
| 1.6 | Orchestrator-Worker | Assign and coordinate tasks across multiple workers. |

### Application structure and boundaries

| Lesson | Topic | Core idea |
| --- | --- | --- |
| 1.7 | Inversion of Control (IoC) | Move control of dependency creation or execution outside a component. |
| 1.8 | Service Layer | Offer a clear boundary for application operations and workflows. |
| 1.9 | Data Transfer Object (DTO) | Carry data across process or architectural boundaries. |
| 1.10 | Domain Model / Aggregate | Model domain behavior and enforce consistency boundaries. |
| 1.11 | Unit of Work | Track and commit a set of related persistence changes together. |
| 1.12 | Data Mapper | Keep object-domain models independent of database representation. |
| 1.13 | Model-View-ViewModel (MVVM) | Separate UI state/presentation logic from views. |
| 1.14 | Hexagonal Architecture (Ports and Adapters) | Use ports and adapters to isolate domain logic from external systems. |
| 1.15 | Clean Architecture | Keep dependency direction centered on application/domain logic. |

### Service and application architecture

| Lesson | Topic | Core idea |
| --- | --- | --- |
| 1.16 | Modular Monolith | Enforce modular boundaries inside one deployable application. |
| 1.17 | Microservices Architecture | Compose systems from independently deployable services. |
| 1.18 | Decomposition by Business Capability / Subdomain | Identify cohesive service boundaries around business capabilities. |
| 1.19 | API Gateway | Provide a single client-facing entry point to backend services. |
| 1.20 | Backend for Frontend (BFF) | Expose APIs adapted to the needs of different clients. |
| 1.21 | Strangler Fig | Replace legacy functionality incrementally. |
| 1.22 | Anti-Corruption Layer | Translate external models without contaminating the domain model. |

### First distributed building blocks and operations

| Lesson | Topic | Core idea |
| --- | --- | --- |
| 1.23 | Publish-Subscribe | Broadcast events to independently interested subscribers. |
| 1.24 | Point-to-Point / Work Queue | Distribute tasks through a queue to one consuming worker per delivery. |
| 1.25 | Request-Reply | Associate a response with a request across a messaging boundary. |
| 1.26 | Worker Pool | Bound and distribute parallel task execution among workers. |
| 1.27 | Fan-Out / Fan-In | Dispatch parallel work and merge results. |
| 1.28 | Cache-Aside | Load data into cache on misses and explicitly manage invalidation. |
| 1.29 | Timeout and Deadline | Limit how long operations and end-to-end requests can run. |
| 1.30 | Rate Limiting | Constrain request throughput to protect resources. |
| 1.31 | Health Endpoint Monitoring | Expose health signals to detect and respond to failures. |
| 1.32 | Feature Flags | Control feature activation separately from deployment. |
| 1.33 | Externalized Configuration | Keep environment-specific configuration outside application code. |

## Level 2 — Essential distributed-systems patterns (2.1–2.42)

Messaging, coordination, resilience, consistency, and deployment.

### Messaging, routing, and delivery semantics

| Lesson | Topic | Core idea |
| --- | --- | --- |
| 2.1 | Competing Consumers | Scale queue processing with multiple consumers. |
| 2.2 | Asynchronous Request-Reply | Accept requests now and make results available later. |
| 2.3 | Correlation Identifier | Link replies and events to the originating operation. |
| 2.4 | Content-Based Router | Choose destinations according to message contents. |
| 2.5 | Pipes and Filters | Compose processing from independently reusable stages. |
| 2.6 | Splitter | Split a composite message into smaller messages. |
| 2.7 | Aggregator | Combine multiple related messages or partial results. |
| 2.8 | Scatter-Gather | Broadcast requests to recipients and gather responses. |
| 2.9 | Dead Letter Queue | Isolate messages that cannot be handled successfully. |
| 2.10 | Idempotent Consumer | Make duplicate deliveries safe to process. |
| 2.11 | Transactional Outbox | Reliably publish events associated with database changes. |
| 2.12 | Claim Check | Store large message contents separately and pass a reference. |

### Service communication and worker coordination

| Lesson | Topic | Core idea |
| --- | --- | --- |
| 2.13 | Service Discovery | Find healthy instances of a changing service. |
| 2.14 | Sidecar | Attach auxiliary service functionality alongside an application. |
| 2.15 | Leader Election | Choose one process to serve as coordinator or leader. |
| 2.16 | Leader-Follower | Organize components around a primary leader and followers. |
| 2.17 | Lease and Heartbeat | Track liveness and time-limited resource ownership. |
| 2.18 | Scheduler-Agent-Supervisor | Assign scheduled work, execute through agents, and supervise outcomes. |
| 2.19 | Work Stealing | Let idle workers pull tasks from busier workers. |

### Resilience and backpressure

| Lesson | Topic | Core idea |
| --- | --- | --- |
| 2.20 | Retry with Exponential Backoff and Jitter | Retry transient failures while avoiding synchronized retries. |
| 2.21 | Circuit Breaker | Temporarily stop calls to failing dependencies. |
| 2.22 | Bulkhead | Isolate resource pools to contain failures. |
| 2.23 | Load Shedding | Reject lower-priority or excess work when overloaded. |
| 2.24 | Queue-Based Load Leveling | Buffer sudden request spikes behind a queue. |
| 2.25 | Fallback | Offer an alternate behavior when the primary path fails. |
| 2.26 | Graceful Degradation | Maintain reduced functionality under partial failure. |
| 2.27 | Failover and Redundancy | Use redundant capacity and switch away from failed components. |

### Data ownership, consistency, and transactions

| Lesson | Topic | Core idea |
| --- | --- | --- |
| 2.28 | Database per Service | Assign independent ownership of persistence to each service. |
| 2.29 | Command Query Responsibility Segregation (CQRS) | Separate read and write responsibilities or representations. |
| 2.30 | Saga | Coordinate multi-service transactions as local steps. |
| 2.31 | Compensating Transaction | Semantically counteract committed operations. |
| 2.32 | Read-Through Cache | Retrieve missing values through a cache's loading mechanism. |
| 2.33 | Write-Through / Write-Behind Cache | Coordinate cache writes synchronously or asynchronously with storage. |
| 2.34 | Sharding | Distribute partitions of data over multiple nodes. |
| 2.35 | Primary-Replica Replication | Replicate data from a primary to one or more replicas. |
| 2.36 | Optimistic Concurrency Control | Detect conflicting updates before committing changes. |
| 2.37 | API Composition | Combine information from multiple services at query time. |

### Deployment and verification

| Lesson | Topic | Core idea |
| --- | --- | --- |
| 2.38 | Blue-Green Deployment | Switch between two separate deployment environments. |
| 2.39 | Canary Deployment | Roll out to a controlled subset before wider adoption. |
| 2.40 | Rolling Deployment | Update instances incrementally while serving traffic. |
| 2.41 | Distributed Tracing | Track an operation across service boundaries. |
| 2.42 | Consumer-Driven Contract Testing | Check providers against requirements expressed by consumers. |

## Level 3 — Advanced architecture and operations (3.1–3.12)

Advanced coordination, ordering, storage, infrastructure, and reliability.

### Advanced messaging and ordering

| Lesson | Topic | Core idea |
| --- | --- | --- |
| 3.1 | Resequencer | Restore required order among related messages. |
| 3.2 | Sequential Convoy | Preserve ordering per group while processing groups in parallel. |

### Advanced distributed computation and coordination

| Lesson | Topic | Core idea |
| --- | --- | --- |
| 3.3 | MapReduce | Map large datasets into parallel tasks and reduce intermediate results. |
| 3.4 | Distributed Lock with Fencing Tokens | Prevent stale lock holders from corrupting shared resources. |

### Advanced storage and data processing

| Lesson | Topic | Core idea |
| --- | --- | --- |
| 3.5 | Event Sourcing | Represent state changes as an append-only event history. |
| 3.6 | Materialized View | Maintain precomputed representations for efficient queries. |
| 3.7 | Consistent Hashing | Reduce key movement when nodes join or leave. |
| 3.8 | Transaction Log Tailing | Extract database changes from a transaction log. |

### Advanced service infrastructure

| Lesson | Topic | Core idea |
| --- | --- | --- |
| 3.9 | Service Mesh | Provide service-to-service traffic and security capabilities. |
| 3.10 | Ambassador | Proxy outbound or inbound communications for a service. |

### Advanced reliability and operations

| Lesson | Topic | Core idea |
| --- | --- | --- |
| 3.11 | Hedged Requests | Send controlled redundant requests to reduce slow outliers. |
| 3.12 | Deployment Stamps | Build repeatable units of applications and infrastructure. |

## Engineering focus

Examples and discussions emphasize:

- Database interfaces, connections, and transactions
- Distributed job scheduling and service configuration
- Network clients, retries, timeouts, and failover
- Concurrency, shared state, and thread safety
- Fault tolerance and backend infrastructure
- Component boundaries, dependency injection, and maintainable APIs

Patterns are presented as **tools rather than rules**. Each lesson
considers simpler Python alternatives, including functions, composition,
dataclasses, and standard-library features. Tests and mocks are included
only when they are useful for explaining the design.

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
