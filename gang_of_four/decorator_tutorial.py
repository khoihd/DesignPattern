from abc import ABC, abstractmethod


class MessageSender(ABC):
    @abstractmethod
    def send(self, message):
        pass

class LoggingDecorator(MessageSender):
    def __init__(self, sender: MessageSender):
        self._sender = sender

    def send(self, message):
        print("LOGGING BEFORE")
        self._sender.send(message)
        print("LOGGING AFTER")


class MetricsDecorator(MessageSender):
    def __init__(self, sender):
        self._sender = sender
        self._count = 0

    def send(self, message):
        self._count += 1
        # print(f"METRICS: Total attempts {self._count}")
        print("Metrics: BEFORE")
        self._sender.send(message)
        print("Metrics: AFTER")


class KafkaSender(MessageSender):
    def send(self, message):
        print(f"Kafka: Sending {message}")


def main():
    kafka = KafkaSender()
    logging_sender = LoggingDecorator(kafka)
    metrics_sender = MetricsDecorator(logging_sender)
    metrics_sender.send("Hello with Decorator")


if __name__ == "__main__":
    main()